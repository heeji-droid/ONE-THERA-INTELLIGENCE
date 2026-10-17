#!/usr/bin/env python3
"""Atomic Insight 검증기.

구조(JSON Schema) + 통제 어휘 + 02_SOURCE_TIERS.md의 절대 규칙(R1-R6)을 강제한다.

    python3 tools/validate.py data/insights/*.jsonl
    python3 tools/validate.py --strict data/insights/2026-q1.jsonl   # 경고도 실패로

`jsonschema` 패키지가 있으면 그것을 쓰고, 없으면 내장 검사기로 동등한 검사를 수행한다.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
SCHEMA = json.loads((ROOT / "schema" / "atomic_insight.schema.json").read_text())

NUMERIC_CLAIM = re.compile(r"(?<![A-Za-z])(\d+(?:[.,]\d+)?\s*(?:%|percent|배|pp)|[$€£₩]\s*\d)")


# ── 최소 JSON Schema 검사기 (생성 스키마가 쓰는 키워드만 지원) ──────────────
def _check(node: dict, val, path: str, errs: list[str]) -> None:
    if "enum" in node and val not in node["enum"]:
        errs.append(f"{path}: {val!r} is not in the controlled vocabulary")
        return

    t = node.get("type")
    types = {"object": dict, "array": list, "string": str, "number": (int, float),
             "integer": int, "boolean": bool}
    if t and not isinstance(val, types[t]):
        errs.append(f"{path}: expected {t}, got {type(val).__name__}")
        return
    if t == "integer" and isinstance(val, bool):
        errs.append(f"{path}: expected integer, got bool")
        return

    if t == "object":
        for key in node.get("required", []):
            if key not in val:
                errs.append(f"{path}: missing required field '{key}'")
        props = node.get("properties", {})
        if node.get("additionalProperties") is False:
            for key in val:
                if key not in props:
                    errs.append(f"{path}: unknown field '{key}'")
        for key, sub in props.items():
            if key in val:
                _check(sub, val[key], f"{path}.{key}", errs)
        for branch in node.get("anyOf", []):
            if any(k in val for k in branch.get("required", [])):
                break
        else:
            if node.get("anyOf"):
                opts = " or ".join(k for b in node["anyOf"] for k in b.get("required", []))
                errs.append(f"{path}: requires one of [{opts}]")

    elif t == "array":
        if len(val) < node.get("minItems", 0):
            errs.append(f"{path}: needs at least {node['minItems']} item(s)")
        if "maxItems" in node and len(val) > node["maxItems"]:
            errs.append(f"{path}: at most {node['maxItems']} item(s), got {len(val)}")
        if node.get("uniqueItems") and len({json.dumps(i, sort_keys=True) for i in val}) != len(val):
            errs.append(f"{path}: duplicate items")
        for i, item in enumerate(val):
            _check(node.get("items", {}), item, f"{path}[{i}]", errs)

    elif t == "string":
        if len(val) < node.get("minLength", 0):
            errs.append(f"{path}: too short (min {node['minLength']} chars)")
        if "maxLength" in node and len(val) > node["maxLength"]:
            errs.append(f"{path}: too long (max {node['maxLength']} chars)")
        if "pattern" in node and not re.search(node["pattern"], val):
            errs.append(f"{path}: {val!r} does not match {node['pattern']}")

    elif t in ("number", "integer"):
        if "minimum" in node and val < node["minimum"]:
            errs.append(f"{path}: below minimum {node['minimum']}")
        if "maximum" in node and val > node["maximum"]:
            errs.append(f"{path}: above maximum {node['maximum']}")


def structural_errors(rec: dict) -> list[str]:
    try:
        import jsonschema
    except ModuleNotFoundError:
        errs: list[str] = []
        _check(SCHEMA, rec, "$", errs)
        return errs
    v = jsonschema.Draft202012Validator(SCHEMA)
    return [f"${'.'.join(str(p) for p in e.absolute_path) and '.' + '.'.join(str(p) for p in e.absolute_path)}: {e.message}"
            for e in v.iter_errors(rec)]


# ── 02_SOURCE_TIERS.md 절대 규칙 ────────────────────────────────────────────
def rule_errors(rec: dict) -> tuple[list[str], list[str]]:
    errs, warns = [], []
    tier = rec.get("source", {}).get("tier")
    ec = rec.get("evidence_class")

    # R1 — Tier 4는 사실이 될 수 없다
    if tier == 4 and ec == "fact":
        errs.append("R1: tier 4 source cannot be evidence_class 'fact' (consumer signal ≠ fact)")

    # R2 — 수치 주장은 Tier 1-2만
    if tier in (3, 4) and NUMERIC_CLAIM.search(rec.get("observation", "")):
        errs.append("R2: numeric claim in `observation` from a tier 3-4 source — "
                    "move it to `quoted_claim` or find the tier 1-2 original")

    # R3 — 안전성/유효성/규제 주장은 Tier 1만
    regulated = ("clinically proven", "fda approved", "fda-approved", "safe for",
                 "cures", "treats", "임상적으로 입증", "승인")
    if tier != 1 and any(k in rec.get("observation", "").lower() for k in regulated):
        errs.append("R3: safety/efficacy/regulatory claim requires a tier 1 source")

    # Tier 4 필수 필드
    if tier == 4:
        for f in ("verbatim", "platform", "n_observed", "window"):
            if not rec.get(f):
                errs.append(f"tier 4 requires `{f}` (raw voice + volume + window)")

    # confidence는 tier와 정합해야 한다 (03_ATOMIC_INSIGHT.md)
    conf = rec.get("confidence")
    ceilings = {1: (0.5, 1.0), 2: (0.5, 0.95), 3: (0.3, 0.8), 4: (0.05, 0.55)}
    if tier in ceilings and isinstance(conf, (int, float)):
        lo, hi = ceilings[tier]
        if not lo <= conf <= hi:
            warns.append(f"confidence {conf} is outside the tier {tier} band {lo}–{hi}")

    # 억지 연결 방지 — relevance가 있다면 자산에 매핑되어야 한다
    rel = rec.get("onethera_relevance", "")
    if rel.strip().lower() != "none" and not rec.get("onethera_asset"):
        warns.append("onethera_relevance is claimed but no `onethera_asset` is named — "
                     "if it maps to no asset, write \"none\"")

    # 08은 손으로 태깅하지 않는다 — 수렴 분석의 산출물이다
    if any(t.startswith("08.") for t in rec.get("tags", [])):
        errs.append("08.* tags are produced by convergence analysis, not assigned at capture")

    # 사실과 해석의 분리 — 이 시스템의 가장 중요한 규칙
    obs = rec.get("observation", "").lower()
    editorial = ("놀랍게도", "급성장", "폭발적", "주목할", "인상적",
                 "explosive", "surprisingly", "massive", "remarkable", "notably")
    causal = ("때문에", "따라서", "시사한다", "의미한다", "보여준다",
              "suggests", "indicates", "implies", "means that", "shows that",
              "driven by", "due to", "because")
    hit = [k for k in editorial + causal if k in obs]
    if hit:
        errs.append(
            f"FACT/INTERPRETATION: `observation` contains interpretation ({', '.join(hit)}) — "
            "observation holds only what the source states; move the reasoning to "
            "`consumer_behavior` and record how sure you are in `inference_strength`")

    # 해석 필드가 있으면 그 확신도를 밝혀야 한다
    if rec.get("consumer_behavior") and "inference_strength" not in rec:
        warns.append("no `inference_strength` — state how sure the interpretation is, "
                     "separately from `confidence` (which rates the fact)")

    return errs, warns


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--strict", action="store_true", help="treat warnings as failures")
    args = ap.parse_args()

    seen: dict[str, str] = {}
    n = fails = warn_count = 0

    for pattern in args.files:
        if any(ch in pattern for ch in "*?[") and not pathlib.Path(pattern).is_absolute():
            paths = sorted(pathlib.Path().glob(pattern)) or [pathlib.Path(pattern)]
        else:
            paths = [pathlib.Path(pattern)]
        for path in paths:
            if not path.exists():
                print(f"✗ {path}: not found")
                fails += 1
                continue
            for lineno, line in enumerate(path.read_text().splitlines(), 1):
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                n += 1
                where = f"{path}:{lineno}"
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"✗ {where}: invalid JSON — {e}")
                    fails += 1
                    continue

                errs = structural_errors(rec)
                r_errs, warns = rule_errors(rec)
                errs += r_errs

                rid = rec.get("id")
                if rid in seen:
                    errs.append(f"duplicate id — already defined at {seen[rid]}")
                elif rid:
                    seen[rid] = where

                for e in errs:
                    print(f"✗ {where} [{rid}] {e}")
                for w in warns:
                    print(f"⚠ {where} [{rid}] {w}")
                warn_count += len(warns)
                fails += bool(errs) or (args.strict and bool(warns))

    print(f"\n{n} insight(s) checked · {fails} failed · {warn_count} warning(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
