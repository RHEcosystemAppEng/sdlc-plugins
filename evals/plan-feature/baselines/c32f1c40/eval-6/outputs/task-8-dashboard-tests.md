## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add comprehensive unit tests and E2E tests for the remediation dashboard page, including MSW mock handlers for the remediation API endpoints, mock fixture data, and a Playwright E2E test covering the full user journey (view summary, apply filters, navigate pagination).

## Files to Create
- `tests/mocks/fixtures/remediation-summary.json` -- mock remediation summary data with entries across all severity/status combinations
- `tests/mocks/fixtures/remediation-by-product.json` -- mock per-product remediation data with pagination
- `src/pages/RemediationDashboard/RemediationDashboard.test.tsx` -- unit tests for the RemediationDashboard page component
- `tests/e2e/remediation-dashboard.spec.ts` -- Playwright E2E test for the remediation dashboard user journey

## Files to Modify
- `tests/mocks/handlers.ts` -- add MSW request handlers for GET /api/v2/remediation/summary and GET /api/v2/remediation/by-product

## Implementation Notes
- Per frontend conventions: Vitest + React Testing Library for unit tests, Playwright for E2E, MSW for API mocking. Follow the patterns in existing test files.
- Per frontend conventions: test setup uses MSW handlers defined in `tests/mocks/handlers.ts` and render helpers from `tests/setup.ts`. Follow the same setup pattern.
- For MSW handlers, mock both remediation endpoints returning the fixture data. Include handlers for filtered requests (with query parameters) to test the filtering behavior.
- Unit tests should verify: summary cards render with correct counts, progress chart renders, filter toolbar appears, table renders with data, loading states display correctly, empty states display correctly.
- E2E test should cover UC-1 (navigate to /remediation, verify summary cards and table) and UC-2 (apply product filter, verify table updates). Follow the pattern in `tests/e2e/sbom-list.spec.ts`.
- Mock fixture data should include: multiple severity levels (Critical, High, Medium, Low), multiple statuses (Open, In Progress, Resolved), multiple products, and enough entries to test pagination.
- Constraints: per docs/constraints.md section 2, commit messages must follow Conventional Commits format and reference TC-9006. Per section 5, changes must be scoped to the files listed.

## Reuse Candidates
- `tests/setup.ts` -- test setup with MSW handlers and render helpers. Reuse for remediation test setup.
- `tests/mocks/handlers.ts` -- existing MSW request handlers. Extend with remediation handlers following the same pattern.
- `tests/mocks/fixtures/sboms.json` -- mock SBOM data fixture. Reference for fixture data structure.
- `tests/mocks/fixtures/advisories.json` -- mock advisory data fixture. Reference for fixture data structure.
- `tests/e2e/sbom-list.spec.ts` -- Playwright E2E test. Follow the same E2E test pattern for remediation dashboard.
- `src/pages/SbomListPage/SbomListPage.test.tsx` -- SBOM list page tests. Reference for unit test patterns with data tables.

## Acceptance Criteria
- [ ] MSW mock handlers are added for both remediation API endpoints
- [ ] Mock fixture data files exist with representative remediation data
- [ ] Unit tests verify summary cards render with correct counts
- [ ] Unit tests verify progress chart renders
- [ ] Unit tests verify vulnerability table renders with data
- [ ] Unit tests verify filter interactions update the table
- [ ] Unit tests verify loading and empty states
- [ ] E2E test covers navigation to /remediation and verifying page content
- [ ] E2E test covers applying a product filter and verifying table updates
- [ ] All tests pass

## Test Requirements
- [ ] Verify summary cards display correct open, in-progress, and resolved counts from mock data
- [ ] Verify progress chart renders without errors
- [ ] Verify vulnerability table displays mock data with correct columns
- [ ] Verify severity filter narrows table results in E2E test
- [ ] Verify product filter narrows table results in E2E test
- [ ] Verify pagination works with mock data exceeding page size

## Verification Commands
- `npx vitest run --reporter=verbose -- RemediationDashboard` -- unit tests pass
- `npx playwright test remediation-dashboard` -- E2E test passes

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 6 -- Create remediation dashboard page with summary cards and progress chart
- Depends on: Task 7 -- Add filterable vulnerability table to remediation dashboard
