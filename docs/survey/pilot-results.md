# OpenAlex·arXiv Seed-Recall Pilot

> 실행일: 2026-08-21  
> 프로토콜: 1.1-pilot 및 1.2-pilot  
> 상태: arXiv 완료, OpenAlex 미완료  
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

## OpenAlex 결과

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

## 프로토콜 결정

1. 공통 Agent 표현을 7개에서 9개로 확장합니다.
2. arXiv v1.2 Q-A/Q-D를 pilot 통과 버전으로 유지합니다.
3. core-security와 contextual seed를 구분합니다.
4. OpenAlex recall은 보고하지 않고 rate-aware 재실행 대상으로 남깁니다.
5. HTTP 429, timeout과 기타 실패는 false negative가 아니라 execution failure로 기록합니다.
6. OpenAlex 재실행 스크립트는 단일 worker, Retry-After 기반 backoff와 unknown 상태를 사용합니다.

## 생성 파일

- data/seed-recall-pilot-2026-08-21.csv
- data/pilot-search-log-2026-08-21.csv
- data/pilot-summary-2026-08-21.json
- scripts/run-seed-recall-pilot.py

Search log에는 raw request URL, 실행 시각, HTTP 상태, 응답 크기와 SHA-256을 기록합니다. API response 전문은 저장소에 커밋하지 않습니다.

## 재현성 및 제한사항

- 공식 arXiv API manual의 id_list와 search_query 결합 동작을 사용했습니다.
- OpenAlex API의 rate limit과 응답 정책은 재실행 시점에 다시 확인해야 합니다.
- Seed recall은 전체 문헌 recall의 대리 지표이며 완전성을 보장하지 않습니다.
- Seed 선정 자체가 연구자의 현재 taxonomy에 영향을 받습니다.
- OpenAlex와 arXiv의 coverage와 query semantics는 동일하지 않습니다.
- 전체 검색 전 query 결과의 noise와 제목·초록 precision pilot을 추가해야 합니다.

## 공식 문서

- [arXiv API User's Manual](https://info.arxiv.org/help/api/user-manual.html)
- [OpenAlex Help Center](https://help.openalex.org/)
