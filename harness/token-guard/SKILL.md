---
name: token-guard
description: >
  장시간 작업의 토큰 소모를 추적하고, 임계값 도달 시 체크포인트 JSON+MD를
  자동 생성하여 다음 세션에서 이어서 작업할 수 있게 합니다.
  MAX_TOKENS 제한이 있는 복합 태스크, 멀티 스텝 코드 생성, 스킬 자동 생성 등
  장시간 에이전트 작업 전에 반드시 활성화하세요.
---

# Token Guard — 토큰 관리 + 체크포인트

## 인터페이스

### 입력 (from Orchestrator)

- 수신: `{ max_tokens, thresholds, task_id, working_dir }`
- 수신 시점:
  - **초기화**: `skills/00-preflight.md` 토큰 게이지 설정 시
  - **종료 체크**: `skills/05-exit.md` 실행 전

### 출력 (to Orchestrator)

- `checkpoint.json` 자동 저장 (`templates/checkpoint.template.jsonc` 형식)
- `{ estimated_used, utilization, action, checkpoint_path }` 반환

### 호출 방식

- Leader가 `skills/00-preflight.md` 실행 중 토큰 게이지 초기화
- `skills/05-exit.md` 실행 전 토큰 내역 확인 + `checkpoint.json` 업데이트

---

## 목적

Antigravity 환경에서 **외부 API 없이** 토큰 소모를 자가 추정하고, 중단 위험 시 작업 상태를 보존합니다.

1. **토큰 추정** — 출력 길이 기반 자가 추정 (tiktoken 불필요)
2. **3단계 임계값** — 80% 경고 / 90% 강제 저장 / 95% 즉시 중단
3. **체크포인트 생성** — JSON + MD 파일 동시 생성 (stop 스킬 handoff 패턴)
4. **Resume** — 체크포인트에서 작업 재개

## 실행 시점

- 복합 태스크(composite/research) 시작 전
- Orchestrator가 `MAX_TOKENS`를 초과할 수 있는 작업을 감지했을 때
- 사용자가 "이어서 해줘", "resume", "체크포인트" 등을 말했을 때
- 이전 세션의 `harness_checkpoint.json`이 작업 디렉토리에 존재할 때

---

## 토큰 추정 방법 (외부 도구 불필요)

외부 API나 tiktoken 없이 토큰을 추정하는 규칙:

```
한국어 1글자 ≈ 2-3 토큰
영어 1단어 ≈ 1.3 토큰
코드 1줄 ≈ 10-15 토큰
마크다운 1줄 ≈ 8-12 토큰
```

### 추정 체크리스트

각 주요 출력 후, 누적 추정치를 자가 점검합니다:

```markdown
## 🔋 토큰 게이지 (자가 추정)
| 항목 | 추정 토큰 |
|------|----------|
| 입력 (유저 요청 + 컨텍스트) | ~2,000 |
| 출력 1: token-guard SKILL.md | ~1,200 |
| 출력 2: orchestrator SKILL.md | ~1,500 |
| **누적** | **~4,700 / 10,000 (47%)** |
```

---

## 3단계 임계값 시스템

| 임계값 | 토큰 (MAX=10,000) | 액션 |
|--------|-------------------|------|
| ⚠️ **경고** | 8,000 (80%) | 토큰 게이지 표시 + 남은 작업 우선순위 조정 |
| 🔶 **강제 저장** | 9,000 (90%) | `harness_checkpoint.json` + `CHECKPOINT.md` 즉시 생성 |
| 🔴 **즉시 중단** | 9,500 (95%) | 최종 저장 후 현재 단계 요약만 출력하고 중단 |

### 각 단계별 행동

#### 80% 경고

```markdown
> ⚠️ **토큰 경고**: ~8,000/10,000 사용 (80%)
> 남은 토큰으로 완료 가능한 작업을 우선 처리합니다.
> 현재 작업: [진행 중인 파일명]
> 남은 작업: [pending 목록]
```

- 남은 작업 중 가장 중요한 것만 선택하여 완료
- 부가 문서(references/) 작성은 후순위

#### 90% 강제 저장

현재 작업 폴더에 체크포인트 파일 2개를 즉시 생성:

1. **`harness_checkpoint.json`** — 기계 판독용 (아래 스키마 참조)
2. **`CHECKPOINT.md`** — 사람 판독용 (간결 요약)

#### 95% 즉시 중단

```markdown
> 🔴 **토큰 한계 도달**: 즉시 중단합니다.
> 체크포인트가 저장되었습니다: `harness_checkpoint.json`
> 새 세션에서 "이어서 해줘"로 재개하세요.
```

---

## 체크포인트 파일 생성

### harness_checkpoint.json

```json
{
  "schema_version": "1.0",
  "session": {
    "timestamp": "ISO-8601",
    "project_name": "harness-skills",
    "project_root": "c:\\hehe\\harness",
    "max_tokens": 10000,
    "estimated_used": 9000
  },
  "token_thresholds": {
    "warning": 8000,
    "force_save": 9000,
    "halt": 9500
  },
  "status": {
    "completed": ["token-guard/SKILL.md", "token-guard/references/checkpoint-schema.md"],
    "in_progress": [{
      "task": "harness-orchestrator/SKILL.md",
      "stopping_point": "ToT 분기 섹션 50% 작성",
      "blockers": []
    }],
    "pending": ["skill-forge/SKILL.md", "mcp-router/SKILL.md"]
  },
  "critical_context": [
    "외부 API 호출 금지 — Antigravity + 로컬 도구만 사용",
    "로컬 도구 설치는 사용자 승인 후에만",
    "MAX_TOKENS: 10000"
  ],
  "next_steps": [
    "harness-orchestrator/SKILL.md ToT 분기 섹션 완성",
    "instruction-gen/SKILL.md 작성"
  ],
  "resume_instructions": "이 JSON을 읽고 in_progress의 stopping_point부터 재개. completed 파일은 건드리지 않음."
}
```

### CHECKPOINT.md

```markdown
# CHECKPOINT — Harness Skills
> 저장 시각: {timestamp} | 토큰: ~{used}/{max} ({percentage}%)

## ✅ 완료
- {완료된 파일 목록}

## 🔄 진행 중
- **{파일명}** — {중단 지점 설명}

## ⏭️ 다음 단계
1. {즉시 실행 가능한 첫 번째 액션}
2. {두 번째 액션}

## 🔑 필수 컨텍스트
- {다음 세션이 반드시 알아야 할 사항}
```

---

## Resume 절차 (새 세션에서)

사용자가 "이어서 해줘", "resume", "체크포인트에서 재개" 등을 말하면:

### Step 1: 체크포인트 탐색

```
# 작업 디렉토리에서 체크포인트 파일 탐색
find_by_name("harness_checkpoint.json", "c:\hehe\harness")
find_by_name("CHECKPOINT.md", "c:\hehe\harness")
```

### Step 2: JSON 파싱 및 상태 복원

`harness_checkpoint.json`을 읽고:

- `status.completed` → 이미 완료된 작업 (건너뜀)
- `status.in_progress` → `stopping_point`에서 재개
- `status.pending` → 대기 목록으로 유지
- `critical_context` → 현재 세션에 적용

### Step 3: 무결성 검증

`completed` 목록의 각 파일이 실제로 존재하는지 확인:

```
# 각 완료 파일 존재 확인 (Antigravity 도구)
view_file("{파일경로}")   ← 파일 존재 + 내용 확인
find_by_name("SKILL.md", "{skill_dir}")  ← 파일 탐색
```

### Step 4: 컨텍스트 브리핑

```markdown
## 🔄 세션 재개
**체크포인트**: {timestamp}
**완료**: {N}개 파일
**재개 지점**: {in_progress 파일} — {stopping_point}
**남은 작업**: {pending 목록}
```

### Step 5: 실행 재개

`next_steps`의 첫 번째 항목부터 실행 시작.

---

## 관련 파일

| File | Purpose |
|------|---------|
| `harness-orchestrator/templates/checkpoint.template.jsonc` | 체크포인트 포맷 템플릿 |
| `harness-orchestrator/skills/00-preflight.md` | Leader가 토큰 게이지 초기 참조 |
| `harness-orchestrator/skills/05-exit.md` | Leader가 종료 시 토큰 최종 확인 |

## 예외사항

다음은 **문제가 아닙니다**:

1. **토큰 추정의 오차** — ±15% 오차는 정상. 임계값에 여유를 두고 설계됨
2. **체크포인트 없는 simple 태스크** — 단순 작업은 토큰 가드 불필요
3. **이전 체크포인트 덮어쓰기** — 새 체크포인트 생성 시 이전 파일은 자동 덮어씀
4. **references/ 미완성** — 핵심 SKILL.md만 완성되면 references/는 다음 세션에서 보강 가능
