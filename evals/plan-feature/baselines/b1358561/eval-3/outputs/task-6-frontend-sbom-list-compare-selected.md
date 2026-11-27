# Task 6 — Add "Compare selected" action to the SBOM list page

**Summary:** TC-9003: Add SBOM multi-select and "Compare selected" action to SBOM list
**Issue type:** Task
**Parent (Epic):** Epic 2 — TC-9003: SBOM comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
main

## Description
Implement the entry point of UC-1 (TC-9003): on the SBOM list page users select two SBOMs
with checkboxes and click "Compare selected", which navigates to
`/sbom/compare?left={id1}&right={id2}`. The comparison page itself is Task 4/5.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row-selection checkboxes and a "Compare selected" toolbar button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — tests for selection and navigation
- `tests/e2e/sbom-list.spec.ts` — E2E flow: select two SBOMs → Compare selected → comparison page loads

## Implementation Notes
- Use PatternFly composable `Table` row selection (`Td select={{ rowIndex, onSelect, isSelected }}`) consistent with how the table in `SbomListPage.tsx` is already built.
- Place the "Compare selected" `Button` (variant secondary) in the existing list toolbar (`src/components/FilterToolbar.tsx` usage on this page). Enabled only when exactly two SBOMs are selected; tooltip "Select exactly two SBOMs to compare" otherwise.
- Ordering: `left` = the older SBOM, `right` = the newer SBOM (by the published/ingested date shown in the list, formatted via `src/utils/formatDate.ts`) so "added"/"new" semantics read as "what changed in the newer version". If dates are equal, use selection order.
- Navigate with React Router `useNavigate()` to `/sbom/compare?left=${left}&right=${right}` — no full page reload.
- Selection state is local to the page; clear it on filter/page change to avoid selecting invisible rows.
- Per CONVENTIONS.md §Component library: use PF5 table selection and `Button`, no custom checkboxes.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React `.tsx` component scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests, Playwright for E2E; extend `tests/e2e/sbom-list.spec.ts`.
  Applies: task modifies `tests/e2e/sbom-list.spec.ts` matching the convention's Playwright E2E `.ts` scope.
- Constraints (docs/constraints.md): §5.1 scope; §5.8 parity with existing list toolbar actions; §2.1–2.3 commit rules; §3.3 PR `--base main`.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table and filters
- `src/components/FilterToolbar.tsx` — existing toolbar to host the action button
- `src/utils/formatDate.ts` — date handling for left/right ordering

## Acceptance Criteria
- [ ] Each SBOM row on the list page has a selection checkbox
- [ ] "Compare selected" is disabled unless exactly two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={olderId}&right={newerId}`
- [ ] Existing list filtering and pagination behavior is unchanged

## Test Requirements
- [ ] Unit test: button disabled with 0, 1 and 3 selections; enabled with 2
- [ ] Unit test: clicking the button navigates to the expected URL with older SBOM as `left`
- [ ] E2E test: select two SBOMs, click "Compare selected", comparison page shows diff sections

## Verification Commands
- `npm run test -- SbomListPage` — tests pass
- `npx playwright test tests/e2e/sbom-list.spec.ts` — E2E passes

## Dependencies
- Depends on: Task 4 — Add /sbom/compare page with SBOM selectors and URL-shareable state
