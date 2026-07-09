## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards and a progress chart. The summary cards display total Open, In Progress, and Resolved vulnerability counts. The progress chart shows the remediation trend over the past 30 days. The page is registered as a new route in the application's routing configuration and uses lazy loading per the established pattern.

## Files to Create
- `src/pages/RemediationDashboard/RemediationDashboard.tsx` — main dashboard page component composing summary cards and progress chart
- `src/pages/RemediationDashboard/components/SummaryCards.tsx` — summary cards component showing Open, In Progress, and Resolved totals
- `src/pages/RemediationDashboard/components/ProgressChart.tsx` — progress chart component showing remediation trend over time

## Files to Modify
- `src/routes.tsx` — add `/remediation` route pointing to `RemediationDashboard` with lazy loading

## Implementation Notes
- Per repo conventions (Page structure): each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. See `src/pages/SbomListPage/` for the canonical example.
  Applies: task creates `src/pages/RemediationDashboard/RemediationDashboard.tsx` matching the convention's TypeScript component file scope.
- Per repo conventions (Component library): all UI components must use PatternFly 5 equivalents. Use PF5 `Card`, `CardTitle`, `CardBody` for summary cards and PF5 layout components for the dashboard grid.
  Applies: task creates `src/pages/RemediationDashboard/components/SummaryCards.tsx` matching the convention's TypeScript component file scope.
- Per repo conventions (Routing): use React Router v6 with lazy-loaded page components. See `src/routes.tsx` for the route definition pattern.
  Applies: task modifies `src/routes.tsx` matching the convention's TypeScript route file scope.
- Per repo conventions (Naming): use PascalCase for component files and camelCase for hooks/utilities.
  Applies: task creates `src/pages/RemediationDashboard/RemediationDashboard.tsx` matching the convention's TypeScript file scope.
- Use the `useRemediationSummary` hook from Task 4 for fetching summary data.
- Use the existing `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` for loading states.
- Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` for empty data states.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity level display in cards.
- For the progress chart, use a PatternFly-compatible charting approach (e.g., Victory charts or similar React charting library used in the project).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity level badge component (Critical/High/Medium/Low); reuse for severity display in summary cards
- `src/components/LoadingSpinner.tsx` — loading indicator component; reuse for data loading states
- `src/components/EmptyStateCard.tsx` — empty state placeholder component; reuse when no remediation data exists
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page component structure with data fetching, loading, and error states
- `src/hooks/useRemediationSummary.ts` — React Query hook from Task 4 for fetching summary data
- `src/utils/severityUtils.ts` — severity level ordering and color mapping; reuse for chart color coding

## Acceptance Criteria
- [ ] Dashboard page renders at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved counts from the backend API
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Loading state is shown while data is being fetched
- [ ] Empty state is shown when no remediation data exists
- [ ] Route is lazy-loaded per the established routing pattern

## Test Requirements
- [ ] Verify the dashboard page renders without errors
- [ ] Verify summary cards display correct counts from API response
- [ ] Verify loading spinner is shown during data fetch
- [ ] Verify empty state renders when API returns zero counts
- [ ] Verify the route `/remediation` resolves to the dashboard component

## Dependencies
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks
