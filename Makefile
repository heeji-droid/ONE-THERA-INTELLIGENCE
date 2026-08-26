.PHONY: all schema validate strict converge coverage agenda

all: schema validate converge coverage

schema:          ## 통제 어휘로부터 JSON Schema 재생성
	python3 tools/gen_schema.py

validate:        ## 저장소 전체 검증 (스키마 + 어휘 + Tier 규칙 + 사실/해석 경계)
	python3 tools/validate.py 'data/insights/*.jsonl'

strict:          ## 경고까지 실패로 처리
	python3 tools/validate.py --strict 'data/insights/*.jsonl'

converge:        ## 수렴 분석 — 반복 신호와 기회 점수 (근거는 Tier 1→4로 층층이)
	python3 tools/converge.py 'data/insights/*.jsonl'

coverage:        ## 커버리지 — 저장소의 결핍 현황
	python3 tools/coverage.py 'data/insights/*.jsonl'

agenda:          ## 다음 수집 지시 — 무엇을 볼지 기계가 정한다
	python3 tools/coverage.py --agenda 'data/insights/*.jsonl'
