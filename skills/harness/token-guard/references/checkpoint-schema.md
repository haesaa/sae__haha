# Checkpoint JSON Schema Reference

## 필드 설명

### `session` (세션 메타데이터)

| 필드 | 타입 | 설명 |
|------|------|------|
| `timestamp` | string | ISO-8601 형식 저장 시각 |
| `project_name` | string | 프로젝트 식별자 |
| `project_root` | string | 절대 경로 |
| `max_tokens` | number | 세션 토큰 한도 (기본: 10000) |
| `estimated_used` | number | 저장 시점 추정 사용량 |

### `token_thresholds` (임계값)

| 필드 | 기본값 | 트리거 액션 |
|------|--------|------------|
| `warning` | 8000 | 게이지 표시 + 우선순위 조정 |
| `force_save` | 9000 | 체크포인트 강제 생성 |
| `halt` | 9500 | 즉시 중단 |

### `status` (작업 진행 상태)

- **`completed`**: `string[]` — 완료된 파일 상대 경로 목록
- **`in_progress`**: `object[]` — 진행 중 작업
  - `task`: 파일 경로
  - `stopping_point`: 중단 지점 설명
  - `blockers`: 차단 사유 (빈 배열이면 없음)
- **`pending`**: `string[]` — 아직 시작하지 않은 작업

### `critical_context` (필수 컨텍스트)

다음 세션이 **반드시** 알아야 할 사항. 예:

- 환경 제약 ("외부 API 금지")
- 핵심 결정 ("로컬 도구 사용자 승인 필수")
- 의존성 ("Phase 1 완료 후 Phase 2 시작")

### `next_steps` (다음 행동)

순서대로 즉시 실행 가능한 액션 목록. 첫 번째 항목이 재개 시 시작점.

### `resume_instructions` (재개 지침)

자연어로 된 한 줄 재개 가이드.

---

## 예시 1: 진행 중 (paused)

```json
{
  "schema_version": "1.0",
  "session": {
    "timestamp": "2026-02-27T15:30:00+09:00",
    "project_name": "harness-skills",
    "project_root": "c:\\hehe\\harness",
    "max_tokens": 10000,
    "estimated_used": 9100
  },
  "token_thresholds": { "warning": 8000, "force_save": 9000, "halt": 9500 },
  "status": {
    "completed": ["token-guard/SKILL.md", "token-guard/references/checkpoint-schema.md", "harness-orchestrator/SKILL.md"],
    "in_progress": [{
      "task": "skill-forge/SKILL.md",
      "stopping_point": "5단계 파이프라인 중 Step 3 SKILL.md 생성 섹션까지 작성",
      "blockers": []
    }],
    "pending": ["mcp-router/SKILL.md", "verification-layer/SKILL.md", "CLAUDE.md"]
  },
  "critical_context": ["외부 API 금지", "MCP 가이드 파일 참조 경로: Awesome-MCP-Servers-한국어-가이드.md"],
  "next_steps": ["skill-forge/SKILL.md Step 4-5 완성", "mcp-router/SKILL.md 작성"],
  "resume_instructions": "skill-forge/SKILL.md의 Step 3까지 완성됨. Step 4(번들 생성)부터 이어서 작성."
}
```

## 예시 2: 완료 (completed)

```json
{
  "schema_version": "1.0",
  "session": {
    "timestamp": "2026-02-27T16:00:00+09:00",
    "project_name": "harness-skills",
    "project_root": "c:\\hehe\\harness",
    "max_tokens": 10000,
    "estimated_used": 8500
  },
  "token_thresholds": { "warning": 8000, "force_save": 9000, "halt": 9500 },
  "status": {
    "completed": [
      "token-guard/SKILL.md", "token-guard/references/checkpoint-schema.md",
      "harness-orchestrator/SKILL.md", "harness-orchestrator/references/tot-guide.md",
      "instruction-gen/SKILL.md", "skill-forge/SKILL.md",
      "mcp-router/SKILL.md", "verification-layer/SKILL.md", "CLAUDE.md"
    ],
    "in_progress": [],
    "pending": []
  },
  "critical_context": [],
  "next_steps": ["검증 실행: 각 SKILL.md YAML frontmatter 확인", "수동 테스트: Antigravity에서 트리거 확인"],
  "resume_instructions": "모든 스킬 작성 완료. 검증 단계만 남음."
}
```
