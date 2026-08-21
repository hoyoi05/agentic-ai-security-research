# 체계적 매핑 연구 범위

## 연구 목적

본 연구는 Agentic AI 보안 문헌을 체계적으로 수집·분류하여 연구 지형, 위협 및 방어의 분포, 실증 방법, 근거 수준과 재현성, 그리고 후속 연구가 필요한 공백을 식별하는 **체계적 매핑 연구(Systematic Mapping Study, SMS)** 입니다.

특정 공격이나 방어의 효과를 하나의 수치로 합성하는 것이 아니라, 아직 경계와 용어가 안정되지 않은 Agentic AI 보안 분야 전체의 구조를 먼저 확립합니다. 자가 진화형 Agent와 Skill Poisoning은 독립된 전체 범위가 아니라 하나의 하위 영역으로 유지합니다.

## 연구 질문

- **RQ1 — 연구 지형:** Agentic AI 보안 연구는 어떤 보안 문제와 시스템 계층을 다루는가?
- **RQ2 — 위협:** 공격자는 Agent의 어떤 자산·인터페이스·수명주기 단계를 공격하는가?
- **RQ3 — 방어:** 현재 방어기법은 예방·탐지·대응·복구 중 어디에 집중되어 있는가?
- **RQ4 — 실증:** 연구들은 어떤 Agent 프레임워크, 모델, 도구, 환경, 데이터셋과 지표를 사용하는가?
- **RQ5 — 증거 수준:** 결과는 저자 주장, 공개 아티팩트 확인, 재현, 독립 검증 중 어느 수준인가?
- **RQ6 — 연구 갭:** 연구 밀도가 낮고 실증 가능성과 학술적 기여도가 높은 영역은 무엇인가?
- **RQ7 — 후속 연구:** 확인된 공백 중 런타임 추적·포렌식·Kubernetes 역량으로 해결할 수 있는 주제는 무엇인가?

RQ1~RQ7은 하나의 통합 질문 세트로 유지합니다. 각 질문은 검색 결과의 포함 여부, 데이터 추출 필드, 분석표와 연구 갭 선정 기준을 연결합니다.

## 분석 대상

- LLM 기반 자율·반자율 Agent
- Tool-using Agent, coding Agent, web Agent와 embodied Agent
- MCP 또는 이에 준하는 tool protocol과 Agent runtime
- Multi-agent orchestration, delegation, communication과 shared state
- Memory, knowledge, trajectory, generated skill과 self-evolution
- Agent identity, credential, authorization, runtime effect와 cloud resource
- 예방, 탐지, 포렌식, 사고 대응, containment, recovery와 rollback
- Agentic AI 보안 평가 방법, 데이터셋, benchmark와 governance

일반적인 LLM jailbreak나 모델 가중치 공격은 Agent의 상태, 도구, 권한, 자율 실행 또는 시스템 효과와 직접 연결될 때 포함합니다. 전통적인 multi-agent system 연구는 LLM 기반 Agentic AI의 보안 문제에 직접 적용되거나 비교 근거를 제공하는 경우에만 인접 문헌으로 코딩합니다.

## 연구 기간과 자료 유형

- 기본 검색 기간: 2022년 1월 1일부터 각 데이터베이스의 실제 검색일까지
- 2022년 이전 연구: backward snowballing으로 발견된 직접적인 선행 연구만 포함
- 학술 문헌: peer-reviewed 논문, conference paper, journal article, 체계적 review
- 조기 연구: arXiv 등 preprint를 별도 publication type으로 포함
- 보충 자료: 공식 표준, 정부·산업기관 보고서, 공식 보안 taxonomy
- 블로그·뉴스·마케팅 문서는 사건 또는 실무 동향의 보조 근거로만 관리

## 주요 산출물

- 데이터베이스별 검색식과 검색 로그
- 중복 제거 및 제목·초록·전문 스크리닝 기록
- 포함 문헌의 구조화된 코딩 데이터
- Agentic AI 보안 taxonomy와 evidence map
- 연구 밀도·평가 성숙도·재현성 분석
- 근거 기반 연구 갭과 후속 실증 연구 우선순위

세부 검색·스크리닝 절차는 [SMS 프로토콜](protocol.md), 코딩 값과 판정 규칙은 [코딩 프레임워크](coding-framework.md)를 따릅니다.
