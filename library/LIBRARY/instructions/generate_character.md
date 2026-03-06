# generate_character Instruction

> Skill: `character_writer`  
> Entry Instruction

---

## 목적

캐릭터 정보를 입력받아 구조화된 캐릭터 시트를 생성한다.

---

## 입력

```json
{
  "character_name": "string",
  "character_type": "string",
  "traits": ["string"],
  "backstory": "string"
}
```

---

## 실행 단계

1. 입력 데이터 유효성 검사 (`character_name` 필수)
2. `writing_character` 가이드를 참조하여 캐릭터 시트 포맷 로드
3. 캐릭터 시트 생성
4. 출력 반환

---

## 출력

```markdown
# {character_name}

**Type**: {character_type}
**Traits**: {traits}

## Backstory
{backstory}
```
