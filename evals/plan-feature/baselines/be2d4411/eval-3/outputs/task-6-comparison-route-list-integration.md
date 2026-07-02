## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the `/sbom/compare` route to the application router with lazy loading, update the SBOM list page to support multi-row selection with a "Compare selected" toolbar action, add MSW mock handlers for the comparison endpoint, and add a Playwright E2E test covering the full comparison workflow from SBOM selection to diff rendering.

## Files to Modify
- `src/routes.tsx` — Add /sbom/compare route definition with lazy-loaded SbomComparePage
- `src/pages/SbomListPage/SbomListPage.tsx` — Add multi-row selection checkboxes and "Compare selected" toolbar action button
- `tests/mocks/handlers.ts` — Add MSW request handler for GET /api/v2/sbom/compare

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — Mock comparison response data for MSW handlers and tests
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E test for the full comparison workflow

## Implementation Notes
- **Route registration in `src/routes.tsx`:**
  - Add `{ path: "/sbom/compare", element: lazy(() => import("./pages/SbomComparePage/SbomComparePage")) }` following the pattern of existing lazy-loaded routes in the file.
  - URL supports query params: `/sbom/compare?left={id1}&right={id2}` for shareable comparison links per UC-2.

- **SbomListPage multi-select updates in `src/pages/SbomListPage/SbomListPage.tsx`:**
  - Add row selection checkboxes using PatternFly Table's `isSelectable` prop.
  - Add a "Compare selected" button in the toolbar (PatternFly `Button` with `variant="primary"`).
  - Button is enabled only when exactly 2 rows are selected; disabled otherwise.
  - On click, navigate to `/sbom/compare?left=${selectedIds[0]}&right=${selectedIds[1]}` using React Router `useNavigate()`.
  - Maintain selected row state using React `useState<string[]>([])`.

- **MSW handler in `tests/mocks/handlers.ts`:**
  - Add `rest.get("/api/v2/sbom/compare", (req, res, ctx) => ...)` handler that reads `left` and `right` query params and returns the mock fixture from `sbom-comparison.json`.
  - Follow the pattern of existing handlers in the file.

- **E2E test in `tests/e2e/sbom-compare.spec.ts`:**
  - Follow the pattern in `tests/e2e/sbom-list.spec.ts` for Playwright test structure.
  - Test flow: navigate to SBOM list, select 2 SBOMs via checkboxes, click "Compare selected", verify navigation to /sbom/compare, verify diff sections render with expected data.
  - Second test: navigate directly to /sbom/compare?left={id1}&right={id2}, verify comparison loads from URL params.

**Convention references:**
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's routing configuration scope.
- Per CONVENTIONS.md §Testing: Playwright for E2E tests; MSW for API mocking.
  Applies: task creates `tests/e2e/sbom-compare.spec.ts` matching the convention's E2E test scope.

## Reuse Candidates
- `src/routes.tsx` — existing lazy-loaded route definitions as pattern for the new route
- `tests/mocks/handlers.ts` — existing MSW handler patterns to follow for the comparison endpoint mock
- `tests/e2e/sbom-list.spec.ts` — existing Playwright E2E test structure to follow for comparison workflow test
- `tests/mocks/fixtures/sboms.json` — existing mock fixture format to reference for comparison fixture structure

## Acceptance Criteria
- [ ] `/sbom/compare` route is registered and lazy-loads SbomComparePage
- [ ] Direct navigation to `/sbom/compare?left={id1}&right={id2}` loads the comparison page with pre-populated selectors
- [ ] SbomListPage displays row selection checkboxes
- [ ] "Compare selected" button appears in toolbar and is enabled only when exactly 2 rows are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` with the selected SBOM IDs
- [ ] MSW handler returns mock comparison data for the comparison endpoint
- [ ] E2E test passes: selection, navigation, and diff rendering work end-to-end

## Test Requirements
- [ ] E2E test: select 2 SBOMs on list page, click "Compare selected", verify comparison page renders with diff sections
- [ ] E2E test: navigate directly to /sbom/compare?left={id}&right={id}, verify comparison loads from URL
- [ ] Unit test: SbomListPage "Compare selected" button is disabled when fewer or more than 2 rows are selected
- [ ] Unit test: SbomListPage "Compare selected" button navigates to correct URL with selected IDs

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 5 — Create SBOM comparison page with diff section components

[sdlc-workflow] Description digest: sha256-md:07dad466c165d0f038de0e07174a87f103a40057aa6f8a517be71ab32e2269ec
