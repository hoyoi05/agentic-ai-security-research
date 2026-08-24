# OpenAlex·arXiv 전수 회수와 중복 제거

> 상태: 자동 회수 워크플로 준비  
> 검색식: OpenAlex v1.3.1, arXiv v1.2 고정본

## 목적

Seed recall 검증을 통과한 공개 검색식을 전체 결과 집합에 실행하고, 제목·초록 스크리닝에 투입할 고유 연구 단위의 목록을 생성합니다. Seed 회수율은 검색식 보정 지표일 뿐 완전성의 증거가 아니므로 전수 회수, 중복 제거와 tail-inclusive 스크리닝을 별도 수행합니다.

## 실행 단위

- OpenAlex: Agent 표현 9개와 공격·위험군(Q-A), 방어·통제군(Q-D)의 18개 query manifest를 cursor pagination으로 끝까지 회수
- arXiv: Q-A와 Q-D를 각각 500건 단위로 pagination
- source 내부에서 동일 OpenAlex Work ID 또는 version을 제거한 arXiv ID를 통합
- 각 레코드에 회수 query ID를 누적해 검색 provenance를 보존
- 요청 시각, HTTP 상태, 응답 크기와 SHA-256을 별도 로그로 기록

API key는 Authorization header에만 사용하며 요청 URL, 로그와 산출물에 기록하지 않습니다.

## 중복 제거 규칙

중복 연결은 다음 식별자를 순서대로 적용합니다.

1. 정규화한 DOI
2. version suffix를 제거한 arXiv ID
3. 정확히 정규화한 제목과 출판연도의 조합

DOI와 arXiv ID는 source 간 연결 식별자로 사용합니다. 제목·연도만으로 연결되었거나 강한 식별자가 없는 레코드는 `manual_dedup_review=true`로 표시하며 자동 확정하지 않습니다. 유사 제목 fuzzy matching과 preprint-출판본의 추정 병합은 이 단계에서 수행하지 않습니다.

## 산출물

GitHub Actions 실행 artifact에는 다음 파일이 포함됩니다.

- `retrieval-summary.json`: query별 원시 결과 수, source별 고유 레코드 수와 중복 제거 후 연구 수
- `source-records.jsonl.gz`: source 단위 정규화 메타데이터와 회수 provenance
- `deduplicated-screening-set.csv`: 제목·초록 스크리닝 입력과 빈 판정 필드
- `request-log.csv`: 재현성과 API 실패 확인용 요청 로그

원시 query 결과 수의 합은 중복 제거 전 수치이므로 고유 문헌 수로 해석하지 않습니다.

## 후속 품질 게이트

1. 모든 요청의 성공 여부와 pagination 완결성 확인
2. title-year 중복군 전수 수동 검토
3. DOI·arXiv 식별자 충돌과 study-family 관계 검토
4. 기존 61건 파일럿 판정을 고유 연구 목록에 이식
5. 전체 title/abstract 스크리닝과 제외 사유 기록
6. backward·forward snowballing 및 공개 보조 검색원으로 coverage 보완

## 제한사항

- OpenAlex와 arXiv의 색인 범위, 메타데이터 품질과 갱신 시점에 영향을 받습니다.
- 구독 데이터베이스를 실행하지 못한 제한은 유지되며 검색 완전성을 주장하지 않습니다.
- 정확 제목·연도 규칙은 보수적이지만 동명이문헌 충돌과 제목이 변경된 버전의 미병합 가능성이 있습니다.
- 자동 생성 목록은 연구자 검토 전 최종 포함 문헌이나 확정 중복군이 아닙니다.
