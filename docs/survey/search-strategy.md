# 공개 검색원별 검색 전략

> 버전: 1.1-draft  
> 작성일: 2026-08-21  
> 실제 검색 결과 수: 미기록  
> 상태: query manifest pilot 실행 전

## 원칙

구독 계정이 필요한 Scopus, Web of Science와 IEEE Xplore는 현재 실행 검색원에서 제외합니다. 공개 API의 검색 문법과 coverage가 서로 다르므로 공통 개념 사전을 유지하면서 검색원별 query를 실행하고 합집합을 구성합니다.

이 문서의 query는 실행 전 초안입니다. 실제 요청 URL, parameter, API 응답 시각, paging 상태와 결과 checksum을 검색 로그에 보존합니다.

## 공통 개념 사전

### Agent 표현

- "AI agent"
- "LLM agent"
- "large language model agent"
- "language model agent"
- "agentic AI"
- "tool-using agent"
- "autonomous agent"

전통적 multi-agent system의 대량 유입을 줄이기 위해 독립된 "multi-agent system"은 초기 Agent 표현에서 제외합니다. LLM 또는 agentic 표현이 함께 나타나는 multi-agent 연구와 snowballing 결과는 포함 가능합니다.

### Q-A — Threats and failures

security, attack, vulnerability, threat, adversarial, prompt injection, poisoning, backdoor, jailbreak, misuse, compromise, privacy

### Q-D — Controls and operations

security, defense, authentication, authorization, identity, credential, access control, privilege, delegation, provenance, observability, monitoring, audit, forensic, containment, recovery, rollback, sandbox

## Query manifest

공개 검색원에서 하나의 거대한 Boolean query에 의존하지 않습니다. 각 Agent 표현에 다음 두 suffix를 결합한 14개 검색 실행을 기본 manifest로 사용합니다.

- QA suffix: security attack vulnerability threat poisoning "prompt injection"
- QD suffix: security defense authorization authentication delegation provenance forensic monitoring

예:

- "AI agent" security attack vulnerability threat poisoning "prompt injection"
- "AI agent" security defense authorization authentication delegation provenance forensic monitoring
- "LLM agent" security attack vulnerability threat poisoning "prompt injection"
- "LLM agent" security defense authorization authentication delegation provenance forensic monitoring

실제 URL encoding 전의 raw query와 encoding 후 요청 URL을 모두 기록합니다. 검색원이 따옴표나 Boolean 의미를 동일하게 처리한다고 가정하지 않습니다.

## OpenAlex

### 역할

- 핵심 metadata discovery
- publication year와 type 기반 필터
- DOI, OpenAlex ID와 citation graph 획득
- seed index presence 확인

### 요청 형태

    GET https://api.openalex.org/works
      ?search=<RAW_QUERY>
      &filter=from_publication_date:2022-01-01,to_publication_date:<SEARCH_DATE>
      &cursor=*
      &per-page=<PAGE_SIZE>

OpenAlex 검색의 ranking을 Boolean 완전 일치로 해석하지 않습니다. 14개 manifest query를 각각 실행하고 모든 cursor page를 수집한 뒤, 포함·제외 기준은 별도 screening에서 적용합니다.

기록 필드:

- raw query와 encoded URL
- API access mode와 version 또는 문서 확인일
- search date와 date filter
- cursor page 수와 total result count
- work ID, DOI, title, abstract availability, year, type
- referenced and citing work identifiers
- raw response checksum

공식 API 문서는 [OpenAlex Help Center](https://help.openalex.org/)에서 확인합니다.

## arXiv API

### 역할

- 최신 Agentic AI security preprint 발견
- 제목·초록 Boolean query
- arXiv ID와 version metadata 확인

### Q-A

    (
      all:"AI agent" OR all:"LLM agent" OR
      all:"large language model agent" OR all:"language model agent" OR
      all:"agentic AI" OR all:"tool-using agent" OR all:"autonomous agent"
    )
    AND
    (
      all:security OR all:attack OR all:vulnerability OR all:threat OR
      all:adversarial OR all:"prompt injection" OR all:poisoning OR
      all:backdoor OR all:jailbreak OR all:misuse OR all:compromise OR all:privacy
    )

### Q-D

    (
      all:"AI agent" OR all:"LLM agent" OR
      all:"large language model agent" OR all:"language model agent" OR
      all:"agentic AI" OR all:"tool-using agent" OR all:"autonomous agent"
    )
    AND
    (
      all:security OR all:defense OR all:authentication OR all:authorization OR
      all:identity OR all:credential OR all:"access control" OR all:privilege OR
      all:delegation OR all:provenance OR all:observability OR all:monitoring OR
      all:audit OR all:forensic OR all:containment OR all:recovery OR
      all:rollback OR all:sandbox
    )

요청은 https://export.arxiv.org/api/query 의 search_query, start, max_results, sortBy와 sortOrder를 기록합니다. 결과는 Atom feed로 저장합니다. 연도 범위는 반환된 submitted date로 재확인하며 2022년 이전 자료는 직접 선행연구일 때 snowballing 후보로 분리합니다.

공식 [arXiv API User's Manual](https://info.arxiv.org/help/api/user-manual.html)의 paging과 요청 간격 지침을 따릅니다.

## Semantic Scholar Academic Graph API

### 역할

- OpenAlex·arXiv 결과의 보조 발견
- seed paper identifier 확인
- reference와 citation expansion
- title·abstract·venue metadata 보완

/graph/v1/paper/search/bulk 또는 실행 시점에 공식 문서가 권고하는 bulk search endpoint를 사용합니다. 14개 query manifest를 동일하게 기록하되 검색 문법이 다른 검색원과 동일한 recall을 보장한다고 가정하지 않습니다.

공식 [Semantic Scholar API documentation](https://api.semanticscholar.org/api-docs/)에서 endpoint, field, paging, rate limit과 인증 요구를 실행 당일 확인합니다.

## Crossref REST API

### 역할

Crossref는 복합 보안 검색의 핵심 recall source가 아니라 DOI와 출판 메타데이터 정규화에 사용합니다.

- DOI 직접 조회: /works/{doi}
- 제목·저자 확인: /works?query.bibliographic=<citation>
- 날짜 검증: filter=from-pub-date:<date>,until-pub-date:<date>

Crossref query 결과를 Boolean 완전 일치로 해석하지 않습니다. 공식 문서는 공개 REST API가 search, filter와 JSON metadata retrieval을 지원한다고 설명합니다.

- [Crossref REST API](https://www.crossref.org/documentation/retrieve-metadata/rest-api/)
- [Crossref filters](https://www.crossref.org/documentation/retrieve-metadata/rest-api/rest-api-filters/)

## DBLP

### 역할

- 컴퓨터과학 publication record 확인
- conference·journal venue와 final title 검증
- preprint와 정식 출판본 연결 후보 발견

Publication Search API:

    GET https://dblp.org/search/publ/api
      ?q=<TITLE_OR_QUERY>
      &format=json
      &h=<HITS>
      &f=<OFFSET>
      &c=0

DBLP 공식 문서는 q, format, 최대 hit 수 h, offset f를 설명하며 결과 수 제한을 명시합니다. 따라서 DBLP는 전체 recall source보다 publication verification과 targeted search에 사용합니다.

공식 문서: [DBLP Search API](https://dblp.org/faq/How+to+use+the+dblp+search+API.html)

## 공식 표준 및 정부 자료

NIST, IETF, W3C 등은 site-restricted targeted search와 공식 목록을 사용합니다. 각 자료에는 다음을 기록합니다.

- issuing organization
- document identifier와 version
- publication 또는 update date
- status: final, draft, concept paper 등
- superseded 또는 expired 여부
- official URL

표준·정부 자료는 peer-reviewed 학술 논문과 별도 분석합니다.

## Snowballing

포함 후보의 reference와 citation을 이용합니다.

- backward: 참고문헌에서 직접 선행연구 확인
- forward: OpenAlex 또는 Semantic Scholar citation graph로 후속 연구 확인
- verification: 발견 레코드를 Crossref, DBLP, arXiv 또는 공식 출판 페이지에서 확인

각 snowballing round, parent study와 발견 수를 기록하고 새로운 포함 후보가 없을 때 종료합니다.

## 실행 순서

1. seed exact-title search로 각 검색원의 index presence 확인
2. OpenAlex 14개 manifest query pilot
3. arXiv Q-A와 Q-D pilot
4. Semantic Scholar 보조 query와 citation expansion
5. DOI·publication status를 Crossref와 DBLP에서 정규화
6. 합집합 구성과 study-family 중복 제거
7. 제목·초록 pilot screening
8. seed recall과 noise를 검토하여 query v1.1 고정 또는 변경
9. full retrieval
10. backward·forward snowballing

## 검색 변경 규칙

- 특정 seed 제목에만 나타나는 고유 단어 추가 금지
- 개념 사전 변경 전후 query version, 결과 수와 recall 보존
- API 정책·문법 변경은 protocol deviation으로 기록
- 검색 오류와 rate-limit 재시도도 search log에 기록
- raw export는 수정하지 않고 정규화 결과를 별도 파일로 생성
