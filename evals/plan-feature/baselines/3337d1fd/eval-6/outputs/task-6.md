## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over time. This is the main page component rendered at the /remediation route.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary card components displaying Open, In Progress, and Resolved counts by severity
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — chart component showing remediation trend over time

## Implementation Notes
Follow the page structure pattern from `src/pages/SbomListPage/SbomListPage.tsx` — each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components. Use PatternFly 5 components for card layout (PF5 Card, CardTitle, CardBody) and grid layout. Use the `useRemediationSummary` hook from Task 5 to fetch data. Use the `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` for loading states and `EmptyStateCard` from `src/components/EmptyStateCard.tsx` for empty states. The progress chart can use PatternFly's built-in charting or a lightweight charting approach consistent with the project.

Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` file scope.

Per CONVENTIONS.md §Page structure: each page gets own directory under src/pages/ with components/ subdirectory.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — page component structure reference
- `src/components/LoadingSpinner.tsx` — loading state component
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/components/SeverityBadge.tsx` — severity level badge for cards
- `src/utils/severityUtils.ts` — severity ordering and color mapping for chart colors

## Acceptance Criteria
- [ ] Dashboard page displays summary cards for Open, In Progress, and Resolved counts
- [ ] Summary cards break down counts by severity (Critical/High/Medium/Low)
- [ ] Progress chart renders remediation trend visualization
- [ ] Loading state shows spinner while data is fetching
- [ ] Empty state shows appropriate message when no remediation data exists
- [ ] Dashboard handles up to 10,000 tracked vulnerabilities without performance degradation

## Test Requirements
- [ ] Unit test for SummaryCards rendering with mock data
- [ ] Unit test for ProgressChart rendering with mock data
- [ ] Unit test for dashboard loading and empty states

## Dependencies
- Depends on: Task 5 — Add remediation API types, client functions, and React Query hooks
