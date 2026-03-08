---
name: verify-outomidea-pipeline
description: Outomidea V4 파이프라인의 입출력 핸드오프 종속성, JSON 스키마, 및 디렉토리 구조 룰 일관성 검증. SKILL-1A, 1B, 2의 스펙 변경 후 사용.
---

# Outomidea 파이프라인 검증

## Purpose

1. **핸드오프 정합성 검증** — 이전 스킬의 산출물이 다음 스킬의 필수 입력으로 누락 없이 정의되어 있는지 확인.
2. **JSON 스키마 일관성 검증** — 생성 스킬에 명시된 JSON 구조가 소모 스킬에서 동일한 규격으로 참조되고 있는지 점검.
3. **디렉토리 룰 일관성** — `00-preflight`에서 정의된 임시 디렉토리 트리(`S2`, `S3`, `S4`, `E1`~`E4`)가 실제 각 스킬 문서 내 저장 경로 명세와 일치하는지 확인.

## When to Run

- `SKILL.md`, `00-preflight.md`, `01-input-gate.md` 오케스트레이터 파일이 변경되었을 때
- `SKILL-1A`, `SKILL-1B`, `SKILL-2` 중 하나라도 입력/출력 사양이 변경되었을 때
- 파이프라인 과정 중 파일을 찾을 수 없거나 스키마 파싱 오류가 발생했을 때

## Related Files

| File | Purpose |
|------|---------|
| `c:/hehe/outomidea/1.music_video/SKILL.md` | 오케스트레이터 헤드 |
| `c:/hehe/outomidea/1.music_video/skills/00-preflight.md` | 파이프라인 디렉토리 설계 |
| `c:/hehe/outomidea/1.music_video/skills/01-input-gate.md` | 모드별 진입/검증 조건 |
| `c:/hehe/outomidea/1.music_video/skills/SKILL-1A_story-conti-prompt_v4.md` | 1A (스토리, 콘티) 기획 스킬 |
| `c:/hehe/outomidea/1.music_video/skills/SKILL-1B_prompt-generation_v4.1.md` | 1B (프롬프트 시퀀스) 설계 스킬 |
| `c:/hehe/outomidea/1.music_video/skills/SKILL-2_clip-edit-assembly_v4.md` | 2 (클립/편집) 조립 스킬 |

## Workflow

### Step 1: 디렉토리 일관성 검증

**파일:** `00-preflight.md` vs `SKILL-1A`, `SKILL-1B`, `SKILL-2`

**검사:** `00-preflight`에 기술된 폴더 구조가 실제 스킬들이 산출물을 저장하는 경로와 일치하는지 확인합니다.

```bash
# S2, S3 폴더가 1A에서 어떻게 참조되는지 확인
grep -n "S2-" c:/hehe/outomidea/1.music_video/skills/SKILL-1A*.md
# E1 폴더가 2에서 참조되는지 확인
grep -n "E1-" c:/hehe/outomidea/1.music_video/skills/SKILL-2*.md
```

**위반:** `00-preflight.md`에는 `work/T1-analysis`가 없는데, 특정 스킬 문서에서는 여전히 해당 폴더에 저장한다고 명시된 경우.

### Step 2: 핸드오프(입출력) 체인 일관성 검증

**파일:** `SKILL-1A` 산출물 섹션 vs `SKILL-2` 필수 입력 섹션

**검사:** 1A가 생성한다고 보장한 필수 파일 목록이 2가 요구하는 필수 파일 목록과 매핑되는지 확인합니다.

```bash
# SKILL-1A 산출물 목록 확인
grep -n "outfit-timeline.json" c:/hehe/outomidea/1.music_video/skills/SKILL-1A*.md
# SKILL-2 요구사항 확인
grep -n "outfit-timeline.json" c:/hehe/outomidea/1.music_video/skills/SKILL-2*.md
```

**위반:** 1A 문서에서는 삭제된 산출물이 2 문서에서는 여전히 `[필수]` 입력으로 남아있는 경우.

### Step 3: JSON 스키마 필드 일관성

**파일:** `SKILL-1A`/`SKILL-1B` vs `SKILL-2`

**검사:** JSON 객체의 필수 속성 구조 변경이 양측 문서에 모두 반영되었는지 점검합니다.

```bash
# empty_cells 속성 참조가 양측에 있는지 확인
grep -n "empty_cells" c:/hehe/outomidea/1.music_video/skills/SKILL-*
```

**위반:** 1A에서 `outfit_delta` 를 `applies_to` 배열 로직으로 바꿨음에도 불구하고 2에서는 여전히 구 스키마(`outfit_target` 단일 문자열 등)를 읽도록 지시되어 있는 경우.

## Output Format

```markdown
### 파이프라인 일관성 검증 결과

| 검증 항목 | 대상 파일 쌍 | 상태 | 발견된 갭 사항 |
|-----------|--------------|------|----------------|
| 디렉토리 일치 | `00-preflight` ↔ `SKILL-1A` | FAIL | 1A가 S2-story가 아닌 T1 경로 참조중 |
| 입출력 핸드오프 | `SKILL-1A` ↔ `SKILL-2` | PASS | `outfit-timeline.json` 정상 매핑 확인 |
| JSON 스키마 | `SKILL-1B` ↔ `SKILL-2` | PASS | `prompt-index` 확장 필드 동기화 완료 |
```

## Exceptions

다음은 파이프라인 일관성 위반에 해당하지 **않습니다**:

1. **선택적(Optional) 파일 누락** — `01-input-gate.md`에서 선택 입력인 파일(예: `style-guide.md`)이 특정 스킬의 필수 입력으로 기술되지 않은 것은 정상입니다.
2. **단독 구동용 입출력** — `SKILL-1B`가 `Direct` 모드로 1A 없이 텍스트 프레임 지시서를 직접 입력받는 경로를 명시하고 있다면, 해당 파이프라인 분기는 정상입니다.
3. **템플릿/샘플 파일 차이** — 산출물 JSON 예시 코드상 임의로 적어둔 예시 값(더미 데이터)의 형태가 스킬별로 다른 것은 스키마 오류가 아닙니다 (구조적 필드 매핑만 중요).
