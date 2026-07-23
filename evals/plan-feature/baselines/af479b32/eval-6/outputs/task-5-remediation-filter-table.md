## Repository
trustify-ui

## Target Branch
main

## Description
Add a filterable vulnerability table to the remediation dashboard page. The table displays outstanding vulnerabilities with columns for vulnerability name, severity, product, and remediation status. Users can filter the table by severity (Critical/High/Medium/Low), product, and status (Open/In Progress/Resolved). This enables security managers to drill down from the summary view to individual vulnerabilities and engineering leads to filter by product for prioritization.

## Files to Create
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` — Filterable vulnerability table component with PatternFly Table and FilterToolbar

## Files to Modify
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Integrate VulnerabilityTable below the summary cards and progress chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — Add tests for the filterable table integration
- `tests/mocks/fixtures/remediation.json` — Add mock data for vulnerability table entries

## Implementation Notes
- Use the existing `src/components/FilterToolbar.tsx` for the filter controls. The FilterToolbar supports PatternFly filter patterns — configure it with filter categories for severity, product, and status.
- Use PatternFly 5 Table component for the vulnerability table display.
- Use the `src/components/SeverityBadge.tsx` component to render severity levels in the table.
- Use the `useRemediationByProduct` hook (created in Task 3) for fetching the data that populates the table. The table data is derived from the by-product endpoint's response, which provides per-product remediation breakdowns.
- Severity filter options should follow the ordering from `src/utils/severityUtils.ts` (Critical, High, Medium, Low).
- Support client-side filtering for severity and status, and server-side pagination for the product dimension.
- The table should support sorting by severity (using severity ordering from severityUtils.ts) and by count columns.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` — Reusable PatternFly filter toolbar component; use directly for severity, product, and status filters
- `src/components/SeverityBadge.tsx` — Severity level badge component; render in the severity column of the table
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping; use for filter option ordering and sort logic
- `src/hooks/useRemediationByProduct.ts` — React Query hook providing per-product data with pagination (created in Task 3)
- `src/pages/SbomListPage/SbomListPage.tsx` — Reference page with table and filter integration pattern

## Acceptance Criteria
- [ ] The remediation dashboard page displays a vulnerability table below the summary cards and progress chart
- [ ] The table shows vulnerability entries with columns for name, severity, product, and status
- [ ] Users can filter the table by severity (Critical, High, Medium, Low)
- [ ] Users can filter the table by product
- [ ] Users can filter the table by status (Open, In Progress, Resolved)
- [ ] Multiple filters can be applied simultaneously
- [ ] The table supports pagination for large datasets
- [ ] SeverityBadge is used to render severity values in the table

## Test Requirements
- [ ] Unit test: VulnerabilityTable renders table rows from mock data
- [ ] Unit test: Severity filter correctly filters table entries
- [ ] Unit test: Product filter correctly filters table entries
- [ ] Unit test: Status filter correctly filters table entries
- [ ] Unit test: Multiple simultaneous filters work correctly
- [ ] Unit test: Table displays empty state when filters produce no results
- [ ] Follow the testing pattern in `src/pages/SbomListPage/SbomListPage.test.tsx` and `src/pages/AdvisoryListPage/AdvisoryListPage.test.tsx`

## Dependencies
- Depends on: Task 4 — Create remediation dashboard page with summary cards and progress chart
