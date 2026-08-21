# FRIDA: Agent 포렌식 레디니스 연구 트랙

> 상태: 연구 의제 초안  
> 기준일: 2026-08-21  
> 주의: 이 문서는 체계적 검색 완료 전의 연구 가설과 범위를 기록한다. 신규성·최초성은 포함 문헌의 전문 검토 후 확정한다.

## 연구 동기

Agentic AI 시스템에서는 논리적 Agent, 설정·모델·도구가 결합된 버전, 짧게 실행되는 인스턴스, 사용자를 대신하는 credential이 서로 다른 수명주기를 가질 수 있다. 또한 Agent가 다른 Agent 또는 도구에 작업을 전달하면 실제 행위의 주체, 원래 권한자, 위임된 범위와 최종 시스템 효과가 서로 분리될 수 있다.

이 연구 트랙은 다음 통합 문제를 다룬다.

- Agent의 생성·수정·복제·정지·폐기·재생성 과정에서 식별 연속성을 보존
- human·service principal에서 Agent로 이어지는 권한 근거를 기록
- Agent 간 위임과 실제 유효권한의 변화를 실행 시점에 결합
- Agent 내부의 자기 보고가 아닌 외부 관측 증거로 행위와 시스템 효과를 연결
- 모든 원문을 저장하지 않고도 사후 재구성에 충분한 핵심 증거를 보존
- 증거 무결성, 보존정책과 조사 질의를 포렌식 레디니스 관점에서 설계

## 중심 연구 문제

> 수명주기가 짧고 권한 위임을 수행하는 Agentic AI 시스템에서, 신원·수명주기·위임·행위·결과를 연결하는 최소 증거를 제한된 오버헤드로 보존하면서 사후 재구성 가능성을 보장할 수 있는가?

## 연구 경계

### 포함

- NHI 및 workload identity를 이용한 Agent 식별
- Agent definition, version, instance와 credential의 분리
- lifecycle event와 signed tombstone
- multi-agent 및 Agent-to-tool delegation
- authorization decision과 effective authority
- tool invocation, state mutation과 외부 시스템 효과
- provenance graph와 incident reconstruction
- tamper-evident evidence preservation
- 위험 기반 상세 증거 승격과 compact audit logging

### 제외 또는 인접 영역

- Agent가 아닌 일반 LLM 대화의 감사만을 다루는 연구
- Agent를 포렌식 분석 도구로만 사용하는 연구
- 모델 내부의 실제 사고과정을 완전하게 복원할 수 있다는 주장
- identity나 실행 효과와 연결되지 않은 일반 성능 observability
- 법적 책임의 최종 판단

## 용어 원칙

이 연구에서는 모델이 서술한 chain-of-thought를 실제 내부 추론의 직접 증거로 취급하지 않는다. 대신 다음 관측 정보를 연결하는 **decision provenance**를 사용한다.

- 요청 및 task identifier
- Agent definition·version·instance
- 적용된 정책과 authorization decision
- 참조한 memory·skill·data의 식별자 또는 무결성 참조
- 사용 가능한 도구와 실제 tool invocation
- 선언된 계획 또는 rationale
- 관찰된 행위, 결과와 검증된 외부 효과

선언된 rationale과 관찰된 사실은 별도 증거 유형으로 관리한다.

## 잠정 시스템명

**FRIDA — Forensic-Ready Identity and Delegation for Agents**

명칭은 연구 범위를 표현하기 위한 작업명이며, 기존 프로젝트·상표와의 충돌 여부를 논문 제출 전에 별도로 확인한다.
