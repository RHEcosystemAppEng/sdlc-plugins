## Repository
trustify-ui

## Target Branch
main

## Description
Register the SBOM comparison page route and integrate a "Compare selected" action into the existing SBOM list page. This task connects the comparison page to the application's routing and provides the primary entry point for users to initiate comparisons by selecting two SBOMs from the list.

## Files to Modify
- `src/routes.tsx` — Add lazy-loaded route for `/sbom/compare` pointing to `SbomComparePage`
- `src/pages/SbomListPage/SbomListPage.tsx` — Add row selection checkboxes and a "Compare selected" toolbar action button

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data for MSW handlers
- `tests/mocks/handlers.ts` — Add MSW handler for `GET /api/v2/sbom/compare` (modify existing file if it already contains handlers)
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the comparison workflow

## Implementation Notes
**Route registration (src/routes.tsx):**
Follow the existing lazy-loading pattern in `src/routes.tsx`. Add a route entry for path `/sbom/compare` that lazy-loads `SbomComparePage` from `src/pages/SbomComparePage/SbomComparePage.tsx`.

**SBOM list page integration (src/pages/SbomListPage/SbomListPage.tsx):**
- Add PatternFly `Table` row selection using the composable table's `select` feature to enable checkboxes on each SBOM row.
- Add a PatternFly `Button` labeled "Compare selected" to the page's `FilterToolbar` area (reference the existing `FilterToolbar` component at `src/components/FilterToolbar.tsx` for toolbar layout patterns).
- The button is disabled unless exactly two SBOMs are selected.
- On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.
- Selection state is managed with local React state (`useState`).

**Mock data (tests/mocks/fixtures/sbom-comparison.json):**
Create a fixture with representative data for all six diff categories, including at least one Critical severity vulnerability for testing highlighted row rendering.

**E2E test (tests/e2e/sbom-compare.spec.ts):**
Follow the pattern in `tests/e2e/sbom-list.spec.ts`. Test the full workflow: navigate to SBOM list, select two SBOMs, click Compare, verify comparison page loads with diff sections.

## Reuse Candidates
- `src/routes.tsx` — Existing route definitions for lazy-loading pattern
- `src/components/FilterToolbar.tsx` — Toolbar layout pattern for action buttons
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing table implementation to extend with selection
- `tests/e2e/sbom-list.spec.ts` — E2E test pattern reference
- `tests/mocks/handlers.ts` — MSW handler registration pattern

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered and loads the comparison page
- [ ] SBOM list page has row selection checkboxes
- [ ] "Compare selected" button appears in the SBOM list toolbar
- [ ] Button is disabled unless exactly two SBOMs are selected
- [ ] Clicking the button navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] URL with query params loads the comparison page with pre-populated selectors
- [ ] MSW mock handler exists for the comparison endpoint
- [ ] E2E test covers the select-and-compare workflow

## Test Requirements
- [ ] Unit test: "Compare selected" button is disabled with 0 or 1 selections
- [ ] Unit test: "Compare selected" button is enabled with exactly 2 selections
- [ ] Unit test: clicking the button navigates to the correct comparison URL
- [ ] E2E test: full workflow from SBOM list selection to comparison page rendering

## Verification Commands
- `npx tsc --noEmit` — TypeScript compilation succeeds
- `npx vitest run --reporter=verbose -- SbomListPage` — list page tests pass
- `npx playwright test sbom-compare` — E2E tests pass

## Dependencies
- Depends on: Task 5 — Frontend SBOM comparison page with diff section components
