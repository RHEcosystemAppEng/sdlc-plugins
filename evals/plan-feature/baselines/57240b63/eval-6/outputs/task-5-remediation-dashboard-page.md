## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Create the main remediation dashboard page at `/remediation` with summary cards and a progress chart. The page displays three summary cards (Open, In Progress, Resolved counts) and a progress chart showing remediation trend over the past 30 days. This is the primary UI for UC-1 (View remediation summary), enabling security managers to see portfolio-wide remediation status at a glance.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component; fetches data via useRemediationSummary hook, renders summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- summary cards component displaying Open, In Progress, and Resolved totals using PatternFly Card components
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` -- progress chart component showing remediation trend over the past 30 days

## Implementation Notes
- Follow the page structure convention: each page gets its own directory under `src/pages/` with a main component and a `components/` subdirectory for page-specific components. Reference `src/pages/SbomListPage/` for the established pattern.
  - Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page structure scope.
- Use PatternFly 5 components throughout:
  - `Card`, `CardTitle`, `CardBody` for summary cards
  - `PageSection`, `Title` for page layout
  - `Grid`, `GridItem` for card layout (3-column grid for the three summary cards)
  - Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's PatternFly 5 component library scope.
- Consume data from `useRemediationSummary()` hook (created in Task 4). Handle loading state with `LoadingSpinner` from `src/components/LoadingSpinner.tsx` and empty state with `EmptyStateCard` from `src/components/EmptyStateCard.tsx`.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` to render severity labels in the summary breakdown.
- For the ProgressChart component, use a charting library compatible with PatternFly (e.g., PatternFly Charts or a lightweight alternative). The chart should display a line or area chart with the X-axis showing dates (past 30 days) and Y-axis showing vulnerability counts by status.
- Summary cards should display:
  - Total Open vulnerabilities (with Critical/High/Medium/Low breakdown)
  - Total In Progress
  - Total Resolved
- The page must handle up to 10,000 tracked vulnerabilities without performance degradation per the non-functional requirements.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- severity level badge with color mapping; reuse for severity labels in summary cards
- `src/components/LoadingSpinner.tsx` -- loading indicator; reuse for data loading state
- `src/components/EmptyStateCard.tsx` -- empty state placeholder; reuse when no remediation data exists
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping; reuse for chart color coding by severity
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference for page structure with data fetching and PatternFly layout

## Acceptance Criteria
- [ ] RemediationDashboardPage renders at /remediation path
- [ ] Three summary cards display Open, In Progress, and Resolved totals
- [ ] Summary cards show severity breakdown (Critical/High/Medium/Low counts)
- [ ] Progress chart displays remediation trend for the past 30 days
- [ ] Loading state shows LoadingSpinner while data is being fetched
- [ ] Empty state shows EmptyStateCard when no vulnerability data exists
- [ ] Page handles up to 10,000 vulnerabilities without visible performance degradation

## Test Requirements
- [ ] Unit test verifying summary cards render correct totals from mock data
- [ ] Unit test verifying loading spinner appears during data fetch
- [ ] Unit test verifying empty state renders when no data is available
- [ ] Unit test verifying progress chart renders with mock trend data

## Dependencies
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks

---
Description digest: sha256-md:9763b5d3f7fd75e36e23c31ab7a73066635488786c55e6990ac3ab898455592d
