## Repository
trustify-ui

## Target Branch
main

## Description
Add a filterable vulnerability table to the remediation dashboard page. The table displays outstanding vulnerabilities with columns for vulnerability ID, severity, product, status, and last updated date. Users can filter by severity, product, and remediation status using a filter toolbar. This implements the MVP requirement for a filterable vulnerability table and supports UC-1 (reviewing outstanding Critical vulnerabilities) and UC-2 (filtering by product for prioritization).

## Files to Create
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` -- filterable vulnerability table component
- `tests/mocks/fixtures/remediation.json` -- mock remediation data for tests

## Files to Modify
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- integrate VulnerabilityTable below the summary cards and progress chart sections
- `tests/mocks/handlers.ts` -- add MSW request handlers for remediation API endpoints

## Implementation Notes
- Use PatternFly 5 composable `Table` component (`Thead`, `Tbody`, `Tr`, `Th`, `Td`) for the vulnerability table layout.
  Per CONVENTIONS.md section "Component library": all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` matching the convention's `.tsx` scope.

- Use the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` for the filter controls. Configure three filter dropdowns: severity (Critical/High/Medium/Low), product (populated from API data), and status (Open/In Progress/Resolved).

- Use `SeverityBadge` from `src/components/SeverityBadge.tsx` to render severity levels in table cells with appropriate color coding.

- Use `severityUtils.ts` from `src/utils/severityUtils.ts` for severity ordering when sorting the table by severity column (Critical > High > Medium > Low).

- Use `formatDate` from `src/utils/formatDate.ts` for the "last updated" column display formatting.

- Product filter dropdown options should be populated from the `useRemediationByProduct` hook data.

- NFR: the table must handle up to 10,000 tracked vulnerabilities without performance degradation. Implement server-side pagination using the by-product endpoint's pagination support, or use client-side virtualization for large datasets.

- Follow the MSW mocking pattern from `tests/mocks/handlers.ts` for test API response setup. Add mock handlers for both remediation endpoints and create representative fixture data in `tests/mocks/fixtures/remediation.json`.
  Per CONVENTIONS.md section "Testing": Vitest + React Testing Library for unit tests; MSW for API mocking.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's `.ts` scope.

- Reference `src/pages/SbomListPage/SbomListPage.tsx` as a reference implementation of a list page with table, filters, and data fetching.

- Reference `src/pages/AdvisoryListPage/AdvisoryListPage.tsx` for advisory list patterns with severity display.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` -- reusable PatternFly filter toolbar with dropdown and text filter support
- `src/components/SeverityBadge.tsx` -- severity level badge for table cell rendering
- `src/utils/severityUtils.ts` -- severity ordering and color mapping for sort logic and display
- `src/utils/formatDate.ts` -- date formatting helpers for the "last updated" column
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference implementation of a list page with table and filter toolbar
- `src/pages/AdvisoryListPage/AdvisoryListPage.tsx` -- reference advisory list page with severity display in table
- `tests/mocks/handlers.ts` -- existing MSW handler patterns for API mocking
- `tests/mocks/fixtures/sboms.json` -- reference fixture data format for MSW mocks

## Acceptance Criteria
- [ ] Vulnerability table renders below summary cards and progress chart on the remediation dashboard
- [ ] Table displays columns: vulnerability ID, severity, product, status, last updated
- [ ] Filter by severity (Critical/High/Medium/Low) correctly narrows displayed rows
- [ ] Filter by product (dropdown populated from API data) correctly narrows displayed rows
- [ ] Filter by status (Open/In Progress/Resolved) correctly narrows displayed rows
- [ ] Multiple filters can be combined simultaneously
- [ ] Sorting by severity column uses correct severity ordering (Critical > High > Medium > Low)
- [ ] Table handles up to 10,000 vulnerabilities without performance degradation (via pagination or virtualization)

## Test Requirements
- [ ] Unit test verifying table renders with mock data from MSW handlers
- [ ] Unit test verifying severity filter narrows displayed rows to matching entries
- [ ] Unit test verifying product filter narrows displayed rows to matching entries
- [ ] Unit test verifying status filter narrows displayed rows to matching entries
- [ ] Unit test verifying sorting by severity uses correct severity ordering
- [ ] MSW handlers for remediation endpoints are added to test setup

## Verification Commands
- `npm run test` -- run unit tests
- `npm run build` -- verify production build succeeds

## Dependencies
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
