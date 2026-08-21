# 데이터베이스별 검색 전략

> 버전: 1.0-draft  
> 작성일: 2026-08-21  
> 실제 검색 결과 수: 미기록

## 공통 설계

검색 결과는 Q-A와 Q-D의 합집합입니다. 데이터베이스마다 같은 개념을 유지하고 필드 문법과 wildcard 제약만 변환합니다.

### Agentic-system 블록

- AI agent
- LLM agent
- large language model agent
- language model agent
- agentic AI
- tool-using agent
- autonomous agent

### Q-A: Threats and failures

security, vulnerability, attack, threat, adversarial, prompt injection, poisoning, backdoor, jailbreak, misuse, harm, privacy, compromise

### Q-D: Controls and operations

defense, safeguard, monitoring, detection, authorization, authentication, access control, privilege, provenance, forensics, audit, containment, recovery, rollback, isolation, sandbox

일반적인 `multi-agent system`은 전통적 MAS 문헌의 대량 유입을 방지하기 위해 Agentic-system 블록에서 제외합니다. LLM 또는 Agentic AI와 연결된 multi-agent 연구는 위 용어를 함께 포함하므로 회수할 수 있고, 추가 문헌은 snowballing으로 보완합니다.

## Scopus

Scopus Advanced Search의 제목·초록·키워드 결합 필드인 `TITLE-ABS-KEY`를 사용합니다. 공식 필드 설명은 [Scopus Advanced Search 도움말](https://service.elsevier.com/app/answers/detail/a_id/11365/supporthub/scopus/)에서 확인합니다.

### SCOPUS-QA

```text
TITLE-ABS-KEY(
  (
    "AI agent*" OR "LLM agent*" OR "large language model agent*" OR
    "language model agent*" OR "agentic AI" OR "tool-using agent*" OR
    "autonomous agent*"
  )
  AND
  (
    secur* OR vulnerab* OR attack* OR threat* OR adversar* OR
    "prompt injection" OR poison* OR backdoor* OR jailbreak* OR
    misuse OR harm* OR privacy OR compromis*
  )
)
AND PUBYEAR > 2021
AND PUBYEAR < 2027
```

### SCOPUS-QD

```text
TITLE-ABS-KEY(
  (
    "AI agent*" OR "LLM agent*" OR "large language model agent*" OR
    "language model agent*" OR "agentic AI" OR "tool-using agent*" OR
    "autonomous agent*"
  )
  AND
  (
    defen* OR safeguard* OR monitor* OR detect* OR authorization OR
    authentication OR "access control" OR privilege* OR provenance OR
    forensic* OR audit* OR containment OR recovery OR rollback OR
    isolation OR sandbox*
  )
)
AND PUBYEAR > 2021
AND PUBYEAR < 2027
```

실행 후 document type은 article, conference paper, review로 필터링합니다. 언어는 검색 단계에서 제한하지 않고 스크리닝 단계에서 판정합니다.

## Web of Science Core Collection

Advanced Search의 Topic 필드 `TS=`를 사용합니다. Topic은 title, abstract, author keywords와 Keywords Plus를 검색합니다. 실제 검색 시 Web of Science Core Collection을 collection으로 기록합니다.

### WOS-QA

```text
TS=(
  (
    "AI agent*" OR "LLM agent*" OR "large language model agent*" OR
    "language model agent*" OR "agentic AI" OR "tool-using agent*" OR
    "autonomous agent*"
  )
  AND
  (
    secur* OR vulnerab* OR attack* OR threat* OR adversar* OR
    "prompt injection" OR poison* OR backdoor* OR jailbreak* OR
    misuse OR harm* OR privacy OR compromis*
  )
)
AND PY=(2022-2026)
```

### WOS-QD

```text
TS=(
  (
    "AI agent*" OR "LLM agent*" OR "large language model agent*" OR
    "language model agent*" OR "agentic AI" OR "tool-using agent*" OR
    "autonomous agent*"
  )
  AND
  (
    defen* OR safeguard* OR monitor* OR detect* OR authorization OR
    authentication OR "access control" OR privilege* OR provenance OR
    forensic* OR audit* OR containment OR recovery OR rollback OR
    isolation OR sandbox*
  )
)
AND PY=(2022-2026)
```

실행 후 document type은 article, proceedings paper, review article로 필터링합니다. 실제 인터페이스에서 허용되는 인용부호와 wildcard를 확인하고, 수정이 필요하면 실행 문자열을 검색 로그에 그대로 저장합니다.

## IEEE Xplore

[IEEE Xplore Command Search](https://ieeexplore.ieee.org/Xplorehelp/searching-ieee-xplore/command-search)의 `All Metadata` 필드를 사용합니다. IEEE Xplore는 clause당 검색어 수와 wildcard 사용에 제약이 있으므로 wildcard 대신 기본형을 사용하고, Q-A와 Q-D를 분리합니다.

### IEEE-QA

```text
(
  ("All Metadata":"AI agent") OR
  ("All Metadata":"LLM agent") OR
  ("All Metadata":"large language model agent") OR
  ("All Metadata":"language model agent") OR
  ("All Metadata":"agentic AI") OR
  ("All Metadata":"tool-using agent") OR
  ("All Metadata":"autonomous agent")
)
AND
(
  ("All Metadata":security) OR
  ("All Metadata":vulnerability) OR
  ("All Metadata":attack) OR
  ("All Metadata":threat) OR
  ("All Metadata":adversarial) OR
  ("All Metadata":"prompt injection") OR
  ("All Metadata":poisoning) OR
  ("All Metadata":backdoor) OR
  ("All Metadata":jailbreak) OR
  ("All Metadata":misuse) OR
  ("All Metadata":harm) OR
  ("All Metadata":privacy) OR
  ("All Metadata":compromise)
)
```

### IEEE-QD

```text
(
  ("All Metadata":"AI agent") OR
  ("All Metadata":"LLM agent") OR
  ("All Metadata":"large language model agent") OR
  ("All Metadata":"language model agent") OR
  ("All Metadata":"agentic AI") OR
  ("All Metadata":"tool-using agent") OR
  ("All Metadata":"autonomous agent")
)
AND
(
  ("All Metadata":defense) OR
  ("All Metadata":safeguard) OR
  ("All Metadata":monitoring) OR
  ("All Metadata":detection) OR
  ("All Metadata":authorization) OR
  ("All Metadata":authentication) OR
  ("All Metadata":"access control") OR
  ("All Metadata":privilege) OR
  ("All Metadata":provenance) OR
  ("All Metadata":forensics) OR
  ("All Metadata":audit) OR
  ("All Metadata":containment) OR
  ("All Metadata":recovery) OR
  ("All Metadata":rollback) OR
  ("All Metadata":isolation) OR
  ("All Metadata":sandbox)
)
```

Command Search 실행 후 publication year 2022–2026, content type Journals와 Conferences를 적용합니다. IEEE 공식 도움말은 Command Search가 자유 형식 Boolean query, proximity operator와 clause당 최대 25개 검색어를 지원한다고 설명합니다.

## 실행 및 변경 규칙

1. 각 식을 별도 search run ID로 실행합니다.
2. 실제 입력한 query, UI filter, 검색일, 결과 수와 export 파일을 `data/search-log.csv`에 기록합니다.
3. 두 검색군과 세 데이터베이스의 결과를 합친 후 중복 제거합니다.
4. seed 누락이 발생하면 먼저 색인 여부를 제목 검색으로 확인합니다.
5. 검색어 수정 전후의 결과 수와 seed recall 변화를 모두 보존합니다.
6. 실제 검색 이후에는 이 문서를 `executed` 상태로 변경하고 검색식 버전을 고정합니다.
