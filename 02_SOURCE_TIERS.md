# 02 — SOURCE TIERS

출처 위계의 목적은 **낮은 Tier를 버리는 것이 아니다.**
목적은 단 하나 — **"사실의 근거"와 "소비자의 신호"를 절대 섞지 않는 것.**

> Reddit에 *"My skin hates retinol"* 이 1,000개 있다면,
> 그것은 **임상적 사실이 아니다.** 그러나 **Consumer Pain Signal로서는 어떤 Tier 1 문헌보다 빠르고 정확하다.**
> 이 둘을 한 문장에 섞는 순간 시스템 전체의 신뢰가 무너진다.

---

## Tier 정의

### Tier 1 — Primary / Official  `tier: 1`
가장 높은 사실 신뢰도. **주장의 근거로 사용 가능.**

FDA · Health Canada · EU CosIng · 정부 통계 · 동료심사 논문 · 임상시험(ClinicalTrials.gov) ·
기업 공시(10-K, 사업보고서) · 규제 문서 · 특허 · 원본 설문 원자료

- `evidence_class: fact`
- 인용 시 **문서명 + 발행처 + 날짜 + 식별자(DOI/특허번호/문서번호)** 필수

### Tier 2 — High-quality Research  `tier: 2`
방법론이 공개된 상용 리서치. **시장 규모·성장률의 근거로 사용 가능.**

McKinsey · NIQ · Circana · Mintel · Euromonitor · Deloitte · Bain · BCG

- `evidence_class: fact`
- **주의:** 패널 구성·정의가 회사마다 다르다. "beauty" 정의가 다르면 수치는 비교 불가.
  → `note` 필드에 정의 범위를 반드시 적는다.

### Tier 3 — Industry Intelligence  `tier: 3`
업계 관찰과 맥락. **사실의 근거로는 약하나, 방향 파악에는 가장 효율적.**

WWD · Beauty Independent · Vogue Business · Cosmetics & Toiletries · Happi · BeautyMatter · 업계지

- `evidence_class: fact` (보도된 사건) 또는 `signal` (해설·전망)
- 원 출처를 재인용한 경우 **원 출처까지 추적**한다. 추적 실패 시 tier 3 유지 + `verification_status: unverified`

### Tier 4 — Consumer Signal  `tier: 4`
**사실이 아니라 신호.** 그리고 이 시스템에서 **가장 빠른 레이어.**

Reddit · TikTok · Instagram · YouTube · Amazon reviews · Sephora/Ulta reviews · Google Trends · Discord · 네이버/올리브영 리뷰

- `evidence_class: signal` — **예외 없음**
- 반드시 **원문 그대로** 기록한다 (`verbatim` 필드). 번역·요약은 별도 필드에.
- 볼륨/반복이 곧 강도다: `n_observed`(관찰 건수), `platform`, `window`(관찰 기간) 기록

---

## 절대 규칙

| # | 규칙 |
|---|---|
| R1 | Tier 4는 **절대** `evidence_class: fact`가 될 수 없다. 검증기가 차단한다. |
| R2 | 수치(%, $, 배수)를 담은 인사이트는 **Tier 1–2**만 허용. Tier 3–4의 수치는 `quoted_claim`으로만 기록하고 사실로 승격하지 않는다. |
| R3 | 안전성·유효성·규제 주장은 **Tier 1**만 허용. |
| R4 | 모든 인사이트는 `source.url` 또는 `source.document` 중 하나를 반드시 갖는다. |
| R5 | 확인 불가 = 삭제 아님. `verification_status: unverified`로 **남긴다.** 나중에 검증될 수 있다. |
| R6 | AI가 생성한 요약·추정은 출처가 아니다. `source_tier` 부여 불가. |

---

## Tier 조합이 만드는 신뢰 등급

기회(08)로 승격될 때 이 조합이 점수를 결정한다 → [`04_SIGNAL_SCORING.md`](04_SIGNAL_SCORING.md)

| 조합 | 의미 | 판단 |
|---|---|---|
| Tier 4만 | 소비자가 말하지만 근거 없음 | **관찰 지속** — 아직 기회 아님 |
| Tier 1–2만 | 데이터는 있으나 소비자 언어 없음 | **언어 부재** — 팔 수 없는 사실 |
| Tier 4 + Tier 1/2 | 소비자가 원하고 근거도 있음 | **★ 기회 후보** |
| Tier 4 + Tier 1/2 + Tier 3 부재 | 업계가 아직 다루지 않음 | **★★ White Space** |
| 4개 Tier 전부 | 이미 모두가 안다 | **레드오션** — 차별화 각도 필요 |

가장 가치 있는 좌표는 **Tier 4에서 이미 시끄럽고, Tier 1–2가 뒷받침하는데, Tier 3(업계)가 아직 조용한 지점**이다.
