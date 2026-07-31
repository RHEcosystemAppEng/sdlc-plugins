# Task 7: Add E2E tests for remediation dashboard

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add Playwright end-to-end tests for the remediation dashboard that verify the full user workflow: navigating to `/remediation`, seeing summary cards and chart, using filters on the vulnerability table, and sorting table columns. These E2E tests complement the unit tests added in Tasks 5 and 6.

## Files to Create
- `tests/e2e/remediation-dashboard.spec.ts` -- Playwright E2E tests for the remediation dashboard
- `tests/mocks/fixtures/remediation-summary.json` -- mock fixture data for remediation summary API response
- `tests/mocks/fixtures/remediation-by-product.json` -- mock fixture data for remediation by-product API response

## Files to Modify
- `tests/mocks/handlers.ts` -- add MSW request handlers for `GET /api/v2/remediation/summary` and `GET /api/v2/remediation/by-product`

## Implementation Notes
- Follow the E2E test pattern in `tests/e2e/sbom-list.spec.ts` for test structure, page navigation, and assertion style.
- Use MSW (Mock Service Worker) handlers from `tests/mocks/handlers.ts` for API mocking, consistent with `tests/setup.ts` configuration.
- Mock fixture data should contain realistic remediation data: multiple severities, products, and statuses to exercise all filter combinations.
- E2E tests should cover both use cases from the feature description:
  - UC-1: View remediation summary (navigate, verify cards, chart, table)
  - UC-2: Filter by product (select product filter, verify dashboard updates)

## Reuse Candidates
- `tests/e2e/sbom-list.spec.ts` -- reference for Playwright E2E test structure and navigation patterns
- `tests/setup.ts` -- test setup with MSW handlers and render helpers
- `tests/mocks/handlers.ts` -- existing MSW handler patterns to follow
- `tests/mocks/fixtures/sboms.json` -- reference for mock fixture data structure

## Acceptance Criteria
- [ ] E2E test verifies navigating to `/remediation` loads the dashboard page
- [ ] E2E test verifies summary cards display correct Open, In Progress, and Resolved counts
- [ ] E2E test verifies the progress chart is rendered
- [ ] E2E test verifies the vulnerability table displays rows from the mocked data
- [ ] E2E test verifies filtering by severity updates the table correctly
- [ ] E2E test verifies filtering by product updates the table correctly
- [ ] E2E test verifies filtering by status updates the table correctly
- [ ] Mock fixture files contain realistic multi-severity, multi-product remediation data
- [ ] All E2E tests pass

## Test Requirements
- [ ] E2E test for UC-1 (View remediation summary): navigate to `/remediation`, assert summary cards show expected counts, assert chart is visible, assert table has expected rows
- [ ] E2E test for UC-2 (Filter by product): navigate to `/remediation`, select product filter, assert table shows only vulnerabilities for selected product
- [ ] E2E test for combined filters: apply severity + product filter, assert correct filtered results
- [ ] E2E test for empty state: mock empty API response, verify empty state is displayed

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 5 -- Create RemediationDashboardPage with summary cards and progress chart
- Depends on: Task 6 -- Add filterable vulnerability table to remediation dashboard
