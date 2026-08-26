#!/usr/bin/env python3
"""수렴 분석 — 저장소 전체에서 반복되는 신호를 찾아 점수화한다.

04_SIGNAL_SCORING.md의 정의를 그대로 구현한다.

    python3 tools/converge.py data/insights/*.jsonl
    python3 tools/converge.py --by drive+need --min-score 50 data/insights/*.jsonl
    python3 tools/converge.py --json data/insights/*.jsonl > clusters.json

기본 클러스터 키는 human_drive다 — 변하지 않는 층이므로 산업과 시점을 가로지른다.
근거는 언제나 Tier 1 → 4 순으로 층층이 출력된다. 낮은 Tier도 숨기지 않는다.

출력은 prompts/20_CONNECT.md 이후 단계의 입력이 된다.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import sys

RECENCY_MONTHS = 12


def load(patterns: list[str]) -> list[dict]:
    recs = []
    for pattern in patterns:
        if any(ch in pattern for ch in "*?[") and not pathlib.Path(pattern).is_absolute():
            paths = sorted(pathlib.Path().glob(pattern))
        else:
            paths = [pathlib.Path(pattern)]
        for path in paths:
            for line in path.read_text().splitlines():
                line = line.strip()
                if line and not line.startswith("//"):
                    recs.append(json.loads(line))
    return recs


SIMPLE_KEYS = {
    "drive": "human_drive",
    "mechanism": "psychological_mechanism",
    "trigger": "behavioral_trigger",
    "trust": "trust_mechanism",
    "outcome": "desired_outcome",
}

TIER_LABEL = {
    1: "Tier 1 · Primary/Official",
    2: "Tier 2 · High-quality Research",
    3: "Tier 3 · Industry Intelligence",
    4: "Tier 4 · Consumer Signal",
}


def cluster_keys(rec: dict, mode: str) -> list[str]:
    if mode in SIMPLE_KEYS:
        return list(rec.get(SIMPLE_KEYS[mode], []))
    left, right = mode.split("+")
    right_field = "underlying_need" if right == "need" else SIMPLE_KEYS[right]
    return [f"{a} × {b}"
            for a in rec.get(SIMPLE_KEYS[left], [])
            for b in rec.get(right_field, [])]


def evidence_ledger(members: list[dict]) -> list[dict]:
    """근거를 신뢰도 층위로 쌓는다. Tier 1이 위, Tier 4가 아래 — 무엇도 버리지 않는다."""
    ledger = []
    for tier in (1, 2, 3, 4):
        rows = [m for m in members if m["source"]["tier"] == tier]
        if not rows:
            continue
        ledger.append({
            "tier": tier,
            "label": TIER_LABEL[tier],
            "class": "fact" if tier <= 2 else "signal" if tier == 4 else "mixed",
            "items": [{
                "id": m["id"],
                "source": m["source"]["name"],
                "url": m["source"].get("url") or m["source"].get("document", ""),
                "observation": m["observation"],
                "interpretation": m.get("consumer_behavior"),
                "inference_strength": m.get("inference_strength"),
                "verbatim": m.get("verbatim"),
                "n_observed": m.get("n_observed"),
                "verification": m["verification_status"],
                "confidence": m["confidence"],
            } for m in sorted(rows, key=lambda r: -r["confidence"])],
        })
    return ledger


def score(members: list[dict], horizon: dt.date) -> dict:
    sources = {m["source"]["name"] for m in members}
    tiers = {m["source"]["tier"] for m in members}
    industries = {i for m in members for i in m.get("cross_industry", [])}

    cutoff = horizon - dt.timedelta(days=RECENCY_MONTHS * 30)
    recent = [m for m in members
              if dt.date.fromisoformat(m["captured_at"]) >= cutoff]

    parts = {
        "independence": min(25, 5 * len(sources)),
        "tier_diversity": 5 * len(tiers),
        "demand_evidence": 15 if 4 in tiers else 0,
        "fact_base": 15 if tiers & {1, 2} else 0,
        "cross_industry": min(15, 5 * len(industries)),
        "recency": 15 * len(recent) / len(members),
    }
    signal = sum(parts.values())

    structural = any(t == "07.STRUCT" for m in members for t in m.get("tags", []))
    if structural:
        signal *= 1.15
    if len(sources) == 1:
        signal *= 0.85
    signal = min(100.0, signal)

    gates = {
        "G1_independent_sources>=3": len(sources) >= 3,
        "G2_distinct_tiers>=2": len(tiers) >= 2,
        "G3_fact_base": bool(tiers & {1, 2}),
        "G4_consumer_voice": 4 in tiers,
    }

    with_asset = [m for m in members
                  if [a for a in m.get("onethera_asset", []) if a != "none"]]
    assets = {a for m in members for a in m.get("onethera_asset", []) if a != "none"}
    asset_fit = 60 * len(with_asset) / len(members) + 40 * min(1, len(assets) / 2)

    t3_share = sum(1 for m in members if m["source"]["tier"] == 3) / len(members)
    white = 100 if t3_share == 0 else 60 if t3_share < 0.25 else 30 if t3_share < 0.5 else 0

    band = ("Structural" if signal >= 85 else "Convergent" if signal >= 70
            else "Emerging" if signal >= 50 else "Weak signal" if signal >= 30 else "Noise")

    passed = all(gates.values())
    return {
        "n_insights": len(members),
        "sources": sorted(sources),
        "tiers": sorted(tiers),
        "industries": sorted(industries),
        "components": {k: round(v, 1) for k, v in parts.items()},
        "structural": structural,
        "signal_strength": round(signal, 1),
        "band": band,
        "gates": gates,
        "gate_passed": passed,
        "asset_fit": round(asset_fit, 1),
        "white_space": white,
        "onethera_assets": sorted(assets),
        "opportunity_score": (
            round(0.5 * signal + 0.3 * asset_fit + 0.2 * white, 1) if passed else None
        ),
        "insight_ids": [m["id"] for m in members],
        "evidence": evidence_ledger(members),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--by", default="drive", choices=[
        *SIMPLE_KEYS,
        "drive+need", "drive+outcome", "drive+mechanism", "drive+trigger",
    ])
    ap.add_argument("--min-score", type=float, default=0.0)
    ap.add_argument("--min-members", type=int, default=2)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    recs = load(args.files)
    if not recs:
        print("no insights found", file=sys.stderr)
        return 1

    horizon = max(dt.date.fromisoformat(r["captured_at"]) for r in recs)

    buckets: dict[str, list[dict]] = collections.defaultdict(list)
    for rec in recs:
        for key in cluster_keys(rec, args.by):
            buckets[key].append(rec)

    clusters = {k: score(v, horizon) for k, v in buckets.items()
                if len(v) >= args.min_members}
    clusters = {k: v for k, v in clusters.items()
                if v["signal_strength"] >= args.min_score}
    ranked = sorted(clusters.items(),
                    key=lambda kv: (kv[1]["opportunity_score"] or -1,
                                    kv[1]["signal_strength"]), reverse=True)

    if args.json:
        print(json.dumps({"horizon": horizon.isoformat(), "clusters": dict(ranked)},
                         indent=2, ensure_ascii=False))
        return 0

    print(f"corpus: {len(recs)} insights · horizon {horizon} · grouped by {args.by}")
    print(f"{len(ranked)} cluster(s) with ≥{args.min_members} members\n")
    for key, c in ranked:
        gate = "PASS" if c["gate_passed"] else "blocked: " + ", ".join(
            g.split("_")[0] for g, ok in c["gates"].items() if not ok)
        opp = f"  opportunity {c['opportunity_score']}" if c["opportunity_score"] else ""
        print(f"■ {key}")
        print(f"    signal {c['signal_strength']:>5}  [{c['band']}]{opp}")
        print(f"    n={c['n_insights']}  sources={len(c['sources'])}  "
              f"tiers={c['tiers']}  industries={c['industries'] or '—'}"
              f"{'  ★STRUCTURAL' if c['structural'] else ''}")
        print(f"    gate {gate}")
        print(f"    asset_fit {c['asset_fit']}  white_space {c['white_space']}  "
              f"assets={c['onethera_assets'] or '—'}")
        print("    ── evidence (신뢰도 높은 순) " + "─" * 32)
        for layer in c["evidence"]:
            print(f"    [{layer['label']}]  ({layer['class']})")
            for it in layer["items"]:
                flag = "" if it["verification"] == "verified" else f" ⚠{it['verification']}"
                print(f"      · {it['id']}  {it['source']}  conf {it['confidence']}{flag}")
                print(f"          FACT   {it['observation']}")
                if it["verbatim"]:
                    n = f" (n≈{it['n_observed']})" if it["n_observed"] else ""
                    print(f"          \u201c{it['verbatim']}\u201d{n}")
                if it["interpretation"]:
                    infer = (f" [{it['inference_strength']}]"
                             if it["inference_strength"] is not None else " [unstated]")
                    print(f"          INFER{infer}  {it['interpretation']}")
                if it["url"]:
                    print(f"          {it['url']}")
        print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
