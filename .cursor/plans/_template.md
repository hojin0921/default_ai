# Plan: <!-- 짧은 제목 -->

## Goal

<!-- 무엇을 달성하는가 -->

## Scope

- In:
- Out:

## Task Size

Small | Medium | **Large**

## Must-have Features

<!-- 사용자가 꼭 넣겠다고 한 기능. Phase에 모두 매핑한다. -->

| Feature | Phase | Notes |
|---------|-------|-------|
| | | |

## Delivery Phases

<!--
Phase 0(bootstrap)과 별개. 제품 개발은 Phase 1부터.
각 Phase 진행 시 6단계(순서 고정):
1 Explore → 2 Document → 3 Plan(상세·승인) → 4 Implement → 5 Verify(+User Test Guide) → 6 Review → Human Verify
-->

### Phase 1 — <!-- 제목 -->

- Goal:
- In / Out:
- 6-step status:
  - [ ] 1 Explore
  - [ ] 2 Document
  - [ ] 3 Plan (상세) → Human approve
  - [ ] 4 Implement
  - [ ] 5 Verify (AI + User Test Guide)
  - [ ] 6 Review → Human Verify
- Docs to update:
- Changes (files):
- AI Verify:
- User Test Guide:
  - Setup / Run:
  - Check:
  - Expected:
  - If fails, report:
- Human Verify: [ ] 통과 (다음 Phase 전 필수)

### Phase 2 — <!-- 제목 -->

- Goal:
- In / Out:
- 6-step status:
  - [ ] 1 Explore
  - [ ] 2 Document (변경분만)
  - [ ] 3 Plan (상세) → Human approve
  - [ ] 4 Implement
  - [ ] 5 Verify (AI + User Test Guide)
  - [ ] 6 Review → Human Verify
- Docs to update:
- Changes (files):
- AI Verify:
- User Test Guide:
  - Setup / Run:
  - Check:
  - Expected:
  - If fails, report:
- Human Verify: [ ] 통과 (다음 Phase 전 필수)

<!-- 필요 시 Phase N 추가 -->

## Changes (전체 요약)

| File | Change | Why | Phase |
|------|--------|-----|-------|
| | | | |

## Steps

1. 전체 Plan 승인
2. Phase 1: Explore → Document → Plan → (승인) Implement → Verify → Review → 사람 검수
3. 승인 후 Phase 2도 동일 6단계 …
4. 전체 마무리 Review

## Verification

- [ ] Phase마다 6단계 완료
- [ ] 관련 테스트 / typecheck / lint / build (해당 시)
- [ ] User Test Guide 제공 (Phase마다)
- [ ] docs 갱신 (Phase 2 Document)

## Risks

<!-- 보안, 데이터, 호환성, 되돌리기 어려움 -->

## Human Review

- [ ] 요구사항·범위·Must-have ↔ Phase 매핑 확인
- [ ] 아키텍처/보안/데이터 영향 수용
- [ ] 전체 Plan 승인 (Approved 전에 Agent는 Phase 구현 금지)
- [ ] 각 Phase: 상세 Plan 승인 + Human Verify (다음 Phase 전)

## Status

Draft | **Approved** | In Progress (Phase N · step K/6) | Done

<!-- 강제 검사 진실 원천은 Status가 아니라 .cursor/gate.json (채팅 선택→./scripts/gate.sh) -->
