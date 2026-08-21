# OpenAlex·arXiv Seed-Recall Pilot

> 실행일: 2026-08-21  
> 프로토콜: 1.1-pilot–1.3.1-pilot  
> 상태: arXiv·OpenAlex core-security seed 기준 통과  
> 시간 기준: API 로그는 UTC

## 목적

18개 seed가 공개 검색원에 색인되어 있는지 확인하고, Q-A 위협·실패 검색군 또는 Q-D 통제·운영 검색군에서 회수되는지 검사했습니다.

## Seed 역할

- core-security: 16개
- contextual: 2개
  - indirect-prompt-injection-2023: Agent 보안의 직접 연구보다 LLM-integrated application 공격의 선행 배경
  - skillopt-2026: self-evolving Agent skill의 기반 시스템 연구이며 보안 연구가 아님

Contextual seed는 인접 연구 발견과 snowballing에는 사용하지만 security query recall 분모에는 포함하지 않습니다. 이 구분은 검색 결과를 높이기 위한 사후 삭제가 아니라 포함 기준과 seed 역할의 불일치를 교정한 것입니다.

## arXiv 결과

arXiv API의 id_list와 search_query 결합 기능을 이용해 18개 identifier를 Q-A와 Q-D로 직접 필터링했습니다.

| 버전 | 변경 | 전체 union | 전체 recall | Core-security recall |
|---|---|---:|---:|---:|
| 1.1-pilot | 최초 7개 Agent 표현 | 14/18 | 77.8% | 14/16, 87.5% |
| 1.2-pilot | LM agent, LLM-based agent 추가 | 16/18 | 88.9% | 16/16, 100% |

1.1에서 누락된 ToolEmu와 Agent Security Bench는 각각 LM agent와 LLM-based agent 표현을 사용합니다. 두 표현은 특정 제목에만 맞춘 단어가 아니라 Agent 문헌에 사용되는 일반적 동의어이므로 v1.2 공통 개념 사전에 추가했습니다.

v1.2에서 회수되지 않은 두 자료는 contextual seed와 일치합니다. 따라서 arXiv core-security recall은 잠정 성공 기준 90%를 충족합니다.

## OpenAlex 최초 무인증 실행

OpenAlex에서는 각 seed에 대해 title.search로 exact normalized title을 확인한 뒤, 색인이 확인된 seed를 query manifest로 검사했습니다.

| 항목 | 결과 |
|---|---:|
| Seed | 18 |
| Index presence 확인 | 6 |
| Index presence 미확정 | 12 |
| Query retrieval 확인 | 2 |
| 색인 확인 후 retrieval 미확정 | 4 |
| HTTP 429 요청 | 30 |

동시 요청 중 HTTP 429가 발생했으므로 미완료 요청을 false로 판정하지 않습니다. 이번 실행으로 OpenAlex conditional recall을 계산할 수 없습니다.

OpenAlex 결과는 다음 세 상태로 보존합니다.

- true: exact-title 또는 query retrieval이 응답으로 확인됨
- false: 필요한 요청이 모두 성공했으며 매칭이 없음
- unknown 또는 not_tested: HTTP 오류 또는 선행 index 확인 실패로 판정 불가

## OpenAlex 인증 재실행

API key 인증 후 모든 요청이 성공했습니다. v1.2는 Boolean 연산자 없이 나열한 용어가 모두 AND로 처리되어 indexed seed 4/16만 회수했습니다. 기존 개념을 명시적 OR 그룹으로 표현한 v1.3은 16/16을 회수했습니다. 최신 arXiv 제목 2건을 반영한 v1.3.1 최종 결과는 다음과 같습니다.

| 검색원·버전 | Index presence | Union recall | Core-security recall |
|---|---:|---:|---:|
| OpenAlex v1.2 | 16/18 | 4/16, 25.0% | 3/14, 21.4% |
| OpenAlex v1.3 | 16/18 | 16/16, 100% | 14/14, 100% |
| OpenAlex v1.3.1 | 18/18 | 18/18, 100% | 16/16, 100% |
| arXiv v1.2 | 18/18 | 16/18, 88.9% | 16/16, 100% |

최종 실행의 OpenAlex 342건과 arXiv 3건은 모두 HTTP 200을 반환했습니다. 세부 결과는 [OpenAlex 인증 파일럿](openalex-authenticated-pilot.md)에 기록합니다.

## 프로토콜 결정

1. 공통 Agent 표현을 7개에서 9개로 확장합니다.
2. arXiv v1.2 Q-A/Q-D를 pilot 통과 버전으로 유지합니다.
3. core-security와 contextual seed를 구분합니다.
4. OpenAlex v1.3.1을 seed-recall 통과 버전으로 유지합니다.
5. HTTP 429, timeout과 기타 실패는 false negative가 아니라 execution failure로 기록합니다.
6. OpenAlex 실행은 API key, 단일 worker, 요청 간격, Retry-After backoff와 unknown 상태를 사용합니다.

## 생성 파일

- data/seed-recall-pilot-2026-08-21.csv
- data/pilot-search-log-2026-08-21.csv
- data/pilot-summary-2026-08-21.json
- scripts/run-seed-recall-pilot.py

Search log에는 raw request URL, 실행 시각, HTTP 상태, 응답 크기와 SHA-256을 기록합니다. API response 전문은 저장소에 커밋하지 않습니다.

## 재현성 및 제한사항

- 공식 arXiv API manual의 id_list와 search_query 결합 동작을 사용했습니다.
- OpenAlex API key는 Authorization 헤더로만 전달하며 URL·로그·산출물에 저장하지 않습니다.
- Seed recall은 전체 문헌 recall의 대리 지표이며 완전성을 보장하지 않습니다.
- Seed 선정 자체가 연구자의 현재 taxonomy에 영향을 받습니다.
- OpenAlex와 arXiv의 coverage와 query semantics는 동일하지 않습니다.
- 전체 검색 전 query 결과의 noise와 제목·초록 precision pilot을 추가해야 합니다.

## 공식 문서

- [arXiv API User's Manual](https://info.arxiv.org/help/api/user-manual.html)
- [OpenAlex Help Center](https://help.openalex.org/)
