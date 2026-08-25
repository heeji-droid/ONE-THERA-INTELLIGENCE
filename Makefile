.PHONY: validate converge schema all

all: schema validate converge

schema:          ## 통제 어휘로부터 JSON Schema 재생성
	python3 tools/gen_schema.py

validate:        ## 저장소 전체 검증 (스키마 + 어휘 + Tier 규칙)
	python3 tools/validate.py 'data/insights/*.jsonl'

converge:        ## 수렴 분석 — 반복 신호와 기회 점수
	python3 tools/converge.py 'data/insights/*.jsonl'

strict:          ## 경고까지 실패로 처리
	python3 tools/validate.py --strict 'data/insights/*.jsonl'
