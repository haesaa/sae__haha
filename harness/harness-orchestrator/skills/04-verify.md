---
name: harness-04-verify
description: >
  생성된 스킬 파일의 구조(Schema), 기능(Functional), 품질(Quality+Reflection)을 3단계로 검증한다.
  critical 이슈는 최대 2회 자동 수정을 시도한다.
---

# 04-verify: 검증 3단계 + Reflection

> **실행자**: Reviewer (Teammate 3)
> **실행 시점**: 03-forge 완료 후
> **쓰기 권한**: `work/verify/` 만

## 목적

03-forge에서 생성된 스킬 파일이 Antigravity 표준 규격을 만족하는지 Schema → Functional → Quality 순으로 검증하고, critical 문제는 자동 수정한다.

## 실행 시점

- 03-forge 완료 시그널 수신 후 Reviewer가 자동 실행.
- `view_file("../../verification-layer/SKILL.md")`로 동적 로딩하여 검증 기준 확인.

## 워크플로우

### Step 1: Stage 1 — Schema Validation

SKILL.md에 대해:

- `---` YAML frontmatter로 시작하는가
- `name` 필드 존재 + 폴더명과 일치하는가
- `description` 필드 존재 + 비어있지 않은가
- 줄 수 ≤ 500인가

JSON/jsonc 파일에 대해:

- 파싱 성공 여부 (구문 오류 없음)

결과:

- 모두 통과 → `schema: "pass"`
- 하나라도 실패 → `schema: "fail"` → 자동 수정 (1회)

### Step 2: Stage 2 — Functional Validation

- `## 관련 파일` 테이블의 각 경로에 대해 `find_by_name`으로 존재 확인
- description에 트리거 조건 3개 이상 포함 여부 확인
- `skills/` 하위 파일이 있으면 각 파일의 YAML frontmatter 유효성 확인

결과: `functional: "pass" | "fail"`

### Step 3: Stage 3 — Quality (Reflection)

`references/tot-guide.md`의 Reflection 프레임워크로 자가 평가:

| 항목 | 심각도 | 설명 | 수정안 |
|------|--------|------|--------|
| 원본 요청 일치도 | ... | ... | ... |
| 에지케이스 처리 | ... | ... | ... |
| 토큰 효율성 | ... | ... | ... |
| 보안/안전성 | ... | ... | ... |

심각도 분류:

- **critical** → 자동 수정 시도 (최대 2회, 3회 초과 시 유저에게 수동 검토 요청)
- **warning** → 유저에게 보고
- **info** → 무시

### Step 4: 최종 보고서 작성

`work/verify/verify-report.json` 저장:

```json
{
  "schema": "pass | fail",
  "functional": "pass | fail",
  "quality_score": 0,
  "issues": [],
  "auto_fixed": 0
}
```

PIPELINE-LOG.md에 기록:

```
## T3: 검증 (Reviewer)
- Schema: {pass/fail} | Functional: {pass/fail} | Quality: {N}/10
- 이슈: {N}건 (자동 수정: {N}건)
- 완료: {시각}
```

## 관련 파일

| File | Purpose |
|------|---------|
| `../../verification-layer/SKILL.md` | 검증 기준 상세 |
| `references/tot-guide.md` | Reflection 프레임워크 |
| `work/forge/` | 검증 대상 파일들 |
| `05-exit.md` | 다음 단계 |

## 예외사항

1. **자동 수정 3회 이상**: 중단하고 유저에게 이슈 목록과 함께 수동 수정 요청
2. **03-forge 실패로 검증 대상 없음**: 이 단계를 스킵하고 05-exit으로 이동
