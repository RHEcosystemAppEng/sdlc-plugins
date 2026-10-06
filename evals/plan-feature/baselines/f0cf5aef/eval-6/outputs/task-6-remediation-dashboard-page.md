## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the `RemediationDashboardPage` component at the `/remediation` route. The page displays summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. This is the primary user-facing page for the vulnerability remediation tracking dashboard (TC-9006).

## Files to Modify
- `src/routes.tsx` — add `/remediation` route pointing to `RemediationDashboardPage` (lazy-loaded)
- `src/App.tsx` — add navigation entry for the remediation dashboard if needed

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards component showing Open/In Progress/Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — progress chart component showing remediation trend over 30 days

## Implementation Notes
- Follow the existing page structure pattern: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory for page-specific components.
- Use PatternFly 5 components for the layout: `PageSection`, `Card`, `CardTitle`, `CardBody`, `Grid`, `GridItem` for the summary cards layout.
- Summary cards should display three key metrics: total Open, total In Progress, and total Resolved counts, sourced from the `useRemediationSummary` hook (Task 5).
- For the progress chart, use a PatternFly-compatible charting solution or a lightweight chart library. The chart should display a line or area chart showing remediation progress over the past 30 days.
- Use the `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` while data is loading.
- Use the `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` when no remediation data is available.
- Register the route in `src/routes.tsx` following the React Router v6 pattern with lazy-loaded page components.
- Per frontend conventions: PascalCase for component names, use PatternFly 5 components exclusively.
- Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity indicators if displayed in the summary cards breakdown.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — page structure pattern with PatternFly layout
- `src/components/LoadingSpinner.tsx` — loading indicator component
- `src/components/EmptyStateCard.tsx` — empty state placeholder component
- `src/components/SeverityBadge.tsx` — severity level badge for Critical/High/Medium/Low display
- `src/hooks/useRemediationSummary.ts` — React Query hook for summary data (created in Task 5)
- `src/routes.tsx` — route registration pattern
- `src/utils/severityUtils.ts` — severity level ordering and color mapping

## Acceptance Criteria
- [ ] `/remediation` route is registered and navigable
- [ ] Dashboard page loads and displays summary cards with Open, In Progress, and Resolved counts
- [ ] Progress chart renders remediation trend over the past 30 days
- [ ] Loading state shows `LoadingSpinner` while data is being fetched
- [ ] Empty state shows `EmptyStateCard` when no remediation data exists
- [ ] Page uses PatternFly 5 components for layout and styling

## Test Requirements
- [ ] Unit test: `RemediationDashboardPage` renders summary cards with correct counts from mock data
- [ ] Unit test: progress chart renders without errors with mock trend data
- [ ] Unit test: loading state is displayed while data is being fetched
- [ ] Unit test: empty state is displayed when no data is available

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 5 — Add API client functions, types, and React Query hooks for remediation endpoints
