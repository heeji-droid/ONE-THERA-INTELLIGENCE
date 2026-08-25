#!/usr/bin/env python3
"""schema/vocabularies.yaml -> schema/atomic_insight.schema.json

통제 어휘와 JSON Schema가 어긋나는 것을 막기 위해 스키마는 손으로 쓰지 않고 생성한다.
어휘를 고쳤으면 이 스크립트를 다시 돌리고 결과를 커밋한다.

    python3 tools/gen_schema.py
"""
import json
import pathlib
import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
VOCAB = yaml.safe_load((ROOT / "schema" / "vocabularies.yaml").read_text())

needs = [n["id"] for layer in VOCAB["underlying_need"].values() for n in layer]
motivations = [m["id"] for m in VOCAB["human_motivation"]]
tags = [t for group in VOCAB["tags"].values() for t in group]
assets = [a["id"] for a in VOCAB["onethera_assets"]] + ["none"]

schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": "https://one-thera.intelligence/atomic_insight.schema.json",
    "title": "Atomic Insight",
    "description": "GENERATED FILE — edit schema/vocabularies.yaml then run tools/gen_schema.py",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "id", "captured_at", "source", "evidence_class", "verification_status",
        "observation", "consumer_behavior", "category",
        "underlying_need", "human_motivation", "onethera_relevance",
        "tags", "confidence",
    ],
    "properties": {
        "id": {"type": "string", "pattern": r"^AI-\d{4}-\d{4,}$"},
        "captured_at": {"type": "string", "format": "date",
                        "pattern": r"^\d{4}-\d{2}-\d{2}$"},
        "source": {
            "type": "object",
            "additionalProperties": False,
            "required": ["name", "tier"],
            "properties": {
                "name": {"type": "string", "minLength": 2},
                "title": {"type": "string"},
                "author": {"type": "string"},
                "year": {"type": "integer", "minimum": 1900, "maximum": 2100},
                "published_at": {"type": "string", "pattern": r"^\d{4}(-\d{2}(-\d{2})?)?$"},
                "tier": {"type": "integer", "minimum": 1, "maximum": 4},
                "url": {"type": "string"},
                "document": {"type": "string"},
                "identifier": {"type": "string",
                               "description": "DOI / patent no. / filing no. — Tier 1 권장"},
                "locator": {"type": "string", "description": "page, table, timestamp"},
            },
            "anyOf": [{"required": ["url"]}, {"required": ["document"]}],
        },
        "evidence_class": {"enum": ["fact", "signal"]},
        "verification_status": {"enum": ["verified", "unverified", "disputed"]},
        "observation": {"type": "string", "minLength": 10, "maxLength": 400},
        "quoted_claim": {"type": "string",
                         "description": "Tier 3-4의 수치 주장. 사실로 승격 금지"},
        "verbatim": {"type": "string", "description": "Tier 4 필수 — 소비자 원문 그대로"},
        "verbatim_lang": {"type": "string"},
        "platform": {"type": "string"},
        "n_observed": {"type": "integer", "minimum": 1},
        "window": {"type": "string", "description": "관찰 기간, e.g. 2025-06..2025-11"},
        "consumer_behavior": {"type": "string", "minLength": 10},
        "category": {"type": "string", "minLength": 2},
        "geo": {"type": "string"},
        "underlying_need": {
            "type": "array", "minItems": 1, "maxItems": 3, "uniqueItems": True,
            "items": {"enum": needs},
        },
        "related_signal": {"type": "array", "items": {"type": "string"}},
        "human_motivation": {
            "type": "array", "minItems": 1, "maxItems": 3, "uniqueItems": True,
            "items": {"enum": motivations},
        },
        "cross_industry": {
            "type": "array",
            "items": {"enum": VOCAB["industries"]},
            "description": "같은 motivation이 관찰된 타 산업",
        },
        "onethera_relevance": {"type": "string", "minLength": 4},
        "onethera_asset": {"type": "array", "items": {"enum": assets}},
        "potential_opportunity": {"type": "string"},
        "tags": {
            "type": "array", "minItems": 1, "maxItems": 4, "uniqueItems": True,
            "items": {"enum": tags},
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "note": {"type": "string"},
    },
}

out = ROOT / "schema" / "atomic_insight.schema.json"
out.write_text(json.dumps(schema, indent=2, ensure_ascii=False) + "\n")
print(f"wrote {out.relative_to(ROOT)}  "
      f"({len(needs)} needs, {len(motivations)} motivations, {len(tags)} tags)")
