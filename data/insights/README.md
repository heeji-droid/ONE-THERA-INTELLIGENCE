# data/insights

Atomic Insight 저장소. **append-only.**

## 파일 규칙

```
YYYY-qN.jsonl      분기별 파일 (예: 2026-q3.jsonl)
0000-EXAMPLES.jsonl  규격 학습용 예시 — 분석에서 제외해도 됨
```

- 1줄 = 1 인사이트 (JSONL)
- **수정하지 않는다.** 사실이 바뀌면 새 인사이트를 추가하고
  옛것의 `verification_status`를 `disputed`로 바꾸는 것만 허용한다
- **삭제하지 않는다.** 틀린 것으로 밝혀진 인사이트도 남긴다 — 시스템의 오차를 측정하는 유일한 방법이다

## id 채번

```bash
grep -ho '"id":"AI-[0-9-]*"' data/insights/*.jsonl | sort | tail -1
```
마지막 번호 다음부터 이어서 쓴다. **재사용 금지** — `related_signal`의 참조가 깨진다.

## 추가 후 반드시

```bash
python3 tools/validate.py data/insights/*.jsonl
```

## 주의 — 예시 파일에 대하여

`0000-EXAMPLES.jsonl`의 모든 레코드는 **규격 설명용 템플릿**이다.
`note` 필드가 `SEED EXAMPLE`로 시작하며 `verification_status`는 전부 `unverified`다.
수치와 `n_observed`는 **검증되지 않았다.** 실제 판단에 인용하기 전에 원문을 직접 확인할 것.
