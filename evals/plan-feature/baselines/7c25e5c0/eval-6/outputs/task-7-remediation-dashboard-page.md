## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add the RemediationDashboardPage component at `/remediation` with three main sections: summary cards showing total Open, In Progress, and Resolved vulnerability counts; a progress chart showing remediation trend over time; and a filterable table of outstanding vulnerabilities with severity, product, and status filters.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with summary cards, progress chart, and filterable table
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — summary card components showing Open/In Progress/Resolved counts
- `src/pages/RemediationDashboardPage/components/RemediationTable.tsx` — filterable vulnerability table with severity, product, and status filters
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` — progress chart showing remediation trend over time

## Files to Modify
- `src/routes.tsx` — add `/remediation` route pointing to RemediationDashboardPage (lazy-loaded)
- `src/App.tsx` — add navigation entry for Remediation Dashboard in the app navigation (if nav is defined here)

## Implementation Notes
Follow the existing page structure patterns:

- **Page organization**: `src/pages/SbomListPage/SbomListPage.tsx` — each page has its own directory with a main component and `components/` subdirectory for page-specific components
- **Route registration**: `src/routes.tsx` — add lazy-loaded route following the React Router v6 pattern used for existing pages
- **Component library**: use PatternFly 5 components throughout:
  - Summary cards: use PF5 `Card`, `CardTitle`, `CardBody` for the three summary cards (Open, In Progress, Resolved)
  - Filterable table: use PF5 `Table`, `Thead`, `Tbody`, `Tr`, `Th`, `Td` with `FilterToolbar` from `src/components/FilterToolbar.tsx`
  - Progress chart: use PF5 chart components or a lightweight chart library compatible with the project
  - Severity badges: reuse `src/components/SeverityBadge.tsx` for severity column rendering
  - Empty state: use `src/components/EmptyStateCard.tsx` when no data is available
  - Loading: use `src/components/LoadingSpinner.tsx` while data is fetching
- **Data fetching**: use the React Query hooks from Task 6 (useRemediationSummary, useRemediationByProduct) — handle loading, error, and success states
- **Filtering**: severity filter should support Critical/High/Medium/Low selection; product filter should be a dropdown populated from the by-product data; status filter should support Open/In Progress/Resolved
- **Severity ordering**: use `src/utils/severityUtils.ts` for severity level ordering and color mapping

Per docs/constraints.md §5 (Code Change Rules): reuse existing shared components — do not create new versions of SeverityBadge, FilterToolbar, EmptyStateCard, or LoadingSpinner.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity level badge rendering, reuse for table severity column
- `src/components/FilterToolbar.tsx` — reusable filter toolbar with PatternFly, reuse for dashboard filters
- `src/components/EmptyStateCard.tsx` — empty state placeholder, reuse for no-data state
- `src/components/LoadingSpinner.tsx` — loading indicator, reuse for data loading state
- `src/utils/severityUtils.ts` — severity level ordering and color mapping

## Acceptance Criteria
- [ ] RemediationDashboardPage renders at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Progress chart displays remediation trend visualization
- [ ] Filterable table shows vulnerability list with severity, product, and status columns
- [ ] Severity filter supports Critical/High/Medium/Low selection
- [ ] Product filter dropdown is populated from by-product data
- [ ] Status filter supports Open/In Progress/Resolved selection
- [ ] Loading and empty states are handled with existing shared components
- [ ] Dashboard handles up to 10,000 vulnerabilities without performance degradation

## Test Requirements
- [ ] Component renders without errors with mock data
- [ ] Summary cards display correct counts from mock remediation summary
- [ ] Filter interactions update the displayed table data
- [ ] Empty state renders when no data is available
- [ ] Loading state renders while data is fetching

## Dependencies
- Depends on: Task 6 — Frontend React Query hooks
