# 검증 문헌 카탈로그

아래 표는 2026-08-20 기준 1차 자료를 확인한 초기 seed set입니다. 수치와 결론은 독립 재현 전까지 저자 주장으로 취급합니다.

| 자료 | 유형 | 연구 관련성 | 검증 상태 |
|---|---|---|---|
| [SkillOpt: Executive Strategy for Self-Evolving Agent Skills](https://arxiv.org/abs/2605.23904) / [code](https://github.com/microsoft/SkillOpt) | 2026 arXiv preprint + Microsoft code | skill 문서를 frozen agent의 trainable state로 최적화하고 validation gate로 승격 | Primary source checked; not reproduced |
| [SkillLens](https://github.com/SkillLens-AI/skilllens) | 2026 artifact; preprint forthcoming | skill utility와 security를 static/dynamic 평가하는 pipeline 및 공개 결과 | Artifact checked; publication pending |
| [Skill Set Optimization](https://arxiv.org/abs/2402.03244) | 2024 arXiv preprint | high-reward subtrajectory에서 transferable skill을 추출·정제 | Metadata checked; not reproduced |
| [AgentPoison](https://arxiv.org/abs/2407.12784) | 2024 arXiv preprint | memory/knowledge base poisoning을 통한 LLM agent red teaming | Metadata checked; not reproduced |
| [Your Agent May Misevolve](https://arxiv.org/abs/2509.26354) | 2025 arXiv preprint | self-evolving agent의 emergent risk를 직접 연구 | Metadata checked; not reproduced |
| [AgentSight](https://arxiv.org/abs/2508.02736) / [code](https://github.com/agent-sight/agentsight) | 2025 arXiv + systems artifact | eBPF boundary tracing으로 의미적 intent와 system effect의 gap을 연결 | Primary source checked; not reproduced |

## 비판적 관찰

### SkillOpt

공식 저장소는 rollout → reflect → aggregate → select → update → evaluate loop와 held-out validation을 설명합니다. 보안 관점의 핵심 질문은 validation score가 상승한 candidate가 기존보다 넓은 filesystem, process, network, tool 또는 identity capability를 획득했는지 여부입니다.

### SkillLens

공개 저장소는 with-skill/without-skill utility 비교, security scenario, Harbor 기반 disposable container 실행, trajectory judge를 제공합니다. 저장소 자체가 정확한 수치 재현의 한계와 raw trajectory 미공개 상태를 명시하므로, 결과 보고서와 audit-level trace availability를 구분해야 합니다.

### AgentPoison

장기 memory나 knowledge base에 삽입된 정보가 이후 agent 의사결정에 영향을 주는 공격을 다룹니다. 본 연구에서는 여기에 **오염된 기억이 skill 합성·승격을 거쳐 실행 가능한 영구 artifact가 되는 단계**를 추가합니다.

### AgentSight

semantic intent와 kernel-observed effect를 연결하는 문제의식을 공유합니다. 본 연구는 이를 self-evolution lifecycle, privilege drift, Kubernetes API/RBAC 및 skill promotion decision까지 확장하는 것을 목표로 합니다.

## 수집 대기열

- 악성 experience/trajectory injection의 직접 실험 연구
- persistent skill backdoor 및 skill supply chain
- memory poisoning 방어와 rollback
- MCP/tool runtime policy와 provenance
- cross-agent skill propagation
