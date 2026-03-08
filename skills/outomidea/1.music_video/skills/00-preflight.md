---
name: 00-preflight
description: >
  파이프라인 실행 전 환경을 검증하고, 프로젝트 디렉토리를 초기화한다. 파이프라인 최초 진입 시 자동 활성화됩니다.
---

# 00-preflight: 사전 검증 및 초기화 스킬

> **실행자**: Leader (직접 실행, 팀 생성 전)
> **실행 시점**: 파이프라인 최초 진입 시
> **쓰기 권한**: 프로젝트 루트 전체 (디렉토리 생성)

## 목적

Music Video Generation v3.0 파이프라인 실행 전 환경을 검증하고, 프로젝트 디렉토리를 초기화합니다.
이 스킬이 실패하면 파이프라인에 진입하지 않으며, 작업의 기반을 마련하는 필수 관문입니다.

## 워크플로우

### Step 1: 프로젝트 디렉토리 생성

- 타임스탬프 형식(`project-YYYYMMDD-HHMMSS`)으로 다음 구조를 생성합니다:

```
project-{YYYYMMDD}-{HHMMSS}/
├── PIPELINE-LOG.md
├── input/
│   ├── music/              ← music-meta.json
│   ├── characters/         ← ⏸ 유저 이미지 삽입 폴더 (char_01.png ...)
│   └── style/              ← 선택된 스타일 가이드
├── work/
│   ├── checkpoint.json     ← PAUSE 영속화 (핵심)
│   ├── S2-story/
│   │   ├── story.md
│   │   └── characters.md
│   ├── S3-conti/
│   │   ├── anchor-keywords.json  ← 고정 키워드
│   │   └── conti-script.json     ← 씬 분할 + Recursive 체인
│   └── S4-prompts/
│       ├── S01_prompts.md ~ SNN_prompts.md
│       └── ALL_PROMPTS.md
├── output/
│   └── ALL_PROMPTS.md
└── logs/
```

### Step 2: PIPELINE-LOG.md 초기화

- `templates/PIPELINE-LOG.template.md`를 기반으로 루트에 `PIPELINE-LOG.md`를 생성합니다.
- 생성일, 시작 시간, 적용 버전을 기록합니다.

### Step 3: 입력 파일 복사 및 분류

- 유저가 제공한 입력 파일들을 `input/` 하위 디렉토리에 맞게 복사합니다.
  - `music-meta.json` -> `input/music/`
  - 캐릭터/표정 이미지 -> `input/characters/`
  - 스타일 가이드 -> `input/style/`
- 파일 목록을 `PIPELINE-LOG.md`에 기록합니다.

### Step 4: 기존 프로젝트 재실행 감지 혹은 재구동(RESUME) 감지

- *"재구동"*, *"RESUME"*, *"계속 진행"* 등의 명령어가 인식되거나 유저가 의도적으로 `checkpoint.json`이 있는 프로젝트를 지시한 경우:
  - `work/checkpoint.json`을 로드합니다.
  - 미완료 단계(next_step) 파악 및 PIPELINE-LOG.md 갱신.
  - 이후 01-input-gate를 건너뛰고 해당 Step으로 바로 이관합니다.

### Step 5: 핸드오프

- 초기화 성공 시 `01-input-gate` 스킬로 진행하여 입력 데이터 형식 검증을 수행합니다.
