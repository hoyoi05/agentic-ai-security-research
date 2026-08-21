# 서베이 범위와 방법

## 연구 질문

1. 자가 진화 과정의 어느 입력과 상태가 오염될 수 있는가?
2. 오염이 trajectory에서 memory와 skill로 어떻게 축적·승격되는가?
3. 태스크 성능 검증만으로 악성 또는 과권한 skill을 걸러낼 수 있는가?
4. 에이전트의 의미적 의도와 실제 시스템 행위를 어떻게 인과적으로 연결할 수 있는가?
5. 로컬 Agent와 Kubernetes·Knative 환경에서 공격 경로와 관측 가능성은 어떻게 달라지는가?

## 포함 범위

- 경험 기반·trajectory 기반 self-improvement
- Skill 생성, 수정, 선택, 배포 및 재사용
- Episodic/semantic/procedural memory와 replay store
- Prompt infection, memory poisoning, tool-result poisoning
- MCP/tool 실행과 runtime supply chain
- 파일·프로세스·네트워크·identity·Kubernetes API 행위
- 지속성, 전이성, 권한 체이닝 및 cross-agent propagation

## 분류 축

| 축 | 값 |
|---|---|
| 연구 역할 | Threat Model, Attack, Propagation, Defense, Evaluation |
| 진화 단계 | Collect, Reflect, Synthesize, Validate, Promote, Execute |
| 오염 대상 | Experience, Memory, Skill, Reward, Tool, Runtime |
| 영향 계층 | Agent, MCP/Tool, Host, Container, Kubernetes, External Service |
| 근거 상태 | Author-claimed, Artifact-checked, Reproduced, Independently-verified |

## 제외·보류

모델 가중치 자체의 학습 공격은 skill/memory 진화와 직접 연결될 때만 포함합니다. 단순 jailbreak 성공률만 보고 시스템 효과를 측정하지 않은 연구는 인접 연구로 분리합니다.

## 검증 원칙

- 논문 제목, 저자, DOI/arXiv ID, 공식 코드 저장소를 1차 자료로 확인
- 저자 보고 수치와 독립 재현 수치를 분리
- 공개되지 않은 구현·데이터·trajectory를 명시
- PDF 원문은 재배포 허가가 확인된 경우에만 저장하고, 기본적으로 공식 링크와 자체 요약만 보관
