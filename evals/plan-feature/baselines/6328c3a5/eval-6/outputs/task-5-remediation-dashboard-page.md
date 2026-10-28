## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. Register the route and add a navigation entry so users can access the dashboard.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main page component composing summary cards, progress chart, and vulnerability table (placeholder for Task 6)
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — three PatternFly Card components displaying Open, In Progress, and Resolved counts from the summary data
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — line or area chart showing remediation trend over the past 30 days

## Files to Modify
- `src/routes.tsx` — add `/remediation` route pointing to lazy-loaded `RemediationDashboardPage`
- `src/App.tsx` — add navigation entry for the remediation dashboard in the app navigation

## Implementation Notes
- Follow the page directory structure convention: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific sub-components. See `src/pages/SbomListPage/` for the reference pattern.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` file scope.
- Per Key Conventions: all UI components use PatternFly 5 equivalents. Use PF5 `Card`, `CardTitle`, `CardBody` for summary cards. Use PF5 `Grid` and `GridItem` for responsive layout.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` file scope.
- Per Key Conventions: React Router v6 with lazy-loaded page components. Add the route with `React.lazy()` import.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` file scope.
- The `SummaryCards` component should consume data from `useRemediationSummary()` hook, computing totals from the severity x status matrix.
- The `ProgressChart` component can use a charting library compatible with PatternFly (e.g., Victory or PatternFly's chart components). Show a line chart with date on x-axis and count on y-axis.
- Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` while data is loading.
- Use `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no remediation data is available.
- The page layout should render summary cards at the top, chart below, and leave a slot for the vulnerability table (Task 6).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page component structure with data fetching hooks
- `src/components/LoadingSpinner.tsx` — loading indicator component
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/components/SeverityBadge.tsx` — severity level badge for displaying severity in cards
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for chart colors

## Acceptance Criteria
- [ ] `/remediation` route is registered and navigable from the app navigation
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Progress chart renders remediation trend over the past 30 days
- [ ] Loading spinner shown while data is fetching
- [ ] Empty state shown when no remediation data exists
- [ ] Page is lazy-loaded for code splitting

## Test Requirements
- [ ] Verify summary cards render correct counts from mock data
- [ ] Verify progress chart renders without errors
- [ ] Verify loading state renders LoadingSpinner
- [ ] Verify empty state renders EmptyStateCard

## Dependencies
- Depends on: Task 4 — Add remediation API client, models, and React Query hooks
