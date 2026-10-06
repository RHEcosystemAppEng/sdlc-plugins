## Repository
trustify-ui

## Target Branch
main

## Description
Add the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing remediation trend over the past 30 days. The page follows the existing page structure pattern with its own directory under `src/pages/`. This implements UC-1 from the feature specification: allowing security managers to view remediation summary at a glance.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component with layout for summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- PatternFly card components displaying Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` -- chart component showing remediation trend over 30 days

## Files to Modify
- `src/routes.tsx` -- add `/remediation` route definition with lazy-loaded RemediationDashboardPage
- `src/App.tsx` -- add navigation entry for the remediation dashboard if applicable

## Implementation Notes
Per CONVENTIONS.md "Page structure": each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. See `src/pages/SbomListPage/` for reference.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page scope.

Per CONVENTIONS.md "Component library": all UI components must use PatternFly 5 equivalents. Use PF5 Card for summary cards, PF5 Grid/Gallery for layout. See `src/components/EmptyStateCard.tsx` for PatternFly card usage.
Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md "Routing": use React Router v6 with lazy-loaded page components. Add the route definition in `src/routes.tsx` following existing patterns.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing scope.

Per CONVENTIONS.md "Naming": PascalCase for components (RemediationDashboardPage, SummaryCards, ProgressChart).
Applies: convention has no file-type restriction (broadly applicable).

Use the `useRemediationSummary` hook from Task 5 for data fetching. Show `LoadingSpinner` during loading state and `EmptyStateCard` when no data is available.

The progress chart requires time-series data. If the backend summary endpoint does not return historical data, the chart should render static summary data with a note that trend data will be available in a future iteration.

Relevant constraints from `docs/constraints.md`:
- Per SS5.3: Implementation must follow the patterns referenced in these Implementation Notes.
- Per SS5.4: Reuse existing shared components (LoadingSpinner, EmptyStateCard, SeverityBadge).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference implementation for page structure and layout patterns
- `src/components/LoadingSpinner.tsx` -- reusable loading indicator for data-fetching states
- `src/components/EmptyStateCard.tsx` -- reusable empty state placeholder
- `src/components/SeverityBadge.tsx` -- severity level badge for displaying Critical/High/Medium/Low indicators
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] RemediationDashboardPage renders at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart renders remediation trend visualization
- [ ] Page uses PatternFly 5 components for layout and cards
- [ ] Route is lazy-loaded following React Router v6 patterns
- [ ] Loading state shows LoadingSpinner while data is being fetched
- [ ] Empty state shows EmptyStateCard when no remediation data exists
- [ ] Navigation entry is accessible from the application

## Test Requirements
- [ ] Verify RemediationDashboardPage renders summary cards with correct count values from mock data
- [ ] Verify loading state displays LoadingSpinner
- [ ] Verify empty state displays EmptyStateCard
- [ ] Verify route `/remediation` renders the dashboard page

## Dependencies
- Depends on: Task 5 -- Add API client and React Query hooks for remediation endpoints

## Parent Epic
TC-9008
