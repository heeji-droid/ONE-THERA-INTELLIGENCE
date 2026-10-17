# ONE THERA INTELLIGENCE

> Not a research AI. An **intelligence system**.
> `Research → Connect → Interpret → Predict → Recommend`

**이 시스템은 자료를 기다리지 않는다. 스스로 돈다.**

결핍을 찾고 → 수집하고 → 케이스로 남기고 → 수렴을 보고 → 기회를 낸다.
사람의 질문은 루프를 멈추는 것이 아니라 **루프에 얹힌다** ([`06_AUTONOMOUS_LOOP.md`](06_AUTONOMOUS_LOOP.md)).

수집으로 끝나는 시스템은 시간이 지나도 축적되지 않는다.
모든 자료를 **Atomic Insight** 단위로 분해해 저장하고,
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
| [`05_MOTIVATION_LIBRARY.md`](05_MOTIVATION_LIBRARY.md) | ★ 동기 라이브러리 5층 · 사실/해석의 분리 |
| [`06_AUTONOMOUS_LOOP.md`](06_AUTONOMOUS_LOOP.md) | ★ 자율 순환 · 상시 비트 · 케이스 축적 · 질문 처리 |
| [`schema/atomic_insight.schema.json`](schema/atomic_insight.schema.json) | 기계 검증용 JSON Schema |
| [`schema/vocabularies.yaml`](schema/vocabularies.yaml) | 통제 어휘 (drive / mechanism / trigger / trust / outcome / need / tag). **교차 분석의 전제조건** |
| [`prompts/`](prompts/) | 5단계 실행 프롬프트 |
| [`data/insights/`](data/insights/) | Atomic Insight 저장소 (JSONL, append-only) |
| [`tools/validate.py`](tools/validate.py) | 스키마 + 어휘 + Tier 규칙 검증기 |
| [`tools/converge.py`](tools/converge.py) | 수렴 분석 — 반복 신호 탐지와 기회 점수 계산 |
| [`tools/coverage.py`](tools/coverage.py) | 결핍 탐지 — **다음에 무엇을 수집할지 기계가 정한다** |
| [`docs/cases/`](docs/cases/) | ★ 케이스 스터디 저장소 — 축적의 실체 |
| [`docs/opportunities/`](docs/opportunities/) | 08 기회 카드 보관소 (폐기분 포함) |
| [`.github/workflows/validate.yml`](.github/workflows/validate.yml) | PR마다 스키마 동기화 + 인사이트 검증 자동 실행 |

---

## 순환

```
      ┌──────────────────────────────────────────────────────┐
      ▼                                          prompts/    │
 ① AGENDA      결핍을 찾는다 (coverage.py)  ──▶  05_AGENDA   │
      │        "무엇이 비어 있는가"                           │
      ▼                                                      │
 ② SWEEP       스스로 수집한다              ──▶  10_COLLECT  │
      │        Tier 4 → 1 순서로                              │
      ▼                                                      │
 ③ CASE        한 주제 = 한 케이스          ──▶  docs/cases/ │
      │        빈손도 케이스다                                 │
      ▼                                                      │
 ④ CONNECT     누적 저장소 전체의 수렴      ──▶  20 · 30 · 40│
      │                                                      │
      ▼                                                      │
 ⑤ OPPORTUNITY 또는 "아직 아님 + 이유"      ──▶  50_OPPORT.  │
      │                                                      │
      └──────────────────────────────────────────────────────┘
                            ▲
                     ⑥ ASK  │  사용자 질문 ──▶ 60_ASK
                            │  저장소를 먼저 본다. 즉답하지 않는다
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
각 인사이트는 drive / need / mechanism / trigger / trust / outcome / tier / date로 색인됨
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

```bash
# ① 무엇이 비어 있는가 — 사람이 주제를 정하지 않는다
make agenda

# ② 그 결핍을 메우는 방향으로 수집 → data/insights/ 에 append
cat prompts/00_MASTER.md prompts/05_AGENDA.md     # 지시서 작성
cat prompts/00_MASTER.md prompts/10_COLLECT.md    # 실제 수집

# ③ 검증 — 규칙 위반은 저장 전에 막힌다
make validate

# ④ 수렴 — 누적 저장소 전체에서 반복 신호를 본다
make converge

# 전부 한 번에
make all
```

질문이 있을 때도 같은 길로 간다:

```bash
cat prompts/00_MASTER.md prompts/60_ASK.md        # + 질문
# → 저장소를 먼저 뒤지고, 없으면 수집한 뒤, 답과 함께 저장소에 남긴다
```

---

## 두 개의 분리 — 이 시스템의 전부

```
① 사실과 해석         무엇이 관찰되었는가  vs  그것이 무엇을 의미하는가
                      confidence           vs  inference_strength

② 욕구와 장치         사람이 왜 원하는가   vs  무엇이 그것을 행동으로 바꾸는가
                      human_drive          vs  mechanism / trigger / trust
```

섞으면 정보에 위계가 생기지 않고, 위계가 없으면 인사이트가 나오지 않는다.
그리고 낮은 신뢰도의 정보는 **버리지 않는다 — Tier 1 → 4 순으로 아래에 쌓는다.**
숨기면 판단할 수 없고, 섞으면 오도된다.

자세히 → [`05_MOTIVATION_LIBRARY.md`](05_MOTIVATION_LIBRARY.md)

---

## 불변 규칙 (Non-negotiables)

1. **출처 없는 문장은 인사이트가 아니다.** `source_tier`와 원문 위치가 없으면 저장하지 않는다.
2. **fact와 signal을 절대 섞지 않는다.** Reddit 1,000개는 임상적 사실이 아니지만, Consumer Pain Signal로서는 Tier 1보다 빠르다.
3. **숫자를 지어내지 않는다.** 확인 불가는 `verification_status: unverified`로 남긴다. 삭제도, 추정도 하지 않는다.
4. **1개 출처 = 1개 기회는 금지.** 기회는 최소 3개 독립 출처 · 2개 이상 Tier에서 수렴할 때만 승격된다 ([`04_SIGNAL_SCORING.md`](04_SIGNAL_SCORING.md)).
5. **08 없이 끝내지 않는다.** 모든 리서치는 실행 가능한 기회로 착지한다.
6. **빈손을 감추지 않는다.** 못 찾았으면 케이스에 `empty`로 남긴다 — 그 기록이 다음 사이클의 중복 탐색을 막는다.
7. **질문에 즉답하지 않는다.** 저장소를 거치지 않은 답은 축적되지 않는다.
