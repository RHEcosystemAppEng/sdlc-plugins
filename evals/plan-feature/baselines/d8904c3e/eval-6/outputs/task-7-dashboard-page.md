## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the main remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. This is the primary user-facing page for the vulnerability remediation tracking feature. Also registers the route in the application router and adds a navigation entry.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component; uses useRemediationSummary hook to fetch data; renders SummaryCards and ProgressChart components; includes layout scaffolding for the filterable table (Task 8)
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- component rendering three PatternFly Card components showing Open, In Progress, and Resolved counts aggregated across all severities
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` -- component rendering a progress chart showing remediation trend over the past 30 days using PatternFly chart components

## Files to Modify
- `src/routes.tsx` -- add route definition mapping `/remediation` to lazy-loaded RemediationDashboardPage component
- `src/App.tsx` -- add navigation entry for "Remediation" in the application navigation menu

## Implementation Notes
- Follow the page structure pattern from `src/pages/SbomListPage/`: each page gets its own directory under `src/pages/` with a main component and a `components/` subdirectory for page-specific components.
  Per CONVENTIONS.md: each page gets its own directory under src/pages/ with a main component, optional test file, and components/ subdirectory.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's TypeScript/React page structure scope.
- Use PatternFly 5 components for all UI elements: PF5 Card for summary cards, PF5 Chart components for the progress chart.
  Per CONVENTIONS.md: all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's TypeScript/React component scope.
- Use React Router v6 with lazy-loaded page components per the routing convention.
  Per CONVENTIONS.md: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's TypeScript file scope.
- Use PascalCase for component names (RemediationDashboardPage, SummaryCards, ProgressChart) per naming conventions.
  Per CONVENTIONS.md: PascalCase for components.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's TypeScript/React file scope.
- Use the LoadingSpinner component from `src/components/LoadingSpinner.tsx` for loading states and EmptyStateCard from `src/components/EmptyStateCard.tsx` for empty data scenarios.
- The progress chart should aggregate summary data over time. If the backend does not provide time-series data in the summary endpoint, note this as a limitation and render the current point-in-time data as a baseline.
- Non-functional: dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation. Use React.memo or useMemo for expensive computations.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- page structure pattern with data fetching and component composition; follow as template
- `src/components/LoadingSpinner.tsx` -- loading indicator; reuse for loading state display
- `src/components/EmptyStateCard.tsx` -- empty state placeholder; reuse when no remediation data exists
- `src/components/SeverityBadge.tsx` -- severity level badge (Critical/High/Medium/Low); reuse for severity display in summary cards
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping; reuse for severity-based color coding in cards and charts

## Acceptance Criteria
- [ ] RemediationDashboardPage renders at /remediation route
- [ ] Summary cards display total Open, In Progress, and Resolved counts aggregated across all severities
- [ ] Progress chart displays remediation trend visualization
- [ ] Navigation entry for "Remediation" appears in the application menu
- [ ] Loading state shows LoadingSpinner while data is being fetched
- [ ] Empty state shows EmptyStateCard when no remediation data exists
- [ ] Page handles up to 10,000 vulnerabilities without visible performance degradation

## Test Requirements
- [ ] Verify RemediationDashboardPage renders summary cards with correct counts from mock data
- [ ] Verify progress chart renders without errors
- [ ] Verify loading spinner appears during data fetch
- [ ] Verify empty state renders when no data is available
- [ ] Verify /remediation route is registered and navigable

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 6 -- Add React Query hooks for remediation data fetching
