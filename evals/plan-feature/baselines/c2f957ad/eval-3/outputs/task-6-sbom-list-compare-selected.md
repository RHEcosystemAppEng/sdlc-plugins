# Task 6 — Add "Compare selected" action to SBOM list page

**Summary:** Add SBOM multi-select and "Compare selected" action to SbomListPage
**Issue type:** Task | **Parent (Epic):** Epic B — TC-9003: Comparison UI and navigation
**Labels:** ai-generated-jira | **Priority:** Critical | **Fix Versions:** RHTPA 1.5.0

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Provide the UC-1 entry point to the comparison view: on the SBOM list page, users select two SBOMs using row checkboxes and click "Compare selected", which navigates to `/sbom/compare?left={id1}&right={id2}` (the page built in Task 5). The action is enabled only when exactly two SBOMs are selected.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes to the SBOM table and a "Compare selected" toolbar button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — tests for selection and navigation
- `tests/e2e/sbom-list.spec.ts` — E2E: select two SBOMs, click Compare selected, land on the compare page

## Implementation Notes
- Use PF5 composable `Table` row `select` (checkbox) support on the existing SBOM table; keep selection as local React state of selected SBOM ids (ordered by selection time).
- "Compare selected": PF `Button` (secondary) placed in the existing toolbar (`src/components/FilterToolbar.tsx` is the shared toolbar — add the button via its existing extension point/children rather than forking it). Disabled unless exactly 2 rows are selected; tooltip "Select exactly two SBOMs to compare" when disabled.
- Navigation: React Router `useNavigate()` to `/sbom/compare?left=${first}&right=${second}` — first-selected SBOM is `left`, second is `right`. Build the query with `URLSearchParams` so ids are encoded. No API call is made from this page for comparison.
- Selection must survive filtering/pagination re-renders only within the current view; clear selection when the filter changes to avoid comparing hidden rows.
- No backend endpoint is called directly by this task; the list continues to use `GET /api/v2/sbom` via `useSboms` (`{ items: SbomSummary[], total: number }`, trustify-backend `modules/fundamental/src/sbom/endpoints/list.rs`).
- Per CONVENTIONS.md §Component library: use PF5 table row selection and `Button`/`Tooltip`.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React component (`.tsx`) scope.
- Per CONVENTIONS.md §Routing: navigate with React Router v6 `useNavigate` to the lazy-loaded `/sbom/compare` route registered in `src/routes.tsx` (Task 5).
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React Router navigation scope.
- Per CONVENTIONS.md §Shared components: extend `src/components/FilterToolbar.tsx` usage instead of creating a parallel toolbar.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` component scope.
- Per CONVENTIONS.md §Testing: Vitest + RTL with MSW SBOM fixtures (`tests/mocks/fixtures/sboms.json`) for unit tests; extend Playwright `tests/e2e/sbom-list.spec.ts`.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.test.tsx` matching the convention's Vitest/RTL test scope.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.3 `--base TC-9003`; §5.1–5.4 scope and reuse; §5.8 parity with existing list-page toolbar actions.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM table and filters (extend, don't duplicate)
- `src/components/FilterToolbar.tsx` — shared PF toolbar to host the new action
- `src/hooks/useSboms.ts` — SBOM list data (unchanged)
- `tests/mocks/fixtures/sboms.json` — SBOM list fixture for tests

## Acceptance Criteria
- [ ] Each SBOM row has a selection checkbox
- [ ] "Compare selected" is disabled with 0, 1 or 3+ selections and enabled with exactly 2
- [ ] Clicking it navigates to `/sbom/compare?left={firstSelectedId}&right={secondSelectedId}`
- [ ] Existing list, filter and delete behaviour is unchanged
- [ ] Selection clears when filters change

## Test Requirements
- [ ] Unit: button disabled with fewer or more than two selections, enabled with two
- [ ] Unit: clicking navigates to the compare URL with correct `left`/`right` ids
- [ ] Unit: changing the filter clears the selection
- [ ] E2E: select two SBOMs → Compare selected → comparison page URL contains both ids and sections render

## Verification Commands
- `npx vitest run src/pages/SbomListPage` — tests pass
- `npx playwright test tests/e2e/sbom-list.spec.ts` — E2E passes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Build SBOM comparison page at /sbom/compare
