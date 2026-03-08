---
name: harness-05-exit
description: >
  파이프라인의 모든 결과(정상/부분 성공/전체 실패)를 처리하고 최종 보고서를 작성한다.
  Graceful Degradation 원칙에 따라 어떤 상황에서도 최선의 결과를 보존한다.
---

# 05-exit: 종료 + 최종 보고

> **실행자**: Leader (직접 실행)
> **실행 시점**: 04-verify 완료 후, 또는 파이프라인 어느 단계에서든 치명적 실패 시
> **쓰기 권한**: `output/`, `quarantine/`, PIPELINE-LOG.md, checkpoint.json

## 목적

파이프라인의 성공/실패 여부와 무관하게 안전하게 종료하고, 가능한 최선의 결과물을 `output/`에 저장한다.
어떤 경우에도 중간 산출물을 삭제하지 않는다.

## 실행 시점

- 04-verify 완료 후 정상 종료 경로에서 실행.
- 어느 단계에서든 치명적 실패 시 즉시 호출.

## 워크플로우

### Step 1: 상태 판별

```
work/verify/verify-report.json 존재 + schema/functional = pass → ✅ 정상 완료
work/forge/ 결과 있음 + verify 실패 → ⚠️ 부분 성공
work/forge/ 결과 없음 → 🔴 전체 실패
checkpoint.json 내 token_used_estimate > 80% → 🟡 토큰 한도 경고
```

### Step 2: Graceful Degradation 처리

| 실패 지점 | output/에 저장 | LOG 표시 |
|----------|--------------|---------|
| 01-complexity 실패 | 복잡도 분석 결과만 | 🔴 |
| 02-analyze 실패 | MCP 추천 목록 + 기본 지침 | ⚠️ |
| 03-forge 실패 | 분석결과 + 프롬프트 텍스트 | ⚠️ |
| 04-verify 2회 실패 | 미검증 스킬 (경고 라벨 부착) | ⚠️ |
| 토큰 80% 도달 | checkpoint.json + 현재까지 최선 결과 | 🟡 |

### Step 3: 최종 산출물 복사

- `work/forge/{skill_name}/` → `output/{skill_name}/`
- `work/verify/verify-report.json` → `output/` 포함

### Step 4: 팀원 전원 종료 + 팀 정리

1. 모든 Teammate에게 종료 시그널 전달
2. `checkpoint.json` 삭제 또는 `status: "완료"` 갱신

### Step 5: 최종 보고

`templates/FINAL-REPORT.template.md` 기반으로 `output/FINAL-REPORT.md` 작성 후 유저에게 보고:

```markdown
## ✅ 파이프라인 완료

**생성된 스킬**: {skill_name}
**위치**: output/{skill_name}/
**파일 목록**:
  - SKILL.md ({lines}줄)
  - (기타 번들 파일)

**검증 결과**:
  Schema: {pass/fail} | Functional: {pass/fail} | Quality: {score}/10
  이슈: {N}건 (자동 수정: {N}건)

**MCP 추천**: {서버명 또는 "없음"}
**토큰 사용**: ~{used}/{max} ({pct}%)
```

## 관련 파일

| File | Purpose |
|------|---------|
| `templates/FINAL-REPORT.template.md` | 최종 보고서 템플릿 |
| `checkpoint.json` | 상태 최종 마킹 |
| `output/` | 최종 산출물 저장 위치 |
| `quarantine/` | 검증 실패 산출물 격리 |

## 예외사항

1. **정상 완료**: `checkpoint.json`의 status를 "completed"로 갱신 후 보존 (삭제 금지)
2. **예산 도달 시강제 속행**: 유저가 명시적으로 계속 요청하면 checkpoint를 기반으로 재개
3. **무응답 팀원**: 강제로 현재까지 작업 파일을 output/에 이관 후 종료
