# Minimum Sufficient Forensic Evidence 초안

> 상태: conceptual schema v0.1  
> 기준일: 2026-08-21  
> 이 문서는 표준이나 확정 스키마가 아니라 실험으로 검증할 연구 가설이다.

## 목적

Minimum Sufficient Forensic Evidence(MSFE)는 저장량을 최소화하는 로그 포맷 자체가 아니다. 정의된 사고 시나리오에서 다음 조사 질문을 신뢰할 수 있게 답하기 위한 최소 증거 집합이다.

1. 누가 Agent의 실행을 시작하거나 승인했는가?
2. 어떤 논리 Agent, 버전과 인스턴스가 실행했는가?
3. 어떤 권한이 어떤 위임 체인을 통해 전달되었는가?
4. 요청된 권한과 실제 유효권한은 무엇이었는가?
5. 어떤 정책이 어떤 결정을 내렸는가?
6. Agent가 어떤 도구와 자원에 행위를 수행했는가?
7. 실제 외부 시스템 효과는 무엇이었는가?
8. 증거가 생성된 후 변경·삭제되었는지 검증할 수 있는가?

## 식별자 계층

| 식별자 | 의미 | 수명 | 포렌식 목적 |
|---|---|---|---|
| principal_id | 원래 사용자 또는 service principal | 조직 정책에 따름 | 책임 근거와 on-behalf-of 연결 |
| agent_subject_id | 논리적으로 동일한 Agent | Agent 폐기까지, tombstone은 이후 보존 | 이름 변경과 재배포 이후에도 논리 신원 연결 |
| agent_version_id | 설정·모델·정책·skill·tool 집합의 불변 버전 | 불변 | 어떤 정의가 실행되었는지 식별 |
| agent_instance_id | 실제 runtime instance | 실행 단위 | ephemeral workload와 행위 연결 |
| credential_id | 발급된 credential 또는 key reference | 단기 또는 정책 기반 | 발급·rotation·revocation 입증 |
| delegation_id | 하나의 위임 관계 | 위임 유효기간과 증거 보존기간 | 권한 전달의 범위와 근거 |
| session_id | 관련 작업 묶음 | 작업 단위 | 동일 목표의 실행 연결 |
| trace_id | 분산 실행 trace | 실행 단위 | cross-system correlation |
| action_id | 개별 외부 행위 | 불변 | 중복·재시도·결과 식별 |

## 항상 보존할 Audit Spine

다음 사건은 일반적인 telemetry sampling 대상에서 제외하는 것을 연구 가설로 둔다.

- Agent subject 생성, 수정, 복제, suspend, revoke와 delete
- agent version 등록과 활성화
- runtime instance 시작·종료
- credential 발급, rotation, 만료와 revocation
- delegation 생성, attenuation, 재위임, 거절과 폐기
- authorization request, decision, policy version과 effective authority
- 고권한 tool invocation
- 외부 상태 변경 및 되돌릴 수 없는 행위
- human approval 또는 override
- 증거 무결성 checkpoint와 signed tombstone

## 조건부 decision provenance

정상 실행에서는 원문 대신 다음 참조와 요약을 우선 검토한다.

- prompt 또는 민감 입력의 keyed digest와 보안 저장소 reference
- model·system prompt·policy version
- memory, knowledge source와 skill identifier·digest
- 사용 가능한 tool set의 version 또는 digest
- 선언된 plan·rationale summary
- 정규화된 tool arguments의 digest
- 입력·출력 데이터의 classification, shape와 size
- 관련 span, log와 외부 audit record pointer

단순 hash는 낮은 엔트로피 입력에 대한 사전대입 위험이 있으므로, 원문 대체 증거로 사용할 때 keyed digest 또는 접근 통제된 content-addressable store를 비교한다.

## 위험 기반 상세 증거 승격

다음 신호가 발생하면 사건 전후의 상세 trace를 별도 evidence tier로 승격하는 정책을 평가한다.

- 저권한 Agent가 고권한 Agent 또는 도구를 호출
- delegation scope 확대 또는 attenuation 실패
- secret, 개인정보 또는 규제 대상 데이터 접근
- 외부 상태 변경과 irreversible action
- 정책 위반, 승인 우회 또는 비정상 credential 사용
- 알려지지 않은 MCP server 또는 동적 tool 등록
- prompt injection, memory·skill poisoning 의심
- 과도한 delegation depth, 반복 호출 또는 실행 loop
- Agent 보고 결과와 외부 상태 검증 결과의 불일치

상세 승격이 사건 이후에 결정되더라도 직전 맥락을 보존하려면 외부 collector의 제한된 pre-event buffer가 필요하다는 가설을 검증한다.

## 증거 수집 위치

Agent 자체 로그는 Agent 삭제·침해·오작동의 영향을 받을 수 있으므로 단독 증거원으로 사용하지 않는다. 다음 독립 관측점을 조합한다.

- Agent Registry와 NHI IdP
- authorization 또는 policy decision point
- Agent·tool·MCP gateway
- OpenTelemetry collector
- container·Kubernetes·cloud audit source
- 대상 자원의 상태 변경 audit log
- 별도 evidence service

## 충분성 제약

MSFE 선택 문제를 다음 목적의 다목적 최적화로 다룬다.

- 최소화: 저장량, 수집·authorization 지연, 민감정보 보존량
- 최대화: attribution, delegation reconstruction, authorization verification, causal reconstruction, tamper detection

증거 집합이 작다는 이유만으로 충분하다고 판정하지 않는다. 사전에 정의한 조사 질의와 ground truth에 대한 reconstruction threshold를 만족해야 한다.

## 무결성 요구 후보

- source identity와 event signing
- trusted timestamp 또는 검증 가능한 시간 순서
- event chaining 또는 batch Merkle commitment
- append-only 또는 WORM 보존
- schema version과 canonical serialization
- clock skew와 누락 event 표시
- 원문 evidence와 digest·pointer의 binding
- retention·legal hold·access 기록

구체적인 암호기법과 보존 매체는 threat model 및 성능 실험 후 선택한다.
