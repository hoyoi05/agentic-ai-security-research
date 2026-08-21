# SMS 코딩 프레임워크

이 문서는 포함 문헌에 적용할 상위 taxonomy와 판정 규칙을 정의합니다. 한 연구가 여러 값을 다루면 다중 코딩하되, 논문이 단순히 언급한 값과 실제로 분석·평가한 값을 구분합니다.

## 1. 연구 역할

| 코드 | 정의 |
|---|---|
| Threat model | 자산, 공격자, 신뢰 경계 또는 공격 경로를 체계화 |
| Attack | 공격 기법 또는 악용 가능성을 제안·실증 |
| Defense | 예방·탐지·대응·복구 기법을 제안·실증 |
| Measurement | 실제 시스템이나 문헌에서 위험을 측정 |
| Benchmark | 재사용 가능한 task, dataset, harness 또는 metric 제공 |
| Survey | 기존 연구를 체계적으로 종합 |
| Governance | 표준, assurance, risk management 또는 운영 지침 |

## 2. 보안 영역

1. Goal·Prompt·Context Integrity
2. Memory·Knowledge·Skill Security
3. Tool·MCP·Agent Supply Chain
4. Identity·Authentication·Authorization
5. Delegation·Multi-agent Communication
6. Runtime Monitoring·Provenance·Forensics
7. Containment·Recovery·Rollback
8. Evaluation·Benchmark·Governance

## 3. Agent 수명주기

- Design and configuration
- Provision and identity binding
- Perception and context ingestion
- Planning and reasoning
- Tool selection and execution
- Memory or skill update
- Delegation and communication
- Deployment and operation
- Incident response and decommissioning

## 4. 영향 계층

- Model and prompt
- Agent runtime and orchestrator
- Memory, knowledge and skill store
- MCP, tool, plugin and external API
- Host process and filesystem
- Container and Kubernetes
- Cloud identity and managed service
- Physical or human environment

## 5. 보안 결과

- Goal or control-flow deviation
- Confidentiality loss
- Integrity loss
- Availability loss
- Unauthorized capability or privilege gain
- Persistence
- Cross-agent or cross-environment propagation
- Financial, physical or external side effect
- Evidence loss or attribution failure

## 6. 방어 단계

- Prevent
- Detect
- Contain
- Investigate and attribute
- Recover or compensate
- Learn and harden

## 7. 실증 성숙도

| 수준 | 기준 |
|---|---|
| Conceptual | 구현 또는 실험 없이 개념·위협만 제시 |
| Demonstrated | 제한된 예제나 proof of concept 제공 |
| Controlled evaluation | 명시적 dataset, baseline, metric으로 반복 가능한 평가 |
| Realistic evaluation | 실제 또는 현실적인 Agent workflow·권한·환경에서 평가 |
| Operational evidence | 운영 배포 또는 독립된 현장 자료를 분석 |

## 8. 근거와 재현 상태

### Evidence status

- `author-claimed`: 논문 또는 기관의 주장만 확인
- `metadata-checked`: 공식 서지정보와 식별자 확인
- `artifact-checked`: 공개 코드·데이터·구성을 직접 확인
- `reproduced`: 명시된 환경에서 핵심 실험을 재실행
- `independently-verified`: 독립 데이터 또는 구현으로 핵심 결론 확인

### Reproduction status

- `not-attempted`
- `blocked-missing-artifact`
- `attempted-failed`
- `partially-reproduced`
- `fully-reproduced`
- `independently-replicated`

## 9. 코딩 규칙

- 제목·초록만으로 추정한 값은 전문 확인 전 provisional로 표시합니다.
- 실제 평가하지 않은 배경 언급은 핵심 분류 값으로 코딩하지 않습니다.
- 공격 성공과 실제 시스템 영향을 별도 필드로 기록합니다.
- framework·model·dataset·metric 이름은 논문 표기를 보존하고 정규화 필드를 추가합니다.
- 미공개 정보는 `unknown`이 아니라 `not-reported`로 기록합니다.
- 연구자가 적용할 수 없다고 명시한 필드는 `not-applicable`로 구분합니다.
- 연구 갭은 논문의 저자 주장과 본 매핑 연구의 해석을 별도 필드로 저장합니다.
