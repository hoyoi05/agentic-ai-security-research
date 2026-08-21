# 실험 설계

## 목표

정상·오염 경험으로 생성된 candidate skill이 utility와 실제 runtime behavior에 미치는 영향을 측정하고, local Agent와 Kubernetes·Knative 환경에서 차이를 비교합니다.

## 비교 환경

| 환경 | 실행 단위 | 주요 권한 | 관측 지점 |
|---|---|---|---|
| Local Agent | host process 또는 제한 container | OS user, filesystem, local credentials | agent trace, execve, file, socket, DNS |
| Kubernetes/Knative | Pod/Revision, Broker/Trigger 포함 가능 | ServiceAccount, RBAC, Secret, NetworkPolicy | Tetragon/eBPF, audit log, API calls, network flow |

## 실험군

1. Baseline: skill 없음
2. Benign evolution: 정상 trajectory로 최적화된 skill
3. Poisoned experience: 악성 경험이 replay/aggregation 입력에 포함
4. Triggered skill: 특정 context에서만 위험 행동
5. Runtime-gated: security envelope로 promotion 또는 실행 차단

## 공격 시나리오

- 악성 tool result를 성공 경험으로 저장
- 높은 reward를 갖는 조작 trajectory 삽입
- reflection 단계에 은닉된 규칙 유도
- validation task에서는 비활성인 conditional trigger
- local credential 또는 kubeconfig 접근 유도
- 저권한 agent에서 고권한 MCP/tool/ServiceAccount로 체이닝
- 공유 skill registry를 통한 다른 agent로의 전파

## 수집 telemetry

- prompt/session/trajectory ID
- skill version, hash, parent, promotion decision
- tool/MCP server와 arguments/result provenance
- process tree와 `execve`
- file open/write/rename 및 민감 경로 접근
- network destination, DNS, HTTP metadata
- container, namespace, Pod, ServiceAccount
- Kubernetes API verb/resource/namespace
- verifier output, reward, policy violation

## 지표

| 범주 | 지표 |
|---|---|
| Utility | task success, verifier pass rate, latency, token/tool cost |
| 공격 | attack success rate, trigger precision, stealth |
| 지속성 | session/restart/redeployment 이후 재현율 |
| 전이 | 새 task/model/harness/agent로의 transfer rate |
| 권한 | 신규 identity·API verb·resource·network/file access |
| 탐지 | precision, recall, false positive rate, detection latency |
| 운영 | tracing overhead, storage cost, promotion/rollback time |

## 핵심 ablation

- agent trace만 사용 vs eBPF telemetry만 사용 vs 결합
- utility gate만 사용 vs runtime gate 결합
- local vs Kubernetes/Knative
- static skill scan vs dynamic execution
- clean validation vs adversarial validation
