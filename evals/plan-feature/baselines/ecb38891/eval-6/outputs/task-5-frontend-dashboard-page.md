# Task 5: Create RemediationDashboardPage with summary cards and progress chart

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Create the main remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. This page serves as the primary entry point for security managers tracking remediation SLAs.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- summary cards component displaying Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` -- progress chart showing remediation trend over time

## Files to Modify
- `src/routes.tsx` -- add `/remediation` route pointing to `RemediationDashboardPage` (lazy-loaded)
- `src/App.tsx` -- add navigation link to the remediation dashboard if navigation is managed here

## Implementation Notes
- Follow the page structure pattern in `src/pages/SbomListPage/` -- each page has its own directory with a main component and `components/` subdirectory for page-specific components.
- Use PatternFly 5 components for all UI elements: `Card`, `CardTitle`, `CardBody` for summary cards, `PageSection` for page layout.
- Use React Router v6 with lazy-loading for the page component, following the pattern in `src/routes.tsx`.
- Summary cards should use `useRemediationSummary` hook (from Task 4) to aggregate total counts by status across all severities.
- Progress chart should visualize remediation trend data -- use a PatternFly chart component or a compatible charting library.
- Handle loading state with `LoadingSpinner` component from `src/components/LoadingSpinner.tsx`.
- Handle empty state (no vulnerabilities) with `EmptyStateCard` from `src/components/EmptyStateCard.tsx`.
- Naming conventions: PascalCase for components, camelCase for hooks, following project conventions.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference for page structure with data fetching and PatternFly layout
- `src/components/LoadingSpinner.tsx` -- loading indicator to show while data is being fetched
- `src/components/EmptyStateCard.tsx` -- empty state placeholder when no remediation data exists
- `src/components/SeverityBadge.tsx` -- severity level badge component for use in summary cards
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping for chart colors

## Acceptance Criteria
- [ ] `RemediationDashboardPage` component renders at the `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart shows remediation trend over the past 30 days
- [ ] Page displays loading indicator while data is being fetched
- [ ] Page displays appropriate empty state when no remediation data exists
- [ ] Page is lazy-loaded via React Router
- [ ] Navigation to `/remediation` is accessible from the app's navigation

## Test Requirements
- [ ] Unit test for `RemediationDashboardPage` verifying summary cards render with correct counts from mocked API data
- [ ] Unit test verifying loading state displays `LoadingSpinner`
- [ ] Unit test verifying empty state displays `EmptyStateCard` when no data
- [ ] Unit test for `SummaryCards` component verifying correct count display
- [ ] Tests use MSW handlers from Task 4 for API mocking

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
