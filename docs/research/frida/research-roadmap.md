# FRIDA 논문 및 실험 로드맵

> 상태: research programme draft  
> 기준일: 2026-08-21

## 연구 프로그램

FRIDA는 하나의 논문에서 모든 컴포넌트를 완성하는 대신, 통합 기반 논문을 먼저 제시하고 각 핵심 문제를 후속 논문으로 심화하는 연구 프로그램으로 구성한다.

## Paper 1 — 통합 기반

### 작업 제목

**FRIDA: A Forensic-Ready Identity and Delegation Architecture for Ephemeral Agentic Systems**

### 중심 질문

수명주기가 짧고 다단계 권한 위임을 수행하는 Agentic AI 시스템에서 identity-bound evidence spine이 제한된 오버헤드로 privileged action을 재구성할 수 있는가?

### 필수 기여

1. Agent subject·version·instance·credential을 분리한 forensic identity model
2. 생성·수정·복제·폐기·재생성을 연결하는 lifecycle provenance
3. 원래 principal, delegation scope와 effective authority를 연결하는 delegation model
4. Minimum Sufficient Forensic Evidence schema
5. 외부 evidence collection과 tamper-evident preservation
6. end-to-end prototype 및 정량 비교실험

아키텍처와 요구사항만 제시하는 경우 position paper 범위에 머물 수 있으므로, 정규 시스템 논문에서는 동작하는 vertical prototype과 반증 가능한 평가가 필요하다.

## 잠정 연구 질문

- **RQ1:** lifecycle과 delegation context를 결합하면 privileged action attribution이 향상되는가?
- **RQ2:** 제안 모델은 scope amplification, confused deputy와 authority laundering을 어느 정도 재구성·탐지하는가?
- **RQ3:** 전체 trace 없이도 정의된 포렌식 질의를 만족하는 최소 증거 집합은 무엇인가?
- **RQ4:** 위험 기반 evidence promotion은 reconstruction quality를 유지하면서 저장량·지연·민감정보 보존량을 줄이는가?
- **RQ5:** 수정·복제·삭제·재생성 이후에도 Agent identity continuity를 검증할 수 있는가?
- **RQ6:** 선언된 intent·rationale, 실제 effective authority와 검증된 시스템 효과의 불일치를 식별할 수 있는가?

## 위협 시나리오

- 동일 표시 이름으로 Agent 삭제 후 재생성
- 설정·model·skill·tool이 변경되었으나 같은 논리 Agent로 동작
- Agent 복제 후 서로 다른 권한으로 실행
- 저권한 Agent가 고권한 Agent를 confused deputy로 이용
- 다단계 위임 중 scope가 확대되거나 원래 제약이 소실
- 만료·폐기된 credential 재사용
- Agent가 성공을 보고했으나 대상 시스템 효과가 다름
- application log 또는 Agent runtime이 삭제·변조
- 일부 telemetry가 sampling 또는 수집 실패로 누락

## 비교군

1. Agent application log only
2. full OpenTelemetry trace
3. 일반 head 또는 tail sampling
4. authorization log without delegation context
5. compact Forensic Audit Spine
6. Audit Spine plus risk-triggered evidence promotion

## 지표

| 평가 목적 | 지표 후보 |
|---|---|
| 행위 귀속 | privileged-action attribution precision, recall |
| 위임 재구성 | delegation-chain reconstruction accuracy |
| 권한 이상 | privilege-amplification detection rate |
| 수명주기 | identity continuity와 clone·recreate 구분 정확도 |
| 증거 품질 | evidence completeness, missing dependency rate |
| 무결성 | alteration·deletion detection rate |
| 조사 효율 | reconstruction time, query completion rate |
| 시스템 비용 | storage bytes, ingestion throughput, runtime·authorization latency |
| 개인정보 최소화 | retained plaintext 및 sensitive-field volume |

## 실험 판정 원칙

- ground truth는 orchestrator, authorization gateway와 대상 자원에서 독립적으로 생성한다.
- 연구 시스템 자체의 로그를 정답으로 사용하지 않는다.
- 각 시나리오를 반복 실행하고 Agent의 비결정성을 보고한다.
- 실패한 실행과 누락된 trace도 제외하지 않고 별도 결과로 기록한다.
- 공개 가능한 synthetic trace와 재현 스크립트를 우선 제공한다.
- 성능 저하뿐 아니라 조사 불가능 사건 수를 함께 보고한다.

## 후속 논문

### Paper 2 — Forensic identity continuity

생성·수정·복제·삭제·재생성, credential rotation·revocation과 signed tombstone을 집중 검증한다.

### Paper 3 — Delegation and privilege provenance

multi-hop delegation, scope attenuation, confused deputy와 effective-authority 계산을 형식화하고 실험한다.

### Paper 4 — Minimum forensic evidence

증거 최소성, adaptive capture와 privacy·storage·reconstructability trade-off를 다양한 workload에서 평가한다.

### Paper 5 — Agent forensics benchmark

사건 시나리오, ground-truth trace, forensic query와 reconstruction metric을 공개 가능한 benchmark로 정리한다.

## 다음 단계

1. 공개 접근 가능한 검색원을 이용해 관련 연구의 포함 후보군을 구축
2. identity·lifecycle·delegation·provenance·forensics별 전문 코딩
3. 선행연구가 이미 해결한 범위와 FRIDA 고유 범위를 novelty matrix로 확정
4. threat model과 adversary capability 고정
5. MSFE schema v0.2와 forensic query set 정의
6. 최소 vertical prototype 구현
7. full logging·sampling·compact evidence 비교실험
8. 결과에 따라 통합 논문과 후속 컴포넌트 논문의 경계 조정

## 저장소 역할

- Public Agentic AI Security Research 저장소: 검색 프로토콜, 공개 가능한 문헌 메타데이터, 코딩 결과, 연구 갭과 재현 가능한 실험 산출물
- Private research-design 저장소: 미검증 아이디어, 상세 threat model, 실험 노트, 내부 decision log와 제출 전 분석
- Private manuscript 저장소: LaTeX 원고, 저널 형식, 그림·표와 review response

공개 문서에는 copyrighted full text, 비공개 자격증명, 민감한 실험 로그와 제출 전략을 저장하지 않는다.
