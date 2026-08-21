# 자료 관리 정책

## 저장 원칙

- 논문: DOI/arXiv/출판사 링크, 서지정보, 자체 요약, 재현 상태 저장
- 뉴스: 제목·발행일·매체·공식 URL과 짧은 자체 요약만 저장
- White paper: 발행기관·버전·날짜·URL·주장과 한계를 기록
- 코드·데이터: 공식 repository/release/DOI와 확인한 commit 또는 version 기록
- PDF: 재배포 허가가 명확한 경우에만 저장

## Evidence status

- `author-claimed`: 저자 또는 제공기관의 주장
- `artifact-checked`: 공개 코드·데이터 구조 확인
- `reproduced`: 동일 또는 명시된 변형 환경에서 재실행
- `independently-verified`: 독립 데이터·구현으로 핵심 결론 확인

## 최소 메타데이터

`id, title, type, year, authors/organization, url, doi, topics, research_role, evidence_status, reproduction_status, added_at, summary, limitations`

## 변경 관리

자료 추가·수정은 출처 링크와 검증 상태를 포함해야 합니다. 미검증 주장과 향후 조사 항목은 사실처럼 서술하지 않고 명시적으로 대기열에 둡니다.
