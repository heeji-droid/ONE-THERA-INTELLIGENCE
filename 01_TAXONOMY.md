# 01 — TAXONOMY

모든 Atomic Insight는 최소 1개, 최대 4개의 노드 ID에 태깅된다.
ID는 **불변**이다. 이름은 바꿔도 ID는 바꾸지 않는다 (과거 데이터가 끊어지므로).

태깅 원칙:
- **1차 태그(primary)는 반드시 1개.** 그 인사이트가 "무엇에 관한 것인가".
- 2차 태그는 교차 분석용. 특히 `05.*`(HUMAN)와 `07.*`(SIGNALS)를 적극적으로 붙인다 — 여기가 cross-industry 연결이 일어나는 지점이다.
- `08.*`는 사람이 직접 태깅하지 않는다. **수렴 분석의 산출물로만 생성된다.**

---

## 01 MARKET — 무엇이 팔리고 있는가

| ID | 노드 | 담는 것 |
|---|---|---|
| `01.BEAUTY` | Beauty Market | 카테고리 규모·성장률·채널 믹스 |
| `01.NA` | North America | 미국/캐나다 고유 역학, 규제, 유통 |
| `01.KBEAUTY` | K-Beauty | 한국발 제형·유통·서사의 해외 전개 |
| `01.RETAIL` | Retail | Sephora/Ulta/Amazon/TikTok Shop/drugstore/clinic |
| `01.MACRO` | Macro | 환율·관세·원료비·인구구조·가처분소득 |

> 주의: 01은 **후행 지표**다. 여기서만 나온 인사이트는 이미 늦은 정보일 확률이 높다. 07과 교차될 때 가치가 생긴다.

## 02 CONSUMER — 무엇을 원하는가

| ID | 노드 | 담는 것 |
|---|---|---|
| `02.NEEDS` | Needs | 충족되지 않은 요구 (기능/정서/사회/정체성) |
| `02.PAIN` | Pain Points | 실패 경험, 자극, 불신, 포기 지점 |
| `02.LANG` | Language | 소비자가 실제로 쓰는 문장 (원문 그대로) |
| `02.BEHAV` | Behavior | 구매·사용·이탈의 실제 행동 패턴 |
| `02.EMERGING` | Emerging Consumer | 아직 세그먼트로 명명되지 않은 집단 |

## 03 PRODUCT — 무엇으로 해결하는가

| ID | 노드 | 담는 것 |
|---|---|---|
| `03.ING` | Ingredients | 성분, 농도, 근거 수준, 규제 상태 |
| `03.FORM` | Formulation | 안정성, 전달체계, pH, 배합 제약 |
| `03.TEX` | Texture | 감각 경험 — 재구매를 결정하는 축 |
| `03.FORMAT` | Format | 제형·용기·투여 형태 |
| `03.ROUTINE` | Routine | 단계 수, 시간대, 시퀀스, 순응도 |
| `03.CLAIM` | Claims | 표시·광고 문구와 그 법적 한계 |

## 04 COMPETITION — 누가 이미 하고 있는가

| ID | 노드 | 담는 것 |
|---|---|---|
| `04.BRAND` | Brands | 경쟁 브랜드의 구조와 자산 |
| `04.LAUNCH` | New Launches | 최근 12개월 출시와 그 반응 |
| `04.PRICE` | Pricing | 가격대, 용량당 단가, 프로모션 구조 |
| `04.POS` | Positioning | 브랜드가 점유한 **말**과 **의미** |
| `04.WHITE` | White Space | 비어 있는 좌표 (04 관점) |

## 05 HUMAN — 왜 원하는가 ★

| ID | 노드 | 담는 것 |
|---|---|---|
| `05.DESIRE` | Desires | 표면 요구 밑의 욕망 |
| `05.PSY` | Psychology | 인지 편향, 휴리스틱, 의사결정 구조 |
| `05.BSCI` | Behavioral Science | 습관 형성, 마찰, 넛지, 순응 |
| `05.ANTH` | Anthropology | 의례, 몸, 돌봄, 지위의 문화적 형식 |
| `05.PHIL` | Philosophy | 자아·통제·시간·노화에 대한 관념 |
| `05.CULT` | Cultural Trends | 미의 규범과 그 이동 |

> 05는 **다른 산업과 공유되는 유일한 레이어**다. 뷰티에서 관찰한 욕구가 금융·식품·피트니스에서 동일하게 관찰되면, 그것은 트렌드가 아니라 **구조적 이동**이다.

## 06 LANGUAGE — 어떤 말로 욕망하게 하는가

| ID | 노드 | 담는 것 |
|---|---|---|
| `06.WORDS` | Consumer Words | 소비자 어휘 ≠ 마케터 어휘 |
| `06.HOOK` | Hooks | 3초 안에 멈추게 하는 문장 구조 |
| `06.META` | Metaphors | 작용기전을 몸으로 이해시키는 비유 |
| `06.CURIO` | Curiosity | 정보 격차를 만드는 문장 설계 |
| `06.PERSUADE` | Persuasion | 신뢰·증거·권위의 언어적 형식 |

## 07 SIGNALS — 아직 트렌드가 아닌 것 ★

| ID | 노드 | 담는 것 |
|---|---|---|
| `07.WEAK` | Weak Signals | 소수가 하지만 논리가 있는 행동 |
| `07.EMERGING` | Emerging Trends | 가속 중이나 아직 주류 아님 |
| `07.CROSS` | Cross-industry | 타 산업의 동일 욕구 발현 |
| `07.STRUCT` | Structural Shifts | 되돌아가지 않는 변화 (규제·기술·인구) |

> 트렌드는 되돌아온다. 구조적 이동은 되돌아오지 않는다. `07.STRUCT` 태그가 붙은 인사이트는 기회 점수에서 가중치를 받는다.

## 08 OPPORTUNITY — 그래서 무엇을 만들 것인가 ★★★

| ID | 노드 | 산출물 |
|---|---|---|
| `08.PRODUCT` | Product Ideas | 컨셉 · 성분 논리 · 제형 · 루틴 위치 |
| `08.BRAND` | Brand Ideas | 포지셔닝 · 서사 · 소유할 단어 |
| `08.CAMPAIGN` | Campaign Ideas | 훅 · 채널 · 증거 구조 |
| `08.NEED` | Consumer Needs | 아직 아무도 명명하지 않은 요구의 명명 |
| `08.WHITE` | White Space | 01–07 교차에서 도출된 빈 좌표 |

**08은 입력이 아니라 출력이다.** 01–07의 수렴 없이 08을 쓰면 그것은 인사이트가 아니라 브레인스토밍이다.
