## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts broken down by severity, and a progress chart showing the remediation trend over the past 30 days. Register the route in the application's router configuration and add a navigation entry.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with layout for summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — card components displaying Open, In Progress, and Resolved counts by severity
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — progress chart showing remediation trend over the past 30 days

## Files to Modify
- `src/routes.tsx` — add route definition for /remediation pointing to RemediationDashboardPage with lazy loading
- `src/App.tsx` — add navigation entry for the remediation dashboard in the app navigation

## Implementation Notes
- Follow the page structure pattern: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory. Reference `src/pages/SbomListPage/SbomListPage.tsx` for the established page layout pattern.
- Use PatternFly 5 components for cards (Card, CardTitle, CardBody), layout (PageSection, Grid, GridItem), and navigation elements.
- Use the `useRemediationSummary` hook (from Task 4) for data fetching. Show `LoadingSpinner` from `src/components/LoadingSpinner.tsx` during loading and `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no data is available.
- Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` to display severity levels in the summary cards.
- For the progress chart, use a PatternFly charting component or a simple SVG-based visualization showing remediation counts over time.
- Register the route with lazy loading following the existing pattern in `src/routes.tsx`.
- Per CONVENTIONS.md §Component Library: use PatternFly 5 components for all UI elements. Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` component file scope.
- Per CONVENTIONS.md §Page Structure: create the page directory under `src/pages/` with main component and `components/` subdirectory. Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page directory scope.
- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route definition file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — page layout pattern with filters and data display
- `src/components/SeverityBadge.tsx` — reuse for severity level display in summary cards
- `src/components/EmptyStateCard.tsx` — reuse for empty state when no remediation data exists
- `src/components/LoadingSpinner.tsx` — reuse for loading state during data fetch
- `src/utils/formatDate.ts` — date formatting helpers for chart axis labels

## Acceptance Criteria
- [ ] Dashboard page is accessible at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Summary cards show breakdown by severity (Critical/High/Medium/Low)
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Page shows loading spinner during data fetch
- [ ] Page shows empty state when no remediation data is available
- [ ] Navigation includes a link to the remediation dashboard

## Test Requirements
- [ ] Component test verifying summary cards render correct counts from mock data
- [ ] Component test verifying progress chart renders with trend data
- [ ] Component test verifying loading and empty states display correctly
- [ ] Verify route registration by navigating to /remediation

## Dependencies
- Depends on: Task 4 — Add API client and React Query hooks for remediation endpoints
