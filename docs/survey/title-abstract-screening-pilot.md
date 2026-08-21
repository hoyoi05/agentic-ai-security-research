# 제목·초록 파일럿 스크리닝 결과

> 실행일: 2026-08-21  
> 상태: 1차 보조 판정 완료, 연구자 검토 필요  
> 범위: arXiv query v1.2의 relevance 상위 결과와 seed calibration set

## 목적

전체 검색 전에 포함·제외 기준의 해석을 보정하고 검색 결과의 초기 noise를 확인합니다. 이 파일럿은 최종 전수 스크리닝이나 전체 검색 정밀도를 대체하지 않습니다.

## 표본 구성

- Q-A 전체 결과 수: 2,525
- Q-D 전체 결과 수: 5,162
- 각 검색군에서 arXiv relevance 상위 25건 회수
- 두 검색군 중복 제거 후 비-seed 표본: 43편
- seed calibration set: 18편
- 총 판정 문헌: 61편

상위 결과만 사용했으므로 아래 포함률은 `precision@25 union` 성격의 지표이며 전체 결과 집합으로 일반화하지 않습니다.

## 판정 기준

- `include`: LLM·AI Agent가 핵심 대상이며 보안, 프라이버시, 권한, 위임, provenance, audit 또는 forensics 문제를 제목·초록에서 명시
- `exclude`: 포함 기준을 충족하지 않으며 하나의 주 제외 사유를 기록
- `uncertain`: 제목·초록만으로 Agent 핵심성 또는 보안 관련성을 확정할 수 없어 전문 검토로 전달

### 제외·보류 코드

| 코드 | 의미 |
|---|---|
| `E02-ai-for-security` | Agent를 보안 업무에 사용하지만 Agent 자체의 보안 문제는 다루지 않음 |
| `E03-no-security-focus` | Agent 연구이지만 보안·프라이버시 문제가 핵심이 아님 |
| `U01-agent-boundary` | LLM 통합 애플리케이션과 Agent의 경계가 초록만으로 불명확 |

## 결과

| 표본 | Include | Exclude | Uncertain | 합계 |
|---|---:|---:|---:|---:|
| Seed calibration | 16 | 1 | 1 | 18 |
| Relevance top-25 union | 41 | 2 | 0 | 43 |
| 전체 파일럿 | 57 | 3 | 1 | 61 |

비-seed 표본의 잠정 포함률은 41/43, 약 95.3%입니다. 이는 relevance 상위 결과에만 적용되며 전체 7,687개 query-result count의 precision 추정치가 아닙니다. Q-A와 Q-D 사이 중복 및 전체 결과 내부 중복을 제거하기 전의 합산 결과 수도 고유 문헌 수로 해석하지 않습니다.

## 제외·보류 문헌

| arXiv ID | 판정 | 사유 |
|---|---|---|
| 2302.12173 | uncertain | LLM-integrated application과 API 효과는 다루지만 Agent가 핵심 연구 대상인지 전문 확인 필요 |
| 2605.23904 | exclude | Self-evolving skill 최적화 연구이며 초록에 보안·프라이버시 문제가 없음 |
| 2601.07880 | exclude | Agent를 identity-security 분석에 사용하는 AI-for-security 연구 |
| 2605.21404 | exclude | Agent benchmark의 보고 완전성 audit이며 Agent 보안 문제를 평가하지 않음 |

## 연구 무결성 상태

현재 판정은 제목·초록에 기반한 보조 1차 판정입니다. 최종 SMS에는 다음 품질 절차가 필요합니다.

1. 연구자가 61편의 판정을 확인하고 변경 내역 기록
2. `uncertain` 1편의 전문 검토
3. 경계 사례를 screening decision log에 추가
4. 전체 검색 후 중복 제거된 고유 문헌에 동일 기준 적용
5. 일정 표본의 재판정 또는 공동 검토로 agreement 확인

## 재현 파일

- `scripts/fetch-arxiv-screening-pilot.py`: 표본 회수
- `data/screening-pilot-decisions-2026-08-21.csv`: 판정과 제목·초록
- `data/screening-pilot-summary-2026-08-21.json`: 집계 결과

## 제한사항

- OpenAlex 재실행은 API key가 없는 실행 환경의 HTTP 429로 완료하지 못했습니다.
- arXiv relevance 상위 표본은 tail noise를 반영하지 않습니다.
- 단일 보조 판정이므로 사람 검토 전 최종 포함 문헌으로 간주하지 않습니다.
- arXiv 최신 문헌의 peer-review 상태와 서지 메타데이터는 후속 정규화가 필요합니다.
