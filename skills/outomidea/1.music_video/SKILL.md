---
name: music-video-skill
description: >
  Music Video Generation Pipeline v3.0
  음원 분석 JSON과 캐릭터 이미지를 기반으로 연속성 있는 씬별 프롬프트를 자동 생성(나노바나나2, Flow, 3x3그리드 특화)합니다.
---

# 🎬 Music Video Generation Skill v3.0

> **변경 이력 v2→v3**:
> Recursive Prompting 내장 / Image-to-Text 역추출 고정키워드 시스템 / PAUSE 영속화 / 나노바나나2 + Flow 전용 프롬프트 산출

## 실행 스킬 시퀀스

본 파이프라인은 Leader와 A1 에이전트 간의 핸드오프 구조로 동작하며, 중간에 유저 개입(이미지 생성)을 위한 PAUSE 구간이 있습니다. 순서대로 실행하세요.

1. **`00-preflight`** (Leader): 프로젝트 환경 구성 및 `PIPELINE-LOG.md` 초기화.
2. **`01-input-gate`** (Leader): 입력 에셋 검증 및 파이프라인 모드(MV-Story / Direct) 결정.
3. **`SKILL-1A`** (A1 Agent): 스토리 도출 및 초기 캐릭터 구성 -> `checkpoint.json` 저장 후 **PAUSE**.
   *(유저가 이미지를 나노바나나2로 생성하여 `input/characters/`에 삽입 후 "재구동"을 명령할 때까지 대기)*
4. **`SKILL-1B`** (A1 Agent): 이미지 속성 역추출(고정 키워드 획득), 씬(scene) 분할표 생성, 그리고 3종 생성 프롬프트 Recursive 도출 (Core 단계).
5. **`QC`** (Leader): 프롬프트 무결성 및 고정키워드/카메라워킹 누락 검증.
6. **`graceful-exit`** (Leader): 최종 보고서 출력 및 작업 종류.

---

## Tools

이 과정에서 에이전트들은 주로 다음 시스템/파일 툴을 활용합니다:

- file_read
- file_write
- python_exec (검증 자동화 스크립트 용, 옵션)

## Guides & References

다음의 가이드를 참조하여 동작을 세밀하게 제어합니다.

- REFERENCE-prompt-and-frame-guide
- mv_char_psychology_ref
- mv_gate_criteria
- mv_mcp_registry
- mv_narrative_technique_ref
- mv_pipeline_guide
