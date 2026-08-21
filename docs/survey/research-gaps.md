# 연구 갭

## 문헌에서 확인되는 공백

| 공백 | 현재 경향 | 필요한 연구 |
|---|---|---|
| Utility–security 분리 | 성공률·보상 향상 중심 | 성능과 runtime 위험을 함께 보는 promotion gate |
| Semantic–system gap | prompt/tool trace 또는 system call 중 한쪽 관측 | 의도–tool–OS/cloud 효과의 인과 상관 |
| 지속성 평가 부족 | 단일 세션 공격 성공 측정 | skill/memory 승격 후 재부팅·재배포·새 태스크 지속성 |
| 권한 변화 미측정 | 호출 성공 여부 중심 | identity, RBAC, filesystem, network capability drift |
| 환경 일반화 부족 | 로컬 sandbox 중심 | 로컬 Agent와 Kubernetes·Knative 비교 |
| 전파 모델 부족 | 단일 agent 공격 | 공유 registry, memory, delegation을 통한 확산 |
| 독립 재현 부족 | 비공개 harness·trajectory·judge 의존 | 고정 corpus, version, raw trace, deterministic verifier 공개 |

## 우선 제안

### Runtime-Verified Secure Skill Evolution

Candidate skill (s')는 다음 조건을 모두 만족할 때만 승격합니다.

1. 기준 skill (s)보다 utility가 개선되거나 사전 임계값을 만족
2. 허용된 process/file/network/API behavior envelope를 벗어나지 않음
3. identity와 privilege 사용량이 증가하지 않거나 승인된 변화임
4. 악성 trigger·오염 trajectory·환경 변화에 대한 stress test 통과
5. promotion 근거를 replay 가능한 trace와 verifier 결과로 남김

## 예상 기여

- 자가 진화 pipeline용 end-to-end 보안 위협 모델
- semantic trace와 eBPF/Kubernetes telemetry를 결합한 provenance graph
- utility·persistence·attack success·privilege drift 통합 benchmark
- 로컬 환경과 Kubernetes·Knative 환경의 비교 실증
- 안전한 skill promotion·rollback 정책
