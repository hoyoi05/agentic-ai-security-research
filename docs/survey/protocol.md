# 체계적 매핑 연구 프로토콜

> 프로토콜 버전: 1.3.1-pilot  
> 기준일: 2026-08-21  
> 상태: arXiv·OpenAlex seed-recall pilot 완료  
> 변경 사유: Scopus, Web of Science와 IEEE Xplore 구독 접근 부재

## 1. 프로토콜 관리

검색 실행 전에 연구 질문, 범위, 포함·제외 기준, 검색원 역할과 필수 코딩 필드를 고정합니다. 변경은 기존 기록을 삭제하지 않고 날짜, 사유, 영향받는 검색 실행과 문헌 집합을 decision log에 기록합니다.

## 2. 검색원

### 핵심 공개 검색원

- **OpenAlex:** 광범위한 학술 메타데이터 발견과 citation graph 확장
- **arXiv API:** 최신 preprint의 제목·초록 검색
- **Semantic Scholar Academic Graph API:** 보조 발견, seed 확인과 citation expansion

### 메타데이터 검증 및 정규화

- **Crossref REST API:** DOI, 출판 메타데이터와 publication type 정규화
- **DBLP publication search API:** 컴퓨터과학 conference·journal 출판 레코드 확인
- **출판사 또는 학회 공식 페이지:** 최종 publication status와 서지사항 확인

### 표준·정부 자료

NIST, IETF, W3C와 기타 공식 표준기관 문서는 학술 문헌과 별도 evidence type으로 관리합니다. IETF Internet-Draft는 표준으로 표현하지 않으며 버전과 만료 상태를 기록합니다.

### 보충 검색

- 포함 연구의 backward·forward snowballing
- 공식 conference·journal 페이지의 누락 확인
- Google Scholar의 보충 발견

Google Scholar는 결과 순위와 전체 결과 집합의 재현이 제한되므로 핵심 검색원이나 PRISMA의 독립 데이터베이스로 사용하지 않습니다. 발견된 레코드에는 supplementary discovery 경로를 기록합니다.

## 3. 검색 전략

검색은 다음 두 개념군의 합집합입니다.

- **Q-A — Threats and failures:** 공격, 취약점, poisoning, misuse와 보안 실패
- **Q-D — Controls and operations:** 방어, identity, authorization, delegation, provenance, observability, forensics, containment와 recovery

각 공개 검색원의 실제 문법이 다르므로 동일한 Boolean 문자열을 강제로 적용하지 않습니다. 공통 개념 사전과 검색군은 유지하되, 검색원별로 지원되는 query와 filter를 사용합니다.

구체적인 endpoint, query manifest, paging과 export 규칙은 [공개 검색원 전략](search-strategy.md)에 기록합니다.

## 4. Seed 검증

각 seed와 검색원 조합에 대해 구분하여 기록합니다.

1. **Index presence:** 식별자 또는 정확한 제목으로 레코드가 존재하는가?
2. **Query retrieval:** Q-A 또는 Q-D query가 해당 레코드를 회수하는가?
3. **Metadata verification:** DOI, arXiv ID, 저자, 연도와 publication status를 권위 있는 원본에서 확인했는가?

색인되지 않은 seed는 query false negative로 계산하지 않습니다. API 실패와 rate limit은 false가 아니라 `unknown` 또는 `not_tested`로 기록합니다. Seed는 보안 query 회수가 기대되는 `core-security`와 경계 검증용 `contextual`로 구분하며, contextual seed는 query-recall 분모에서 제외합니다. 검색어 수정은 특정 제목에만 맞춘 용어가 아니라 누락된 일반 개념을 보완할 때만 허용합니다.

## 5. 포함 기준

다음을 모두 만족하는 자료를 포함합니다.

1. Agentic AI 또는 LLM 기반 Agent가 핵심 연구 대상이다.
2. 보안·프라이버시 문제, 공격, 방어, 평가 또는 보안 운영을 명시적으로 다룬다.
3. Agent의 자율적 의사결정, 상태, 도구, 권한, 위임 또는 실제 시스템 효과 중 하나 이상을 분석한다.
4. 제목과 초록 또는 전문을 확인할 수 있다.
5. 중복 출판인 경우 가장 완전한 버전을 대표 레코드로 선택할 수 있다.

## 6. 제외 기준

- Agent 행동이나 시스템 효과와 연결되지 않은 일반 LLM jailbreak·prompt injection
- LLM 기반 Agentic AI와 직접 연결되지 않은 전통적 MAS 보안
- 보안 주장 없이 성능·정확도·효율만 평가
- 초록, 발표 슬라이드 또는 홍보문만 존재하여 연구 방법을 판단할 수 없음
- 영어 또는 한국어 이외의 자료로서 신뢰할 수 있는 전문 검토가 불가능함
- 철회되었거나 출처·저자를 확인할 수 없음

제외 시 최초로 적용한 하나의 주 제외 사유를 기록합니다.

## 7. 중복 제거와 study family

1. DOI 소문자화와 URL prefix 제거 후 완전 일치
2. arXiv ID, 표준 문서 번호 또는 공식 URL 일치
3. 정규화 제목과 제1저자·연도 비교
4. preprint, conference와 journal 확장본 연결
5. 유사 레코드 수동 검토

preprint와 peer-reviewed 버전은 하나의 study family로 연결합니다. publication status, version date, artifact와 결과 차이는 보존하며, peer-reviewed 상태를 자동 추론하지 않습니다.

## 8. 스크리닝

### 1단계: 제목·초록

포함, 제외, 불확실로 판정합니다. 불확실은 전문 단계로 전달합니다.

### 2단계: 전문

모든 포함·제외 기준을 다시 적용하고 표준화된 제외 사유를 기록합니다.

### 품질 관리

- 기준 변경 시 이미 검토한 레코드에 소급 적용
- 경계 사례를 decision log에 기록
- 단일 검토자는 무작위 표본을 일정 기간 후 재판정하여 intra-rater consistency 확인
- 공동 검토자는 중복 표본의 agreement와 불일치 기록

## 9. 데이터 추출

- 서지사항, 식별자, publication status와 발견 경로
- 연구 역할과 보안 수명주기
- 공격자, 보호 자산, 공격 표면과 신뢰 경계
- Agent 아키텍처, 모델, 도구, 프로토콜과 배포 환경
- identity, credential, delegation과 authorization
- 공격·방어 방법과 실제 시스템 효과
- logging, tracing, provenance와 forensic evidence
- 데이터셋, benchmark, baseline, 지표와 반복 수
- 코드·데이터·trace 공개 여부
- evidence status와 reproduction status
- 한계, validity threat와 연구 갭 후보

## 10. 분석

- 연도·publication type·연구 역할별 분포
- 보안 영역 × 시스템 계층 evidence map
- 공격 수명주기 × 방어 수명주기 coverage
- identity·lifecycle·delegation·provenance·forensics coverage
- 평가 환경·데이터셋·지표 분포
- 아티팩트 공개와 재현 상태
- 연구 밀도, 실증 성숙도와 재현성을 결합한 gap matrix
- RQ7 후보의 신규성, 실험 가능성, 역량 적합성과 예상 기여

연구 수가 적다는 사실만으로 연구 갭을 확정하지 않습니다.

## 11. 보고

검색·중복 제거·스크리닝 흐름은 PRISMA 형태로 보고합니다. 최종 보고에는 다음을 포함합니다.

- 검색원과 접근 방식
- 검색일과 실제 raw query·filter
- API endpoint, paging, cursor와 결과 수
- export 파일의 checksum
- 검색원별·검색군별 결과와 중복 수
- 단계별 제외 수와 제외 사유
- seed index presence와 query recall
- 검색원 coverage와 metadata limitation

구독 데이터베이스를 실행하지 않았다는 사실은 제한사항으로 명시하며, 실행하지 않은 검색 결과 수를 추정하거나 보고하지 않습니다.

## 12. 현재 실행 단계

OpenAlex v1.3.1과 arXiv v1.2 검색식을 고정하고 전수 pagination, source 내부 정규화, source 간 식별자 기반 중복 제거를 자동화했습니다. 실행 규칙, 산출물과 검토 게이트는 [OpenAlex·arXiv 전수 회수와 중복 제거](full-retrieval.md)에 기록합니다. 자동 생성된 중복군과 스크리닝 입력은 연구자 검토 전 확정 자료로 간주하지 않습니다.
