# Task 8 — Add MSW mocks, fixtures, and E2E test for remediation dashboard

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add Mock Service Worker (MSW) request handlers and fixture data for the remediation endpoints, and add a Playwright E2E test verifying the remediation dashboard page loads correctly with mock data. This completes the frontend testing infrastructure for the remediation feature.

## Files to Create
- `tests/mocks/fixtures/remediation-summary.json` — Mock fixture data for the remediation summary endpoint response
- `tests/mocks/fixtures/remediation-by-product.json` — Mock fixture data for the remediation by-product endpoint response
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E test for the remediation dashboard page

## Files to Modify
- `tests/mocks/handlers.ts` — Add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
- Follow the MSW handler pattern in `tests/mocks/handlers.ts` for defining request handlers: use `rest.get()` with the endpoint path and return the fixture data.
- Model fixture data after the backend response shapes defined in Task 6's TypeScript interfaces. The summary fixture should include realistic counts across all severity levels and statuses. The by-product fixture should include multiple products with varying remediation counts.
- Follow the fixture pattern in `tests/mocks/fixtures/sboms.json` and `tests/mocks/fixtures/advisories.json` for data structure and naming.
- For the Playwright E2E test, follow the pattern in `tests/e2e/sbom-list.spec.ts`: navigate to the page, wait for data to load, assert on key UI elements (summary cards, chart, table).
- Per Key Conventions (Testing): Vitest + React Testing Library for unit tests; Playwright for E2E; MSW for API mocking.
  Applies: task creates `tests/e2e/remediation-dashboard.spec.ts` matching the convention's `.ts` test file scope.

## Reuse Candidates
- `tests/mocks/handlers.ts` — Existing MSW request handlers pattern to follow
- `tests/mocks/fixtures/sboms.json` — Mock SBOM data fixture format reference
- `tests/mocks/fixtures/advisories.json` — Mock advisory data fixture format reference
- `tests/e2e/sbom-list.spec.ts` — Playwright E2E test pattern for page-level testing

## Acceptance Criteria
- [ ] MSW handlers intercept `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product` requests and return fixture data
- [ ] Fixture data matches the TypeScript interface shapes defined in Task 6
- [ ] Playwright E2E test navigates to `/remediation` and verifies summary cards, chart, and table render correctly
- [ ] MSW handlers are registered in the existing handler setup so unit tests can use them

## Test Requirements
- [ ] E2E test: verify remediation dashboard page loads and displays summary cards with data
- [ ] E2E test: verify the vulnerability table renders rows from fixture data
- [ ] E2E test: verify filter interactions update the displayed data
- [ ] Verify MSW handlers return correct fixture data shapes

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 7 — Add remediation dashboard page with summary cards, chart, and filterable table

## Parent Epic
TC-9006: trustify-ui
