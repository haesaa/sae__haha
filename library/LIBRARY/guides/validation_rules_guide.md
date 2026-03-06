# Validation Rules Guide

> Blueprint Validator의 5가지 검증 규칙 상세 설명.  
> anti_task_v0.4.md 섹션 5 기반.

---

## Rule 1: skill_name must be unique

**검사 대상**: `skill_registry.json`의 `skills[].name`  
**실패 메시지**: `"Skill name must be unique"`

```python
if blueprint["skill_name"] in existing_skills:
    return False, "Skill name must be unique"
```

---

## Rule 2: entry_instruction must exist

**검사 대상**: `blueprint["entry_instruction"]`이 truthy 값  
**실패 메시지**: `"Entry instruction must exist"`

```python
if not blueprint.get("entry_instruction"):
    return False, "Entry instruction must exist"
```

---

## Rule 3: guides must exist in guide_graph

**검사 대상**: `blueprint["guides"]`가 비어있지 않은 배열  
**실패 메시지**: `"Guides must exist"`

```python
if not blueprint.get("guides"):
    return False, "Guides must exist"
```

---

## Rule 4: instructions must exist in instruction_graph

**검사 대상**: `blueprint["instructions"]`의 각 항목이 `instruction_graph` 목록에 존재  
**실패 메시지**: `"Invalid instruction: {name}"`

---

## Rule 5: tools must exist in tool_registry

**검사 대상**: `blueprint["tools"]`의 각 항목이 `tool_registry` 목록에 존재  
**실패 메시지**: `"Invalid tool: {name}"`

---

## 검증 통과 조건

Rule 1~5 **모두 통과**해야 Builder 단계로 이동한다.  
단 하나라도 실패하면 즉시 오류를 반환하고 파이프라인을 중단한다.
