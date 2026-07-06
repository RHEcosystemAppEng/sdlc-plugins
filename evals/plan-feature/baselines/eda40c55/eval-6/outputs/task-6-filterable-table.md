## Repository
trustify-ui

## Target Branch
main

## Description
Add a filterable vulnerability table to the remediation dashboard page. The table displays individual outstanding vulnerabilities with columns for vulnerability ID, severity, product, status, and age. Users can filter by severity (Critical/High/Medium/Low), product (dropdown), and status (Open/In Progress/Resolved). The table uses the by-product data from `useRemediationByProduct` hook and supports sorting and pagination.

## Files to Create
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` -- Filterable vulnerability table component using PatternFly Table with toolbar filters
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.test.tsx` -- Unit tests for the vulnerability table component

## Files to Modify
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- Integrate VulnerabilityTable component below the summary cards and progress chart

## Implementation Notes
- Use PatternFly 5 `Table` component with `Toolbar` for filter controls. Reference `src/pages/SbomListPage/SbomListPage.tsx` for the table-with-filters pattern.
- Reuse `FilterToolbar` from `src/components/FilterToolbar.tsx` for the filter toolbar implementation. The toolbar should include severity filter (multi-select), product filter (dropdown), and status filter (multi-select).
- Use `useRemediationByProduct` hook (Task 4) for the data source. Apply client-side filtering based on user selections, or pass filter parameters to the API if supported.
- Severity badges should reuse `SeverityBadge` from `src/components/SeverityBadge.tsx` for consistent styling.
- Use severity ordering and color mapping from `src/utils/severityUtils.ts` for sorting by severity.
- Per CONVENTIONS.md §Page Structure: page-specific components go in the `components/` subdirectory. See `src/pages/SbomDetailPage/components/PackageTable.tsx` for a table component within a page.
  Applies: task creates `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` matching the convention's TypeScript/React component file scope.
- Per CONVENTIONS.md §Component Library: use PatternFly 5 Table and Toolbar components. See `src/pages/SbomListPage/SbomListPage.tsx` for PatternFly table usage.
  Applies: task creates `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` matching the convention's TypeScript/React component file scope.
- Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests with MSW for API mocking. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the test pattern.
  Applies: task creates `src/pages/RemediationDashboardPage/components/VulnerabilityTable.test.tsx` matching the convention's TypeScript test file scope.

## Reuse Candidates
- `src/components/FilterToolbar.tsx` -- Reusable filter toolbar with PatternFly; reuse for severity, product, and status filters
- `src/components/SeverityBadge.tsx` -- Severity level badge component; reuse for severity column rendering
- `src/utils/severityUtils.ts` -- Severity ordering and color mapping; reuse for sort-by-severity logic
- `src/pages/SbomListPage/SbomListPage.tsx` -- Reference for table-with-filters page pattern
- `src/pages/SbomDetailPage/components/PackageTable.tsx` -- Reference for table component within a page's components directory

## Acceptance Criteria
- [ ] Vulnerability table renders on the remediation dashboard page below the summary section
- [ ] Table displays columns for vulnerability ID, severity, product, status
- [ ] Filter by severity (Critical/High/Medium/Low) works correctly
- [ ] Filter by product (dropdown selection) works correctly
- [ ] Filter by status (Open/In Progress/Resolved) works correctly
- [ ] Multiple filters can be combined simultaneously
- [ ] Table supports pagination for large datasets
- [ ] Severity badges use the existing SeverityBadge component

## Test Requirements
- [ ] Unit test: table renders with mock vulnerability data
- [ ] Unit test: severity filter reduces displayed rows to matching severity
- [ ] Unit test: product filter reduces displayed rows to matching product
- [ ] Unit test: status filter reduces displayed rows to matching status
- [ ] Unit test: combined filters work correctly (intersection of filter criteria)
- [ ] Unit test: pagination controls appear when data exceeds page size

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage/components/VulnerabilityTable` -- Expected: all table tests pass

## Dependencies
- Depends on: Task 4 -- Add API client functions and React Query hooks for remediation endpoints
- Depends on: Task 5 -- Add remediation dashboard page with summary cards and progress chart (provides the page to integrate into)
