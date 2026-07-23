# Task 5: Create remediation dashboard page with summary cards and progress chart

## Repository
trustify-ui

## Target Branch
main

## Description
Create the main remediation dashboard page at `/remediation` for TC-9006. The page displays summary cards showing total Open, In Progress, and Resolved vulnerability counts, plus a progress chart showing the remediation trend over the past 30 days. This is the primary entry point for security managers tracking remediation SLAs across the portfolio. The page uses the React Query hooks and API types established in Task 4.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- component rendering Open, In Progress, and Resolved count cards
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` -- component rendering the 30-day remediation trend chart

## Files to Modify
- `src/routes.tsx` -- add `/remediation` route pointing to `RemediationDashboardPage` (lazy-loaded)
- `src/App.tsx` -- add navigation entry for the Remediation Dashboard if a navigation menu exists

## Implementation Notes
- Follow the existing page structure: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory. See `src/pages/SbomListPage/` for the canonical example.
  - Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the page directory scope.
- Use PatternFly 5 components for the UI. Summary cards can use PF5 `Card` components. The progress chart can use a PatternFly chart component or a lightweight charting library already in the project.
- Use React Router v6 lazy loading for the route, consistent with existing routes in `src/routes.tsx`.
  - Applies: task modifies `src/routes.tsx` matching the TypeScript routing file scope.
- Consume the `useRemediationSummary` hook from Task 4 for the summary cards data.
- Use the existing `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` for loading states.
- Use the existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` for empty data states.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity display in any breakdowns.
- Use the severity color mapping from `src/utils/severityUtils.ts` for chart colors.
- Testing: use Vitest + React Testing Library with MSW for API mocking, following the pattern in `src/pages/SbomListPage/SbomListPage.test.tsx`.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` -- loading indicator; use for data loading states
- `src/components/EmptyStateCard.tsx` -- empty state placeholder; use when no remediation data exists
- `src/components/SeverityBadge.tsx` -- severity level badge (Critical/High/Medium/Low); reuse for severity display
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping; reuse for chart colors and severity sorting
- `src/utils/formatDate.ts` -- date formatting helpers; reuse for chart axis labels and card timestamps

## Acceptance Criteria
- [ ] `/remediation` route renders the `RemediationDashboardPage` component
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Loading state displays `LoadingSpinner` while data is being fetched
- [ ] Empty state displays `EmptyStateCard` when no remediation data exists
- [ ] Page uses PatternFly 5 components consistent with the rest of the application
- [ ] Route is lazy-loaded

## Test Requirements
- [ ] Unit test: `RemediationDashboardPage` renders summary cards with correct counts from mocked API data
- [ ] Unit test: `RemediationDashboardPage` renders the progress chart
- [ ] Unit test: loading state shows `LoadingSpinner`
- [ ] Unit test: empty state shows `EmptyStateCard` when API returns no data
- [ ] Add mock remediation data fixtures in `tests/mocks/fixtures/`

## Dependencies
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
