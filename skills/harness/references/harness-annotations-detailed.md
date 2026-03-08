# Harness Skills v2 — 코어 파이프라인 상세 주석 및 주해

> **안내**: 원본 파일의 무결성을 유지하라는 지침("never touch 이미 만들어진 코드와 글들")에 따라,
> 각 모듈의 동작 원리, 상태 관리, 설계 의도 등 숨겨진 컨텍스트를 이 파일에 별도 주석으로 상세히 기록합니다.

---

## 1. `pipeline_state` 생명주기 주석 (harness-orchestrator)

**📁 대상 파일**: `harness-orchestrator/SKILL.md`
**📌 주요 메커니즘**: 단일 상태 관리 (Single Source of Truth)

- **[설계 의도]**: 6개의 모듈이 독립적으로 동작하면서도 데이터를 주고받아야 하므로, Orchestrator가 `pipeline_state`라는 전역 JSON 객체를 멱등성(Idempotency) 있게 관리합니다.
- **[동적 로딩 (view_file)]**: 각 모듈의 코드를 메모리에 상주시키지 않고 필요할 때만 불러와 모듈 간 결합도를 낮추고 토큰을 아낍니다.
- **[복잡도 판정 로직]**:
  - `simple`: 도메인이 하나면 ToT(Tree of Thoughts)를 생략해 불필요한 토큰/시간 낭비를 방지.
  - `composite`/`research`: 갈래가 다양한 요청은 AI가 길을 잃기 쉬우므로, ToT 3분기 생성 및 ToC(Token of Cost) 가중 채점으로 최적의 경로를 강제로 고르도록 설계되었습니다.
- **[비동기/Resume 지원]**: `completed_procedures` 배열에 완료된 단계를 `"5a"`, `"5b"` 식으로 푸시하여, 토큰 부족 시 언제든 체크포인트에서 재개할 수 있는 앵커 역할을 합니다.

---

## 2. Token Guard의 자가 추정 로직 주석

**📁 대상 파일**: `token-guard/SKILL.md`
**📌 주요 메커니즘**: 외부 API 없는 로컬 토큰 계측 (Heuristic Token Counting)

- **[토큰 추정 휴리스틱]**: `tiktoken` 같은 외부 의존성 없이 "한국어 1글자 ≈ 2-3토큰, 코드 1줄 ≈ 10-15토큰"의 경험칙(Rule of Thumb)을 사용합니다.
- **[3단계 임계값]**:
  - `80% (Warning)`: 우선순위가 떨어지는 덧붙임 문서 생성 등을 스킵하도록 AI의 행동 양식을 압박.
  - `90% (Checkpoint)`: `harness_checkpoint.json`에 `in_progress` 상태와 `stopping_point`를 스냅샷하여 안전망 구축.
  - `95% (Halt)`: 하드 리밋(10,000)을 넘어 컨텍스트가 잘리는 치명적 상황 전, 강제로 프로세스를 직렬화하여 종료.
- **[Handoff 패턴]**: 이전 세션의 기억을 새 세션에 전달하기 위한 `critical_context`와 `resume_instructions`를 체크포인트에 담아, 컨텍스트 소실 후에도 완벽한 재개가 가능하게 함.

---

## 3. MCP Router의 2단계 검색 로직 주석

**📁 대상 파일**: `mcp-router/SKILL.md`
**📌 주요 메커니즘**: 토큰 절약형 텍스트 스크래핑 (Deep Search Filter)

- **[Quick Match]**: 부하가 큰 2500+개 카탈로그 검색 전, 가장 빈도가 높은 상위 10개(Slack, GitHub 등)를 하드코딩된 테이블에서 먼저 걸러 토큰 소모를 `0`으로 만듭니다.
- **[Deep Search]**:
  - 정규표현식이나 `findstr` 같은 OS 종속 명령어를 쓰지 않고, Antigravity의 `grep_search` 도루를 안전하게 활용합니다.
  - 카테고리(예: `💬 커뮤니케이션`) 문자열에 걸리는 섹션 내부만 부분 조준하여, 불필요한 서버 목록이 검색 결과에 딸려 오지 않게 필터링하는 고도의 트릭입니다.

---

## 4. Instruction Gen의 도메인 매트릭스 주석

**📁 대상 파일**: `instruction-gen/SKILL.md`
**📌 주요 메커니즘**: 프롬프트 레고 블록 (Composite Prompting)

- **[동적 조립형 System Prompt]**: 정적인 지시문 프롬프트를 쓰지 않고, Base(역할+출력제한) + Extension(코드/분석/글쓰기 등 도메인 조각) + Scaffold(CoT 4단계)를 레고처럼 조립합니다.
- **[토큰 예산 연동 (Token-Aware Scaffold)]**: Token Guard가 남은 예산이 적다고 보고하면, 스스로 CoT 예시 조각을 잘라내어 길이를 동적으로 축소합니다. 이는 환각을 줄이면서 컨텍스트 제한에 적응하는 고급 기법입니다.

---

## 5. Skill Forge의 파일 포징 주석

**📁 대상 파일**: `skill-forge/SKILL.md`
**📌 주요 메커니즘**: 템플릿 및 자동 라우팅 보장

- **[빈출 조건 강제 주입(Pushy Principle)]**: 생성된 스킬이 수동적이지 않고, 특정 단어나 상황에 능동적으로 스스로 개입하도록 `description`을 매우 공격적이고 빈도가 높게 유도합니다.
- **[5대 필수 섹션 락(Lock)]**: Purpose, When to Use, Workflow, Related Files, Exceptions를 강제로 명시하게 하여, 어떠한 AI가 생성해도 일관된 품질(Antigravity 표준)을 보장합니다.
- **[용량 분산]**: 500줄이 넘어가는 코드는 `scripts/` 나 `references/` 로 찢어내어 메인 `SKILL.md`의 컨텍스트 비대를 막습니다.

---

## 6. Verification Layer의 자가 치유(Self-Healing) 주석

**📁 대상 파일**: `verification-layer/SKILL.md`
**📌 주요 메커니즘**: 3단계 무결성 검증

- **[Schema 단계]**: `view_file`을 통해 생성된 파일의 첫 줄이 반드시 `---`(YAML 시작점)인지 검사하는 스트릭트(strict) 모드.
- **[Functional 단계]**: 껍데기만 생성되었는지 실제 코드가 있는지 `find_by_name` 등의 참조 추적을 통해 파일 간 연결 고리가 깨지지 않았는지 파악합니다.
- **[Quality (Reflection) 루프]**: 가장 핵심으로, 비판적 자아(Critique) 역할을 수행해 에지케이스 헛점이 발견되면 강제로 다시 작성 단계(auto_fixed)로 피드백을 두어(최대 2회) 품질을 보정합니다.
