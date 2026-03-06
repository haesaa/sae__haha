# Interface Specification — Harness Skills v2

> 모듈 간 데이터 교환 스키마. Pipeline Runner가 `pipeline_state` 객체를 통해 각 모듈에 데이터를 전달.

## ToC

- [I1: UserRequest → Orchestrator](#i1-userrequest--orchestrator)
- [I2: Orchestrator → TokenGuard](#i2-orchestrator--tokenguard)
- [I3: Orchestrator → MCP Router](#i3-orchestrator--mcp-router)
- [I4: Orchestrator → InstructionGen](#i4-orchestrator--instructiongen)
- [I5: Orchestrator → SkillForge](#i5-orchestrator--skillforge)
- [I6: SkillForge → Verification](#i6-skillforge--verification)
- [I7: TokenGuard → Orchestrator](#i7-tokenguard--orchestrator)
- [pipeline_state 전체 스키마](#pipeline_state-전체-스키마)

---

## I1: UserRequest → Orchestrator

```json
{
  "interface_id": "I1",
  "source_module": "user",
  "target_module": "harness-orchestrator",
  "payload": {
    "raw_request":   { "type": "string",  "required": true,  "desc": "유저 원본 요청" },
    "timestamp":     { "type": "string",  "required": true,  "desc": "ISO-8601 요청 시각" },
    "max_tokens":    { "type": "integer", "required": false, "default": 10000, "desc": "세션 최대 토큰 수" },
    "working_dir":   { "type": "string",  "required": false, "default": "c:\\hehe\\harness", "desc": "작업 디렉토리" },
    "resume_from":   { "type": "string",  "required": false, "desc": "체크포인트 파일 경로 (Resume 시)" }
  },
  "example": {
    "raw_request": "Slack 메시지를 분석해서 주간 리포트 만드는 스킬 만들어줘",
    "timestamp": "2026-02-27T15:00:00+09:00",
    "max_tokens": 10000,
    "working_dir": "c:\\hehe\\harness"
  }
}
```

---

## I2: Orchestrator → TokenGuard

```json
{
  "interface_id": "I2",
  "source_module": "harness-orchestrator",
  "target_module": "token-guard",
  "payload": {
    "max_tokens":  { "type": "integer", "required": true,  "desc": "세션 한도" },
    "thresholds": {
      "warning":    { "type": "float", "default": 0.80 },
      "force_save": { "type": "float", "default": 0.90 },
      "halt":       { "type": "float", "default": 0.95 }
    },
    "task_id":     { "type": "string", "required": true,  "desc": "세션 식별자" },
    "working_dir": { "type": "string", "required": true }
  },
  "example": {
    "max_tokens": 10000,
    "thresholds": { "warning": 0.80, "force_save": 0.90, "halt": 0.95 },
    "task_id": "slack-weekly-report-20260227",
    "working_dir": "c:\\hehe\\harness"
  }
}
```

---

## I3: Orchestrator → MCP Router

```json
{
  "interface_id": "I3",
  "source_module": "harness-orchestrator",
  "target_module": "mcp-router",
  "payload": {
    "intent":    { "type": "string",   "required": true,  "desc": "태스크 의도 요약" },
    "keywords":  { "type": "string[]", "required": true,  "desc": "추출된 서비스 키워드" },
    "fallback_ok":{ "type": "boolean", "required": false, "default": true, "desc": "MCP 실패 시 fallback 허용" }
  },
  "example": {
    "intent": "slack_message_analysis_and_report_generation",
    "keywords": ["Slack", "슬랙", "메시지", "분석", "리포트"],
    "fallback_ok": true
  }
}
```

---

## I4: Orchestrator → InstructionGen

```json
{
  "interface_id": "I4",
  "source_module": "harness-orchestrator",
  "target_module": "instruction-gen",
  "payload": {
    "task_type":   { "type": "string",   "required": true,  "desc": "skill_generation|code|analysis|writing|integration" },
    "domain":      { "type": "string[]", "required": true,  "desc": "도메인 목록 (복합 가능)" },
    "constraints": { "type": "object",   "required": false, "desc": "토큰 예산, API 제약 등" },
    "mcp_context": { "type": "object",   "required": false, "desc": "I3 결과 (MCP 서버 정보)" }
  },
  "example": {
    "task_type": "skill_generation",
    "domain": ["analysis", "writing"],
    "constraints": { "remaining_tokens": 7000, "no_external_api": true },
    "mcp_context": { "matched_servers": [{ "name": "Slack", "status": "recommended" }] }
  }
}
```

---

## I5: Orchestrator → SkillForge

```json
{
  "interface_id": "I5",
  "source_module": "harness-orchestrator",
  "target_module": "skill-forge",
  "payload": {
    "skill_name":     { "type": "string",   "required": true,  "desc": "kebab-case 스킬명" },
    "domain":         { "type": "string",   "required": true },
    "raw_request":    { "type": "string",   "required": true,  "desc": "유저 원본 (I1상속)" },
    "system_prompt":  { "type": "string",   "required": false, "desc": "I4 결과" },
    "output_dir":     { "type": "string",   "required": true,  "desc": "스킬 생성 경로" },
    "constraints":    { "type": "object",   "required": false }
  },
  "example": {
    "skill_name": "slack-weekly-report",
    "domain": "analysis",
    "raw_request": "Slack 메시지를 분석해서 주간 리포트 만드는 스킬 만들어줘",
    "system_prompt": "## Role\nSlack 데이터 분석 전문가...",
    "output_dir": "c:\\hehe\\harness\\slack-weekly-report",
    "constraints": { "max_skill_lines": 500 }
  }
}
```

---

## I6: SkillForge → Verification

```json
{
  "interface_id": "I6",
  "source_module": "skill-forge",
  "target_module": "verification-layer",
  "payload": {
    "target_files":    { "type": "string[]", "required": true,  "desc": "검증 대상 파일 절대 경로" },
    "original_request":{ "type": "string",   "required": true },
    "skill_name":      { "type": "string",   "required": true },
    "stages":          { "type": "string[]", "required": false, "default": ["schema","functional","quality"] }
  },
  "example": {
    "target_files": [
      "c:\\hehe\\harness\\slack-weekly-report\\SKILL.md",
      "c:\\hehe\\harness\\slack-weekly-report\\scripts\\analyze_slack.py"
    ],
    "original_request": "Slack 메시지를 분석해서 주간 리포트 만드는 스킬 만들어줘",
    "skill_name": "slack-weekly-report",
    "stages": ["schema", "functional", "quality"]
  }
}
```

---

## I7: TokenGuard → Orchestrator

> ⚠️ **단방향** (TokenGuard → Orchestrator). 순환 참조 없음.

```json
{
  "interface_id": "I7",
  "source_module": "token-guard",
  "target_module": "harness-orchestrator",
  "payload": {
    "estimated_used":  { "type": "integer", "required": true,  "desc": "추정 사용 토큰" },
    "utilization":     { "type": "float",   "required": true,  "desc": "0.0 ~ 1.0" },
    "action":          { "type": "string",  "required": true,  "desc": "continue|warn|checkpoint|halt" },
    "checkpoint_path": { "type": "string",  "required": false, "desc": "저장된 체크포인트 경로" }
  },
  "example": {
    "estimated_used": 8200,
    "utilization": 0.82,
    "action": "warn",
    "checkpoint_path": null
  }
}
```

---

## pipeline_state 전체 스키마

Orchestrator가 전체 파이프라인 진행 중 유지하는 공유 상태 객체.

```json
{
  "task_id": "string",
  "original_request": "string",
  "complexity": "simple|composite|research",
  "selected_branch": "A|B|C",
  "token_guard": {
    "estimated_used": 0,
    "utilization": 0.0,
    "action": "continue"
  },
  "mcp_result": {
    "matched_servers": [],
    "fallback": null
  },
  "system_prompt": "string|null",
  "skill_forge_result": {
    "skill_name": "string",
    "output_dir": "string",
    "files": []
  },
  "verification_report": {
    "schema": "pass|fail",
    "functional": "pass|fail",
    "quality_score": 0,
    "issues": [],
    "auto_fixed": 0
  },
  "completed_procedures": [],
  "errors": []
}
```
