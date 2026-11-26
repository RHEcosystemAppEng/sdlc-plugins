# Task 7 — Add "Compare selected" action to the SBOM list page

**Summary:** Add two-SBOM checkbox selection and "Compare selected" action on the SBOM list page
**Epic:** TC-9003: SBOM comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003; fixVersion scope = both)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Implement the entry point described in UC-1 (TC-9003): on the SBOM list page users select two SBOMs with checkboxes and click "Compare selected", which navigates to `/sbom/compare?left={id1}&right={id2}`. This connects the existing list workflow to the new comparison page.

## Files to Modify
- `src/pages/SbomListPage/SbomListPage.tsx` — add row selection checkboxes and a "Compare selected" toolbar button
- `src/pages/SbomListPage/SbomListPage.test.tsx` — add tests for selection and navigation
- `tests/e2e/sbom-list.spec.ts` — add an E2E scenario: select two SBOMs → Compare selected → comparison page loads

## Implementation Notes
- Use PatternFly composable `Table` row selection (`Td select={{ rowIndex, onSelect, isSelected }}`) consistent with the existing table in `SbomListPage.tsx`.
- "Compare selected" button is enabled only when exactly two SBOMs are selected; with more than two selected it stays disabled with a tooltip ("Select exactly two SBOMs to compare").
- Ordering: `left` = the first selected SBOM, `right` = the second (document this in the tooltip/help text). If SBOM ingestion dates are available on `SbomSummary` (`src/api/models.ts`), prefer older = left, newer = right so "added" means "added in the newer version" — confirm with the field list in `models.ts`.
- Navigate with React Router `useNavigate()` to `/sbom/compare?left=<id1>&right=<id2>` (use `createSearchParams` to build the query string). Do not use `window.location`.
- Place the button in the existing toolbar (`src/components/FilterToolbar.tsx` is used by the list page) without disrupting existing filters.
- Selection state is local UI state (`useState`); it is not server state and must not be stored in React Query.

**Conventions:**
- Per CONVENTIONS.md §Component library: use PatternFly 5 table selection and `Button`/`Tooltip`. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's UI component (`.tsx`) scope.
- Per CONVENTIONS.md §Routing: navigation via React Router v6. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's React Router page scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests, Playwright for E2E. Applies: task modifies `tests/e2e/sbom-list.spec.ts` matching the convention's Playwright E2E scope. Example: existing scenarios in `tests/e2e/sbom-list.spec.ts`.

**Project constraints (docs/constraints.md):**
- §2 Commit rules: Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5 Code change rules: scope to listed files; preserve existing list-page behavior (filters, delete via `useDeleteSbomMutation`); doc comments on every test.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — existing table and toolbar to extend
- `src/components/FilterToolbar.tsx` — existing toolbar where the action button is added
- `tests/e2e/sbom-list.spec.ts` — existing Playwright setup for the list page

## Acceptance Criteria
- [ ] Each SBOM row on the list page has a selection checkbox
- [ ] "Compare selected" is disabled with 0, 1, or more than 2 selections and enabled with exactly 2
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left=<id1>&right=<id2>` with the selected IDs
- [ ] Existing list page functionality (filtering, deletion) is unchanged

## Test Requirements
- [ ] Unit test: button disabled/enabled states for 0, 1, 2, and 3 selections
- [ ] Unit test: clicking the button navigates to the compare route with both IDs in the query string
- [ ] E2E test: select two SBOMs, click "Compare selected", comparison page renders with both selectors pre-populated
- [ ] Regression: existing `SbomListPage.test.tsx` and `sbom-list.spec.ts` tests still pass

## Verification Commands
- `npx vitest run src/pages/SbomListPage` — tests pass
- `npx playwright test tests/e2e/sbom-list.spec.ts` — E2E tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Add SBOM comparison page with selectors, URL state, empty and loading states
