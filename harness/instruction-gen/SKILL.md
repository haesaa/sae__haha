---
name: instruction-gen
description: >
  태스크 타입에 맞는 system prompt와 실행 지침을 자동 조합합니다.
  Orchestrator가 실행 계획을 수립한 후, 각 모듈에 전달할 지침을 생성할 때
  사용됩니다. "프롬프트 만들어줘", "지침 생성", "시스템 프롬프트" 요청에 활성화.
---

# Instruction Generator — 지침 자동 조합

## 인터페이스

### 입력 (from Orchestrator)

- 수신: `{ task_type, domain, constraints, mcp_context }` (Analyst 팀원이 수신)
- 수신 시점: **`skills/02-analyze.md` Step 2** 에서 호출

### 출력 (to Orchestrator)

- 결과를 `work/analysis/system-prompt.md`에 저장
- Token Guard 잔여 토큰 수신 후 지침 길이 조정

### 호출 방식

- Analyst가 `view_file("instruction-gen/SKILL.md")`로 동적 로딩
- Base + Extension 조합 후 `work/analysis/system-prompt.md`에 저장

---

## 목적

태스크의 도메인과 제약조건에 맞는 **최적화된 지침**을 자동 생성합니다.
Base Instruction(공통) + Domain Extension(도메인별)을 조합하여
토큰 예산 내에서 최대 효과를 발휘합니다.

## 실행 시점

- Orchestrator가 실행 계획을 수립한 후
- 사용자가 system prompt 또는 지침 생성을 요청할 때
- Skill Forge가 새 스킬의 내부 지침을 필요로 할 때

---

## 템플릿 시스템

### Base Instruction (공통)

모든 태스크에 적용되는 기본 구조:

```markdown
## Role
{태스크 도메인에 맞는 페르소나}

## Output Format
{기대 출력 형식 — 마크다운/JSON/코드 등}

## Constraints
- MAX_TOKENS: {Token Guard에서 전달받은 잔여 토큰}
- 언어: 한국어 출력, 영어 내부 추론
- 외부 API 호출 금지

## CoT Scaffold
단계별 사고 과정:
1. {입력 분석}
2. {핵심 변환/처리}
3. {출력 구성}
4. {자가 검증}
```

### Domain Extension (도메인별)

| 도메인 | 추가 지침 | 예상 토큰 |
|--------|----------|----------|
| **code** | 언어, 프레임워크, 린트 규칙, 테스트 요구사항 | ~200 |
| **writing** | 톤, 대상 독자, 길이, 구조 | ~150 |
| **analysis** | 데이터 소스, 분석 프레임, 출력 시각화 | ~180 |
| **integration** | MCP 서버, 인증, 에러 핸들링 | ~170 |
| **skill** | YAML frontmatter, 섹션 구조, 품질 기준 | ~160 |

---

## 생성 프로세스

### Step 1: 태스크 메타데이터 수신

Orchestrator로부터:

- 선택된 실행 경로 (ToT 결과)
- 사용할 모듈 목록
- 잔여 토큰 예산

### Step 2: 도메인 판정

```
IF 코드 생성/수정 → code
IF 문서/글쓰기 → writing
IF 데이터 분석/BI → analysis
IF MCP/API 연동 → integration
IF SKILL.md 생성 → skill
```

### Step 3: Base + Extension 조합

Base Instruction 템플릿에 해당 Domain Extension을 결합합니다.

### Step 4: 토큰 예산 적합

**잔여 토큰이 부족한 경우** (잔여 < 2000):

- CoT Scaffold를 1-2단계로 축소
- 예시를 제거하고 규칙만 유지
- Domain Extension을 핵심 3개 항목으로 줄임

**잔여 토큰이 충분한 경우** (잔여 > 5000):

- CoT Scaffold 4단계 전개
- Do/Don't 예시 추가
- Domain Extension 전체 포함

---

## CoT Scaffold 자동 삽입

최종 지침에 자동으로 추론 단계를 삽입합니다:

```markdown
## 추론 단계
다음 순서로 사고합니다:

1. **입력 분석**: 유저 요청의 핵심 의도와 제약조건 파악
2. **계획 수립**: 출력 구조와 작업 순서 결정
3. **실행**: 계획에 따라 출력 생성
4. **자가 검증**: 출력이 요청과 일치하는지, 제약조건을 준수하는지 확인
```

---

## 관련 파일

| File | Purpose |
|------|---------|
| `harness-orchestrator/skills/02-analyze.md` | Analyst가 Instruction Gen 호출 |
| `token-guard/SKILL.md` | 토큰 예산 정보 제공 |

## 예외사항

1. **simple 태스크의 지침 생성** — 오버헤드. 직접 실행이 더 효율적
2. **유저가 직접 지침을 제공한 경우** — 유저 지침을 우선, Extension으로 보강만
3. **토큰 잔여 500 미만** — 지침 생성 자체를 스킵하고 Token Guard에 위임
