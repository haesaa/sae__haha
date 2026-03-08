# E2E Dry-Run: Slack 주간 리포트 스킬 생성

> **시나리오 출처**: `harness-architecture-design_v1.md §3`
> **실행 기준**: `harness-orchestrator/SKILL.md v2` 파이프라인 런너

## 테스트 입력 (I1)

```json
{
  "raw_request": "Slack 메시지를 분석해서 주간 리포트 만드는 스킬 만들어줘",
  "timestamp": "2026-02-27T16:09:00+09:00",
  "max_tokens": 10000,
  "working_dir": "c:\\hehe\\harness"
}
```

---

## 기대 실행 흐름

### Step 1: Orchestrator 트리거 (I1 수신)

- **입력**: I1 `{ raw_request, timestamp, max_tokens, working_dir }`
- **복잡도 판정**: `composite`
  - 키워드 2개 이상: `슬랙`, `메시지`, `분석`, `스킬 만들어` → 도메인 교차
- **ToT 3분기 생성**:

| 분기 | 전략 | 실현(×0.4) | 품질(×0.35) | 비용(×0.25) | 총점 |
|------|------|-----------|------------|------------|------|
| A | 단일 SKILL.md (Slack MCP + 분석 + 리포트 통합) | 8 | 8 | 9 | **8.25** |
| B | MCP + 분석 스크립트 + 별도 리포트 스킬 | 6 | 9 | 5 | **6.90** |
| C | 기존 prompts 파이프라인 fork | 4 | 6 | 8 | **5.75** |

→ **Branch A 선택** (총점 8.25)

- **pipeline_state 초기화**: `task_id = "slack-weekly-report-20260227"`

---

### Step 2: TokenGuard 초기화 — 프로시저 4a (I2 송신)

- **I2 송신**:

  ```json
  { "max_tokens": 10000, "thresholds": { "warning": 0.80, "force_save": 0.90, "halt": 0.95 }, "task_id": "slack-weekly-report-20260227", "working_dir": "c:\\hehe\\harness" }
  ```

- **I7 수신** (기대):

  ```json
  { "estimated_used": 800, "utilization": 0.08, "action": "continue" }
  ```

- **결과**: `pipeline_state.token_guard = { utilization: 0.08, action: "continue" }`

---

### Step 3: MCP Router — 프로시저 4b (I3 송신)

- **동적 로딩**: `view_file("mcp-router/SKILL.md")`
- **I3 송신**:

  ```json
  { "intent": "slack_message_analysis_report", "keywords": ["Slack", "슬랙", "메시지", "분석"], "fallback_ok": true }
  ```

- **매핑 테이블 매칭**: `슬랙|채널|메시지` → Slack MCP Server
- **기대 결과**:

  ```json
  { "matched_servers": [{ "name": "Slack MCP", "status": "recommended", "install_guide": "사용자 승인 후 설치" }], "fallback": null }
  ```

- **pipeline_state.mcp_result** 업데이트

---

### Step 4: InstructionGen — 프로시저 4c (I4 송신)

- **동적 로딩**: `view_file("instruction-gen/SKILL.md")`
- **I4 송신**:

  ```json
  { "task_type": "skill_generation", "domain": ["analysis", "writing"], "constraints": { "remaining_tokens": 8000, "no_external_api": true }, "mcp_context": { "matched_servers": [{ "name": "Slack MCP" }] } }
  ```

- **생성 결과** (기대):

  ```
  Base: Role + OutputFormat + Constraints + CoT Scaffold
  Extension: analysis (데이터 소스, 분석 프레임) + writing (리포트 구조, 톤)
  ```

- **pipeline_state.system_prompt** = 생성된 지침

---

### Step 5: SkillForge — 프로시저 4d (I5 송신)

- **동적 로딩**: `view_file("skill-forge/SKILL.md")`
- **I5 송신**:

  ```json
  { "skill_name": "slack-weekly-report", "domain": "analysis", "raw_request": "Slack 메시지를 분석해서 주간 리포트 만드는 스킬 만들어줘", "output_dir": "c:\\hehe\\harness\\slack-weekly-report", "constraints": { "max_skill_lines": 500 } }
  ```

- **5단계 파이프라인 실행**:
  1. Intent Extraction → `domain: analysis+writing, trigger: Slack MCP 활성 시`
  2. Registry Search → 유사 스킬 없음 → blank template
  3. SKILL.md 생성 → frontmatter + 4개 필수 섹션
  4. 번들 생성 → `scripts/analyze_slack.py`, `references/report-format.md`
  5. I6 포장 → Verification 전달
- **기대 파일**:
  - `slack-weekly-report/SKILL.md`
  - `slack-weekly-report/scripts/analyze_slack.py`
  - `slack-weekly-report/references/report-format.md`

---

### Step 6: Verification — 프로시저 4e (I6 수신)

- **동적 로딩**: `view_file("verification-layer/SKILL.md")`
- **I6 수신**:

  ```json
  { "target_files": ["slack-weekly-report/SKILL.md", "slack-weekly-report/scripts/..."], "original_request": "...", "skill_name": "slack-weekly-report", "stages": ["schema", "functional", "quality"] }
  ```

- **Stage 1 (Schema)**: frontmatter + name + description → PASS
- **Stage 2 (Functional)**: 파일 존재 확인 → PASS
- **Stage 3 (Quality/Reflection)**: Self-review → score 8/10, warning 1건 (에지케이스 처리)
  - → 자동 수정 1회 → 재검증 PASS
- **pipeline_state.verification_report** 업데이트

---

### Step 7: TokenGuard 최종 체크 — 프로시저 4f

- **토큰 추정**: ~5,500 / 10,000 (55%)
- **I7 수신** (기대):

  ```json
  { "estimated_used": 5500, "utilization": 0.55, "action": "continue" }
  ```

- **결과**: 임계값 이하 → 파이프라인 완료

---

### Step 8: 결과 반환

```markdown
## ✅ 파이프라인 완료

**생성된 스킬**: slack-weekly-report
**위치**: c:\hehe\harness\slack-weekly-report\
**검증**: Schema PASS / Functional PASS / Quality 8/10
**MCP 추천**: Slack MCP Server (설치 안내 링크 포함)
**토큰 사용**: ~5,500/10,000 (55%)
```
