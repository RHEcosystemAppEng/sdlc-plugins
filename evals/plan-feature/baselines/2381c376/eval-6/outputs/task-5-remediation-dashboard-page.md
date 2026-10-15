## Repository
trustify-ui

## Target Branch
main

## Description
Add the RemediationDashboardPage component at the /remediation route for the vulnerability remediation tracking dashboard (TC-9006). The page displays summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. This task also registers the route in the router and adds a navigation link.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — Unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — Summary cards component showing Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — Progress chart component showing 30-day remediation trend

## Files to Modify
- `src/routes.tsx` — Add /remediation route pointing to RemediationDashboardPage (lazy-loaded)
- `src/App.tsx` — Add navigation link for the remediation dashboard in the app navigation

## Implementation Notes
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page structure scope.
- Per CONVENTIONS.md §Component library: all UI components must use PatternFly 5 equivalents. Use PF5 Card for summary cards, PF5 Grid/Gallery for layout.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component scope.
- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing scope.
- Per CONVENTIONS.md §Naming: use PascalCase for components (RemediationDashboardPage, SummaryCards, ProgressChart).
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` naming scope.
- Reference `src/pages/SbomListPage/SbomListPage.tsx` for the established page component structure.
- Reference `src/components/EmptyStateCard.tsx` for empty state when no remediation data exists.
- Reference `src/components/LoadingSpinner.tsx` for loading state display.
- The page should use the `useRemediationSummary` hook (from Task 4) for data fetching.
- Summary cards: three cards showing total Open, In Progress, and Resolved counts respectively.
- Progress chart: display remediation trend over the past 30 days. Use a PatternFly-compatible charting approach or a lightweight chart library if PF5 charts are available.
- Handle loading and error states gracefully with existing shared components.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — Page structure pattern; follow for dashboard layout
- `src/components/EmptyStateCard.tsx` — Empty state component; use when no remediation data exists
- `src/components/LoadingSpinner.tsx` — Loading indicator; use during data fetch
- `src/components/SeverityBadge.tsx` — Severity level badge; may be useful for severity-labeled summary cards
- `src/utils/severityUtils.ts` — Severity ordering and color mapping; use for consistent severity colors in cards and chart

## Acceptance Criteria
- [ ] RemediationDashboardPage renders at /remediation route
- [ ] Summary cards display total Open, In Progress, and Resolved counts from the API
- [ ] Progress chart displays 30-day remediation trend
- [ ] Page is lazy-loaded via React Router
- [ ] Navigation link to /remediation is present in the app navigation
- [ ] Loading state shows a spinner while data is being fetched
- [ ] Empty state is shown when no remediation data exists
- [ ] Dashboard handles up to 10,000 tracked vulnerabilities without performance degradation (NFR)

## Test Requirements
- [ ] Unit test: RemediationDashboardPage renders summary cards with mocked API data
- [ ] Unit test: RemediationDashboardPage shows loading spinner during fetch
- [ ] Unit test: RemediationDashboardPage shows empty state when API returns no data
- [ ] Unit test: Progress chart renders with sample trend data

## Dependencies
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks
