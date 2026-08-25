# 03 — ATOMIC INSIGHT

자료 수집으로 끝나는 시스템은 축적되지 않는다.
**자료 1건은 반드시 원자 단위로 분해되어야 한다.**

하나의 자료에서 보통 **3~8개**의 Atomic Insight가 나온다.
1개밖에 안 나온다면 분해가 부족한 것이고, 15개가 나온다면 쪼개기가 아니라 늘리기를 한 것이다.

---

## 9단계 사슬

```
1. Source              누가, 언제, 무엇을 발표했는가
        ↓
2. Observation         그 자료가 말한 사실 1개 (해석 없음)
        ↓
3. Consumer behavior   그 사실이 함의하는 실제 행동
        ↓
4. Category            어느 카테고리에서 일어나는가
        ↓
5. Underlying need     그 행동 밑의 충족되지 않은 요구
        ↓
6. Related signal      같은 방향을 가리키는 다른 신호
        ↓
7. Human motivation    왜 인간이 그것을 원하는가 (통제 어휘)
        ↓
8. OneThera relevance  우리의 자산(약사 전문성)과 어떻게 만나는가
        ↓
9. Potential opportunity  → 08로 승격 가능한 후보 문장
```

**5·7번이 이 시스템의 심장이다.**
1~4는 누구나 수집한다. 5·7이 통제 어휘로 정규화되어 있기 때문에
서로 다른 산업·카테고리·시점의 인사이트가 **같은 축에서 비교**된다.

---

## 표준 예시 (사용자 원안)

```json
{
  "id": "AI-2025-0001",
  "captured_at": "2025-11-04",
  "source": {
    "name": "NIQ",
    "title": "Beauty & Personal Care Report",
    "year": 2025,
    "tier": 2,
    "url": "https://nielseniq.com/...",
    "locator": "p.12, Fig. 3"
  },
  "evidence_class": "fact",
  "verification_status": "unverified",
  "observation": "North America online beauty sales +21% YoY",
  "quoted_claim": "+21% YoY, online channel, NA",
  "consumer_behavior": "Digital discovery is replacing shelf discovery",
  "category": "beauty / skincare",
  "geo": "NA",
  "underlying_need": ["convenience", "discovery"],
  "related_signal": ["TikTok Shop GMV growth", "social commerce"],
  "human_motivation": ["novelty", "social_proof", "effort_minimization"],
  "onethera_relevance": "Pharmacist expertise를 digital discovery 경험과 결합",
  "potential_opportunity": "Pharmacist-curated skincare discovery",
  "tags": ["01.RETAIL", "02.BEHAV", "07.EMERGING"],
  "confidence": 0.7
}
```

---

## 같은 자료에서 나오는 두 번째 원자 (분해의 예)

위 자료의 같은 페이지에서 이런 원자도 나온다:

```json
{
  "id": "AI-2025-0002",
  "observation": "Online growth outpaces total category growth",
  "consumer_behavior": "구매 전 검색·검증 단계가 길어지고 채널 밖에서 완결됨",
  "underlying_need": ["risk_reduction", "verification"],
  "human_motivation": ["uncertainty_reduction", "efficacy_proof"],
  "onethera_relevance": "약사의 역할이 '판매'가 아니라 '검증'으로 재정의될 수 있음",
  "potential_opportunity": "Proof-first product page — 성분 근거를 구매 경로에 직접 배치",
  "tags": ["02.PAIN", "05.PSY", "06.PERSUADE"]
}
```

같은 사실(+21%)에서 **convenience**와 **risk_reduction**이라는 서로 다른 욕구가 나온다.
이 분리가 나중에 두 개의 다른 기회로 자란다.

---

## 필드 규격

| 필드 | 필수 | 규칙 |
|---|:--:|---|
| `id` | ✅ | `AI-YYYY-NNNN`. 불변. 재사용 금지 |
| `captured_at` | ✅ | ISO date. 자료 발행일이 아니라 **수집일** |
| `source.name/tier/url\|document` | ✅ | tier는 1–4. url 또는 document 중 하나 필수 |
| `source.locator` | | 페이지·표·타임스탬프. 재현 가능해야 함 |
| `evidence_class` | ✅ | `fact` \| `signal`. **Tier 4는 무조건 signal** |
| `verification_status` | ✅ | `verified` \| `unverified` \| `disputed` |
| `observation` | ✅ | **해석 없는 사실 1문장.** 형용사 금지 |
| `verbatim` | Tier 4 필수 | 소비자 원문 그대로. 번역/윤색 금지 |
| `n_observed`, `platform`, `window` | Tier 4 필수 | 신호의 볼륨과 기간 |
| `quoted_claim` | | Tier 3–4의 수치는 여기에만. 사실로 승격 금지 |
| `consumer_behavior` | ✅ | 관찰된/함의된 **행동**. 태도가 아님 |
| `category` | ✅ | 자유 텍스트 + `geo` |
| `underlying_need` | ✅ | **통제 어휘**에서만 (1–3개) |
| `related_signal` | | 다른 인사이트 `id` 또는 서술 |
| `human_motivation` | ✅ | **통제 어휘**에서만 (1–3개) |
| `onethera_relevance` | ✅ | 우리 자산과의 접점. 없으면 `"none"` — 억지로 쓰지 않는다 |
| `potential_opportunity` | | 후보 문장. **여기서 08이 확정되지 않는다** |
| `tags` | ✅ | 택소노미 ID 1–4개. 첫 번째가 primary |
| `confidence` | ✅ | 0–1. 아래 기준 |
| `note` | | 정의 범위, 방법론 한계, 반증 |

### confidence 기준

| 값 | 의미 |
|---|---|
| 0.9–1.0 | Tier 1 원문 직접 확인 |
| 0.7–0.9 | Tier 2, 또는 Tier 1 재인용 확인 |
| 0.5–0.7 | Tier 3, 또는 방법론 미공개 |
| 0.3–0.5 | Tier 4 다수 반복 관찰 |
| 0.1–0.3 | Tier 4 소수 관찰 / 단일 목격 |

**confidence는 신호의 가치가 아니라 사실성의 정도다.**
confidence 0.3의 Reddit 신호가 confidence 0.9의 시장 규모보다 더 큰 기회를 만들 수 있다.

---

## 분해할 때의 금지 사항

- ❌ 한 원자에 두 개의 사실 (→ 두 개로 쪼갠다)
- ❌ `observation`에 해석·형용사 ("놀랍게도", "급성장하는")
- ❌ 자료에 없는 수치 보완 (모르면 비운다)
- ❌ `underlying_need`에 자유 텍스트 (통제 어휘 밖은 검증기가 차단)
- ❌ `onethera_relevance` 억지 연결 — 관련 없으면 `"none"`. 억지 연결이 쌓이면 저장소 전체가 오염된다
