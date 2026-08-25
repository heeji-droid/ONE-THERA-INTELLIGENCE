# ONE THERA INTELLIGENCE

> Not a research AI. An **intelligence system**.
> `Research → Connect → Interpret → Predict → Recommend`

수집으로 끝나는 시스템은 시간이 지나도 축적되지 않는다.
이 레포는 모든 자료를 **Atomic Insight** 단위로 분해해 저장하고,
수천 개가 쌓였을 때 기계가 스스로 물을 수 있게 만든다:

> *"최근 12개월 동안 서로 다른 분야에서 반복적으로 나타나는 신호는 무엇인가?"*

그리고 그 답을 **08 OPPORTUNITY** — 제품/브랜드/캠페인 아이디어 — 로 끝맺는다.
08이 나오지 않은 리서치는 완료된 리서치가 아니다.

---

## 시스템 구조

| 파일 | 역할 |
|---|---|
| [`01_TAXONOMY.md`](01_TAXONOMY.md) | 8개 도메인 · 41개 노드. 모든 인사이트가 붙는 좌표계 |
| [`02_SOURCE_TIERS.md`](02_SOURCE_TIERS.md) | Tier 1–4 출처 위계. **사실(fact)** 과 **신호(signal)** 의 분리 |
| [`03_ATOMIC_INSIGHT.md`](03_ATOMIC_INSIGHT.md) | 자료 1건 → 원자 단위 9단계 분해 규격 |
| [`04_SIGNAL_SCORING.md`](04_SIGNAL_SCORING.md) | 신호 강도 · 수렴(convergence) · 기회 점수 계산 |
| [`schema/atomic_insight.schema.json`](schema/atomic_insight.schema.json) | 기계 검증용 JSON Schema |
| [`schema/vocabularies.yaml`](schema/vocabularies.yaml) | 통제 어휘 (need / motivation / tag). **교차 분석의 전제조건** |
| [`prompts/`](prompts/) | 5단계 실행 프롬프트 |
| [`data/insights/`](data/insights/) | Atomic Insight 저장소 (JSONL, append-only) |
| [`tools/validate.py`](tools/validate.py) | 스키마 + 어휘 + Tier 규칙 검증기 |
| [`tools/converge.py`](tools/converge.py) | 수렴 분석 — 반복 신호 탐지와 기회 점수 계산 |
| [`docs/opportunities/`](docs/opportunities/) | 08 기회 카드 보관소 (폐기분 포함) |
| [`.github/workflows/validate.yml`](.github/workflows/validate.yml) | PR마다 스키마 동기화 + 인사이트 검증 자동 실행 |

---

## 5단계 파이프라인

```
                                     prompts/
[ 자료 ]  ──1. RESEARCH──────────▶  10_COLLECT.md      → Atomic Insight N개
   │                                                      (data/insights/*.jsonl)
   │      ──2. CONNECT────────────▶  20_CONNECT.md      → 반복·수렴 패턴
   │      ──3. INTERPRET──────────▶  30_INTERPRET.md    → "왜 지금인가"
   │      ──4. PREDICT────────────▶  40_PREDICT.md      → 12–36개월 전개 시나리오
   └──────5. RECOMMEND───────────▶  50_OPPORTUNITY.md  → 08 OPPORTUNITY ★
```

각 단계는 **앞 단계의 산출물만** 입력으로 받는다.
5단계에서 근거 없는 아이디어가 나오면, 그건 4단계까지가 부실했다는 뜻이다.

---

## 왜 Atomic Insight인가

❌ 나쁜 방식
```
"2026년 북미 skincare trend를 찾아줘"
→ 요약문 1개. 다음 리서치와 연결 불가. 3개월 뒤 재사용 불가.
```

✅ 이 시스템
```
자료 1건 → Atomic Insight 3~8개
각 인사이트는 need / motivation / tag / tier / date로 색인됨
→ 1,000건이 쌓이면 "cross-industry에서 반복되는 욕구"가 자동으로 드러남
```

한 건의 요약은 자산이 아니다. **색인된 원자 1,000개가 자산이다.**

---

## 사고의 사슬 (이 시스템이 매번 통과하는 질문)

```
Market signal        → 사람들이 무엇을 사고 있는가
Consumer signal      → 사람들이 무엇을 원하는가
Human psychology     → 왜 그것을 원하는가
Cultural signal      → 왜 지금 그것이 중요해졌는가
Cross-industry       → 다른 분야에서도 같은 욕구가 나타나는가
Product intelligence → 어떤 제품으로 해결할 수 있는가
Language intelligence→ 어떤 말로 욕망하게 만들 것인가
        ↓
   ONE THERA OPPORTUNITY
```

---

## 사용법

`make all` 로 3·4단계를 한 번에 돌릴 수 있다.

```bash
# 1. 수집 — 프롬프트를 AI에 넣고 자료를 분해시킨다
cat prompts/10_COLLECT.md          # + 원자료 URL/텍스트

# 2. 저장 — 산출된 JSON을 append
cat new.jsonl >> data/insights/2026-q1.jsonl

# 3. 검증 — 스키마·어휘·출처 규칙 위반 차단
python3 tools/validate.py data/insights/*.jsonl

# 4. 수렴 — 기계가 반복 신호를 먼저 찾는다
python3 tools/converge.py data/insights/*.jsonl

# 5. 해석 → 예측 → 기회
cat prompts/00_MASTER.md prompts/20_CONNECT.md    # + converge 출력
```

---

## 불변 규칙 (Non-negotiables)

1. **출처 없는 문장은 인사이트가 아니다.** `source_tier`와 원문 위치가 없으면 저장하지 않는다.
2. **fact와 signal을 절대 섞지 않는다.** Reddit 1,000개는 임상적 사실이 아니지만, Consumer Pain Signal로서는 Tier 1보다 빠르다.
3. **숫자를 지어내지 않는다.** 확인 불가는 `verification_status: unverified`로 남긴다. 삭제도, 추정도 하지 않는다.
4. **1개 출처 = 1개 기회는 금지.** 기회는 최소 3개 독립 출처 · 2개 이상 Tier에서 수렴할 때만 승격된다 ([`04_SIGNAL_SCORING.md`](04_SIGNAL_SCORING.md)).
5. **08 없이 끝내지 않는다.** 모든 리서치는 실행 가능한 기회로 착지한다.
