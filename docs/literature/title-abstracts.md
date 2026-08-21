# Agentic AI 보안 제목·초록 카탈로그

> 수집일: 2026-08-21  
> 배치: broad survey batch 1  
> 포함: 학술논문 11건, 공식 화이트페이퍼·가이드 4건

## 정리 원칙

- 제목, 저자·기관, 연도, DOI 또는 공식 URL을 1차 출처에서 확인했습니다.
- 저작권이 있는 원문 초록은 그대로 복제하지 않고 **한국어 자체 초록 요약**으로 정리했습니다.
- 논문의 성능·공격 성공률·방어 효과는 독립 재현 전까지 저자 주장으로 취급합니다.
- 공식 가이드에 학술 초록이 없는 경우 공식 소개문을 바탕으로 **개요 요약**을 제공합니다.
- 기계 판독용 전체 메타데이터는 [literature-catalog.yaml](https://github.com/hoyoi05/agentic-ai-security-research/blob/main/data/literature-catalog.yaml)에 있습니다.

## 공격·벤치마크

### Identifying the Risks of LM Agents with an LM-Emulated Sandbox

- **저자:** Yangjun Ruan et al.
- **연도·식별자:** 2023, [arXiv:2309.15817](https://arxiv.org/abs/2309.15817)
- **초록 요약:** ToolEmu는 실제 도구 환경을 매번 구축하지 않고 언어모델이 도구 실행을 모사하게 하여 장기 꼬리 위험을 시험합니다. 고위험 도구, 테스트 사례와 자동 평가기를 이용해 개인정보 유출이나 재무 손실로 이어질 수 있는 실패를 찾습니다.
- **한계:** 모사된 도구 동작과 자동 평가가 실제 시스템의 결과와 다를 수 있습니다.

### InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agents

- **저자:** Qiusi Zhan, Zhixiang Liang, Zifan Ying, Daniel Kang
- **연도·식별자:** 2024, Findings of ACL 2024, [arXiv:2403.02691](https://arxiv.org/abs/2403.02691)
- **초록 요약:** 외부 콘텐츠의 악성 지시가 도구 통합형 에이전트를 조작하는 간접 프롬프트 주입을 평가합니다. 사용자 피해와 비공개 데이터 유출을 포함한 공격 의도 및 다양한 사용자·공격자 도구를 벤치마킹합니다.
- **한계:** 공격률은 평가한 프롬프트, 에이전트 구조와 모델 버전에 종속됩니다.

### AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents

- **저자:** Edoardo Debenedetti et al.
- **연도·식별자:** 2024, [arXiv:2406.13352](https://arxiv.org/abs/2406.13352)
- **초록 요약:** 신뢰할 수 없는 데이터를 처리하면서 도구를 실행하는 에이전트의 공격과 방어를 동적으로 비교하는 확장형 환경입니다. 현실적 업무와 보안 테스트를 함께 제공해 유용성과 보안의 상충관계를 평가합니다.
- **한계:** 포함된 업무군과 당시 모델 스냅샷을 넘어서는 일반화는 추가 검증이 필요합니다.

### Agent Security Bench (ASB): Formalizing and Benchmarking Attacks and Defenses in LLM-based Agents

- **저자:** Hanrong Zhang et al.
- **연도·식별자:** 2024, ICLR 2025, [arXiv:2410.02644](https://arxiv.org/abs/2410.02644)
- **초록 요약:** 여러 응용 시나리오, 에이전트, 도구, 공격·방어 기법과 지표를 통합해 LLM 에이전트 보안을 비교합니다. 프롬프트 주입, 메모리 오염, Plan-of-Thought 백도어와 혼합 공격을 다룹니다.
- **한계:** 넓은 벤치마크이지만 실제 배포 환경의 모든 공격 표면을 포괄한다고 볼 수 없습니다.

### AgentHarm: A Benchmark for Measuring Harmfulness of LLM Agents

- **저자:** Maksym Andriushchenko et al.
- **연도·식별자:** 2024, ICLR 2025, [arXiv:2410.09024](https://arxiv.org/abs/2410.09024)
- **초록 요약:** 사기, 사이버범죄, 괴롭힘 등을 포함한 악성 다단계 작업으로 에이전트 오용 가능성을 평가합니다. 탈옥 이후에도 작업 능력을 유지하면서 실제 유해 행동을 완료하는지를 함께 측정합니다.
- **한계:** 명시적인 악성 요청을 중심으로 하므로 우발적 실패나 간접 공격 전체를 대표하지 않습니다.

## 방어·권한 통제

### Defeating Prompt Injections by Design

- **저자:** Edoardo Debenedetti et al.
- **연도·식별자:** 2025, [arXiv:2503.18813](https://arxiv.org/abs/2503.18813)
- **초록 요약:** CaMeL은 신뢰된 질의에서 제어 흐름과 데이터 흐름을 분리해 비신뢰 데이터가 프로그램 흐름을 변경하지 못하도록 설계합니다. 도구 호출에는 capability 정책을 적용해 승인되지 않은 데이터 유출 경로를 차단합니다.
- **한계:** 보안 성질은 흐름 추출의 정확성과 정책·도구 중재 가정에 의존합니다.

### Progent: Securing AI Agents with Privilege Control

- **저자:** Tianneng Shi et al.
- **연도·식별자:** 2025, [arXiv:2504.11703](https://arxiv.org/abs/2504.11703)
- **초록 요약:** 도구 이름과 인자에 대한 기호 정책으로 모든 호출을 검사하고 최소권한을 집행합니다. 정책 축소는 자동 허용하지만 확장에는 명시적 승인을 요구해 승인 없는 권한 상승을 제한합니다.
- **한계:** 정책 생성에 LLM을 사용하므로 정책 품질과 모든 도구 호출이 중재된다는 가정이 중요합니다.

## 다중 에이전트·서베이·SoK

### Open Challenges in Multi-Agent Security: Towards Secure Systems of Interacting AI Agents

- **저자:** Christian Schroeder de Witt et al.
- **연도·식별자:** 2025, [arXiv:2505.02077](https://arxiv.org/abs/2505.02077)
- **초록 요약:** 에이전트 간 상호작용과 공유 환경에서 증폭되는 공모, 스웜 공격, 개인정보 침해, 탈옥과 데이터 오염을 다중 에이전트 보안 문제로 체계화합니다. 분산·탈중앙 환경의 상충관계와 통합 연구 의제를 제시합니다.
- **한계:** 종단 간 방어를 실증한 논문보다는 분류와 연구 의제의 성격이 강합니다.

### From Prompt Injections to Protocol Exploits: Threats in LLM-Powered AI Agents Workflows

- **저자:** Mohamed Amine Ferrag et al.
- **연도·식별자:** 2025, ICT Express, [DOI:10.1016/j.icte.2025.12.001](https://doi.org/10.1016/j.icte.2025.12.001), [arXiv](https://arxiv.org/abs/2506.23260)
- **초록 요약:** 호스트-도구와 에이전트-에이전트 통신을 포함하는 종단 간 위협 모델을 구성하고 입력 조작부터 프로토콜 취약점까지 분류합니다. 신뢰 관리, provenance 및 샌드박스 인터페이스를 대응 방향으로 검토합니다.
- **한계:** 분류의 교차 매핑과 전문가 검토가 모든 공격의 독립 실증을 의미하지는 않습니다.

### A Survey on Agentic Security: Applications, Threats and Defenses

- **저자:** Asif Shahriar et al.
- **연도·식별자:** 2025, [arXiv:2510.06445](https://arxiv.org/abs/2510.06445)
- **초록 요약:** Agentic AI 보안을 응용, 위협, 방어의 세 축으로 구성하고 대규모 문헌을 통합 분류합니다. 공격 진입점과 에이전트 루프 단계, 방어 배치 위치, 비용·보안 상충관계를 연결합니다.
- **한계:** 저자들이 구성한 문헌 집합과 분류 체계이므로 독립적인 검색·선별 검증이 필요합니다.

### SoK: The Attack Surface of Agentic AI - Tools and Autonomy

- **저자:** Ali Dehghantanha, Sajad Homayoun
- **연도·식별자:** 2026, [arXiv:2603.22928](https://arxiv.org/abs/2603.22928)
- **초록 요약:** 도구, RAG, 자율 다중 에이전트 루프로 확장되는 신뢰 경계와 공격 표면을 정리합니다. 프롬프트 주입, 지식베이스 오염, 플러그인 악용 및 교차 에이전트 조작을 분류하고 배포 단계별 방어책을 제안합니다.
- **한계:** 선택된 논문·보고서를 종합한 SoK이며 완전한 체계적 문헌고찰로 보고되지는 않았습니다.

## 공식 화이트페이퍼·가이드

### OWASP Top 10 for Agentic Applications for 2026

- **기관·발행일:** OWASP GenAI Security Project, 2025-12-09
- **공식 링크:** [OWASP 리소스](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/)
- **공식 개요 요약:** 자율적으로 계획·행동·의사결정하는 애플리케이션에서 우선 대응할 보안 위험을 운영 관점의 목록으로 정리합니다. 개발자와 방어자가 위험 완화를 시작할 수 있는 공통 분류와 지침을 제공합니다.
- **한계:** 합의 기반 위험 가이드이며 실증 벤치마크나 공식 표준은 아닙니다.

### Securing Agentic Applications Guide 1.0

- **기관·발행일:** OWASP GenAI Security Project, 랜딩 페이지에 날짜 미표기
- **공식 링크:** [OWASP 리소스](https://genai.owasp.org/resource/securing-agentic-applications-guide-1-0/)
- **공식 개요 요약:** LLM 기반 Agentic 애플리케이션의 설계, 개발, 배포 단계에서 적용할 구체적인 보안 권고를 제공합니다. 위협 분류보다 구현자와 방어자가 적용할 기술적 통제에 초점을 둡니다.
- **한계:** 환경별 위협 모델과 구현 조건에 맞춘 추가 검증이 필요합니다.

### Agentic AI - Threats and Mitigations

- **기관·발행일:** OWASP GenAI Security Project, 랜딩 페이지에 날짜 미표기
- **공식 링크:** [OWASP 리소스](https://genai.owasp.org/resource/agentic-ai-threats-and-mitigations/)
- **공식 개요 요약:** LLM과 결합된 Agentic AI의 규모와 자율성이 확대하면서 나타나는 위협을 위협 모델 기반으로 설명하고 완화책을 연결합니다. OWASP Agentic Security Initiative의 기초 참조 자료입니다.
- **한계:** 공식 표준이 아니며 제품·환경별 통제 효과를 직접 입증하지 않습니다.

### Accelerating the Adoption of Software and Artificial Intelligence Agent Identity and Authorization

- **기관·발행일:** NIST NCCoE, 2026-02-05
- **공식 링크:** [NIST CSRC 문서 페이지](https://csrc.nist.gov/pubs/other/2026/02/05/accelerating-the-adoption-of-software-and-ai-agent/ipd)
- **공식 개요 요약:** 소프트웨어 및 AI 에이전트에 신원 표준과 모범사례를 적용하기 위한 프로젝트 고려사항을 제시합니다. 식별, 권한부여, 감사, 부인방지 및 프롬프트 주입 통제를 포함한 사용 사례·기술·표준 현황을 다룹니다.
- **한계:** 초기 공개 초안인 개념 문서이며 확정 NIST 표준이 아닙니다.

## 다음 수집 우선순위

- MCP server·tool description poisoning과 공급망 보안
- memory·experience·skill poisoning 및 장기 지속성
- multi-agent delegation, collusion, propagation
- runtime provenance, 감사 로그와 포렌식 재구성
- 정량 비교가 가능한 방어 및 공개 재현 artifact
