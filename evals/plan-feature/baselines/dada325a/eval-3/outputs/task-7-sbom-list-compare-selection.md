# Task 7 — Add "Compare selected" multi-select to the SBOM list page

**Summary:** Add checkbox selection and "Compare selected" action to SbomListPage
**Epic:** TC-9003: SBOM comparison UI

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the UC-1 entry point to the comparison view. Users select two SBOMs on the SBOM list page with checkboxes and click "Compare selected". The click navigates to `/sbom/compare?left={id1}&right={id2}`, and the comparison loads immediately.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and a "Compare selected" toolbar button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — add tests for selection and navigation

## Files to Create
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the full UC-1/UC-2 flow: list → select two → compare → URL reload shows the same comparison

## Implementation Notes
- Use PF5 composable `Table` row selection (`Td select={{ rowIndex, onSelect, isSelected }}`) in the existing list table. Keep the selection in local component state as a list of SBOM IDs. Selection is UI state, so it does not belong in React Query.
- Add a "Compare selected" `Button` (secondary) in the existing filter toolbar, `src/components/FilterToolbar.tsx`, or next to it in the page toolbar. Enable it only when exactly two SBOMs are selected. Explain with a tooltip when 0, 1, or more than 2 are selected.
- On click, navigate with React Router `useNavigate()` to `/sbom/compare?left={first}&right={second}`. Order the pair by selection order (first selected = left) and document this in the tooltip or help text. If `SbomSummary` exposes an ingestion or creation date, ordering older → left is a reasonable alternative; pick one and test it.
- Do not change the existing delete mutation behavior (`src/hooks/useDeleteSbomMutation.ts`). If row selection interacts with bulk actions, keep the delete flow on its `onSuccess` + `invalidateQueries` pattern.

**Conventions:**
- Per CONVENTIONS.md §Component library: use PF5 table row selection and `Button`. Do not use custom checkbox markup.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Routing: navigate with React Router v6 `useNavigate`, never `window.location`.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React Router navigation scope.
- Per CONVENTIONS.md §Testing: unit tests with Vitest + RTL (MSW for the list); E2E with Playwright, following `tests/e2e/sbom-list.spec.ts`.
  Applies: task modifies `tests/e2e/sbom-compare.spec.ts` matching the convention's Playwright E2E (`tests/e2e/`) scope.

**Project constraints (docs/constraints.md):**
- §2: Conventional Commits, `Implements TC-XXXX` footer, `Assisted-by:` trailer.
- §3: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5: Change only the listed files; leave existing list filtering, pagination, and delete behavior unchanged.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table and toolbar to extend.
- `src/components/FilterToolbar.tsx` — reusable toolbar where the action button can sit.
- `tests/e2e/sbom-list.spec.ts` — existing Playwright patterns for the SBOM list.

## Acceptance Criteria
- [ ] Each SBOM row on the list page has a selection checkbox
- [ ] "Compare selected" is enabled only when exactly two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` with the selected IDs in the documented order
- [ ] Existing list filtering, pagination, and deletion keep working

## Test Requirements
- [ ] Unit test: the button is disabled with 0, 1, or 3 selections and enabled with 2
- [ ] Unit test: clicking the button navigates to the expected URL with both IDs
- [ ] E2E test: select two SBOMs → click Compare selected → the comparison page shows diff sections; reloading the URL shows the same comparison (UC-2)

## Verification Commands
- `npx vitest run src/pages/SbomListPage` — tests pass
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — E2E passes against a running dev stack

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, and empty/loading states
- Depends on: Task 6 — Render the six collapsible diff sections (the E2E test asserts the diff sections)
