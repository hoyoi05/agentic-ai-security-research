#!/usr/bin/env python3
"""Fetch a reproducible arXiv title/abstract pilot-screening set."""

from __future__ import annotations

import csv
import importlib.util
import json
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT.parent / "data" if ROOT.name == "scripts" else ROOT / "screening"
OUT.mkdir(parents=True, exist_ok=True)

seed_script = ROOT / "run-seed-recall-pilot.py"
if not seed_script.exists():
    seed_script = ROOT / "run_seed_pilot.py"
spec = importlib.util.spec_from_file_location("seed_pilot", seed_script)
pilot = importlib.util.module_from_spec(spec)
assert spec.loader
spec.loader.exec_module(pilot)

ATOM = {"atom": "http://www.w3.org/2005/Atom"}
ENDPOINT = "https://export.arxiv.org/api/query?"


def clean(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def fetch(params: dict[str, object]) -> list[dict[str, object]]:
    url = ENDPOINT + urllib.parse.urlencode(params)
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "agentic-ai-security-research-screening-pilot/1.0"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        root = ET.fromstring(response.read())
    rows = []
    for entry in root.findall("atom:entry", ATOM):
        raw_id = entry.findtext("atom:id", default="", namespaces=ATOM).rsplit("/", 1)[-1]
        rows.append({
            "arxiv_id": re.sub(r"v\d+$", "", raw_id),
            "title": clean(entry.findtext("atom:title", default="", namespaces=ATOM)),
            "abstract": clean(entry.findtext("atom:summary", default="", namespaces=ATOM)),
            "published": entry.findtext("atom:published", default="", namespaces=ATOM),
            "updated": entry.findtext("atom:updated", default="", namespaces=ATOM),
            "authors": "; ".join(
                clean(author.findtext("atom:name", default="", namespaces=ATOM))
                for author in entry.findall("atom:author", ATOM)
            ),
            "categories": ";".join(
                category.attrib.get("term", "") for category in entry.findall("atom:category", ATOM)
            ),
            "url": f"https://arxiv.org/abs/{re.sub(r'v\\d+$', '', raw_id)}",
        })
    return rows


def main() -> None:
    retrieved: dict[str, dict[str, object]] = {}
    for family, query in (("qa", pilot.ARXIV_QA), ("qd", pilot.ARXIV_QD)):
        rows = fetch({
            "search_query": query,
            "start": 0,
            "max_results": 25,
            "sortBy": "relevance",
            "sortOrder": "descending",
        })
        for rank, row in enumerate(rows, 1):
            item = retrieved.setdefault(str(row["arxiv_id"]), row | {"retrieved_by": [], "ranks": {}})
            item["retrieved_by"].append(family)
            item["ranks"][family] = rank
        time.sleep(3)

    seed_ids = ",".join(seed[2] for seed in pilot.SEEDS)
    seeds = fetch({"id_list": seed_ids, "max_results": 100})
    seed_map = {seed[2]: seed[0] for seed in pilot.SEEDS}
    for row in seeds:
        item = retrieved.setdefault(str(row["arxiv_id"]), row | {"retrieved_by": [], "ranks": {}})
        item["seed_id"] = seed_map.get(str(row["arxiv_id"]), "")
    for item in retrieved.values():
        item.setdefault("seed_id", seed_map.get(str(item["arxiv_id"]), ""))
        item["sample_role"] = "seed-calibration" if item["seed_id"] else "precision-at-25"
        item["decision"] = "pending"
        item["exclusion_reason"] = ""
        item["reviewer_note"] = ""

    ordered = sorted(retrieved.values(), key=lambda x: (x["sample_role"] != "seed-calibration", str(x["arxiv_id"])))
    (OUT / "screening-pilot-records.json").write_text(json.dumps(ordered, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    fields = [
        "arxiv_id", "seed_id", "sample_role", "retrieved_by", "ranks", "title", "abstract",
        "authors", "published", "updated", "categories", "url", "decision", "exclusion_reason", "reviewer_note",
    ]
    with (OUT / "screening-pilot.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for item in ordered:
            row = item.copy()
            row["retrieved_by"] = ";".join(row["retrieved_by"])
            row["ranks"] = json.dumps(row["ranks"], sort_keys=True)
            writer.writerow({field: row.get(field, "") for field in fields})
    print(json.dumps({
        "unique_records": len(ordered),
        "seed_records": sum(bool(item["seed_id"]) for item in ordered),
        "precision_sample_records": sum(not bool(item["seed_id"]) for item in ordered),
    }))


if __name__ == "__main__":
    main()
