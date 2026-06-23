## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add unit tests and E2E tests for the SBOM comparison page. Unit tests cover component rendering (empty state, loading state, diff sections, critical vulnerability highlighting) using Vitest and React Testing Library with MSW for API mocking. E2E tests cover the full comparison workflow using Playwright.

## Files to Create
- `src/pages/SbomComparePage/SbomComparePage.test.tsx` -- Unit tests for the comparison page component
- `tests/mocks/fixtures/sbom-comparison.json` -- Mock comparison API response fixture
- `tests/e2e/sbom-compare.spec.ts` -- Playwright E2E test for the comparison workflow

## Files to Modify
- `tests/mocks/handlers.ts` -- Add MSW request handler for `GET /api/v2/sbom/compare`

## Implementation Notes
- Follow the existing test patterns in `src/pages/SbomListPage/SbomListPage.test.tsx` for unit tests: render the component, interact with elements, assert on rendered output.
- Use MSW handlers from `tests/mocks/handlers.ts` for API mocking per project conventions.
- The mock fixture in `tests/mocks/fixtures/sbom-comparison.json` should include data for all six diff categories to ensure full test coverage.
- For E2E tests, follow the pattern in `tests/e2e/sbom-list.spec.ts`: navigate to the page, interact with UI elements, assert on visible content.
- Use React Testing Library queries (e.g., `getByText`, `getByRole`) per PatternFly component accessibility attributes.

## Reuse Candidates
- `tests/setup.ts` -- Test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` -- Existing MSW handler patterns; follow the same structure for the comparison endpoint handler
- `tests/mocks/fixtures/sboms.json` -- Existing mock SBOM data; reference for SBOM list fixture format used by selector dropdowns
- `tests/e2e/sbom-list.spec.ts` -- Existing Playwright E2E test pattern

## Acceptance Criteria
- [ ] Unit tests pass for: empty state rendering, loading state rendering, diff section rendering with mock data, critical vulnerability row highlighting
- [ ] MSW handler correctly intercepts comparison API calls and returns fixture data
- [ ] E2E test completes the full comparison workflow: select two SBOMs, click Compare, verify diff sections appear
- [ ] All tests pass in CI

## Test Requirements
- [ ] Unit test: page renders empty state with CodeBranchIcon when no query params
- [ ] Unit test: page shows Skeleton loading state while API call is in progress
- [ ] Unit test: diff sections render with correct titles, badge counts, and table data from mock response
- [ ] Unit test: New Vulnerabilities section highlights Critical severity rows
- [ ] Unit test: sections with 0 items are collapsed by default
- [ ] E2E test: navigate to `/sbom/compare`, select two SBOMs, click Compare, verify Added Packages section appears with expected data
- [ ] E2E test: navigate to `/sbom/compare?left={id1}&right={id2}`, verify comparison loads automatically

## Verification Commands
- `npx vitest run src/pages/SbomComparePage/` -- unit tests pass
- `npx playwright test tests/e2e/sbom-compare.spec.ts` -- E2E tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 6 -- SBOM comparison page with diff sections

[sdlc-workflow] Description digest: sha256-md:57efc2efca2a7440fb6c57d964bdc5f27f79c8ae8ec99741854089868486e696
