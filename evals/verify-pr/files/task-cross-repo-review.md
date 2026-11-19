<!-- SYNTHETIC TEST DATA — mock Jira task description for cross-repository review feedback eval testing; names, URLs, and identifiers are fictional -->

# Jira Task: TC-9110

**Key**: TC-9110
**Summary**: Stabilize advisory table ordering
**Status**: In Review
**Labels**: ai-generated-jira
**PR URL**: https://github.com/trustify/trustify-ui/pull/1450
**Web URL**: https://redhat.atlassian.net/browse/TC-9110
**Parent Feature**: TC-9009

---

## Repository
trustify-ui

## Target Branch
main

## Description
Advisory rows in the advisory table must render in a stable order so screenshots and exports are reproducible. The rows currently arrive in arbitrary order and the table sorts them in memory before rendering.

## Files to Modify
- `src/pages/advisories/AdvisoryTable.tsx` — sort advisory rows in memory by advisory date, tiebreaking on advisory ID
- `src/api/advisories.ts` — no change; fetched rows are passed straight to the table

## Files to Create
- `src/pages/advisories/__tests__/AdvisoryTable.sorting.test.tsx` — component test for the in-memory sort

## Implementation Notes
- Sort by `advisory.date` descending, tiebreaking on `advisory.id`, inside a `useMemo` so the work is not repeated on every render
- Keep the existing `AdvisoryTable` props unchanged so no call site changes are needed
- Follow the component test pattern in `src/pages/advisories/__tests__/AdvisoryTable.test.tsx`

## Acceptance Criteria
- [ ] Advisory rows render with the newest advisory date first
- [ ] Rows sharing a date are ordered by advisory ID
- [ ] The in-memory sort is covered by a component test

## Test Requirements
- [ ] Component test feeds an out-of-order API payload and asserts the rendered row order
- [ ] Component test covers the equal-date tiebreaker on advisory ID
