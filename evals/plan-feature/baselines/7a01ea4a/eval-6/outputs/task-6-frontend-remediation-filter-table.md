# Task 6: Add filterable vulnerability table to remediation dashboard

## Repository
trustify-ui

## Target Branch
main

## Description
Add a filterable vulnerability table to the remediation dashboard page created in Task 5. The table displays individual outstanding vulnerabilities with columns for severity, product, status, and other relevant fields. Users can filter the table by severity, product, and remediation status to drill down into specific subsets of vulnerabilities. This supports UC-1 (reviewing outstanding Critical vulnerabilities) and UC-2 (filtering by product for prioritization) from TC-9006.

## Files to Create
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` -- filterable vulnerability table component with severity, product, and status filter controls
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.test.tsx` -- unit tests for the vulnerability table component

## Files to Modify
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- integrate the `VulnerabilityTable` component below the summary cards and chart
- `src/api/rest.ts` -- add `fetchRemediationVulnerabilities()` function if a separate endpoint is needed for the table data, or reuse existing by-product data
- `src/api/models.ts` -- add `RemediationVulnerability` interface if not already covered

## Implementation Notes
- Use the existing `FilterToolbar` component from `src/components/FilterToolbar.tsx` for the filter controls. This component provides PatternFly-based filter UI that other pages already use. See `src/pages/SbomListPage/SbomListPage.tsx` for how `FilterToolbar` is integrated with a table.
  - Applies: task creates `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` matching the TypeScript component file scope.
- Use PatternFly 5 `Table` component for the data table, consistent with the table patterns in `src/pages/SbomListPage/SbomListPage.tsx` and `src/pages/RemediationDashboardPage/components/PackageTable.tsx`.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` to render severity values in table cells.
- Use the severity ordering from `src/utils/severityUtils.ts` for sort order (Critical > High > Medium > Low).
- Implement client-side filtering using React state for the filter values. If the vulnerability dataset exceeds 10,000 rows, consider server-side filtering via query parameters to the backend API.
- The product filter should be a dropdown populated from the available products in the data (from the by-product endpoint data).
- Testing: use Vitest + React Testing Library with MSW for API mocking.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` -- reusable filter toolbar with PatternFly; use directly for the filter controls
- `src/components/SeverityBadge.tsx` -- severity level badge; reuse for severity column rendering
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping; reuse for sort logic
- `src/pages/SbomListPage/SbomListPage.tsx` -- example of a page with table and filter integration; follow the same pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- example table component; follow the same PatternFly table pattern

## Acceptance Criteria
- [ ] Vulnerability table displays individual vulnerabilities with columns: severity, product, status, vulnerability ID, description
- [ ] Filter by severity works (dropdown with Critical, High, Medium, Low options)
- [ ] Filter by product works (dropdown populated from available products)
- [ ] Filter by status works (dropdown with Open, In Progress, Resolved options)
- [ ] Multiple filters can be applied simultaneously
- [ ] Table sorts by severity by default (Critical first)
- [ ] Severity column uses `SeverityBadge` component
- [ ] Table handles up to 10,000 vulnerabilities without performance degradation
- [ ] Table integrates into the existing `RemediationDashboardPage` below the summary cards and chart

## Test Requirements
- [ ] Unit test: `VulnerabilityTable` renders rows with correct vulnerability data
- [ ] Unit test: severity filter correctly limits displayed rows
- [ ] Unit test: product filter correctly limits displayed rows
- [ ] Unit test: status filter correctly limits displayed rows
- [ ] Unit test: multiple simultaneous filters work correctly
- [ ] Unit test: empty filter state shows all vulnerabilities
- [ ] Unit test: table renders `SeverityBadge` for severity column

## Dependencies
- Depends on: Task 5 -- Create remediation dashboard page with summary cards and progress chart
