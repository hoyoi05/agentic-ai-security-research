# OpenAlex 인증 Seed-recall 파일럿 결과

> 실행일: 2026-08-21  
> 최종 query version: 1.3.1-pilot  
> 상태: seed-recall 잠정 기준 통과

## 실행 개요

GitHub Actions repository secret `OPENALEX_API_KEY`를 사용해 OpenAlex API key를 `Authorization: Bearer` 헤더로 전달했습니다. 키는 URL, 로그와 산출물에 기록하지 않았습니다. 요청은 직렬 실행하고 최소 0.35초 간격과 HTTP 429 backoff를 적용했습니다.

최종 실행은 OpenAlex 342건과 arXiv 3건, 총 345건의 요청으로 구성되며 모두 HTTP 200을 반환했습니다.

## Query 변경과 검증

### v1.2

초기 OpenAlex query는 Agent 표현 뒤에 보안 용어를 공백으로 나열했습니다.

```text
"AI agent" security attack vulnerability threat poisoning "prompt injection"
```

OpenAlex는 Boolean 연산자 없이 인접한 단어를 `AND`로 처리합니다. 따라서 위 query는 모든 보안 용어를 동시에 요구하는 과도하게 엄격한 검색이었습니다.

- OpenAlex index presence: 16/18
- 전체 indexed seed query recall: 4/16, 25.0%
- core-security indexed seed query recall: 3/14, 21.4%
- Q-D retrieval: 0/16

### v1.3

특정 seed 제목에 맞춘 용어를 추가하지 않고, 기존 개념 사전에 명시적 Boolean 구조를 적용했습니다.

```text
"AI agent" AND (security OR attack OR vulnerability OR threat OR ...)
```

- OpenAlex index presence: 16/18
- indexed seed query recall: 16/16, 100%

### v1.3.1

두 arXiv record의 최신 version에서 제목이 변경된 사실을 반영했습니다.

- arXiv:2504.11703 → `Progent: Securing AI Agents with Privilege Control`
- arXiv:2606.04990 → `From Agent Traces to Trust: A Survey of Evidence Tracing and Execution Provenance in LLM Agents`

최신 제목으로 exact-title index 검증을 반복한 최종 결과는 다음과 같습니다.

| 검색원 | Index presence | Q-A | Q-D | Union recall |
|---|---:|---:|---:|---:|
| OpenAlex v1.3.1 | 18/18 | 15/18 | 18/18 | 18/18, 100% |
| arXiv v1.2 | 18/18 | 14/18 | 16/18 | 16/18, 88.9% |

Seed 역할을 적용하면 다음과 같습니다.

- OpenAlex core-security: 16/16, 100%
- OpenAlex contextual: 2/2
- arXiv core-security: 16/16, 100%
- arXiv contextual: 0/2

두 핵심 공개 discovery source 모두 core-security seed에 대한 잠정 90% 기준을 통과했습니다.

## 해석

- OpenAlex API 접근 문제는 API key 기반 인증으로 해결되었습니다.
- v1.2의 낮은 recall은 검색원 coverage가 아니라 Boolean query 표현 오류가 주원인이었습니다.
- v1.3.1은 seed recall 기준을 통과했지만, 이것이 full retrieval의 precision이나 전체 문헌 coverage를 자동 보장하지 않습니다.
- Q-D가 OpenAlex seed 전체를 회수하므로 full retrieval에서 noise가 클 수 있습니다. 제목·초록 screening pilot과 full-result 표본으로 precision을 별도 평가해야 합니다.
- OpenAlex에 동일 제목 record가 복수 존재할 수 있으므로 DOI, arXiv ID와 study-family 기준의 중복 제거가 필요합니다.
- arXiv title drift는 versioned seed metadata를 실행 시점에 재검증해야 함을 보여줍니다.

## 재현 산출물

- `data/seed-recall-openalex-v1.3.1-2026-08-21.csv`
- `data/search-log-openalex-v1.3.1-2026-08-21.csv`
- `data/pilot-summary-openalex-v1.3.1-2026-08-21.json`
- workflow run: https://github.com/hoyoi05/agentic-ai-security-research/actions/runs/32463174666

### SHA-256

| 파일 | SHA-256 |
|---|---|
| search log | `4ea00a58711fd1d2b5373246bbf7cc927b525eb7f1d1298bc35517b51804feab` |
| summary | `971355808f0d341e6dc234802d02e7738ea7da477cb717770aaf3ddd896c12e7` |
| seed recall | `7f01f5a1b3657008ce68ee3ad47858f3d6c631aa9ea9979e053f8c9faaa670bc` |

## 다음 protocol 상태

OpenAlex v1.3.1과 arXiv v1.2를 full retrieval 후보 query로 고정할 수 있습니다. 고정 전 마지막 검토 항목은 다음과 같습니다.

1. OpenAlex와 arXiv full-result count 기록
2. source 내부·source 간 DOI/arXiv ID/title 중복 제거
3. relevance 상위뿐 아니라 tail을 포함하는 precision 표본 추출
4. 연구자에 의한 제목·초록 판정 확인
5. query 변경 이력과 title drift를 protocol deviation log에 보존
