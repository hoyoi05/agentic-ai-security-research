#!/usr/bin/env python3
"""Retrieve and conservatively deduplicate the frozen OpenAlex/arXiv search set."""

from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

AGENT_TERMS = [
    '"AI agent"', '"LM agent"', '"LLM agent"', '"LLM-based agent"',
    '"large language model agent"', '"language model agent"', '"agentic AI"',
    '"tool-using agent"', '"autonomous agent"',
]
SUFFIXES = {
    "qa": '(security OR attack OR vulnerability OR threat OR adversarial OR "prompt injection" OR poisoning OR backdoor OR jailbreak OR misuse OR compromise OR privacy)',
    "qd": '(security OR defense OR authentication OR authorization OR identity OR credential OR "access control" OR privilege OR delegation OR provenance OR observability OR monitoring OR audit OR forensic OR containment OR recovery OR rollback OR sandbox)',
}
ARXIV_AGENT = 'all:"AI agent" OR all:"LM agent" OR all:"LLM agent" OR all:"LLM-based agent" OR all:"large language model agent" OR all:"language model agent" OR all:"agentic AI" OR all:"tool-using agent" OR all:"autonomous agent"'
ARXIV_QUERIES = {
    "qa": f'({ARXIV_AGENT}) AND (all:security OR all:attack OR all:vulnerability OR all:threat OR all:adversarial OR all:"prompt injection" OR all:poisoning OR all:backdoor OR all:jailbreak OR all:misuse OR all:compromise OR all:privacy)',
    "qd": f'({ARXIV_AGENT}) AND (all:security OR all:defense OR all:authentication OR all:authorization OR all:identity OR all:credential OR all:"access control" OR all:privilege OR all:delegation OR all:provenance OR all:observability OR all:monitoring OR all:audit OR all:forensic OR all:containment OR all:recovery OR all:rollback OR all:sandbox)',
}
ATOM = {"atom": "http://www.w3.org/2005/Atom", "opensearch": "http://a9.com/-/spec/opensearch/1.1/", "arxiv": "http://arxiv.org/schemas/atom"}
USER_AGENT = "agentic-ai-security-research-full-retrieval/1.0"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def clean(value: str | None) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def norm_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def norm_doi(value: str | None) -> str:
    value = clean(value).casefold()
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value)
    return value.removeprefix("doi:").strip()


def arxiv_id(value: str | None) -> str:
    value = clean(value).rsplit("/", 1)[-1]
    return re.sub(r"v\d+$", "", value)


def uninvert(index: dict[str, list[int]] | None) -> str:
    if not index:
        return ""
    positions = [(position, word) for word, values in index.items() for position in values]
    return " ".join(word for _, word in sorted(positions))


class Client:
    def __init__(self, api_key: str, log: list[dict[str, object]]) -> None:
        self.api_key = api_key
        self.log = log
        self.last_request: dict[str, float] = {}

    def get(self, source: str, query_id: str, url: str) -> bytes:
        minimum = 0.35 if source == "openalex" else 3.0
        elapsed = time.monotonic() - self.last_request.get(source, 0.0)
        if elapsed < minimum:
            time.sleep(minimum - elapsed)
        started = utc_now()
        status, body, error = 0, b"", ""
        for attempt in range(5):
            try:
                headers = {"User-Agent": USER_AGENT}
                if source == "openalex":
                    headers["Authorization"] = f"Bearer {self.api_key}"
                request = urllib.request.Request(url, headers=headers)
                with urllib.request.urlopen(request, timeout=90) as response:
                    status, body = response.status, response.read()
                break
            except urllib.error.HTTPError as exc:
                status, error = exc.code, f"HTTPError: {exc}"
                if exc.code in {429, 500, 502, 503, 504} and attempt < 4:
                    time.sleep(max(int(exc.headers.get("Retry-After", "5")), 5) * (attempt + 1))
                    continue
                break
            except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                error = f"{type(exc).__name__}: {exc}"
                if attempt < 4:
                    time.sleep(5 * (attempt + 1))
                    continue
                break
        self.last_request[source] = time.monotonic()
        self.log.append({
            "source": source, "query_id": query_id, "executed_at_utc": started,
            "http_status": status, "response_bytes": len(body),
            "response_sha256": hashlib.sha256(body).hexdigest() if body else "",
            "request_url": url, "error": error,
        })
        if status != 200:
            raise RuntimeError(f"{source} {query_id} failed with HTTP {status}: {error}")
        return body


def openalex_queries() -> list[tuple[str, str]]:
    return [(f"oa-{family}-{index:02d}", f"{term} AND {suffix}") for family, suffix in SUFFIXES.items() for index, term in enumerate(AGENT_TERMS, 1)]


def normalize_openalex(item: dict[str, object], query_id: str) -> dict[str, object]:
    ids = item.get("ids") or {}
    authorships = item.get("authorships") or []
    authors = [clean((entry.get("author") or {}).get("display_name")) for entry in authorships]
    location = item.get("primary_location") or {}
    source = location.get("source") or {}
    return {
        "source": "openalex", "source_id": str(item.get("id", "")),
        "doi": norm_doi(item.get("doi")), "arxiv_id": arxiv_id(ids.get("arxiv")),
        "title": clean(item.get("display_name") or item.get("title")),
        "abstract": uninvert(item.get("abstract_inverted_index")),
        "year": item.get("publication_year") or "", "published": item.get("publication_date") or "",
        "updated": item.get("updated_date") or "", "type": item.get("type") or "",
        "authors": "; ".join(value for value in authors if value),
        "venue": clean(source.get("display_name")), "url": location.get("landing_page_url") or item.get("id") or "",
        "retrieved_by": [query_id],
    }


def retrieve_openalex(client: Client, counts: dict[str, int]) -> list[dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for query_id, query in openalex_queries():
        cursor = "*"
        while cursor:
            params = {"search": query, "per-page": "100", "cursor": cursor}
            url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
            payload = json.loads(client.get("openalex", query_id, url))
            counts.setdefault(query_id, int(payload.get("meta", {}).get("count", 0)))
            for item in payload.get("results", []):
                row = normalize_openalex(item, query_id)
                existing = records.get(row["source_id"])
                if existing:
                    existing["retrieved_by"] = sorted(set(existing["retrieved_by"] + [query_id]))
                else:
                    records[row["source_id"]] = row
            cursor = payload.get("meta", {}).get("next_cursor")
            if not payload.get("results"):
                break
    return list(records.values())


def parse_arxiv(body: bytes, query_id: str) -> tuple[int, list[dict[str, object]]]:
    root = ET.fromstring(body)
    total = int(root.findtext("opensearch:totalResults", default="0", namespaces=ATOM))
    rows = []
    for entry in root.findall("atom:entry", ATOM):
        raw_id = entry.findtext("atom:id", default="", namespaces=ATOM)
        doi = entry.findtext("arxiv:doi", default="", namespaces=ATOM)
        rows.append({
            "source": "arxiv", "source_id": arxiv_id(raw_id), "doi": norm_doi(doi),
            "arxiv_id": arxiv_id(raw_id), "title": clean(entry.findtext("atom:title", default="", namespaces=ATOM)),
            "abstract": clean(entry.findtext("atom:summary", default="", namespaces=ATOM)),
            "year": entry.findtext("atom:published", default="", namespaces=ATOM)[:4],
            "published": entry.findtext("atom:published", default="", namespaces=ATOM),
            "updated": entry.findtext("atom:updated", default="", namespaces=ATOM), "type": "preprint",
            "authors": "; ".join(clean(a.findtext("atom:name", default="", namespaces=ATOM)) for a in entry.findall("atom:author", ATOM)),
            "venue": "arXiv", "url": f"https://arxiv.org/abs/{arxiv_id(raw_id)}", "retrieved_by": [query_id],
        })
    return total, rows


def retrieve_arxiv(client: Client, counts: dict[str, int]) -> list[dict[str, object]]:
    records: dict[str, dict[str, object]] = {}
    for family, query in ARXIV_QUERIES.items():
        query_id, start, total = f"arxiv-{family}", 0, None
        while total is None or start < total:
            params = {"search_query": query, "start": start, "max_results": 500, "sortBy": "submittedDate", "sortOrder": "descending"}
            body = client.get("arxiv", query_id, "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params))
            total, rows = parse_arxiv(body, query_id)
            counts[query_id] = total
            if not rows:
                break
            for row in rows:
                existing = records.get(row["source_id"])
                if existing:
                    existing["retrieved_by"] = sorted(set(existing["retrieved_by"] + [query_id]))
                else:
                    records[row["source_id"]] = row
            start += len(rows)
    return list(records.values())


def deduplicate(records: list[dict[str, object]]) -> list[dict[str, object]]:
    parent = list(range(len(records)))

    def find(value: int) -> int:
        while parent[value] != value:
            parent[value] = parent[parent[value]]
            value = parent[value]
        return value

    def union(left: int, right: int, reason: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root == right_root:
            return
        parent[right_root] = left_root

    indexes: dict[str, dict[str, int]] = {"doi": {}, "arxiv": {}, "title-year": {}}
    for position, row in enumerate(records):
        keys = []
        if row["doi"]:
            keys.append(("doi", str(row["doi"])))
        if row["arxiv_id"]:
            keys.append(("arxiv", str(row["arxiv_id"])))
        title_year = f"{norm_title(str(row['title']))}|{row['year']}"
        if norm_title(str(row["title"])) and row["year"]:
            keys.append(("title-year", title_year))
        for kind, value in keys:
            if value in indexes[kind]:
                union(position, indexes[kind][value], kind)
            else:
                indexes[kind][value] = position

    groups: dict[int, list[dict[str, object]]] = {}
    for position, row in enumerate(records):
        groups.setdefault(find(position), []).append(row)
    output = []
    ordered_groups = sorted(groups.values(), key=lambda members: (norm_title(str(members[0]["title"])), str(members[0]["year"])))
    for number, members in enumerate(ordered_groups, 1):
        preferred = sorted(members, key=lambda row: (not bool(row["doi"]), row["source"] != "openalex", -len(str(row["abstract"]))))[0]
        dois = sorted({str(row["doi"]) for row in members if row["doi"]})
        arxiv_ids = sorted({str(row["arxiv_id"]) for row in members if row["arxiv_id"]})
        key_type = "doi" if dois else ("arxiv" if arxiv_ids else "title-year")
        key_value = dois[0] if dois else (arxiv_ids[0] if arxiv_ids else f"{norm_title(str(preferred['title']))}|{preferred['year']}")
        title_review = len(members) > 1 and any(
            not (left["doi"] and left["doi"] == right["doi"])
            and not (left["arxiv_id"] and left["arxiv_id"] == right["arxiv_id"])
            for index, left in enumerate(members) for right in members[index + 1:]
        )
        output.append({
            "study_id": f"S{number:06d}", "dedup_key_type": key_type, "dedup_key": key_value,
            "title": preferred["title"], "abstract": preferred["abstract"], "year": preferred["year"],
            "doi": preferred["doi"], "arxiv_id": preferred["arxiv_id"], "authors": preferred["authors"],
            "url": preferred["url"], "sources": ";".join(sorted({str(row["source"]) for row in members})),
            "source_ids": ";".join(sorted(str(row["source_id"]) for row in members)),
            "retrieved_by": ";".join(sorted({query for row in members for query in row["retrieved_by"]})),
            "source_record_count": len(members), "manual_dedup_review": title_review or key_type == "title-year",
            "screening_decision": "pending", "exclusion_reason": "", "reviewer_note": "",
        })
    return output


def write_outputs(out: Path, records: list[dict[str, object]], studies: list[dict[str, object]], counts: dict[str, int], log: list[dict[str, object]]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    with gzip.open(out / "source-records.jsonl.gz", "wt", encoding="utf-8") as handle:
        for row in sorted(records, key=lambda value: (value["source"], value["source_id"])):
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    fields = list(studies[0]) if studies else ["study_id"]
    with (out / "deduplicated-screening-set.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader(); writer.writerows(studies)
    with (out / "request-log.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(log[0]) if log else ["source"])
        writer.writeheader(); writer.writerows(log)
    summary = {
        "query_version": "openalex-1.3.1_arxiv-1.2", "retrieved_at_utc": utc_now(),
        "query_result_counts": dict(sorted(counts.items())), "unique_source_records": len(records),
        "deduplicated_studies": len(studies), "openalex_records": sum(r["source"] == "openalex" for r in records),
        "arxiv_records": sum(r["source"] == "arxiv" for r in records),
        "manual_dedup_review": sum(bool(r["manual_dedup_review"]) for r in studies),
        "deduplication_order": ["normalized DOI", "versionless arXiv ID", "exact normalized title plus year"],
    }
    (out / "retrieval-summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False), flush=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("full-retrieval-output"))
    args = parser.parse_args()
    api_key = os.environ.get("OPENALEX_API_KEY", "").strip()
    if not api_key:
        raise SystemExit("OPENALEX_API_KEY is required")
    log: list[dict[str, object]] = []
    counts: dict[str, int] = {}
    client = Client(api_key, log)
    records = retrieve_openalex(client, counts) + retrieve_arxiv(client, counts)
    write_outputs(args.output, records, deduplicate(records), counts, log)


if __name__ == "__main__":
    main()
