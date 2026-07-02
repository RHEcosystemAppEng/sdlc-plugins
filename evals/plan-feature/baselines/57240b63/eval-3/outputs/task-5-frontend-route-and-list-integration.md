## Repository
trustify-ui

## Target Branch
main

## Description
Register the `/sbom/compare` route for the comparison page, add a "Compare selected" action to the SBOM list page enabling users to select two SBOMs via checkboxes and navigate to the comparison view, and add MSW mock handlers and test fixtures for the comparison endpoint to support unit testing.

## Files to Modify
- `src/routes.tsx` -- Add route definition for `/sbom/compare` with lazy-loaded `SbomComparePage`
- `src/pages/SbomListPage/SbomListPage.tsx` -- Add checkbox-based row selection and "Compare selected" toolbar button
- `tests/mocks/handlers.ts` -- Add MSW request handler for `GET /api/v2/sbom/compare`

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- Unit tests for the comparison page component
- `tests/mocks/fixtures/sbom-comparison.json` -- Mock comparison response data with all six diff categories populated

## Implementation Notes
- **Route registration**: Add a new route entry in `src/routes.tsx` for path `/sbom/compare` pointing to a lazy-loaded `SbomComparePage`. Follow the existing pattern in the file -- other pages like `SbomDetailPage` use `React.lazy(() => import("./pages/SbomComparePage/SbomComparePage"))`. Place the `/sbom/compare` route before `/sbom/:id` to ensure the static path matches before the dynamic parameter path.
- **SBOM list page integration (UC-1 flow)**: In `src/pages/SbomListPage/SbomListPage.tsx`, add PatternFly table row checkbox selection. Track selected SBOM IDs in component state (e.g., `useState<string[]>([])`). Add a "Compare selected" PatternFly `Button` to the page toolbar that is enabled only when exactly two SBOMs are selected. On click, navigate to `/sbom/compare?left={selectedIds[0]}&right={selectedIds[1]}` using React Router's `useNavigate` hook.
- **MSW handler**: Add a handler in `tests/mocks/handlers.ts` for `rest.get("/api/v2/sbom/compare", ...)` that returns the fixture data from `tests/mocks/fixtures/sbom-comparison.json`. Follow the existing handler patterns in the file (e.g., the handler for `/api/v2/sbom`).
- **Test fixture**: Create `tests/mocks/fixtures/sbom-comparison.json` with representative data covering all six diff categories. Include: at least 2 added packages, 2 removed packages, 1 version change (upgrade), 1 version change (downgrade), 1 Critical severity new vulnerability, 1 High severity new vulnerability, 1 resolved vulnerability, and 1 license change. This ensures all table columns and conditional rendering (Critical row highlighting) can be tested.
- **Unit tests**: Write tests in `src/pages/SbomComparePage/SbomComparePage.test.tsx` using Vitest + React Testing Library following the pattern in `src/pages/SbomListPage/SbomListPage.test.tsx`. Use `tests/setup.ts` for test setup and MSW handlers for API mocking. Test both the comparison page rendering and the list page "Compare selected" interaction.
- Per CONVENTIONS.md section Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` route definition scope.
- Per CONVENTIONS.md section Testing: Vitest + React Testing Library for unit tests; MSW for API mocking.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` test scope.
- Per CONVENTIONS.md section Naming: PascalCase for components, camelCase for hooks and utilities, kebab-case for directories.
  Applies: task creates `src/pages/SbomComparePage/SbomComparePage.test.tsx` matching the convention's `.tsx` component naming scope.

## Reuse Candidates
- `src/routes.tsx` -- Existing route definitions with `React.lazy()` pattern; follow for comparison page route
- `tests/mocks/handlers.ts` -- Existing MSW request handlers for other endpoints; follow pattern for comparison handler
- `tests/mocks/fixtures/sboms.json` -- Existing mock SBOM data; reference for SBOM ID format and data structure consistency
- `tests/mocks/fixtures/advisories.json` -- Existing mock advisory data; reference for advisory ID and severity formats
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- Existing list page tests; follow setup, render, and assertion patterns
- `tests/setup.ts` -- Test setup with MSW server initialization and render helpers; import in test files

## Acceptance Criteria
- [ ] Route `/sbom/compare` is registered in `src/routes.tsx` and navigable
- [ ] `SbomComparePage` is lazy-loaded (code-split) via `React.lazy()`
- [ ] `/sbom/compare` route is defined before `/sbom/:id` to prevent dynamic parameter matching conflicts
- [ ] SBOM list page displays checkboxes for each SBOM row
- [ ] "Compare selected" button appears in the SBOM list page toolbar
- [ ] "Compare selected" button is enabled only when exactly two SBOMs are selected
- [ ] Clicking "Compare selected" navigates to `/sbom/compare?left={id1}&right={id2}` with the correct SBOM IDs
- [ ] MSW mock handler responds to `GET /api/v2/sbom/compare` requests with fixture data
- [ ] All unit tests pass

## Test Requirements
- [ ] Unit test: comparison page renders all six diff sections with correct data from MSW mock handler
- [ ] Unit test: comparison page renders empty state when no query params are present
- [ ] Unit test: "Compare selected" button on SBOM list page is disabled when fewer than two SBOMs are selected
- [ ] Unit test: "Compare selected" button on SBOM list page is disabled when more than two SBOMs are selected
- [ ] Unit test: clicking "Compare selected" navigates to the comparison page URL with correct left and right query parameters
- [ ] Unit test: Critical severity vulnerability rows have visually distinct styling

## Verification Commands
- `npm run test` -- run all unit tests including comparison page and list page tests
- `npx tsc --noEmit` -- verify TypeScript compilation with no type errors

## Dependencies
- Depends on: Task 4 -- Add SBOM comparison page with diff sections

---
sha256-md:4fe7dd02a4e61ad21e0402e6fac280167628337b470d1b2d284373de77a67f10
