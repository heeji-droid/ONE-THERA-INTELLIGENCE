# 20 — CONNECT · 반복과 수렴 찾기

> 앞에 `00_MASTER.md`를 붙인다.
> 입력: `data/insights/*.jsonl` 전체 + `tools/converge.py` 출력
> 출력: Signal Cluster 목록 (마크다운)

이 단계의 질문은 단 하나다:

> **"최근 12개월 동안 서로 다른 분야에서 반복적으로 나타나는 신호는 무엇인가?"**

---

## 먼저 기계를 돌린다

```bash
python3 tools/converge.py --json data/insights/*.jsonl > clusters.json
python3 tools/converge.py --by motivation+need --min-members 3 data/insights/*.jsonl
```

기계는 **점수**를 준다. 사람(AI)은 **의미**를 준다.
점수 없이 의미를 말하지 말고, 의미 없이 점수를 보고하지 마라.

---

## TASK

### 1. 클러스터 읽기
`converge.py`가 낸 각 클러스터에 대해:
- 어떤 **동기(motivation)** 로 묶였는가
- 몇 개의 **독립 출처**, 몇 개의 **Tier**, 몇 개의 **산업**에서 왔는가
- 게이트를 통과했는가 / 무엇이 막고 있는가

### 2. 진짜 반복 vs 에코 구분

같은 원 자료를 여러 매체가 재인용한 것은 **반복이 아니다.**
아래를 확인한다:
- 서로 다른 출처가 **같은 원본**을 인용하고 있지 않은가
- Tier 3 기사 3건이 사실은 하나의 Tier 2 리포트인가
- 그렇다면 독립 출처는 1개다. 클러스터를 강등한다

### 3. Cross-industry 연결 ★

**이 시스템의 가장 큰 가치가 여기서 나온다.**

같은 `human_motivation`이 뷰티 밖에서도 관찰되는지 확인한다:

```
uncertainty_reduction  → skincare / supplements / finance / mental_health
effort_minimization    → routine 축소 / 구독 해지 / 미니멀 재테크
transparency_demand    → 성분 공개 / 수수료 공개 / 알고리즘 공개
authority_trust        → 약사 / 전문의 콘텐츠 / 자격 기반 크리에이터
```

**한 산업의 트렌드는 유행이고, 세 산업의 동일 동기는 구조다.**
후자를 찾으면 `07.CROSS` 또는 `07.STRUCT`로 태깅할 근거가 된다.

### 4. 침묵 읽기 (Negative space)

**있어야 하는데 없는 것**을 찾는다. 이것이 White Space의 원료다.
- Tier 4는 시끄러운데 Tier 3(업계지)이 조용한 주제
- 소비자가 매번 말하는데 어떤 브랜드도 이름 붙이지 않은 문제
- 통제 어휘 중 저장소에 거의 등장하지 않는 need — 수집의 사각지대인가, 진짜 공백인가

### 5. 모순 기록

서로 반대를 가리키는 인사이트를 **해소하지 말고 기록한다.**
모순은 보통 **세그먼트가 갈라지고 있다는 신호**다.
(예: "단순화를 원한다" vs "루틴을 늘린다" → 두 개의 다른 소비자다)

---

## OUTPUT

```markdown
## Cluster: {motivation} [× {need}]
- Signal Strength: {score} / {band}   Gate: {PASS | blocked by G_}
- 구성: 인사이트 {n}건 · 독립 출처 {n} · Tier {[...]} · 산업 {[...]}
- 근거: {insight ids}

**무엇이 반복되는가**
{1–3문장. 사실만}

**어디까지 퍼져 있는가**
{뷰티 안/밖. cross-industry 근거}

**에코 검증**
{독립성 확인 결과. 강등했다면 그 이유}

**모순**
{반대 방향 신호와 그 해석}

**아직 없는 것**
{이 클러스터에서 비어 있는 Tier / 확인이 필요한 것}
```

마지막에:
```markdown
## 수집 지시 (다음 라운드)
{게이트를 막고 있는 요소를 채우기 위해 무엇을 어디서 더 수집해야 하는가}
```

**이 단계에서 기회를 말하지 않는다.** 아직 왜(30)와 언제(40)를 모른다.
