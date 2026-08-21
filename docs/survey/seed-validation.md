# Seed-paper 회수 검증

Seed set은 최종 포함 문헌 목록이 아니라 검색식의 알려진 관련 연구 회수 능력을 검사하는 도구입니다. 공격, 방어, benchmark, memory·skill, authorization, MCP, runtime observability와 provenance를 의도적으로 분산해 선정했습니다.

## 이중 검증 절차

각 데이터베이스와 seed study 조합에 대해 다음 두 단계를 수행합니다.

1. **Index presence:** 정확한 제목 또는 DOI/arXiv ID로 검색하여 해당 데이터베이스에 색인되어 있는지 확인
2. **Query retrieval:** 색인된 연구가 Q-A 또는 Q-D 결과에 포함되는지 확인

색인되지 않은 연구는 검색식의 false negative로 계산하지 않습니다. 색인되어 있으나 Q-A와 Q-D 모두 회수하지 못한 경우에만 검색어와 field restriction을 검토합니다.

## 성공 기준

- 전체 recall: 색인 확인된 seed study 중 90% 이상 회수
- 영역별 최소 조건: 각 보안 영역에서 색인 확인된 seed가 하나 이상이면 최소 하나 회수
- 특정 제목만 맞추는 과적합 금지
- 검색식 변경 시 기존·변경 버전의 recall과 결과 수를 모두 기록

## 기록 파일

- Seed 메타데이터: `data/seed-studies.yaml`
- 데이터베이스별 검증 결과: `data/seed-recall.csv`
- 실제 검색 실행: `data/search-log.csv`

현재 검증 상태는 `pending`입니다. Scopus, Web of Science와 IEEE Xplore의 기관 접근이 가능한 환경에서 검증 값을 채웁니다.
