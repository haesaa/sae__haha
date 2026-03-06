# clean_csv Instruction

> Skill: `data_cleaner`
> Entry Instruction - 02testcode.md 3단계 기반

---

## 목적

CSV 파일을 입력받아 스키마 검증, 중복 제거, 결측값 처리를 수행하고 정제된 파일을 반환한다.

---

## 입력

```json
{
  "input_path": "string (CSV 파일 경로)",
  "output_path": "string (출력 경로, optional)",
  "schema": {
    "columns": ["string"],
    "types": {}
  }
}
```

---

## 실행 단계

1. `file_read` tool로 CSV 파일 로드
2. `validate_schema` instruction 호출 - 컬럼 구조 검증
3. `remove_duplicates` instruction 호출 - 중복 행 제거
4. 결측값(NaN) 처리 - 기본값으로 채우거나 행 삭제
5. `file_write` tool로 정제된 CSV 저장
6. 처리 결과 통계 반환

---

## 출력

```json
{
  "output_path": "string",
  "original_rows": "number",
  "cleaned_rows": "number",
  "removed_duplicates": "number",
  "null_handled": "number"
}
```
