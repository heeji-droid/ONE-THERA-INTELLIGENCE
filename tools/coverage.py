#!/usr/bin/env python3
"""커버리지 분석 — 저장소에서 "비어 있는 곳"을 찾아 다음 수집 지시를 생성한다.

자율 루프의 심장. 사람이 주제를 정하지 않아도 시스템이 스스로 결핍을 찾는다.

    python3 tools/coverage.py data/insights/*.jsonl
    python3 tools/coverage.py --agenda data/insights/*.jsonl     # 수집 지시만
    python3 tools/coverage.py --json data/insights/*.jsonl

원칙: 많이 쌓인 곳이 아니라 **비어 있는 곳**이 다음 수집의 대상이다.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import pathlib
import sys

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOCAB = yaml.safe_load((ROOT / "schema" / "vocabularies.yaml").read_text())
DRIVES = [d["id"] for d in VOCAB["human_drive"]]
INDUSTRIES = VOCAB["industries"]

STALE_DAYS = 120        # 이 기간 넘게 갱신 안 된 drive는 신선도 결핍
THIN = 3                # drive당 최소 인사이트 수


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


def analyse(recs: list[dict]) -> dict:
    horizon = max(dt.date.fromisoformat(r["captured_at"]) for r in recs)
    by_drive: dict[str, list[dict]] = collections.defaultdict(list)
    for r in recs:
        for d in r.get("human_drive", []):
            by_drive[d].append(r)

    rows, gaps = {}, []
    for drive in DRIVES:
        members = by_drive.get(drive, [])
        tiers = collections.Counter(m["source"]["tier"] for m in members)
        industries = {i for m in members for i in m.get("cross_industry", [])}
        newest = (max(dt.date.fromisoformat(m["captured_at"]) for m in members)
                  if members else None)
        age = (horizon - newest).days if newest else None

        rows[drive] = {
            "n": len(members),
            "tiers": {t: tiers.get(t, 0) for t in (1, 2, 3, 4)},
            "industries": sorted(industries),
            "newest": newest.isoformat() if newest else None,
            "age_days": age,
        }

        # ── 결핍 판정 — 우선순위 순 ──────────────────────────────
        if not members:
            gaps.append((100, drive, "blank",
                         f"'{drive}'에 인사이트가 하나도 없다. 이 욕구는 정말 뷰티에 없는가, "
                         f"아니면 우리가 안 본 것인가"))
            continue
        if not (tiers[1] + tiers[2]):
            gaps.append((90, drive, "no_fact_base",
                         f"'{drive}'에 Tier 1–2 근거가 없다 → 지금은 유행이지 기회가 아니다. "
                         f"규제·임상·시장 데이터를 찾아라"))
        if not tiers[4]:
            gaps.append((85, drive, "no_consumer_voice",
                         f"'{drive}'에 소비자 목소리(Tier 4)가 없다 → 근거는 있으나 수요 증거가 없다. "
                         f"Reddit·리뷰·TikTok에서 원문을 찾아라"))
        if len(industries) < 2:
            gaps.append((70, drive, "no_cross_industry",
                         f"'{drive}'가 뷰티 안에서만 관찰됐다 → 구조인지 유행인지 판별 불가. "
                         f"타 산업에서 같은 drive를 찾아라"))
        if len(members) < THIN:
            gaps.append((60, drive, "thin",
                         f"'{drive}'가 {len(members)}건뿐이다 (최소 {THIN}). 독립 출처를 더 확보하라"))
        if age is not None and age > STALE_DAYS:
            gaps.append((50, drive, "stale",
                         f"'{drive}'가 {age}일째 갱신되지 않았다. 여전히 유효한지 재확인하라"))

    unverified = [r["id"] for r in recs if r["verification_status"] == "unverified"]
    industry_gaps = [i for i in INDUSTRIES
                     if not any(i in r.get("cross_industry", []) for r in recs)]

    return {
        "horizon": horizon.isoformat(),
        "total": len(recs),
        "by_drive": rows,
        "gaps": [{"priority": p, "drive": d, "kind": k, "instruction": m}
                 for p, d, k, m in sorted(gaps, key=lambda g: -g[0])],
        "unverified": unverified,
        "untouched_industries": industry_gaps,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--agenda", action="store_true", help="수집 지시만 출력")
    ap.add_argument("--top", type=int, default=6, help="지시 개수")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    recs = load(args.files)
    if not recs:
        print("no insights found", file=sys.stderr)
        return 1
    rep = analyse(recs)

    if args.json:
        print(json.dumps(rep, indent=2, ensure_ascii=False))
        return 0

    if not args.agenda:
        print(f"corpus: {rep['total']} insights · horizon {rep['horizon']}\n")
        print(f"{'drive':<18} {'n':>3}  T1 T2 T3 T4   age  industries")
        print("─" * 74)
        for drive, r in rep["by_drive"].items():
            t = r["tiers"]
            age = f"{r['age_days']:>3}d" if r["age_days"] is not None else "  —"
            mark = "" if r["n"] else "  ← 공백"
            print(f"{drive:<18} {r['n']:>3}  "
                  f"{t[1]:>2} {t[2]:>2} {t[3]:>2} {t[4]:>2}  {age}  "
                  f"{', '.join(r['industries']) or '—'}{mark}")
        if rep["untouched_industries"]:
            print(f"\n한 번도 안 본 산업: {', '.join(rep['untouched_industries'])}")
        if rep["unverified"]:
            print(f"미검증 인사이트 {len(rep['unverified'])}건 — 원문 확인 대기")
        print()

    print("── NEXT COLLECTION AGENDA " + "─" * 40)
    for i, g in enumerate(rep["gaps"][:args.top], 1):
        print(f"{i}. [{g['priority']:>3}] {g['kind']:<18} {g['instruction']}")
    if not rep["gaps"]:
        print("결핍 없음 — 모든 drive가 Tier 1–2와 Tier 4를 갖추고 2개 이상 산업에서 관찰됨")
    return 0


if __name__ == "__main__":
    sys.exit(main())
