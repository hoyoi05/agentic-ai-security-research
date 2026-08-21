#!/usr/bin/env python3
"""Run the 2026-08-21 OpenAlex and arXiv seed-recall pilot."""

from __future__ import annotations

import csv
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path


OUT = Path(__file__).resolve().parent / "output"
OUT.mkdir(parents=True, exist_ok=True)

SEEDS = [
    ("indirect-prompt-injection-2023", "Not what you've signed up for: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection", "2302.12173"),
    ("toolemu-2023", "Identifying the Risks of LM Agents with an LM-Emulated Sandbox", "2309.15817"),
    ("injecagent-2024", "InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents", "2403.02691"),
    ("agentdojo-2024", "AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents", "2406.13352"),
    ("agentpoison-2024", "AgentPoison: Red-teaming LLM Agents via Poisoning Memory or Knowledge Bases", "2407.12784"),
    ("asb-2024", "Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents", "2410.02644"),
    ("agentharm-2024", "AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents", "2410.09024"),
    ("progent-2025", "Progent: Programmable Privilege Control for LLM Agents", "2504.11703"),
    ("saga-2025", "SAGA: A Security Architecture for Governing AI Agentic Systems", "2504.21034"),
    ("mcp-attack-vectors-2025", "Beyond the Protocol: Unveiling Attack Vectors in the Model Context Protocol (MCP) Ecosystem", "2506.02040"),
    ("agentsight-2025", "AgentSight: System-Level Observability for AI Agents Using eBPF", "2508.02736"),
    ("prov-agent-2025", "PROV-AGENT: Unified Provenance for Tracking AI Agent Interactions in Agentic Workflows", "2508.02866"),
    ("skillopt-2026", "SkillOpt: Executive Strategy for Self-Evolving Agent Skills", "2605.23904"),
    ("mcp-tdp-2026", "When the Manual Lies: A Realistic Benchmark to Evaluate MCP Poisoning Attacks for LLM Agents", "2605.24069"),
    ("delegated-observability-2026", "Observability for Delegated Execution in Agentic AI Systems", "2606.09692"),
    ("evidence-provenance-survey-2026", "A Survey of Evidence Tracing and Execution Provenance for LLM Agents", "2606.04990"),
    ("agentic-investigations-2026", "Foundations for Agentic AI Investigations from the Forensic Analysis of OpenClaw", "2604.05589"),
    ("sentinelagent-2026", "SentinelAgent: Intent-Verified Delegation Chains for Securing Federal Multi-Agent AI Systems", "2604.02767"),
]

AGENT_TERMS = [
    '"AI agent"',
    '"LM agent"',
    '"LLM agent"',
    '"LLM-based agent"',
    '"large language model agent"',
    '"language model agent"',
    '"agentic AI"',
    '"tool-using agent"',
    '"autonomous agent"',
]
SUFFIXES = {
    "qa": 'security attack vulnerability threat poisoning "prompt injection"',
    "qd": "security defense authorization authentication delegation provenance forensic monitoring",
}

ARXIV_AGENT = 'all:"AI agent" OR all:"LM agent" OR all:"LLM agent" OR all:"LLM-based agent" OR all:"large language model agent" OR all:"language model agent" OR all:"agentic AI" OR all:"tool-using agent" OR all:"autonomous agent"'
ARXIV_QA = f'({ARXIV_AGENT}) AND (all:security OR all:attack OR all:vulnerability OR all:threat OR all:adversarial OR all:"prompt injection" OR all:poisoning OR all:backdoor OR all:jailbreak OR all:misuse OR all:compromise OR all:privacy)'
ARXIV_QD = f'({ARXIV_AGENT}) AND (all:security OR all:defense OR all:authentication OR all:authorization OR all:identity OR all:credential OR all:"access control" OR all:privilege OR all:delegation OR all:provenance OR all:observability OR all:monitoring OR all:audit OR all:forensic OR all:containment OR all:recovery OR all:rollback OR all:sandbox)'

LOG_ROWS: list[dict[str, object]] = []


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def normalize_title(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.casefold()).strip()


def request(url: str, source: str, purpose: str, query_id: str, seed_id: str = "") -> tuple[int, bytes]:
    started = now()
    status = 0
    body = b""
    error = ""
    for attempt in range(5):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "agentic-ai-security-research-seed-pilot/1.2"})
            with urllib.request.urlopen(req, timeout=45) as response:
                status = response.status
                body = response.read()
            break
        except urllib.error.HTTPError as exc:
            status = exc.code
            error = f"HTTPError: {exc}"
            if exc.code == 429 and attempt < 4:
                delay = int(exc.headers.get("Retry-After", "5")) * (attempt + 1)
                time.sleep(delay)
                continue
            break
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            error = f"{type(exc).__name__}: {exc}"
            break
    LOG_ROWS.append({
        "source": source,
        "purpose": purpose,
        "query_id": query_id,
        "seed_id": seed_id,
        "executed_at_utc": started,
        "http_status": status,
        "response_bytes": len(body),
        "response_sha256": hashlib.sha256(body).hexdigest() if body else "",
        "request_url": url,
        "error": error,
    })
    return status, body


def openalex() -> list[dict[str, object]]:
    def check_seed(seed: tuple[str, str, str]) -> dict[str, object]:
        seed_id, title, _ = seed
        params = {"filter": f"title.search:{title}", "per-page": "20"}
        url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
        status, body = request(url, "openalex", "index-presence", "exact-title", seed_id)
        exact_ids: list[str] = []
        if status == 200:
            payload = json.loads(body)
            exact_ids = [
                item["id"] for item in payload.get("results", [])
                if normalize_title(item.get("title", "")) == normalize_title(title)
            ]

        matched = {"qa": [], "qd": []}
        attempted = {"qa": [], "qd": []}
        if exact_ids:
            for family, suffix in SUFFIXES.items():
                for term_index, term in enumerate(AGENT_TERMS, 1):
                    query_id = f"oa-{family}-{term_index:02d}"
                    query = f"{term} {suffix}"
                    params = {
                        "filter": f"title.search:{title}",
                        "search": query,
                        "per-page": "1",
                    }
                    url = "https://api.openalex.org/works?" + urllib.parse.urlencode(params)
                    q_status, q_body = request(url, "openalex", "query-retrieval", query_id, seed_id)
                    attempted[family].append(q_status)
                    if q_status == 200 and json.loads(q_body).get("meta", {}).get("count", 0) > 0:
                        matched[family].append(query_id)

        index_state = "true" if exact_ids else ("false" if status == 200 else "unknown")
        retrieval = {}
        for family in ("qa", "qd"):
            if matched[family]:
                retrieval[family] = "true"
            elif not exact_ids:
                retrieval[family] = "not_tested"
            elif attempted[family] and all(code == 200 for code in attempted[family]):
                retrieval[family] = "false"
            else:
                retrieval[family] = "unknown"
        row = {
            "seed_id": seed_id,
            "source": "openalex",
            "source_role": "core-discovery",
            "index_presence": index_state,
            "index_check_method": "title.search exact normalized title",
            "index_check_date": "2026-08-21",
            "retrieved_by_qa": retrieval["qa"],
            "retrieved_by_qd": retrieval["qd"],
            "query_version": "1.2-pilot",
            "metadata_verified": "partial" if exact_ids else "unknown",
            "notes": f"openalex_ids={'|'.join(exact_ids)};qa={'|'.join(matched['qa'])};qd={'|'.join(matched['qd'])}",
        }
        print(f"OpenAlex {seed_id}: index={bool(exact_ids)} qa={bool(matched['qa'])} qd={bool(matched['qd'])}", flush=True)
        return row

    with ThreadPoolExecutor(max_workers=1) as executor:
        return list(executor.map(check_seed, SEEDS))


def arxiv_ids(body: bytes) -> set[str]:
    root = ET.fromstring(body)
    ns = {"atom": "http://www.w3.org/2005/Atom"}
    found = set()
    for entry in root.findall("atom:entry", ns):
        value = entry.findtext("atom:id", default="", namespaces=ns).rsplit("/", 1)[-1]
        found.add(re.sub(r"v\d+$", "", value))
    return found


def arxiv() -> list[dict[str, object]]:
    id_list = ",".join(item[2] for item in SEEDS)
    base = "https://export.arxiv.org/api/query?"
    urls = {
        "index": base + urllib.parse.urlencode({"id_list": id_list, "max_results": 100}),
        "qa": base + urllib.parse.urlencode({"id_list": id_list, "search_query": ARXIV_QA, "max_results": 100}),
        "qd": base + urllib.parse.urlencode({"id_list": id_list, "search_query": ARXIV_QD, "max_results": 100}),
    }
    sets: dict[str, set[str]] = {}
    for position, (name, url) in enumerate(urls.items()):
        status, body = request(url, "arxiv", "index-presence" if name == "index" else "query-retrieval", f"arxiv-{name}")
        sets[name] = arxiv_ids(body) if status == 200 and body else set()
        if position < len(urls) - 1:
            time.sleep(3)

    rows = []
    for seed_id, _, arxiv_id in SEEDS:
        rows.append({
            "seed_id": seed_id,
            "source": "arxiv",
            "source_role": "core-preprint",
            "index_presence": str(arxiv_id in sets["index"]).lower(),
            "index_check_method": "id_list",
            "index_check_date": "2026-08-21",
            "retrieved_by_qa": str(arxiv_id in sets["qa"]).lower(),
            "retrieved_by_qd": str(arxiv_id in sets["qd"]).lower(),
            "query_version": "1.2-pilot",
            "metadata_verified": str(arxiv_id in sets["index"]).lower(),
            "notes": f"arxiv_id={arxiv_id}",
        })
    print(f"arXiv: index={len(sets['index'])} qa={len(sets['qa'])} qd={len(sets['qd'])}", flush=True)
    return rows


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    recall_rows = openalex() + arxiv()
    write_csv(OUT / "seed-recall-pilot-2026-08-21.csv", recall_rows)
    write_csv(OUT / "pilot-search-log-2026-08-21.csv", LOG_ROWS)

    summary = {}
    for source in ("openalex", "arxiv"):
        source_rows = [row for row in recall_rows if row["source"] == source]
        indexed = [row for row in source_rows if row["index_presence"] == "true"]
        retrieved = [row for row in indexed if row["retrieved_by_qa"] == "true" or row["retrieved_by_qd"] == "true"]
        known = [row for row in indexed if row["retrieved_by_qa"] in {"true", "false"} and row["retrieved_by_qd"] in {"true", "false"}]
        summary[source] = {
            "seed_count": len(source_rows),
            "indexed": len(indexed),
            "retrieved_union": len(retrieved),
            "conditional_recall": len(retrieved) / len(indexed) if indexed and len(known) == len(indexed) else None,
        }
    summary["requests"] = len(LOG_ROWS)
    summary["generated_at_utc"] = now()
    (OUT / "pilot-summary-2026-08-21.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2), flush=True)


if __name__ == "__main__":
    main()
