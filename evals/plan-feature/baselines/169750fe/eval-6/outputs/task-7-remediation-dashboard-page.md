## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Create the remediation dashboard page at `/remediation` with three main sections: summary cards showing total Open, In Progress, and Resolved counts; a progress chart showing remediation trend over time; and a filterable vulnerability table with severity, product, and status filters. Uses PatternFly 5 components throughout.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — component tests
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards showing Open/In Progress/Resolved counts
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` — progress chart showing trend over time
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` — filterable table of outstanding vulnerabilities

## Files to Modify
- `src/routes.tsx` — add route definition for `/remediation` path
- `src/App.tsx` — add navigation entry for the remediation dashboard (if nav is defined here)

## Implementation Notes
- Follow the page structure pattern: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory, as seen in `src/pages/SbomListPage/` and `src/pages/AdvisoryListPage/`.
- Use PatternFly 5 components:
  - `Card` and `CardBody` for summary cards
  - `Toolbar` and `ToolbarContent` for filter controls (follow the pattern in `src/components/FilterToolbar.tsx`)
  - `Table`, `Thead`, `Tbody`, `Tr`, `Th`, `Td` for the vulnerability table
  - Chart components from `@patternfly/react-charts` for the progress chart
- Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display in the table.
- Use the `FilterToolbar` component from `src/components/FilterToolbar.tsx` for the filter controls.
- Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` for loading states and `EmptyStateCard` from `src/components/EmptyStateCard.tsx` for empty states.
- Use React Router v6 lazy loading for the page component, matching the pattern in `src/routes.tsx`.
- Per Key Conventions: all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's component library scope.
- Per Key Conventions: PascalCase for components.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's naming scope.
- Per Key Conventions: React Router v6 with lazy-loaded page components.
Applies: task modifies `src/routes.tsx` matching the convention's routing scope.
- The severity × status data from `useRemediationSummary()` populates the summary cards.
- The product data from `useRemediationByProduct()` populates the table with client-side filtering by severity and status.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — example page with table and filters
- `src/components/FilterToolbar.tsx` — reusable filter toolbar component
- `src/components/SeverityBadge.tsx` — severity level badge component
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/utils/severityUtils.ts` — severity level ordering and color mapping

## Acceptance Criteria
- [ ] Dashboard page renders at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Progress chart shows remediation trend over time
- [ ] Vulnerability table displays outstanding vulnerabilities with severity, product, and status columns
- [ ] Filters for severity, product, and status work correctly
- [ ] Loading and empty states are handled with PatternFly components
- [ ] Navigation entry for the remediation dashboard is present
- [ ] Dashboard handles up to 10,000 tracked vulnerabilities without performance degradation

## Test Requirements
- [ ] Component renders without errors with mocked hook data
- [ ] Summary cards display correct counts from mock data
- [ ] Filter interactions update the table correctly
- [ ] Empty state renders when no data is available
- [ ] Loading state renders while data is being fetched

## Dependencies
- Depends on: Task 6 — React Query hooks for remediation data
