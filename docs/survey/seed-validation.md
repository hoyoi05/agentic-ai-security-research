# Seed-paper 회수 검증

Seed set은 최종 포함 문헌 목록이 아니라 검색 전략의 알려진 관련 연구 회수 능력을 검사하는 도구입니다. 공격, 방어, benchmark, memory·skill, identity·authorization, delegation, MCP, runtime observability, provenance와 Agent forensics를 분산해 선정합니다.

## 검색원별 검증

각 검색원과 seed 조합에 대해 다음을 분리합니다.

1. **Index presence:** 정확한 제목, DOI 또는 arXiv ID로 레코드가 존재하는가?
2. **Query retrieval:** Q-A 또는 Q-D 실행 결과에 포함되는가?
3. **Metadata verification:** 저자, 연도, identifier와 publication status가 권위 있는 원본과 일치하는가?

색인되지 않은 seed는 query false negative로 계산하지 않습니다. 색인되었으나 어떤 query에서도 회수되지 않을 때만 검색어, field, date filter 또는 검색원 coverage를 검토합니다.

## 검색원 역할

| 검색원 | Seed index 확인 | Query recall | Metadata 검증 |
|---|---:|---:|---:|
| OpenAlex | 예 | 핵심 | 보조 |
| arXiv | arXiv 자료 | 핵심 | arXiv ID·version |
| Semantic Scholar | 예 | 보조 | 보조 |
| Crossref | DOI 자료 | 해당 없음 | DOI·출판정보 |
| DBLP | CS 출판 자료 | targeted only | conference·journal |
| 공식 출판 페이지 | 해당 없음 | 해당 없음 | 최종 확인 |

Crossref와 DBLP를 OpenAlex·arXiv와 동일한 recall denominator로 합치지 않습니다. 각 검색원의 의도된 역할에 따라 index와 retrieval을 해석합니다.

## 잠정 성공 기준

- 핵심 discovery source에서 색인 확인된 seed의 90% 이상을 Q-A 또는 Q-D가 회수
- 각 주요 보안 영역에서 색인 seed가 하나 이상이면 최소 하나 회수
- identity·lifecycle·delegation·provenance·forensics seed가 개별적으로 점검됨
- 특정 논문 제목에만 맞춘 과적합 용어를 추가하지 않음
- 검색식 변경 전후 recall, precision pilot과 결과 수를 모두 기록

90%는 protocol tuning을 위한 잠정 기준이며 최종 연구 품질을 자동 보장하지 않습니다. 검색원 coverage의 차이와 seed 선정 편향을 제한사항으로 보고합니다.

## 기록 파일

- Seed 메타데이터: data/seed-studies.yaml
- 검색원별 검증: data/seed-recall.csv
- 실제 검색 실행: data/search-log.csv

## 실행 순서

1. 모든 seed의 identifier와 제목을 공식 원본에서 확인
2. OpenAlex, arXiv와 Semantic Scholar에서 exact-title index 확인
3. query manifest pilot 실행
4. source별 retrieved_by_qa와 retrieved_by_qd 기록
5. 누락 원인을 index, query, date, type, metadata 또는 API failure로 분류
6. 일반화 가능한 query 변경만 제안
7. 변경 전후 seed recall과 pilot noise 비교
8. v1.1 query를 고정하거나 protocol deviation 기록

현재 상태는 pending입니다. 구독 데이터베이스 계정은 실행 조건이 아닙니다.
