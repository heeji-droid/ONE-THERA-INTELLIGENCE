# PROMPTS

각 단계는 **반드시 `00_MASTER.md`를 앞에 붙여서** 실행한다.

| 파일 | 단계 | 입력 | 출력 |
|---|---|---|---|
| `00_MASTER.md` | — | — | 항상 앞에 붙이는 시스템 프롬프트 |
| `10_COLLECT.md` | RESEARCH | 원자료 | Atomic Insight JSONL |
| `20_CONNECT.md` | CONNECT | 저장소 전체 + `converge.py` | Signal Cluster |
| `30_INTERPRET.md` | INTERPRET | 20의 출력 | 왜 / 왜 지금 |
| `40_PREDICT.md` | PREDICT | 30의 출력 | 경로 · 타이밍 · 폐기 조건 |
| `50_OPPORTUNITY.md` | RECOMMEND | 20+30+40 | **08 Opportunity Card ★** |

## 실행 예

```bash
# 1. 수집
cat prompts/00_MASTER.md prompts/10_COLLECT.md            # + 원자료
#    → 결과를 data/insights/2026-q3.jsonl 에 append
python3 tools/validate.py data/insights/2026-q3.jsonl

# 2. 수렴 (기계)
python3 tools/converge.py --json data/insights/*.jsonl > clusters.json

# 3. 연결 (AI)
cat prompts/00_MASTER.md prompts/20_CONNECT.md clusters.json

# 4~5. 해석 · 예측
cat prompts/00_MASTER.md prompts/30_INTERPRET.md          # + 3의 출력
cat prompts/00_MASTER.md prompts/40_PREDICT.md            # + 4의 출력

# 6. 기회 ★
cat prompts/00_MASTER.md prompts/50_OPPORTUNITY.md        # + 3,4,5의 출력 전부
#    → docs/opportunities/YYYY-MM-{name}.md 로 저장
```

## 단계를 건너뛰지 않는다

10 → 50으로 바로 가면 그것은 브레인스토밍이다.
20(반복 확인)과 30(왜)을 건너뛴 기회는 근거가 아니라 취향이다.
