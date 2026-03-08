---
name: skill-forge
description: >
  유저 요청 또는 Orchestrator 지시를 입력받아 Antigravity 표준 SKILL.md와
  번들 리소스(scripts/, references/)를 자동 생성합니다.
  "스킬 만들어줘", "skill 생성", "새 스킬", "자동화 스킬" 등의 요청에 활성화.
---

# Skill Forge — 스킬 자동 생성

## 인터페이스

### 입력 (from Orchestrator)

- 수신: `{ skill_name, domain, raw_request, system_prompt, output_dir, constraints }` (Builder 팀원이 수신)
- 수신 시점: **`skills/03-forge.md` Step 1** 에서 호출

### 출력 (to Verification)

- `work/forge/forge-result.json`에 결과 저장
- 결과를 Reviewer(`skills/04-verify.md`)에 전달

### 호출 방식

- Builder가 `view_file("skill-forge/SKILL.md")`로 동적 로딩
- 5단계 생성 파이프라인 실행
- 완료 후 Reviewer에 전달

---

## 목적

유저 요청에서 도메인·트리거·출력을 추출하여 Antigravity 표준에 맞는
SKILL.md 패키지를 자동 생성합니다.

## 실행 시점

- "~스킬 만들어줘", "~를 자동화하는 스킬" 등 요청
- Orchestrator가 Skill Forge를 디스패치한 경우
- 기존 스킬의 fork/확장 요청

---

## 5단계 생성 파이프라인

### Step 1: Intent Extraction (의도 추출)

유저 요청에서 핵심 정보를 추출합니다:

```markdown
| 항목 | 추출 내용 |
|------|----------|
| **도메인** | {스킬이 다루는 영역} |
| **트리거** | {스킬이 활성화되는 조건 3-5개} |
| **기대 출력** | {스킬 실행 결과물} |
| **제약조건** | {토큰 제한, 도구 제한 등} |
```

### Step 2: Registry Search / Fork

기존 스킬 레지스트리를 검색합니다:

1. 작업 디렉토리(`c:\hehe\harness\`)에서 유사 SKILL.md 탐색
2. `c:\hehe\antigravity-awesome-skills\skills\`에서 유사 스킬 검색
3. `c:\hehe\.claude\` 아래 참조 스킬 확인

```
# 유사 스킬 검색 (Antigravity 도구)
find_by_name("SKILL.md", "c:\hehe\harness")
grep_search("{키워드}", "c:\hehe\antigravity-awesome-skills\skills")
```

**유사 스킬 존재 시**: Fork → 기존 구조를 기반으로 수정
**없으면**: 빈 템플릿에서 시작

### Step 3: SKILL.md 생성

YAML frontmatter + Body를 생성합니다:

```yaml
---
name: {kebab-case-name}
description: >
  {1-2줄 설명}. {트리거 조건} 시 사용.
---
```

**필수 섹션**:

- **Purpose** — 2-5줄 목적 설명
- **When to Use** — 트리거 조건 3-5개
- **Workflow** — 단계별 실행 지침 (Step 1, 2, 3...)
- **Related Files** — 관련 파일 테이블
- **Exceptions** — 위반이 아닌 케이스 2-3개

**품질 기준**:

- SKILL.md: 500줄 이내 권장
- 300줄 초과 시 references/로 상세 분리
- `stop` 스킬 패턴: 토큰 이코노미 적용 (문장마다 가치 제공)

### Step 4: 번들 리소스 생성

필요 시 추가 파일을 생성합니다:

```
{skill-name}/
├── SKILL.md           ← 필수
├── references/        ← 선택 (300줄 초과 시)
│   └── detail.md
└── scripts/           ← 선택 (실행 스크립트 필요 시)
    └── helper.py
```

**references/**: 도메인별 상세 문서, 예시 확장판
**scripts/**: 반복 작업용 실행 코드 (로컬 도구 정책 준수)

### Step 5: Verification 호출

생성된 스킬을 `verification-layer`로 검증합니다:

- YAML frontmatter 필수 필드 확인
- name과 폴더명 일치 확인
- 마크다운 형식 유효성

---

## Description 최적화 (Pushy 원칙)

skill-creator의 "pushy" 원칙을 적용합니다:

- **트리거 범위를 넓게** — "~할 때", "~하고 싶을 때", "~가 필요할 때" 다양하게
- **구체적 시나리오 명시** — 추상적이지 않게
- **능동적 톤** — "사용해야 합니다" 대신 "자동 활성화됩니다"

---

## 관련 파일

| File | Purpose |
|------|---------|
| `harness-orchestrator/SKILL.md` | 실행 계획에서 Skill Forge로 디스패치 |
| `verification-layer/SKILL.md` | 생성된 스킬 검증 |
| `c:\hehe\antigravity-awesome-skills\skills\skill-creator\SKILL.md` | 참조 표준 |

## 예외사항

1. **기존 스킬 수정 요청** — 새로 생성하지 않고 기존 SKILL.md를 편집
2. **비기술 스킬** — 코드가 없는 순수 지침형 스킬도 유효
3. **테스트/실험용 스킬** — 품질 기준 완화 가능 (사용자 동의 시)
