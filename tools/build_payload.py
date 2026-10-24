#!/usr/bin/env python3
"""뷰어(desk artifact)가 읽는 payload.json 생성.

converge.py / coverage.py 와 같은 코드로 계산한다 — 손으로 조립하지 않는다.
시드 예시는 기본 제외한다(도구 기본값과 동일). 그래야 게이트 판정이 어긋나지 않는다.

    python3 tools/build_payload.py -o payload.json
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import converge  # noqa: E402
import coverage  # noqa: E402

try:
    import yaml
except ImportError:
    yaml = None

DEFAULT_PATTERNS = ["data/insights/*.jsonl"]
REPO = pathlib.Path(__file__).resolve().parent.parent


def drive_defs(repo: pathlib.Path) -> dict[str, str]:
    """vocabularies.yaml 의 human_drive 정의를 그대로 쓴다 — 뷰어가 용어를 재정의하지 않도록."""
    path = repo / "schema" / "vocabularies.yaml"
    if yaml is None or not path.exists():
        return {}
    doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = {}
    for item in (doc.get("human_drive") or []):
        if isinstance(item, dict):
            out[item.get("id")] = item.get("def") or ""
    return {k: v for k, v in out.items() if k}


CASE_REPO = "https://github.com/heeji-droid/ONE-THERA-INTELLIGENCE/blob/claude/thera-intelligence-framework-mv9hn9"


def cases(repo: pathlib.Path) -> list[dict]:
    """주간 심층 케이스 목록 — 뷰어에서 깊은 산출물이 보이지 않던 자리를 메운다.

    본문을 옮기지 않는다. 제목·VERDICT·초점 drive·원문 링크만 뽑는다.
    """
    out = []
    d = repo / "docs" / "cases"
    if not d.exists():
        return out
    for path in sorted(d.glob("20*.md"), reverse=True):
        text = path.read_text(encoding="utf-8")
        title = verdict = drive = ""
        for line in text.splitlines():
            line = line.strip()
            if not title and line.startswith("# "):
                title = line[2:].strip()
            elif not verdict and line.startswith("**VERDICT**"):
                verdict = line.split(":", 1)[-1].strip()
            elif not drive and line.startswith("**초점 drive**"):
                drive = line.split(":", 1)[-1].strip()
            if title and verdict and drive:
                break
        out.append({
            "file": path.name,
            "date": path.name[:10],
            "title": title,
            "verdict": verdict,
            "focus": drive,
            "url": f"{CASE_REPO}/docs/cases/{path.name}",
        })
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*", default=DEFAULT_PATTERNS)
    ap.add_argument("-o", "--out", default="payload.json")
    ap.add_argument("--include-seeds", action="store_true")
    args = ap.parse_args()

    patterns = args.files or DEFAULT_PATTERNS
    recs, skipped = converge.load(patterns, include_seeds=args.include_seeds)
    if not recs:
        print("no records", file=sys.stderr)
        return 1

    horizon = max(dt.date.fromisoformat(r["captured_at"]) for r in recs)

    buckets: dict[str, list[dict]] = {}
    for r in recs:
        for k in converge.cluster_keys(r, "drive"):
            buckets.setdefault(k, []).append(r)

    clusters = {k: converge.score(v, horizon) for k, v in buckets.items() if len(v) >= 2}
    clusters = dict(sorted(clusters.items(),
                           key=lambda kv: -(kv[1]["signal_strength"])))

    payload = {
        "insights": recs,
        "coverage": coverage.analyse(recs),
        "clusters": clusters,
        "drive_defs": drive_defs(REPO),
        "cases": cases(REPO),
    }
    out = pathlib.Path(args.out)
    out.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
    passed = sum(1 for c in clusters.values() if c["gate_passed"])
    print(f"{out} · {len(recs)} insights (시드 {skipped}건 제외) · "
          f"{len(clusters)} clusters · 게이트 통과 {passed}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
