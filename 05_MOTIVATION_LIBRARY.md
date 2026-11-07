# 05 — HUMAN MOTIVATION LIBRARY

이 시스템에서 가장 중요한 분리 두 가지가 여기서 일어난다.

> **① 사실과 해석을 나눈다** — 무엇이 관찰되었는가 vs 그것이 무엇을 의미하는가
> **② 욕구와 장치를 나눈다** — 사람이 왜 원하는가 vs 무엇이 그것을 행동으로 바꾸는가

이 둘을 섞으면 정보에 위계가 생기지 않고, 위계가 없으면 인사이트가 나오지 않는다.

---

## 질문의 계층

```
                사람은 왜 무언가를 원하는가
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
   그 욕구는          어떤 심리적        브랜드는 어떻게
   소비에서           메커니즘이         자극하거나
   어떻게             욕구를 행동으로     충족시키는가
   나타나는가          전환시키는가
        │                 │                 │
   01 DRIVES     02 MECHANISMS      04 TRUST
                 03 TRIGGERS        05 OUTCOMES
```

---

## 5개 층위

| 층 | 무엇인가 | 누구 안에 있는가 | 변하는가 | 분석에서의 역할 |
|---|---|---|---|---|
| **01 HUMAN DRIVES** (7) | 왜 원하는가 | 사람 | **변하지 않음** | 교차산업·장기 분석의 축 |
| **02 PSYCHOLOGICAL MECHANISMS** (16) | 욕구를 행동으로 바꾸는 인지 구조 | 사람 | 거의 변하지 않음 | 왜 지금 이 방식이 먹히는가 |
| **03 BEHAVIORAL TRIGGERS** (12) | 지금 행동하게 만든 방아쇠 | 환경·브랜드가 배치 | 빠르게 변함 | 실행 레버 |
| **04 TRUST MECHANISMS** (6) | 무엇이 믿게 만드는가 | 브랜드가 제공 | 느리게 변함 | ★ OneThera가 가장 강한 층 |
| **05 DESIRED OUTCOMES** (7) | 도달하려는 상태 | 사람이 원하는 미래 | 변하지 않음 | 제품이 약속하는 것 · 06 LANGUAGE의 출발점 |

전체 어휘는 [`schema/vocabularies.yaml`](schema/vocabularies.yaml)에 있고, 검증기가 이 목록 밖의 단어를 차단한다.

### 01 HUMAN DRIVES — 변하지 않는 7개

```
Security          위협·손실·불확실로부터 지키려는 힘
Growth            어제보다 나아지려는 힘
Autonomy          내 삶과 몸을 내가 결정하려는 힘
Connection        이어지고, 돌보고, 돌봄받으려는 힘
Identity/Status   내가 누구인지 규정하고 인정받으려는 힘
Exploration       새로운 것을 찾고 알아내려는 힘
Pleasure/Relief   즐거움을 얻고 고통을 줄이려는 힘
```

**클러스터링의 기본 키가 이것이다.** 뷰티에서 관찰한 `security`가 supplements·finance·mental_health에서 동일하게 나타난다면,
그것은 세 개의 트렌드가 아니라 **하나의 구조적 이동**이다.

> 트렌드는 03(Triggers)에서 일어나고, 구조는 01(Drives)에서 일어난다.
> 03만 보면 유행을 쫓게 되고, 01만 보면 아무것도 실행하지 못한다. 그래서 둘을 나눠서 **둘 다** 기록한다.

---

## 왜 나누는가 — 실제 차이

같은 관찰을 옛 방식과 새 방식으로 태깅해 보면 차이가 분명하다.

**관찰**: *"My skin hates retinol. I tried three times and gave up."* (Reddit, n≈1,000)

```
❌ 이전 (한 층에 뒤섞임)
   human_motivation: [loss_aversion, uncertainty_reduction]
   → 이것이 욕구인지 장치인지 알 수 없다. 제품도, 카피도 여기서 나오지 않는다.

✅ 지금 (층위 분리)
   drive       : security          ← 변하지 않는 것. 다른 산업과 비교되는 축
   mechanism   : loss_aversion, uncertainty_reduction
                                   ← 왜 한 번 실패하고 영구 이탈하는지의 설명
   trust       : expertise         ← 무엇이 있었다면 이탈을 막았을까
   outcome     : control           ← 이 사람이 도달하고 싶은 상태
```

읽는 방식이 달라진다:
- `drive: security` → 이 신호를 supplements·fitness의 `security`와 **합쳐서** 볼 수 있다
- `mechanism: loss_aversion` → 왜 "천천히 늘리세요"라는 조언이 실패하는지 설명한다
- `trust: expertise` → **약사 자격이 정확히 이 지점에 꽂힌다**
- `outcome: control` → 제품이 약속할 것은 "효과"가 아니라 **"통제"** 다

마지막 줄이 카피가 된다. 층위를 나누지 않았다면 나오지 않았을 문장이다.

---

## 사실과 해석의 분리

하나의 Atomic Insight는 세 개의 띠로 나뉘어 있다. **띠를 넘어가면 안 된다.**

```
┌─ FACT ─────────────── 검증 가능. 원문에 있음 ─────────────────┐
│  source · observation · verbatim · quoted_claim · n_observed   │
│  → 확신의 정도 = confidence                                     │
└────────────────────────────────────────────────────────────────┘
              ↓  여기서 추론이 시작된다
┌─ INFERENCE ────────── 자료에서 도출. 원문에 없음 ───────────────┐
│  consumer_behavior · underlying_need                            │
│  human_drive · mechanism · trigger · trust · outcome            │
│  → 확신의 정도 = inference_strength                             │
└────────────────────────────────────────────────────────────────┘
              ↓  여기서 우리의 입장이 들어간다
┌─ JUDGMENT ─────────── OneThera의 판단 ──────────────────────────┐
│  onethera_relevance · potential_opportunity                     │
│  → 근거는 위 두 띠. 여기서 새 사실을 만들지 않는다              │
└────────────────────────────────────────────────────────────────┘
```

### confidence와 inference_strength는 다른 축이다

섞으면 안 되는 이유가 여기 있다:

| 인사이트 | confidence (사실성) | inference_strength (해석) | 읽는 법 |
|---|---:|---:|---|
| `AI-2025-0004` FDA MoCRA | 0.85 | **0.90** | 사실도 단단하고, 거기서 함의로 가는 거리도 짧다 |
| `AI-2025-0002` NIQ 온라인 성장률 | 0.65 | **0.40** | 숫자는 믿을 만하지만, "검증 단계가 길어졌다"는 **먼 추론이다** |
| `AI-2025-0003` Reddit 이탈 서사 | 0.40 | **0.70** | 임상적 사실은 아니지만, **해석은 오히려 단단하다** |

마지막 줄이 핵심이다. **낮은 Tier의 낮은 confidence가 곧 낮은 가치를 뜻하지 않는다.**
Reddit 1,000건은 사실이 아니지만, 그것이 무엇을 의미하는지는 어떤 Tier 1 문헌보다 분명할 수 있다.

검증기는 `observation`에 해석어(때문에 · 시사한다 · suggests · driven by · 급성장 …)가 들어가면 **실패시킨다.**
경고가 아니라 오류다. 이 경계가 무너지면 시스템 전체가 무의미해지기 때문이다.

---

## 근거는 층으로 보여준다 — 버리지 않는다

`tools/converge.py`는 모든 클러스터의 근거를 **Tier 1 → 4 순으로 쌓아서** 출력한다.

```
[Tier 1 · Primary/Official]   (fact)
  · AI-2025-0004  U.S. FDA  conf 0.85 ⚠unverified
      FACT   MoCRA requires cosmetic facility registration...
      INFER [0.9]  브랜드의 증거 문서 보유가 의무화된다
[Tier 2 · High-quality Research]  (fact)
  · AI-2025-0002  NIQ  conf 0.65 ⚠unverified
      FACT   Online channel growth outpaced total category growth
      INFER [0.4]  구매 결정 이전의 검증 단계가 길어진다
[Tier 4 · Consumer Signal]  (signal)
  · AI-2025-0003  Reddit  conf 0.4 ⚠unverified
      FACT   Users describe abandoning retinol after an irritation episode
      “My skin hates retinol. I tried three times and gave up.” (n≈1000)
      INFER [0.7]  실패 1회 후 성분을 영구 배제한다
```

낮은 신뢰도의 정보를 **숨기지 않는다.** 아래에 놓을 뿐이다.
숨기면 판단할 수 없고, 섞으면 오도된다. 그래서 **층으로 쌓는다.**

---

## 이 라이브러리를 채우는 5개 분야

한 분야만 보면 반쪽이 된다. 각 층위는 서로 다른 학문에서 온다.

```
Evolutionary Psychology     사람이 왜 애초에 이런 행동을 하는가
        ↓                                              → 01 DRIVES
Psychology                  인지·감정·동기가 어떻게 작동하는가
        ↓                                              → 02 MECHANISMS
Behavioral Economics        왜 합리적이지 않은 선택을 하는가
        ↓                                              → 02 MECHANISMS / 03 TRIGGERS
Anthropology / Sociology    집단과 문화 속에서 어떻게 욕망하는가
        ↓                                              → 01 DRIVES / 05 OUTCOMES
Marketing / Consumer Behavior  그 욕구가 실제 구매로 어떻게 나타나는가
                                                       → 03 TRIGGERS / 04 TRUST
```

**읽기의 원칙**
- 위 두 분야(진화심리·심리학)는 **왜 변하지 않는가**를 알려준다 → 01·05에 반영
- 아래 두 분야(인류학·마케팅)는 **왜 지금 달라 보이는가**를 알려준다 → 03에 반영
- 가운데(행동경제학)가 **둘을 잇는 다리**다 → 02

여기서 읽은 것을 어휘로 추가할 때도 규칙은 같다:
기존 어휘로 80% 표현되면 추가하지 않고, 추가할 때는 정의를 함께 쓰며, **삭제하지 않는다.**
어휘를 지우면 그것으로 태깅된 과거 인사이트가 전부 끊어진다.
