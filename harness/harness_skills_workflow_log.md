# Harness Skills 워크플로우 로그

---

### [1단계]: 아키텍처 분석 및 계획 수립

- **핵심 요약**: `harness-architecture-design.md`의 6개 모듈(Orchestrator, Skill Forge, MCP Router, Instruction Generator, Token Guard, Verification Layer)을 분석하고, Antigravity 네이티브 스킬로 경량 변환하는 구현 계획 v3 수립
- **주요 워크플로우**:
  - [완료] 하네스 아키텍처 문서 분석
  - [완료] Antigravity SKILL.md 표준(SKILL_ANATOMY.md, skill-creator) 분석
  - [완료] 참조 스킬 3개(manage-skills, stop, verify-implementation) 패턴 분석
  - [완료] 구현 계획서 v3 작성 및 사용자 승인
- **수정/특이사항**: 사용자 피드백으로 외부 API 금지, 로컬 도구 사용자 승인 후만 실행, MAX_TOKENS 10000 제한 확정
- **현재 상태**: [완료]
- **다음 단계**: Phase 1 구현

---

### [2단계]: Phase 1 — Token Guard + Checkpoint

- **핵심 요약**: 토큰 자가 추정 + 3단계 임계값(80%/90%/95%) + 체크포인트 JSON+MD 자동 생성 스킬 구현
- **주요 워크플로우**:
  - [완료] `token-guard/SKILL.md` 작성 (221줄)
  - [완료] `token-guard/references/checkpoint-schema.md` 작성 (96줄, JSON 스키마 상세 + 예시 2개)
- **수정/특이사항**: `stop` 스킬의 handoff.json 패턴을 체크포인트 스키마에 차용
- **현재 상태**: [완료]
- **다음 단계**: Phase 2 구현

---

### [3단계]: Phase 2 — Orchestrator + Instruction Generator

- **핵심 요약**: ToT 3분기 + ToC 가중 채점을 단일 프롬프트에서 수행하는 오케스트레이터와, Base+Domain Extension 조합 지침 생성기 구현
- **주요 워크플로우**:
  - [완료] `harness-orchestrator/SKILL.md` 작성 (195줄, 복잡도 판정 + ToT + DisPatch)
  - [완료] `harness-orchestrator/references/tot-guide.md` 작성 (ToT/ToC/Reflection 가이드)
  - [완료] `instruction-gen/SKILL.md` 작성 (131줄, CoT Scaffold 자동 삽입)
- **수정/특이사항**: `manage-skills`의 결정트리 패턴을 복잡도 판정에 차용
- **현재 상태**: [완료]
- **다음 단계**: Phase 3 구현

---

### [4단계]: Phase 3 — Skill Forge + MCP Router + Verification Layer

- **핵심 요약**: 스킬 자동 생성, MCP 서버 추천, 3단계 품질 검증 모듈 구현 완료
- **주요 워크플로우**:
  - [완료] `skill-forge/SKILL.md` 작성 (130줄, 5단계 파이프라인)
  - [완료] `mcp-router/SKILL.md` 작성 (105줄, 2596개 MCP 카탈로그 참조)
  - [완료] `verification-layer/SKILL.md` 작성 (159줄, Schema/Functional/Quality + 자동수정)
  - [완료] `CLAUDE.md` 작성 (하네스 전체 가이드)
- **수정/특이사항**: `verify-implementation`의 순차 검증 루프를 Quality Stage에 차용
- **현재 상태**: [완료]
- **다음 단계**: 구조 검증

---

### [5단계]: 구조 검증

- **핵심 요약**: 6개 SKILL.md 존재 확인 및 줄 수 검증 — 전체 PASS
- **주요 워크플로우**:
  - [완료] PowerShell 자동 검증 스크립트 실행
  - [완료] 6/6 SKILL.md 정상 확인 (105~221줄, 전부 500줄 이내)
  - [완료] 11개 파일 전체 존재 확인
- **현재 상태**: [완료]
- **다음 단계**: 수동 테스트 (Antigravity 세션에서 트리거 확인)

---

## [6단계]: harness-orchestrator Agent Teams 구조 전환 (1차 + 2차 수정)

- **핵심 요약**: `skills_teams_v1.md` + `skills_teams_v1_v1.md` 참조 기반으로 `harness-orchestrator`를 단일 에이전트 구조(448줄 모노리식)에서 Agent Teams 구조(Leader/Analyst/Builder/Reviewer + skills/ 분리)로 전면 리팩토링.
- **주요 워크플로우**:
  - [완료] 1차 수정: SKILL.md를 슬림한 진입점으로 재작성 (팀 구성, 흐름 지도, 전역 룰)
  - [완료] 1차 수정: `skills/00-preflight.md` — 환경 초기화 + Resume 판정 + 보안 스캔
  - [완료] 1차 수정: `skills/01-complexity.md` — 복잡도 판정 + ToT 3분기 + ToC 채점
  - [완료] 1차 수정: `skills/02-analyze.md` — Analyst: MCP Router + Instruction Gen
  - [완료] 1차 수정: `skills/03-forge.md` — Builder: simple/composite 템플릿 분기 + 스킬 생성
  - [완료] 1차 수정: `skills/04-verify.md` — Reviewer: Schema/Functional/Quality 3단계 검증
  - [완료] 1차 수정: `skills/05-exit.md` — Graceful Degradation + 최종 보고
  - [완료] 1차 수정: `templates/` 3종 (PIPELINE-LOG, TASK-REPORT, FINAL-REPORT)
  - [완료] 2차 수정: SKILL.md에 토큰 하드리밋(MAX_TOKENS=10,000) 정책 추가
  - [완료] 2차 수정: 파일 보존 정책 세분화 (보존 대상/정리 가능 구분)
  - [완료] 2차 수정: 보안 정책 테이블 (위협/대응/내장위치 7종) 추가
  - [완료] 2차 수정: 한글 주석 정책 명시 (jsonc 형식, 블록쿼트 설명)
  - [완료] 2차 수정: `templates/checkpoint.template.jsonc` 신규 생성 (한글 주석 포함)
- **수정/특이사항**: 기존 ToT/ToC/Reflection 로직은 모두 01-complexity + 04-verify로 분산 이관하여 보존. pipeline_state JSON은 checkpoint.json으로 명칭 변경 및 jsonc 형식 전환.
- **현재 상태**: [완료]
- **다음 단계**: Antigravity 세션에서 `--harness` 트리거로 E2E 파이프라인 검증
