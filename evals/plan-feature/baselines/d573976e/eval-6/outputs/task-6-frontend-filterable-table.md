# Task 6 — Add filterable vulnerability table to the remediation dashboard

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add a filterable vulnerability table component to the remediation dashboard page. The table displays outstanding vulnerabilities with columns for severity, product, status, and other relevant fields. Users can filter by severity, product, and remediation status. This completes the dashboard's interactive data exploration capabilities.

## Files to Create
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` — filterable table component with severity, product, and status filter controls
- `tests/mocks/fixtures/remediation.json` — mock fixture data for remediation endpoints (summary and by-product responses)

## Files to Modify
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — integrate VulnerabilityTable component into the dashboard layout
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — add tests for the vulnerability table integration
- `tests/mocks/handlers.ts` — add MSW request handlers for remediation endpoints

## Implementation Notes
- Use the `FilterToolbar` component from `src/components/FilterToolbar.tsx` for the filter controls — this is the project's reusable filter toolbar built with PatternFly.
- Follow the table pattern in `src/pages/SbomListPage/SbomListPage.tsx` which implements a data table with filters.
- Use PatternFly 5 `Table`, `Thead`, `Tbody`, `Tr`, `Th`, `Td` components for the table structure.
- Filter controls should support: severity (Critical/High/Medium/Low), product (dropdown), and remediation status (Open/In Progress/Resolved).
- Use `SeverityBadge` from `src/components/SeverityBadge.tsx` for rendering severity values in the table cells.
- Use `useRemediationByProduct` hook from Task 4 for fetching the filterable data.
- The table should support pagination for large datasets (up to 10,000 vulnerabilities) using the paginated API response.
- MSW handlers should follow the pattern in `tests/mocks/handlers.ts` and fixtures should follow `tests/mocks/fixtures/sboms.json` pattern.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` — reusable PatternFly filter toolbar component
- `src/components/SeverityBadge.tsx` — severity badge for table cell rendering
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for table with filters page pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` — reference for data table component
- `tests/mocks/handlers.ts` — MSW handler patterns for API mocking
- `tests/mocks/fixtures/sboms.json` — mock fixture data pattern

## Acceptance Criteria
- [ ] Vulnerability table renders on the remediation dashboard with columns for severity, product, status
- [ ] Severity filter allows selecting one or more severity levels (Critical/High/Medium/Low)
- [ ] Product filter allows selecting a product from a dropdown
- [ ] Status filter allows selecting one or more statuses (Open/In Progress/Resolved)
- [ ] Filters update the displayed data (client-side or server-side filtering)
- [ ] Table supports pagination for large datasets
- [ ] Selecting a product from the product filter shows only vulnerabilities affecting that product (UC-2)

## Test Requirements
- [ ] Unit test verifying the vulnerability table renders with mock data
- [ ] Unit test verifying severity filter updates displayed rows
- [ ] Unit test verifying product filter updates displayed rows
- [ ] Unit test verifying status filter updates displayed rows
- [ ] Unit test verifying pagination controls work correctly
- [ ] MSW mock handlers are added to `tests/mocks/handlers.ts` for remediation endpoints
- [ ] Mock fixture data in `tests/mocks/fixtures/remediation.json` covers multiple severities, products, and statuses

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 4 — Add remediation API client, TypeScript models, and React Query hooks
- Depends on: Task 5 — Add remediation dashboard page with summary cards and progress chart
