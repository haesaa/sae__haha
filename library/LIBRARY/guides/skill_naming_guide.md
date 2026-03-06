# Skill Naming & Structure Guide

> Skill 이름 규칙 및 디렉토리 구조 가이드.

---

## 1. Skill 명명 규칙

- **snake_case** 사용: `my_skill_name`
- 동사+명사 형태 권장: `data_cleaner`, `report_generator`, `kpi_manager`
- 약어 지양: `csv_proc` → `csv_processor`
- 단수형 사용: `file_readers` → `file_reader`

---

## 2. Skill 디렉토리 구조

```
library/
└── {skill_name}/
    └── SKILL.md    ← 빌더가 자동 생성
```

> 추가 파일이 필요한 경우 `LIBRARY/instructions/`에 분리 정의한다.

---

## 3. SKILL.md 구조

```markdown
---
name: {skill_name}
description: {한 줄 설명}
---

# Skill {Skill Name Title}

entry_instruction

{entry_instruction_value}

---

## Guides
- {guide_1}

---

## Tools
- {tool_1}

---

## Instructions
### {entry_instruction_value}
```

---

## 4. Skill 등록 흐름

1. Blueprint 작성 → `FACTORY/blueprints/` 저장
2. Validator 통과 확인
3. Builder 실행 → `SKILL.md` 자동 생성
4. `skill_registry.json` 자동 등록
