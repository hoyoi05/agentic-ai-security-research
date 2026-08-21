# Agentic AI Security Research

이 포털은 Agentic AI 보안 자료를 단순 수집하는 대신 **근거, 재현성, 실제 시스템 영향**을 중심으로 정리합니다.

## 첫 번째 연구 트랙

### Runtime-Verified Secure Skill Evolution

자가 진화형 에이전트는 성공·실패 trajectory, 장기 메모리, 사용자 피드백, 도구 실행 결과를 이용해 skill을 만들거나 수정합니다. 기존 최적화는 주로 태스크 성능을 기준으로 후보 skill을 채택하지만, 성능 향상이 다음 변화를 동반하는지는 별도로 검증해야 합니다.

- 새 파일·프로세스·네트워크 접근 능력
- MCP 또는 외부 도구 호출 범위 확장
- 인증정보·서비스 계정·Kubernetes RBAC 사용 변화
- 오염된 경험의 장기 기억 및 다른 작업으로의 전이
- Skill 배포 이후 지속되는 조건부 backdoor

본 연구는 **utility gate**와 **runtime security gate**를 함께 통과한 skill만 승격하는 방법을 목표로 합니다.

## 핵심 관측 경로

`사용자 의도 → 에이전트 계획 → Skill/Memory → Tool·MCP → Process/File/Network → Identity/Kubernetes API → 외부 효과`

## 현재 상태

- 초기 분류체계와 위협 모델 수립
- SkillOpt·SkillLens 및 관련 공격/관측 연구의 1차 자료 등록
- 로컬 Agent와 Kubernetes·Knative 비교 실험 설계
- 독립 재현 결과는 아직 없으며, 문헌상의 수치는 저자 주장으로 구분

## 다음 단계

1. 악성 경험·trajectory 주입 공격군 구체화
2. 정상/오염 skill evolution 데이터셋 구축
3. eBPF/Tetragon 및 에이전트 trace의 교차 계층 provenance 결합
4. utility, attack success, persistence, privilege drift 동시 평가
