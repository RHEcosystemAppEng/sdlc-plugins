# Task 6: Add filterable vulnerability table to remediation dashboard

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add a filterable vulnerability table to the RemediationDashboardPage that displays outstanding vulnerabilities with filters for severity, product, and remediation status. This table sits below the summary cards and chart, enabling security managers and engineering leads to drill down into specific vulnerabilities for prioritization.

## Files to Create
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` -- filterable table component displaying vulnerability rows with severity, product, status columns
- `src/pages/RemediationDashboardPage/components/RemediationFilterToolbar.tsx` -- filter toolbar with severity, product, and status filter controls

## Files to Modify
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- integrate `VulnerabilityTable` and `RemediationFilterToolbar` below the summary cards and chart

## Implementation Notes
- Use PatternFly 5 `Table` component (or `TableComposable`) for the vulnerability table, following the pattern in `src/pages/SbomListPage/SbomListPage.tsx`.
- Use the `FilterToolbar` component from `src/components/FilterToolbar.tsx` as a base, or create a remediation-specific filter toolbar using PatternFly `ToolbarFilter` components.
- Filters: severity dropdown (Critical/High/Medium/Low), product dropdown (populated from API data), status dropdown (Open/In Progress/Resolved).
- Filtering should update the React Query hook parameters to refetch data from the backend with the selected filters, or filter client-side if the dataset is small enough.
- Use `SeverityBadge` from `src/components/SeverityBadge.tsx` for the severity column rendering.
- Table should support sorting by severity (using ordering from `src/utils/severityUtils.ts`), product name, and status.
- Must handle up to 10,000 vulnerabilities without performance degradation -- consider pagination or virtualized scrolling for large datasets.
- Product filter dropdown should be populated from the `useRemediationByProduct` hook data.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` -- reusable filter toolbar with PatternFly; extend or reference for remediation-specific filters
- `src/components/SeverityBadge.tsx` -- severity level badge for table cell rendering
- `src/utils/severityUtils.ts` -- severity ordering and color mapping for sorting
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference for table with filters pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- reference for data table component pattern

## Acceptance Criteria
- [ ] Vulnerability table renders on the remediation dashboard below the summary cards and chart
- [ ] Table displays columns for vulnerability identifier, severity, product, and remediation status
- [ ] Severity filter dropdown filters table rows by severity level (Critical/High/Medium/Low)
- [ ] Product filter dropdown filters table rows by product name
- [ ] Status filter dropdown filters table rows by remediation status (Open/In Progress/Resolved)
- [ ] Multiple filters can be applied simultaneously (AND logic)
- [ ] Table supports sorting by severity, product, and status columns
- [ ] Severity column uses `SeverityBadge` component for consistent rendering
- [ ] Table handles large datasets (up to 10,000 rows) without performance degradation

## Test Requirements
- [ ] Unit test for `VulnerabilityTable` verifying correct row rendering with mocked data
- [ ] Unit test for severity filter: apply Critical filter, verify only Critical rows remain
- [ ] Unit test for product filter: apply a specific product filter, verify filtered results
- [ ] Unit test for status filter: apply Open filter, verify only Open rows remain
- [ ] Unit test for combined filters: apply severity + status filter, verify AND logic
- [ ] Unit test for sorting by severity column

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 5 -- Create RemediationDashboardPage with summary cards and progress chart
