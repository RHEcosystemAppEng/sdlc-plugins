## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Wire up the comparison page route, add a "Compare selected" action to the SBOM list page so users can select two SBOMs and navigate to the comparison view, add MSW mock handlers for testing, and create Playwright E2E tests that exercise the full comparison workflow.

## Files to Modify
- `src/routes.tsx` — add `/sbom/compare` route pointing to lazy-loaded SbomComparePage
- `src/pages/SbomListPage/SbomListPage.tsx` — add checkbox selection column to the SBOM table and a "Compare selected" toolbar button that navigates to `/sbom/compare?left={id1}&right={id2}`
- `tests/mocks/handlers.ts` — add MSW handler for `GET /api/v2/sbom/compare` that returns mock comparison data

## Files to Create
- `tests/mocks/fixtures/sbom-comparison.json` — mock comparison response fixture with representative data across all six diff categories
- `tests/e2e/sbom-compare.spec.ts` — Playwright E2E tests: select two SBOMs from list, click Compare, verify comparison page loads with diff sections; test direct URL navigation with query params

## Implementation Notes
**Figma: SBOM List Selection** — Add a checkbox column to the SBOM list table (PatternFly composable `Table` with `select` variant). Add a "Compare selected" `Button` to the toolbar area, disabled until exactly two SBOMs are checked. On click, navigate to `/sbom/compare?left={id1}&right={id2}` using React Router's `useNavigate`.

Route registration in `routes.tsx` follows the existing lazy-loading pattern:
```typescript
const SbomComparePage = React.lazy(() => import("./pages/SbomComparePage/SbomComparePage"));
// In route config:
{ path: "/sbom/compare", element: <SbomComparePage /> }
```

Ensure the `/sbom/compare` route is defined before `/sbom/:id` to prevent the router from matching "compare" as an ID parameter.

MSW handler in `tests/mocks/handlers.ts` follows the existing handler pattern:
```typescript
rest.get("/api/v2/sbom/compare", (req, res, ctx) => {
  return res(ctx.json(sbomComparisonFixture));
})
```

E2E tests follow the existing pattern in `tests/e2e/sbom-list.spec.ts`.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking. Applies: task creates `tests/e2e/sbom-compare.spec.ts` and modifies `tests/mocks/handlers.ts` matching the convention's `.ts` test scope.

Per CONVENTIONS.md §Component library: use PatternFly 5 components for checkbox selection and toolbar button. Applies: task modifies `src/pages/SbomListPage/SbomListPage.tsx` matching the convention's `.tsx` scope.

## Reuse Candidates
- `src/routes.tsx` — existing route definitions and lazy-loading pattern
- `tests/e2e/sbom-list.spec.ts` — existing E2E test patterns for Playwright
- `tests/mocks/handlers.ts` — existing MSW handler patterns
- `tests/mocks/fixtures/sboms.json` — existing fixture format reference

## Acceptance Criteria
- [ ] `/sbom/compare` route loads SbomComparePage via lazy loading
- [ ] SBOM list page shows checkbox column for row selection
- [ ] "Compare selected" button appears in the SBOM list toolbar
- [ ] "Compare selected" button is disabled until exactly two SBOMs are checked
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}`
- [ ] Direct navigation to `/sbom/compare?left={id1}&right={id2}` loads the comparison view
- [ ] MSW handler returns mock comparison data for unit test environments
- [ ] E2E test covers the full flow: list page selection through comparison result display

## Test Requirements
- [ ] E2E test: navigate to SBOM list, select two SBOMs via checkboxes, click "Compare selected", verify comparison page renders with diff sections
- [ ] E2E test: navigate directly to `/sbom/compare?left={id1}&right={id2}`, verify comparison loads from URL params
- [ ] Unit test: "Compare selected" button is disabled with fewer or more than two SBOMs selected

## Verification Commands
- `npx playwright test tests/e2e/sbom-compare.spec.ts` — run E2E comparison tests
- `npx vitest run src/pages/SbomListPage/SbomListPage.test.tsx` — verify list page selection behavior

## Dependencies
- Depends on: Task 1 — Create feature branch (create-branch bookend)
- Depends on: Task 5 — Frontend comparison page (SbomComparePage must exist for route target)
