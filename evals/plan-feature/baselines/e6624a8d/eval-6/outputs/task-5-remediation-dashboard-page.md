## Repository
trustify-ui

## Target Branch
main

## Description
Create the Remediation Dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing remediation trend over time. The page uses the React Query hooks (Task 4) to fetch data from the backend remediation endpoints. This establishes the dashboard layout that the filterable table (Task 6) will extend.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards component displaying Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` — progress chart component showing remediation trend over time

## Files to Modify
- `src/routes.tsx` — add route definition for `/remediation` path mapping to `RemediationDashboardPage`
- `src/App.tsx` — add navigation entry for the Remediation Dashboard (if navigation is defined here)

## Implementation Notes
- Follow the page directory structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components. See `src/pages/SbomListPage/` for the established pattern.
  Per CONVENTIONS.md §Page Structure: each page has its own directory under src/pages/ with main component and components/ subdirectory.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page component scope.
- Component library: use PatternFly 5 components for all UI elements — `Card`, `CardTitle`, `CardBody` for summary cards, `Grid`/`GridItem` for layout.
  Per CONVENTIONS.md §Component Library: all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` component file scope.
- Routing: use React Router v6 with lazy-loaded page component. See `src/routes.tsx` for the route definition pattern.
  Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` route file scope.
- Summary cards should show: total Open count (across all severities), total In Progress count, total Resolved count. Compute totals by summing across the `RemediationSummary[]` array from the hook.
- Progress chart: use a line or area chart showing remediation trend. If the backend does not provide time-series data in the initial implementation, display the current-state breakdown as a bar chart (severity x status) and note that trend data can be added in a future iteration.
- Use the `useRemediationSummary` hook from Task 4 to fetch summary data.
- Handle loading state with `LoadingSpinner` component from `src/components/LoadingSpinner.tsx`.
- Handle empty state with `EmptyStateCard` component from `src/components/EmptyStateCard.tsx`.
- Non-functional requirement: dashboard must handle up to 10,000 tracked vulnerabilities. Summary cards aggregate server-side counts, so frontend performance should not be affected by data volume.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator for async data states
- `src/components/EmptyStateCard.tsx` — empty state placeholder when no remediation data exists
- `src/components/SeverityBadge.tsx` — severity level badge for displaying severity in cards or chart legends
- `src/pages/SbomListPage/SbomListPage.tsx` — page structure pattern with data fetching, loading, and empty states
- `src/utils/severityUtils.ts` — severity level ordering and color mapping; use for chart color coding

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the Remediation Dashboard page
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart renders a visual breakdown of remediation data
- [ ] Loading spinner is shown while data is being fetched
- [ ] Empty state is shown when no remediation data exists
- [ ] Route is registered in `src/routes.tsx`
- [ ] Page uses PatternFly 5 components for layout and styling

## Test Requirements
- [ ] Unit test: RemediationDashboardPage renders summary cards with correct counts from mocked data
- [ ] Unit test: RemediationDashboardPage shows loading spinner during data fetch
- [ ] Unit test: RemediationDashboardPage shows empty state when no data is returned
- [ ] Unit test: SummaryCards component renders correct values for each status category

## Dependencies
- Depends on: Task 4 — Add remediation API types, client functions, and hooks
