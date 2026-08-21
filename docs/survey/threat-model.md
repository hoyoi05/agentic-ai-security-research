# 자가 진화형 에이전트 위협 모델

## 보호 대상

- 원본 사용자 목표와 system policy
- 경험·trajectory·feedback 저장소
- 장기 memory와 retrieval index
- 생성·수정된 `SKILL.md`, 코드, 리소스
- validation dataset, verifier, reward signal
- MCP server, tool schema, 실행 권한
- host·container·Kubernetes identity와 외부 서비스

## 구조적 공격 흐름

| 단계 | 공격 예시 | 보안 결과 |
|---|---|---|
| 정찰 | Skill loader, memory API, tool schema, validation 규칙 탐색 | 신뢰 경계와 승격 조건 식별 |
| 경험 오염 | 간접 prompt, 악성 tool result, 조작된 성공 trajectory 주입 | 학습 입력 왜곡 |
| 진화 조작 | reflection·aggregation·reward·selection 편향 | 악성 규칙이 candidate skill에 포함 |
| 검증 우회 | held-out set 과적합, trigger 은닉, utility-only gate 악용 | 안전하지 않은 skill 승격 |
| 지속성 확보 | skill/memory artifact에 조건부 행동 저장 | 세션을 넘어선 backdoor |
| 실행 | MCP/tool을 통한 command, file, network, API 호출 | 실제 시스템 영향 |
| 전파 | 공유 skill registry, memory, agent delegation, CI/CD 배포 | 다른 에이전트·환경으로 확산 |

## 핵심 가설

> 태스크 성공률을 높이는 skill이라도 runtime capability와 privilege 사용을 확장할 수 있으며, utility-only validation은 이 변화를 충분히 탐지하지 못한다.

## 신뢰 경계

1. 외부 데이터·웹·사용자 입력 → Agent context
2. Agent trace → Experience/Memory store
3. Experience store → Skill optimizer
4. Candidate skill → Validation and promotion gate
5. Deployed skill → Agent control plane
6. Agent → MCP/Tool data plane
7. Tool → Host/Container/Kubernetes/Cloud

## 공격 기법 백로그

초기 분류에는 indirect prompt infection, malicious success trajectory, negative-example suppression, reward manipulation, reflection hijacking, skill trigger implantation, tool-description poisoning, schema manipulation, replay persistence, memory retrieval steering, privilege chaining, validation-set gaming, cross-agent skill propagation을 포함합니다. 30개 이상의 세부 기법은 후속 taxonomy 버전에서 공격 전제조건과 관측 지표까지 함께 공개합니다.
