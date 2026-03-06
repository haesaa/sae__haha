---
name: 01_creation
description: "크랙 프롬프트 파이프라인 Phase 1 — 세계관·캐릭터 생성. 1단계(세계관빌더)+2단계(성격유형)를 순차 실행. romance_guide.md를 기법 사전으로 상속."
version: 5.0.0
author: Antigravity
tags: [crack, phase1, phase2, worldbuilding, personality, creation]
---

# Phase 1: Creation (세계관 + 캐릭터 생성)

## 포함 에이전트

| 단계 | 에이전트 | 산출물 |
|------|---------|--------|
| 1 | world_builder | outputs/1_full_prompt.md |
| 2 | personality_designer | outputs/2_personality_prompt.md |

## 문체 레이어 구조

- **Layer 1:** `resources/romance_guide.md` — 기법 32개 정의 사전. 읽기전용, 수정 금지.
- **Layer 2:** `resources/world_builder.md` — 기법을 `[코드]`로만 호출. 재정의 금지.

## 모델 타겟

기본: `MODEL_TARGET: SC25_PC25`
변경: `shared/model_profiles.md` 참조.

## 실행

```bash
python scripts/config.py --phases 1,2
```

## 결과물

- `outputs/1_full_prompt.md`: 세계관 + 캐릭터 전체 프롬프트
- `outputs/2_personality_prompt.md`: 성격유형 통합 프롬프트

## 제약

- max_tokens: 8000
- 캐릭터 수 하드코딩 금지
- {user} 성별/신분 하드코딩 금지
- romance_guide.md 기법 재정의 금지
