## Repository
trustify-ui

## Target Branch
main

## Description
Create the RemediationDashboardPage at /remediation with summary cards and a progress chart. The summary cards display total Open, In Progress, and Resolved vulnerability counts. The progress chart shows the remediation trend over the past 30 days. This page provides security managers with portfolio-wide remediation visibility in a single view. The page follows the existing page structure pattern (each page in its own directory under src/pages/).

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — Unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — Summary cards component displaying Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — Progress chart component showing 30-day remediation trend

## Files to Modify
- `src/routes.tsx` — Add /remediation route pointing to RemediationDashboardPage (lazy-loaded)

## Implementation Notes
- Follow the page directory structure pattern from `src/pages/SbomListPage/` — main component, test file, and components/ sub-directory.
- Use PatternFly 5 components for layout and cards. Summary cards should use PF5 Card components with distinct visual indicators for each status category.
- Use the `useRemediationSummary` hook (created in Task 3) for data fetching.
- Use `src/components/LoadingSpinner.tsx` for loading state and `src/components/EmptyStateCard.tsx` for empty state.
- For the progress chart, use a PatternFly-compatible charting approach. The chart should display daily resolved vulnerability counts over the past 30 days using the trend data from the summary API response.
- Register the route in `src/routes.tsx` following the existing route definition pattern with lazy-loaded page components (React Router v6).
- Use PascalCase for component names and camelCase for hooks, following the project naming conventions.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — Reusable loading indicator; use for loading state
- `src/components/EmptyStateCard.tsx` — Empty state placeholder; use when no remediation data exists
- `src/pages/SbomListPage/SbomListPage.tsx` — Reference page component for page structure, data fetching, and PatternFly layout patterns
- `src/hooks/useRemediationSummary.ts` — React Query hook providing summary data (created in Task 3)
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping; reuse for severity-based visual indicators in summary cards

## Acceptance Criteria
- [ ] RemediationDashboardPage is accessible at /remediation
- [ ] The page displays summary cards showing total Open, In Progress, and Resolved counts
- [ ] The page displays a progress chart showing the remediation trend over the past 30 days
- [ ] The page shows a loading spinner while data is being fetched
- [ ] The page shows an empty state when no remediation data exists
- [ ] The route is registered in src/routes.tsx with lazy loading

## Test Requirements
- [ ] Unit test: RemediationDashboardPage renders summary cards with correct count values from mock data
- [ ] Unit test: RemediationDashboardPage renders the progress chart component
- [ ] Unit test: RemediationDashboardPage shows loading spinner during data fetch
- [ ] Unit test: RemediationDashboardPage shows empty state when no data is returned
- [ ] Use MSW handlers and mock fixtures from Task 3 for test data
- [ ] Follow the testing pattern in `src/pages/SbomListPage/SbomListPage.test.tsx`

## Dependencies
- Depends on: Task 3 — Add remediation API types, client functions, and React Query hooks
