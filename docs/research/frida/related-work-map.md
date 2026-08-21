# FRIDA 선행연구 맵

> 검토 상태: preliminary scoping review  
> 기준일: 2026-08-21  
> 범위 제한: 아래 목록은 연구 가설을 구체화하기 위한 seed set이며 체계적 매핑 연구의 최종 포함 문헌이 아니다. arXiv 논문은 preprint로, IETF 문서는 Internet-Draft로 구분한다.

## 잠정 연구 공백

Agent identity, authorization, delegation, provenance, observability와 Agent 포렌식에 관한 인접 연구는 존재한다. 현재 검토한 자료에서는 이 요소들을 Agent lifecycle 전체에 연결하고, 최소 포렌식 증거와 비용·재구성 가능성의 trade-off까지 실험적으로 평가한 단일 통합 체계는 확인되지 않았다.

따라서 안전한 연구 공백 진술은 “관련 연구가 없다”가 아니라 다음과 같다.

> 개별 기술은 빠르게 발전하고 있으나, ephemeral·mutable Agent의 identity continuity와 delegation-aware authority provenance를 포렌식 증거요건 및 adaptive evidence capture와 함께 검증하는 통합 연구가 부족하다.

이 진술은 공개 학술 데이터베이스 검색, 전문 검토와 forward/backward snowballing 이후 갱신한다.

## Seed literature matrix

| 영역 | 자료 | 상태 | 직접 제공하는 내용 | FRIDA에서 추가 검토할 공백 |
|---|---|---|---|---|
| Identity·authorization 요구 | [NIST NCCoE concept paper](https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf) | 정부 concept paper, 2026 | 위임, human binding, auditing와 non-repudiation을 공개 연구 질문으로 제시 | 실행 가능한 증거 모델과 정량 평가 |
| Agent 표준화 | [NIST AI Agent Standards Initiative](https://www.nist.gov/artificial-intelligence/ai-agent-standards-initiative) | 공식 initiative, 2026 | secure, trusted, interoperable Agent 표준화 추진 | 포렌식 최소증거의 구체적 구현 |
| Identity·delegation protocol | [Agent Identity Protocol](https://datatracker.ietf.org/doc/draft-singla-agent-identity-protocol/) | IETF Internet-Draft, 2026 | DID, capability authorization과 cryptographic delegation chain | centralized NHI IdP 및 포렌식 비용 평가 |
| Agent authentication | [AI Agent Authentication and Authorization](https://www.ietf.org/archive/id/draft-klrc-aiagent-auth-00.html) | IETF Internet-Draft, 2026 | workload identity token과 HTTP message signature 결합 | lifecycle provenance와 조사 모델 |
| Agent use-case requirements | [Agentic AI Use Cases and Requirements](https://www.ietf.org/archive/id/draft-agentic-ai-usecases-requirements-01.html) | IETF Internet-Draft, 2026 | delegation 전 구간의 원 발급자 신원·권한 제약 보존 요구 | 증거 최소화와 복원성 실험 |
| Delegated execution observability | [Observability for Delegated Execution in Agentic AI Systems](https://arxiv.org/abs/2606.09692) | arXiv preprint, 2026 | 실행 시점 delegation context 결합과 cross-tool reconstruction | Agent lifecycle, evidence integrity, adaptive retention |
| Intent-aware delegation | [SentinelAgent](https://arxiv.org/abs/2604.02767) | arXiv preprint, 2026 | verifiable delegation chain과 authority non-escalation 속성 | 실제 포렌식 수집 비용과 lifecycle continuity |
| Evidence tracing·provenance | [A Survey of Evidence Tracing and Execution Provenance for LLM Agents](https://arxiv.org/abs/2606.04990) | arXiv preprint, 2026 | trace source, evidence unit, provenance relation taxonomy | forensic readiness와 minimum sufficient evidence 검증 |
| Agent forensic analysis | [Foundations for Agentic AI Investigations](https://arxiv.org/abs/2604.05589) | arXiv preprint, 2026 | 단일 Agent assistant의 상태·행위 재구성 실증 | multi-agent delegation, NHI IdP와 권한 증폭 |
| Provenance standard | [W3C PROV-DM](https://www.w3.org/TR/prov-dm/) | W3C Recommendation, 2013 | entity, activity, agent 중심 provenance model | Agent-specific identity, authorization와 evidence profile |
| Telemetry schema | [OpenTelemetry GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) | 공식 specification | GenAI operation·Agent 관련 telemetry attribute | 포렌식 충분성, 무결성과 delegation semantics |

## 차별화 축

FRIDA 후보가 선행연구와 구분되려면 다음 네 축이 동시에 포함되어야 한다.

1. **Lifecycle-aware identity continuity:** 이름이 아닌 논리 Agent·version·instance·credential의 관계를 보존한다.
2. **Delegation-aware authority provenance:** 호출 그래프뿐 아니라 원래 권한, 위임 범위, 유효권한과 정책결정을 기록한다.
3. **Forensic sufficiency:** 사고 후 attribution, authorization, causality와 integrity를 검증하는 데 필요한 증거를 명시한다.
4. **Bounded evidence cost:** 전체 trace와 비교하여 저장량·지연·민감정보 노출을 줄이면서 재구성 성능을 유지하는지 평가한다.

## 검증할 반증 가능성

체계적 검색 과정에서는 다음 가능성을 적극적으로 확인한다.

- 이미 동일한 lifecycle identity 계층과 delegation evidence schema가 제안되었는가?
- 기존 observability 연구가 이미 포렌식 충분성을 정량적으로 평가했는가?
- identity protocol이 deletion·recreation·clone 구분까지 지원하는가?
- 최소증거 또는 risk-triggered capture의 효율성이 기존 연구에서 검증되었는가?
- Agent 포렌식이 아닌 distributed tracing·workflow provenance 분야가 문제를 사실상 해결했는가?

## 검색 상태

Scopus, Web of Science와 IEEE Xplore의 구독 접근을 전제로 하지 않는다. 우선 OpenAlex, Crossref, DBLP, Semantic Scholar, arXiv와 공식 표준 사이트를 이용해 공개 재현 가능한 검색을 수행하고, forward/backward snowballing으로 보완한다. Google Scholar 결과는 검색 재현성이 제한되므로 보충 발견 경로로만 기록한다.
