# 10 — RESEARCH · 수집과 원자 분해

> 앞에 `00_MASTER.md`를 붙인다.
> 입력: 원자료(URL / PDF / 리뷰 덤프 / 스크린샷 텍스트) 또는 수집 지시
> 출력: **JSONL — Atomic Insight 1건당 1줄. 그 외 아무것도 출력하지 않는다.**

---

## TASK

주어진 자료를 **Atomic Insight로 분해**한다. 요약하지 않는다.

하나의 자료에서 보통 **3–8개**가 나온다.
1개만 나왔다면 분해가 덜 된 것이고, 15개가 나왔다면 없는 말을 만든 것이다.

### 분해 절차

```
1. 자료를 끝까지 읽는다
2. "해석 없는 사실" 목록을 먼저 만든다        ← 여기서 형용사 금지
3. 각 사실마다 물어본다: 이것이 함의하는 행동은 무엇인가
4. 그 행동 밑의 need를 통제 어휘에서 고른다     ← 자유 텍스트 금지
5. 그 need 밑의 motivation을 통제 어휘에서 고른다
6. 같은 방향을 가리키는 기존 인사이트 id를 related_signal에 연결한다
7. OneThera 자산과 만나는가? 아니면 "none"
8. 후보 기회 문장을 쓴다 (여기서 확정하지 않는다)
9. 태깅 → 검증
```

### 한 문장으로 두 개를 말하지 않는다

> "온라인 매출이 21% 늘었고 소비자는 리뷰를 더 많이 본다"
> → 두 개의 원자다. 쪼갠다.

---

## SOURCE 수집 지침

`02_SOURCE_TIERS.md`의 Tier를 따른다. 한 주제를 수집할 때는 **의도적으로 Tier를 섞는다.**

```
Tier 1–2 에서 : 무엇이 사실인가        (규모 · 규제 · 임상 · 공시)
Tier 3   에서 : 업계가 무엇을 말하는가  (경쟁 · 출시 · 해설)
Tier 4   에서 : 소비자가 무엇을 말하는가 (원문 · 반복 · 좌절)
```

**Tier 4를 마지막에 하지 말 것.** 대부분의 진짜 기회는 Tier 4에서 먼저 보이고
Tier 1–2에서 나중에 확인된다. 순서를 뒤집으면 이미 아는 것만 확인하게 된다.

### Tier 4 수집 시 필수 기록
- `verbatim` — **번역·윤색 없이 원문 그대로.** 소비자의 문법 오류까지 자산이다
- `platform`, `n_observed`, `window` — 볼륨과 기간 없이는 신호가 아니라 일화다
- 검색 조건을 `note`에 남긴다 (재현 가능해야 한다)

---

## OUTPUT — JSONL only

```json
{"id":"AI-2026-0012","captured_at":"2026-08-25","source":{"name":"...","tier":2,"url":"...","locator":"p.4"},"evidence_class":"fact","verification_status":"unverified","observation":"...","consumer_behavior":"...","category":"...","geo":"NA","underlying_need":["..."],"human_motivation":["..."],"cross_industry":["..."],"onethera_relevance":"...","onethera_asset":["..."],"potential_opportunity":"...","tags":["02.PAIN","05.PSY"],"confidence":0.7,"note":"..."}
```

- `id`는 `AI-YYYY-NNNN`, 기존 저장소의 마지막 번호 다음부터
- `tags` 첫 번째가 primary. **`08.*`은 절대 붙이지 않는다**
- 스키마 전체는 [`schema/atomic_insight.schema.json`](../schema/atomic_insight.schema.json)

## 저장 후 반드시

```bash
python3 tools/validate.py data/insights/2026-q3.jsonl
```

검증기가 막는 것은 실수가 아니라 **시스템의 규칙**이다.
통과하지 못한 인사이트는 고치거나 버린다. 규칙을 끄지 않는다.

---

## SELF-CHECK — 출력 전 스스로 확인

- [ ] `observation`에 형용사·부사가 없는가
- [ ] Tier 3–4인데 `observation`에 수치를 넣지 않았는가
- [ ] `need`와 `motivation`이 전부 통제 어휘 안에 있는가
- [ ] `onethera_relevance`가 억지가 아닌가 — 억지면 `"none"`
- [ ] 같은 자료에서 나온 원자들이 서로 다른 need를 가리키는가 (전부 같다면 분해 실패)
