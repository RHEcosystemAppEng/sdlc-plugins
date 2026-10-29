## Repository
trustify-ui

## Target Branch
main

## Description
Add the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing remediation trend over the past 30 days. This is the primary view for security managers tracking remediation SLAs.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component composing summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards component displaying Open, In Progress, and Resolved counts by severity
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — progress chart component showing remediation trend over time

## Files to Modify
- `src/routes.tsx` — add route definition for /remediation path pointing to RemediationDashboardPage

## Implementation Notes
Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components. Follow the pattern established by `src/pages/SbomListPage/`.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page component scope.

Per CONVENTIONS.md §Component Library: all UI components must use PatternFly 5 equivalents. Use PF5 Card components for summary cards, and a PF5-compatible charting solution for the progress chart.
Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. Add a lazy import for RemediationDashboardPage in routes.tsx.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing file scope.

The summary cards should display three top-level counts (Open, In Progress, Resolved) with a breakdown by severity (Critical/High/Medium/Low) within each card.

The progress chart should show a time-series line or area chart with remediation trend data over the past 30 days. Use the summary endpoint with date range parameters.

Use the `useRemediationSummary` hook from Task 4 for data fetching. Show LoadingSpinner during data fetch and EmptyStateCard when no data is available.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page component structure and layout
- `src/components/SeverityBadge.tsx` — reuse for displaying severity levels (Critical/High/Medium/Low) in summary cards
- `src/components/EmptyStateCard.tsx` — reuse for empty state when no remediation data exists
- `src/components/LoadingSpinner.tsx` — reuse for loading state during data fetch
- `src/utils/severityUtils.ts` — reuse severity level ordering and color mapping for chart and card rendering

## Acceptance Criteria
- [ ] RemediationDashboardPage renders at the /remediation route
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Summary cards show breakdown by severity level (Critical/High/Medium/Low)
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Loading state shows LoadingSpinner during data fetch
- [ ] Empty state shows EmptyStateCard when no vulnerability data exists
- [ ] Page uses PatternFly 5 components throughout

## Test Requirements
- [ ] Verify summary cards render correct counts from mocked API data
- [ ] Verify progress chart renders with trend data
- [ ] Verify loading spinner appears during data fetch
- [ ] Verify empty state card appears when API returns no data
- [ ] Verify route /remediation renders the RemediationDashboardPage component

## Dependencies
- Depends on: Task 4 — Add remediation API client and React Query hooks
