## Repository
trustify-ui

## Target Branch
main

## Description
Create the filterable vulnerability table component for the remediation dashboard. The table displays outstanding vulnerabilities with columns for severity, product, status, and details, and supports filtering by severity, product, and remediation status.

## Files to Create
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` — filterable vulnerability table with columns for severity, product, status, and details
- `src/pages/RemediationDashboardPage/components/RemediationFilterToolbar.tsx` — filter toolbar with severity, product, and status filter dropdowns

## Implementation Notes
Follow the table and filter pattern from `src/pages/SbomListPage/SbomListPage.tsx` which implements a list page with table and filters. Use the reusable `FilterToolbar` component from `src/components/FilterToolbar.tsx` as the base for filter controls, extending it with remediation-specific filter options (severity, product, status). Use `SeverityBadge` from `src/components/SeverityBadge.tsx` for severity column rendering. Use the `useRemediationByProduct` hook from Task 5 for data fetching with filter parameters. Apply PatternFly 5 Table component for the data table.

Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` matching the convention's `.tsx` file scope.

Per CONVENTIONS.md §State management: React Query for server state, no Redux.
Applies: task creates `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` matching the convention's `.tsx` file scope.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` — reusable filter toolbar with PatternFly
- `src/components/SeverityBadge.tsx` — severity level badge component
- `src/utils/severityUtils.ts` — severity ordering and color mapping
- `src/pages/SbomListPage/SbomListPage.tsx` — table with filters reference implementation

## Acceptance Criteria
- [ ] Vulnerability table displays columns: severity, product, status, vulnerability details
- [ ] Filter by severity (Critical/High/Medium/Low) works correctly
- [ ] Filter by product works correctly
- [ ] Filter by remediation status (Open/In Progress/Resolved) works correctly
- [ ] Multiple filters can be combined simultaneously
- [ ] Table supports sorting by severity column
- [ ] Table handles large datasets (up to 10,000 rows) with pagination

## Test Requirements
- [ ] Unit test for VulnerabilityTable rendering with mock data
- [ ] Unit test for filter application and data refresh
- [ ] Unit test for empty filtered results state

## Dependencies
- Depends on: Task 5 — Add remediation API types, client functions, and React Query hooks
