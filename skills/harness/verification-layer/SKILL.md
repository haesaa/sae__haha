---
name: verification-layer
description: >
  스킬, 코드, 지침 등 하네스 출력물에 대해 3단계 검증(Schema → Functional → Quality)을
  수행합니다. Reflection(자체 리뷰) 기법으로 품질을 보증하고,
  critical 이슈는 최대 2회 자동 수정합니다.
  "검증해줘", "확인해줘", "품질 체크", "리뷰" 등의 요청에 활성화.
---

# Verification Layer — 3단계 검증 파이프라인

## 인터페이스

### 입력 (from SkillForge)

- 수신: `{ target_files, original_request, skill_name, stages }` (Reviewer 팀원이 수신)
- 수신 시점: **`skills/04-verify.md`** 에서 호출

### 출력 (to Orchestrator)

- `work/verify/verify-report.json`에 결과 저장
- critical 이슈 자동 수정 후 Leader에 업데이트

### 호출 방식

- Reviewer가 `view_file("verification-layer/SKILL.md")`로 동적 로딩
- 3단계 검증 실행
- 결과를 `work/verify/verify-report.json`에 저장

---

## 목적

하네스가 생성한 모든 출력물(SKILL.md, 코드, 지침 등)에 대해
`verify-implementation` 패턴의 순차 검증 → 수정 → 재검증 루프를 적용합니다.

## 실행 시점

- Skill Forge가 스킬 생성을 완료한 후
- Orchestrator가 최종 출력 전 품질 확인 요청 시
- 사용자가 "검증해줘", "리뷰해줘" 요청

---

## 워크플로우

### Stage 1: Schema Validation (구조 검증)

출력물의 구조적 정합성을 확인합니다.

### SKILL.md 검증

```markdown
| 항목 | 검사 내용 | PASS 기준 |
|------|----------|----------|
| YAML frontmatter | `---` 블록 존재 | 파일 시작이 `---` |
| name 필드 | 필수 필드 존재 | 비어있지 않은 문자열 |
| description 필드 | 필수 필드 존재 | 비어있지 않은 문자열 |
| name-폴더 일치 | name = 폴더명 | 정확히 일치 |
| 줄 수 | 500줄 이내 권장 | ≤500 (초과 시 warning) |
```

```
# YAML frontmatter 확인 (Antigravity 도구)
view_file("{file_path}")  ← 파일 내용 확인, 첫 줄이 "---"인지 검증
```

### JSON 출력 검증

```
# JSON 유효성 (Antigravity 도구)
view_file("{file_path}")  ← JSON 내용 읽기 후 구조 확인
```

---

## Stage 2: Functional Validation (기능 검증)

출력물이 실제로 동작하는지 확인합니다.

### 스킬 Dry-run

1. SKILL.md의 "When to Use" 섹션에서 트리거 조건 추출
2. 테스트 프롬프트 생성 → 스킬이 활성화되는지 확인
3. Related Files의 경로가 실제 존재하는지 확인

```
# 파일 존재 확인 (Antigravity 도구)
find_by_name("{filename}", "{Related Files의 디렉토리}")
```

### MCP Health Check (MCP Router 출력 시)

추천된 MCP 서버 URL이 접근 가능한지 확인:

```
# URL 접근 확인 (Antigravity 도구)
read_url_content("{url}")  ← 접근 가능 여부 확인
```

---

## Stage 3: Quality Validation (품질 검증 — Reflection)

ToT Reflection 기법을 적용하여 자체 출력물을 비판적으로 리뷰합니다.

### Self-Review 프롬프트

```markdown
다음 출력물을 검토합니다:

[출력물 내용]

검토 기준:
1. **원본 요청 일치도** — 유저가 원한 것과 실제 출력이 일치하는가?
2. **에지케이스** — 예외 상황이 처리되어 있는가?
3. **토큰 효율성** — 불필요한 반복이나 장황한 설명이 없는가?
4. **보안/안전성** — 위험한 작업이 포함되어 있지 않은가?

결과:
| # | 심각도 | 설명 | 수정안 |
|---|--------|------|--------|
```

### 심각도 분류

| 심각도 | 기준 | 자동 수정 |
|--------|------|----------|
| **critical** | 기능 불가, 보안 위험 | ✅ 자동 (최대 2회) |
| **warning** | 품질 저하, 비효율 | 사용자에게 보고 |
| **info** | 개선 가능 사항 | 무시 가능 |

---

## 자동 수정 루프

critical 이슈 발견 시:

```
1회차: critical 이슈 수정 → 재검증
2회차: 여전히 critical → 수정 → 재검증
3회차 이상: 수정 중단 → 사용자에게 수동 수정 요청
```

---

## 통합 보고서

모든 Stage 완료 후 (`verify-implementation` 패턴):

```markdown
## 검증 보고서

| Stage | 상태 | 이슈 |
|-------|------|------|
| 1. Schema | PASS/FAIL | {상세} |
| 2. Functional | PASS/FAIL | {상세} |
| 3. Quality | {점수}/10 | {상세} |

**총평**: {1줄 요약}
**자동 수정**: {N}건 적용
**남은 이슈**: {M}건 (사용자 확인 필요)
```

---

## 관련 파일

| File | Purpose |
|------|---------|
| `harness-orchestrator/skills/04-verify.md` | Reviewer가 Verification Layer 호출 |
| `skill-forge/SKILL.md` | 검증 대상 생성원 |

## 예외사항

1. **드래프트/WIP 출력물** — 완성되지 않은 출력물은 Stage 3 스킵
2. **사용자가 검증 스킵 요청** — "검증 건너뛰기" 시 전체 스킵
3. **simple 태스크** — Stage 1만 실행, Stage 2-3 스킵
4. **자동 수정 루프 무한반복** — 최대 2회로 제한
