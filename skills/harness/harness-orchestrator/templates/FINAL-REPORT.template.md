# Final Report

- 작업 ID: {task_id}
- 요청: {raw_request 요약}
- 결과: {✅ 성공 | ⚠️ 부분 성공 | 🔴 실패}

## 최종 산출물

- `output/{skill_name}/` ({파일 수}개 파일)
- SHA-256: {해시값}

## 파이프라인 요약

| 단계 | 상태 | 소요시간 |
|------|------|---------|
| 00-preflight | {상태} | {시간} |
| 01-complexity | {상태} | {시간} |
| 02-analyze | {상태} | {시간} |
| 03-forge | {상태} | {시간} |
| 04-verify | {상태} | {시간} |
| **합계** | | **{총시간}** |

## 검증 결과

- Schema: {pass/fail} | Functional: {pass/fail} | Quality: {N}/10
- 이슈: {N}건 | 자동 수정: {N}건

## 재개 방법

이 작업을 이어서 진행하려면: "{task_id} {N}단계부터 재실행해줘"
