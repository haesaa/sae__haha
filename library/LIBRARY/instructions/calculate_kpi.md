# calculate_kpi Instruction

> Skill: `kpi_manager`  
> Entry Instruction

---

## 목적

입력된 데이터를 기반으로 KPI 지표를 계산하고 리포트를 생성한다.

---

## 입력

```json
{
  "metrics": {
    "sales": "number",
    "target": "number",
    "period": "string"
  }
}
```

---

## 실행 단계

1. `metrics` 데이터 수신
2. 달성률 계산: `achievement_rate = (sales / target) * 100`
3. `aggregate_metrics` instruction 호출 (세부 집계)
4. `generate_report` instruction 호출 (리포트 생성)
5. 결과 반환

---

## 출력

```json
{
  "achievement_rate": "number",
  "status": "achieved | on_track | at_risk | missed",
  "report_path": "string"
}
```
