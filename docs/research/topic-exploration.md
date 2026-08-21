# 신규 연구 주제 탐색

> 상태: **탐색 중 — 최종 주제 미선정**  
> 기존 자가 진화형 에이전트 보안은 후보군으로 유지하지만, 관련 공격·평가 논문이 빠르게 증가하므로 Agentic AI 전반에서 더 큰 연구 갭을 비교한다.

## 평가 기준

- 학술적 신규성: 기존 공격 변형이 아닌 새로운 문제 정의 또는 시스템 기여
- 실증 가능성: RTX 3090·RAM 128GB 및 API 모델로 반복 실험 가능
- 기존 역량 적합성: runtime tracing, eBPF/Tetragon, Kubernetes·Knative, permission graph
- 재현성: 공개 harness, attack scenario, telemetry, evaluator 제공 가능
- 국제 논문 기여: threat model + system + benchmark/evaluation을 결합할 수 있는가

## 1차 후보 비교

| 순위 | 후보 | 초기 신규성 | 실험성 | 기존 연구와의 차별점 |
|---|---|---:|---:|---|
| 1 | Agentic Incident Response & Causal Rollback | 높음 | 높음 | 방어를 차단에서 containment·forensics·recovery까지 확장 |
| 2 | Delegation-Chain Intent Laundering Detection | 높음 | 중상 | 단일 tool authorization이 아닌 agent 간 위임 전체를 검증 |
| 3 | Dynamic Effective-Capability & Blast-Radius Graph | 중상 | 높음 | 선언된 권한 대신 실제 조합 가능한 권한과 피해 범위 측정 |
| 4 | Long-Horizon Agent Security Benchmark | 중상 | 높음 | 단발 공격 성공률 대신 지속성·전파·복구 가능성 평가 |
| 5 | Ephemeral Agent / Persistent State Boundary Security | 높음 | 중간 | serverless 실행과 장기 memory·identity 사이의 경계 분석 |

## 우선 후보: Agentic Incident Response & Causal Rollback

### 문제

현재 Agentic AI 방어는 주로 unsafe tool call의 사전 차단 또는 runtime monitoring에 집중한다. 그러나 공격이 이미 일부 성공한 경우 다음 질문이 남는다.

- 어느 prompt, memory, agent, tool과 identity가 침해 경로에 포함됐는가?
- 어떤 file, process, network request, Kubernetes object, SaaS/API side effect가 영향을 받았는가?
- credential revoke, memory quarantine, skill rollback과 외부 side-effect 보상을 어떤 순서로 수행해야 하는가?
- 정상 작업 결과는 보존하면서 악성 영향만 선택적으로 되돌릴 수 있는가?

### 제안 방향

**AgentIR: Cross-Layer Incident Reconstruction and Causal Rollback for Agentic AI**

1. Semantic trace, agent/tool event, OS/eBPF, identity, Kubernetes audit를 하나의 causal provenance graph로 결합
2. 침해 indicator에서 원인과 downstream side effect를 역추적해 blast radius 계산
3. side effect를 reversible, compensatable, irreversible로 분류
4. memory/skill quarantine, token revocation, Pod/Revision 격리, compensating action을 포함한 recovery plan 생성
5. 복구 plan을 policy와 replay로 검증한 뒤 bounded autonomy로 실행

### 잠정 연구 질문

- RQ1: Agent trace만으로는 실제 blast radius를 얼마나 누락하는가?
- RQ2: semantic + system + cloud telemetry 결합이 원인·영향 복원 정확도를 얼마나 향상하는가?
- RQ3: causal rollback이 전체 환경 초기화보다 정상 결과 보존율과 복구 시간을 개선하는가?
- RQ4: local Agent와 Kubernetes·Knative에서 필요한 telemetry와 rollback primitive는 어떻게 다른가?
- RQ5: irreversible external action이 포함될 때 안전한 중단·human escalation 지점을 정의할 수 있는가?

### 핵심 지표

- root-cause localization accuracy
- affected-object precision/recall
- attack-chain reconstruction completeness
- residual malicious state
- benign-state preservation
- rollback success and compensation correctness
- MTTC/MTTR
- telemetry and enforcement overhead

## 인접 연구와 남은 공백

- [PROV-AGENT](https://arxiv.org/abs/2508.02866)은 agent workflow provenance 통합을 다루지만, 보안 사고의 cross-layer containment와 causal rollback은 중심 범위가 아니다.
- [AgentSight](https://arxiv.org/abs/2508.02736)은 agent intent와 system effect 관측의 semantic gap을 줄인다. AgentIR은 identity·Kubernetes object·external side effect와 복구까지 확장한다.
- [Fault-Tolerant Sandboxing for AI Coding Agents](https://arxiv.org/abs/2512.12806)은 transactional filesystem rollback을 제안한다. 외부 API, credential, memory, multi-agent propagation과 cloud resource는 별도 문제다.
- [PROVSEEK](https://arxiv.org/abs/2508.21323)은 provenance를 이용해 일반 cyber threat investigation을 자동화하며, “agent 자체가 침해된 시스템”의 상태 복구 문제와는 구분된다.
- NIST의 [Software and AI Agent Identity and Authorization](https://www.nccoe.nist.gov/projects/software-and-ai-agent-identity-and-authorization)은 agent identity와 authority의 실무적 중요성을 확인한다.
- OWASP [Top 10 for Agentic Applications 2026](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)은 goal hijacking, tool misuse, identity/privilege abuse 등 사고 원인을 분류하지만, cross-layer recovery benchmark를 제공하지 않는다.

## 다른 후보에 대한 판단

### Delegation-chain intent laundering

A2A와 multi-agent delegation에서 원래 사용자 의도가 중간 agent를 거치며 변형되고, 고권한 agent가 confused deputy가 되는 문제다. 중요하지만 BlockA2A, trust–authorization mismatch, agent identity 연구가 이미 빠르게 증가하고 있어 **위임 lineage + runtime effect**로 차별화해야 한다.

### Dynamic effective capability

정적 IAM 목록이 아니라 tool composition, credential delegation, network reachability, runtime usage를 결합해 agent가 실제로 만들 수 있는 행동 집합을 계산한다. 실험성이 높지만 Progent, MiniScope, SEAgent 등 authorization 연구와의 중복을 피하려면 **시간에 따른 capability drift와 blast-radius prediction**이 필요하다.

### Long-horizon benchmark

공격 성공률뿐 아니라 persistence, propagation, privilege gain, blast radius, detection delay, recovery completeness를 평가한다. 독립 benchmark만으로도 가치가 있지만, AgentIR 또는 capability graph의 평가 기반으로 포함할 때 기여가 더 강하다.

### Ephemeral/persistent boundary

Knative 같은 ephemeral execution이 종료돼도 external memory, event trigger, service identity와 side effect는 지속된다. 독창적이지만 실험 범위가 serverless 구조에 치우칠 수 있으므로 AgentIR의 환경 비교 축으로 먼저 포함하는 편이 적절하다.

## 현재 결론

자가 진화형 skill poisoning은 독립 주제보다 **AgentIR의 persistent-state compromise 시나리오**로 유지한다. 다음 심층 서베이의 우선 대상은 다음과 같다.

1. agent provenance와 failure attribution
2. containment, credential revocation, state quarantine
3. reversible action과 compensating transaction
4. agent memory/skill recovery
5. multi-agent propagation recovery
6. Kubernetes·serverless rollback primitives
