# Task 7 — Add "Compare selected" multi-select to SBOM list page

**Summary:** Add row checkboxes and a "Compare selected" action on the SBOM list page that navigates to /sbom/compare
**Epic:** TC-9003: Comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the entry point to the comparison flow, steps 1–3 of TC-9003 UC-1. On the SBOM list page, the user selects two SBOMs with row checkboxes and clicks "Compare selected", which navigates to `/sbom/compare?left={id1}&right={id2}`. This task also adds an end-to-end Playwright test that covers the full flow from list to comparison.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and a "Compare selected" toolbar button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — tests for selection and navigation

## Files to Create
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test: select two SBOMs on the list page → Compare selected → comparison view renders the sections; then reload the URL directly and assert that the same view loads (UC-2)

## Implementation Notes
- **Selection.** Use PF5 composable `Table` row selection (`Td select={{ rowIndex, onSelect, isSelected }}`) on the existing table in `SbomListPage.tsx`. Keep the selected IDs in local state, in selection order.
- **Button rules.**
  - Enable "Compare selected" only when exactly two SBOMs are selected.
  - With more than two selected, keep the button disabled and show a tooltip: "Select exactly two SBOMs to compare".
- **Left/right assignment.** The first selected SBOM becomes `left` (baseline) and the second becomes `right`. Alternatively, order by ingestion or creation date (older = left) if `SbomSummary` exposes a date. Pick one rule, state it in the PR, and test it.
- **Navigation.** Use React Router `useNavigate()` to go to `/sbom/compare?left=<id1>&right=<id2>`, building the query with `URLSearchParams`. Do not use `window.location`.
- **Toolbar placement.** Add the button to the existing `FilterToolbar` (`src/components/FilterToolbar.tsx`) as a toolbar item, if it supports extra items. Otherwise place it in a `ToolbarItem` next to it. Do not fork `FilterToolbar`.
- Per CONVENTIONS.md §Component library: use PF5 `Table` selection and `Button`/`Tooltip`; no custom checkbox components.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Testing: unit tests with Vitest + React Testing Library + MSW, and E2E with Playwright under `tests/e2e/`. See `tests/e2e/sbom-list.spec.ts` for the established E2E pattern.
  Applies: task creates `tests/e2e/sbom-compare.spec.ts` matching the convention's Playwright E2E scope.
- Per CONVENTIONS.md §Routing: navigate with React Router v6 APIs, so the lazy-loaded `/sbom/compare` route from Task 5 is used.
  Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React Router navigation scope.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits format, a `Implements TC-<task-key>` footer, and an `Assisted-by:` trailer.
  - §3 PR rules: use `--base TC-9003` and post the PR link on the Jira task.
  - §5 Code change rules: stay within the listed files; inspect before modifying.
  - §1.4/§1.5: no unrelated refactoring.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing SBOM table; extend it in place with row selection
- `src/components/FilterToolbar.tsx` — existing toolbar; host the "Compare selected" action here
- `tests/e2e/sbom-list.spec.ts` — existing Playwright test for the list page; reuse its navigation and fixture setup

## Acceptance Criteria
- [ ] Each SBOM row on the list page has a selection checkbox
- [ ] "Compare selected" is enabled only when exactly two SBOMs are selected
- [ ] Clicking it navigates to `/sbom/compare?left={firstId}&right={secondId}` following the documented ordering rule
- [ ] Existing list page behaviour (filters, deletion, pagination) is unchanged
- [ ] The E2E flow from list to comparison passes, and reloading the comparison URL shows the same view

## Test Requirements
- [ ] Unit test: selecting one SBOM → button disabled; two → enabled; three → disabled with a tooltip
- [ ] Unit test: clicking "Compare selected" calls navigate with the expected URL and ordering
- [ ] Existing `SbomListPage.test.tsx` tests still pass
- [ ] E2E test (`tests/e2e/sbom-compare.spec.ts`): select two SBOMs → Compare selected → the six section titles are visible; open the copied URL in a new page → the same sections are visible

## Verification Commands
- `npx vitest run src/pages/SbomListPage` — all tests pass
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — the E2E test passes against a running dev stack

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add /sbom/compare page with SBOM selectors, Compare button, URL-shareable state, empty and loading states
- Depends on: Task 6 — Add six collapsible diff sections (needed for the E2E assertions)
