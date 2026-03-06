# Pipeline Log: {task_id}

- 생성일: {YYYY-MM-DD HH:MM:SS}
- 작업: {raw_request 요약}
- 상태: 🟡 진행중

---

## Preflight

- [ ] 환경 검증
- [ ] 보안 스캔
- [ ] 모드: {신규 | Resume}

## 복잡도 판정

- 분류: {simple | composite | research}
- 선택 전략: {Branch A/B/C — 사유}

## T1: 분석 (Analyst)

- MCP 매칭: {서버명 또는 없음}
- 지침 생성: {도메인}
- 완료: {시각}

## T2: 스킬 생성 (Builder)

- 스킬명: {skill_name}
- 템플릿: {simple | composite}
- 파일 수: {N}
- 완료: {시각}

## T3: 검증 (Reviewer)

- Schema: {pass/fail} | Functional: {pass/fail} | Quality: {N}/10
- 이슈: {N}건 (자동 수정: {N}건)
- 완료: {시각}

## 최종

- 상태: {✅ 완료 | ⚠️ 부분 성공 | 🔴 실패}
- 총 소요시간: {시간}
- 토큰 사용: ~{N}/{MAX}
- 산출물: output/{skill_name}/
