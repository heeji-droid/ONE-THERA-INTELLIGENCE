#!/usr/bin/env python3
"""수렴 분석 — 저장소 전체에서 반복되는 신호를 찾아 점수화한다.

04_SIGNAL_SCORING.md의 정의를 그대로 구현한다.

    python3 tools/converge.py data/insights/*.jsonl
    python3 tools/converge.py --by motivation+need --min-score 50 data/insights/*.jsonl
    python3 tools/converge.py --json data/insights/*.jsonl > clusters.json

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


def cluster_keys(rec: dict, mode: str) -> list[str]:
    motivations = rec.get("human_motivation", [])
    if mode == "motivation":
        return list(motivations)
    return [f"{m} × {n}" for m in motivations for n in rec.get("underlying_need", [])]


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
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--by", choices=["motivation", "motivation+need"], default="motivation")
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
        print(f"    {', '.join(c['insight_ids'])}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
