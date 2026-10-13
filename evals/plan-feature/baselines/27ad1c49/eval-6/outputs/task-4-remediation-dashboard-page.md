## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Build the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. Register the route and add navigation to the dashboard from the application layout.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Main dashboard page component that composes summary cards and progress chart, uses `useRemediationSummary` hook for data
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — Unit tests for the dashboard page component
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — Summary cards component displaying Open, In Progress, and Resolved counts with severity breakdown using PatternFly Card components
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — Progress chart component showing remediation trend over the past 30 days using PatternFly Charts

## Files to Modify
- `src/routes.tsx` — Add route definition for `/remediation` pointing to lazy-loaded `RemediationDashboardPage`
- `src/App.tsx` — Add navigation entry for the remediation dashboard in the application sidebar/nav

## Implementation Notes
Follow the page structure pattern where each page has its own directory under `src/pages/` with a main component and a `components/` subdirectory for page-specific components.

- Use PatternFly 5 `Card`, `CardTitle`, `CardBody` components for summary cards, following the component usage patterns in existing pages like `SbomListPage`
- Use PatternFly Charts (e.g., `ChartDonut` or `ChartBar`) for the progress chart — these are PF5-compatible chart components
- The `RemediationDashboardPage` should call `useRemediationSummary()` and pass the data down to `SummaryCards` and `ProgressChart` as props
- Show `LoadingSpinner` from `src/components/LoadingSpinner.tsx` while data is loading
- Show `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no remediation data exists
- Register the route with lazy loading in `src/routes.tsx` following the React Router v6 pattern used by existing routes
- Summary cards should use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity labels

Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with main component and `components/` subdirectory. Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Component Library: use PatternFly 5 components for all UI elements. Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` scope.

Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Severity level badge (Critical/High/Medium/Low); reuse in summary cards for severity labels
- `src/components/LoadingSpinner.tsx` — Loading indicator; show while remediation data loads
- `src/components/EmptyStateCard.tsx` — Empty state placeholder; show when no remediation data exists
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping; use for chart colors and card ordering
- `src/pages/SbomListPage/SbomListPage.tsx` — Existing page component; reference for page layout and PatternFly usage patterns

## Acceptance Criteria
- [ ] Dashboard page renders at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Summary cards show severity breakdown (Critical, High, Medium, Low) within each status
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Loading spinner shown while data is fetching
- [ ] Empty state displayed when no remediation data exists
- [ ] Navigation entry added for remediation dashboard in application layout

## Test Requirements
- [ ] Unit test verifying summary cards render correct counts from mock data
- [ ] Unit test verifying progress chart renders without errors
- [ ] Unit test verifying loading state displays spinner
- [ ] Unit test verifying empty state displays when no data returned

## Dependencies
- Depends on: Task 3 — Add remediation API types, client functions, and React Query hooks
