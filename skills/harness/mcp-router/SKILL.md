---
name: mcp-router
description: >
  태스크의 의도를 분석하여 적합한 MCP 서버를 자동 추천합니다.
  Awesome-MCP-Servers-한국어-가이드.md (2596개)를 참조 데이터로 활용합니다.
  "MCP 연결", "외부 서비스", "API 연동", "Slack", "Gmail", "GitHub" 등의
  키워드가 포함된 요청에 활성화됩니다.
---

# MCP Router — MCP 서버 자동 추천

## 인터페이스

### 입력 (from Orchestrator)

- 수신: `{ intent, keywords, fallback_ok }` (Analyst 팀원이 전달)
- 수신 시점: **`skills/02-analyze.md` Step 1** 에서 호출

### 출력 (to Orchestrator)

- `work/analysis/mcp-result.json`에 결과 저장
- 실패 시: `fallback = "no_mcp"`

### 호출 방식

- Analyst가 `view_file("mcp-router/SKILL.md")`로 동적 로딩
- `grep_search`로 `Awesome-MCP-Servers-한국어-가이드.md` 검색
- 결과를 `work/analysis/mcp-result.json`에 기록

---

## 목적

태스크에 필요한 외부 서비스를 식별하고, 적합한 MCP 서버를 **추천**합니다.
실제 설치/연결은 하지 않으며, 사용자에게 정보와 링크를 제공합니다.

> ⚠️ **중요**: MCP 서버 설치는 자동으로 하지 않습니다.
> 추천 + 설치 링크 제공 → 사용자 승인 후에만 실행합니다.

## 실행 시점

- 태스크에 외부 서비스(Slack, Gmail, GitHub 등)가 필요할 때
- **Analyst**(`skills/02-analyze.md`)가 Step 1에서 디스패치한 경우
- "MCP 추천해줘", "어떤 서비스가 필요해?" 등 요청

---

> 🔋 **Token Guard 연동**: MCP 검색 결과가 길 경우 토큰 사용량을 체크하고, 80% 이상이면 결과를 핵심 3개로 축약합니다.

## 의도 → MCP 매핑 테이블 (Quick Match)

| 의도 패턴 | 추천 MCP | 카테고리 |
| ---------- | --------- | --------- |
| 일정, 캘린더, 미팅, 스케줄 | Google Calendar MCP | 프로젝트 관리 |
| 이메일, 메일, 발송, inbox | Gmail MCP | 커뮤니케이션 |
| 슬랙, 채널, 메시지 | Slack MCP | 커뮤니케이션 |
| git, PR, 이슈, 저장소 | GitHub MCP Server | 소스 제어 |
| 파일, 드라이브, 문서공유 | Google Drive MCP | 파일 관리 |
| DB, 데이터베이스, 쿼리 | PostgreSQL / SQLite MCP | 데이터베이스 |
| 검색, 웹검색, 리서치 | Brave Search / Perplexity | 검색 엔진 |
| 브라우저, 자동화, 스크래핑 | Playwright MCP | 브라우저 & 웹 |
| 태스크, 프로젝트, 보드 | Linear / Jira MCP | 프로젝트 관리 |
| 배포, 클라우드, 서버 | Vercel / Cloudflare MCP | 클라우드 |

---

## 카테고리 라우팅 테이블 (Deep Search)

매핑 테이블에 없을 때, 키워드를 아래 카테고리에 매칭 후 해당 섹션 내에서 검색합니다.

| 의도 키워드 그룹 | 카테고리 | 서버 수 |
| ---------------- | -------- | ------- |
| AI, 모델, LLM, 임베딩, 벡터 | 🤖 AI 플랫폼 & 모델 | 146 |
| DB, 데이터베이스, SQL, 쿼리, 테이블 | 🗄️ 데이터베이스 | 163 |
| AWS, GCP, Azure, 배포, 인프라 | ☁️ 클라우드 & 인프라 | 119 |
| 브라우저, 크롤링, 스크래핑, 웹 | 🌐 브라우저 & 웹 | 84 |
| git, PR, 커밋, 브랜치, 코드리뷰 | 📝 소스 제어 & 코드 관리 | 31 |
| 태스크, 프로젝트, 보드, 스프린트 | 📋 프로젝트 관리 | 64 |
| 로그, 메트릭, 알림, 모니터링 | 📊 모니터링 & 옵저버빌리티 | 78 |
| 마케팅, CRM, 세일즈, 리드 | 📈 마케팅 & CRM | 30 |
| 보안, 인증, 암호화, 취약점 | 🔒 보안 | 66 |
| 테스트, QA, 자동화테스트 | 🧪 테스팅 & QA | 8 |
| 분석, BI, 대시보드, 시각화 | 📉 데이터 분석 & BI | 44 |
| API, 통합, 웹훅, REST | 🔗 API & 통합 | 38 |
| 자동화, 워크플로우, 파이프라인, 스케줄 | ⚡ 자동화 & 워크플로우 | 70 |
| 검색, 인덱싱, 서치 | 🔍 검색 엔진 | 57 |
| 파일, 문서, PDF, 변환 | 📁 파일 & 문서 관리 | 170 |
| 디자인, UI, 피그마, 이미지 | 🎨 디자인 & UI | 18 |
| 슬랙, 이메일, 메일, 채팅, 메시지 | 💬 커뮤니케이션 | 77 |
| SNS, 트위터, 인스타, 소셜 | 📱 소셜미디어 | 56 |
| 미디어, 유튜브, 음악, 영상 | 🎮 미디어 & 엔터테인먼트 | 53 |
| 결제, 금융, 주식, 커머스, 쇼핑 | 💰 금융 & 커머스 | 189 |
| 지도, 위치, 여행, 네비 | 🗺️ 지도 & 위치 & 여행 | 36 |
| IoT, 하드웨어, 센서, 디바이스 | 🔌 IoT & 하드웨어 | 25 |
| 건강, 의료, 진단, 헬스 | 🏥 헬스 & 의료 | 32 |
| 법률, 계약, 규정 | ⚖️ 법률 & 계약 | 7 |
| 교육, 연구, 논문, 학습 | 🎓 교육 & 연구 | 82 |
| 날씨, 시간, 타임존 | 🌤️ 날씨 & 시간 | 18 |
| 시스템, 데스크톱, OS, 터미널 | 🖥️ 시스템 & 데스크톱 | 36 |
| 코드실행, 런타임, 샌드박스 | 💻 코드 실행 & 개발 | 48 |
| SaaS, 플랫폼, Notion, Airtable | 🔗 SaaS & 플랫폼 통합 | 677 |

---

## 워크플로우 (라우팅 절차)

### Step 1: 키워드/의도 추출

I3 페이로드에서 `intent`와 `keywords` 를 수신합니다.
단독 모드의 경우 유저 요청에서 직접 추출합니다.

### Step 2: Quick Match — 매핑 테이블 매칭

위 "의도 → MCP 매핑 테이블"의 10개 패턴에서 일치를 찾습니다.
→ 매칭되면 즉시 Step 4로.

### Step 3: Deep Search — 카테고리 기반 2단계 검색

매핑 테이블에 없으면 아래 절차를 따릅니다:

```
Step 3-1: 카테고리 매칭
  → keywords를 카테고리 라우팅 테이블에 매칭
  → 매칭된 카테고리 1~3개 선정
  → 예: ["Slack", "분석"] → 💬 커뮤니케이션, 📉 데이터 분석 & BI

Step 3-2: 카테고리 내 서버 검색
  → grep_search로 Awesome-MCP-Servers-한국어-가이드.md를 검색:
    grep_search("{키워드}", "c:\\hehe\\harness\\Awesome-MCP-Servers-한국어-가이드.md")
  → 검색 결과에서 카테고리 헤더(## 이모지 카테고리명) 범위 내 결과만 필터
  → 서버명, 설명, GitHub URL 추출
  → 상위 3개만 추천 (토큰 절약)
```

### Step 4: 결과 기록

#### 4-A. 파이프라인 모드 (Orchestrator에서 호출 시)

`pipeline_state`에 결과를 기록만 합니다 (사용자 출력 없음):

```json
{
  "matched_servers": [
    { "name": "서버명", "desc": "용도", "url": "GitHub URL", "category": "카테고리명", "install_guide": "설치 명령어" }
  ],
  "fallback": null
}
```

→ 사용자 출력은 Orchestrator §7(결과 반환)에서 일괄 처리됩니다.

#### 4-B. 단독 모드 (유저가 직접 트리거한 경우)

사용자에게 직접 추천 결과를 출력합니다:

```markdown
## 🔌 MCP 서버 추천

| MCP 서버 | 용도 | 카테고리 | 링크 |
| --------- | ---- | -------- | ---- |
| {서버명} | {용도} | {카테고리} | {URL} |

### 설치 방법
{설치 명령어 또는 설정 안내}

> 설치하시겠습니까? "설치해줘"라고 말씀하시면 진행합니다.
```

#### 모드 판정

```
IF checkpoint.json이 존재 AND completed에 "01-complexity"가 있음:
  → 파이프라인 모드 (4-A)
ELSE:
  → 단독 모드 (4-B)
```

### Step 5: Fallback (MCP 미사용 시)

MCP 서버를 사용할 수 없는 경우 대체 방안을 제시합니다:

```markdown
## 대체 방안
MCP 서버 없이도 다음 방법으로 진행할 수 있습니다:
1. Antigravity의 `read_url_content` 도구로 웹 데이터 수집
2. `browser_subagent`로 브라우저 자동화
3. 로컬 스크립트로 데이터 처리
```

---

## 관련 파일

| File | Purpose |
| ---- | ------- |
| `Awesome-MCP-Servers-한국어-가이드.md` | 2596개 MCP 서버 참조 카탈로그 |
| `harness-orchestrator/skills/02-analyze.md` | Analyst가 MCP Router 호출 |

## 예외사항

1. **이미 활성화된 MCP** — 중복 추천하지 않음
2. **로컬 전용 작업** — MCP 불필요 시 "MCP 불필요" 판정
3. **유료 서비스** — 무료 대안이 있으면 먼저 추천
