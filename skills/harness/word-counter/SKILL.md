---
name: word-counter
description: >
  텍스트 파일 또는 문자열에서 단어, 줄, 글자 수를 세어 보고합니다.
  "단어 세줘", "word count", "글자 수", "텍스트 분석" 등의
  요청에 활성화됩니다.
---

# Word Counter — 텍스트 통계 분석

## 목적

텍스트 파일 또는 입력 문자열의 단어 수(word count), 줄 수, 글자 수를 계산하여
간결한 통계 보고서를 생성합니다.

## 실행 시점

- "단어 세줘", "word count" 등 카운팅 요청
- "이 파일의 글자 수 알려줘" 등 텍스트 통계 요청
- "텍스트 분석" 등 기초 통계 요청

---

## 워크플로우

### Step 1: 입력 소스 판별

| 입력 유형 | 처리 방법 |
|----------|----------|
| 파일 경로 | `view_file`로 내용 로드 |
| 직접 텍스트 | 그대로 처리 |
| 클립보드/선택 영역 | 현재 에디터 선택 텍스트 |

### Step 2: 카운팅 실행

```python
lines = text.count('\n') + 1
words = len(text.split())
chars = len(text)
chars_no_space = len(text.replace(' ', '').replace('\n', ''))
```

### Step 3: 결과 보고

```markdown
## 📊 텍스트 통계

| 항목 | 값 |
|------|-----|
| 줄 수 (Lines) | {lines} |
| 단어 수 (Words) | {words} |
| 글자 수 (Characters) | {chars} |
| 공백 제외 | {chars_no_space} |

> 소스: {파일명 또는 "직접 입력"}
```

---

## 관련 파일

| File | Purpose |
|------|---------|
| `scripts/count.py` | 독립 실행 가능한 카운팅 스크립트 (선택) |

## 예외사항

1. **바이너리 파일** — 처리 불가, 사용자에게 텍스트 파일로 안내
2. **빈 파일** — 모든 값 0으로 보고
3. **인코딩 이슈** — UTF-8 기본, 실패 시 cp949 시도
