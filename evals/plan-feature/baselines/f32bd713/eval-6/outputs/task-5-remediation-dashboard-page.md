## Repository
trustify-ui

## Parent Epic
TC-9008 (TC-9006: trustify-ui)

## Target Branch
main

## Description
Add the RemediationDashboardPage component at `/remediation` with summary cards displaying total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. This is the main container page for the remediation tracking dashboard (TC-9006), implementing Use Case UC-1 (View remediation summary).

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component with layout for summary cards, progress chart, and vulnerability table placeholder
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- summary cards component showing Open, In Progress, and Resolved totals
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` -- progress chart component showing 30-day remediation trend

## Implementation Notes
- Follow the page structure convention: each page gets its own directory under `src/pages/` with a main component file and a `components/` subdirectory for page-specific child components.
  Per CONVENTIONS.md section Page Structure: each page gets its own directory under src/pages/ with a main component, optional test file, and components/ subdirectory for page-specific components.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page directory scope.
- Use PatternFly 5 components for all UI elements:
  - `Card` / `CardTitle` / `CardBody` for summary cards
  - `Grid` / `GridItem` for dashboard layout
  - `PageSection` for page structure
  Per CONVENTIONS.md section Component Library: PatternFly 5 -- all UI components use PF5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's TypeScript/React component scope.
- Use the `useRemediationSummary` hook from Task 4 for data fetching.
- SummaryCards component: compute total counts per status by summing across all severity groups from the RemediationSummaryResponse.
- ProgressChart component: display trend data. If the backend does not provide historical time-series data, note this as a limitation and render a placeholder or static chart with current-point-in-time data.
- Handle loading state using `LoadingSpinner` from `src/components/LoadingSpinner.tsx`.
- Handle empty state (no vulnerabilities) using `EmptyStateCard` from `src/components/EmptyStateCard.tsx`.
- Use `SeverityBadge` from `src/components/SeverityBadge.tsx` for any severity-level display.
- Leave a placeholder section in the page layout for the filterable vulnerability table (added in Task 6).

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- severity level badge component for displaying Critical/High/Medium/Low indicators
- `src/components/EmptyStateCard.tsx` -- empty state placeholder for when no remediation data is available
- `src/components/LoadingSpinner.tsx` -- loading indicator for data fetching states
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping utilities
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference for page layout structure with PatternFly components
- `src/pages/AdvisoryListPage/AdvisoryListPage.tsx` -- reference for list page structure

## Acceptance Criteria
- [ ] RemediationDashboardPage component renders correctly
- [ ] Summary cards display total Open, In Progress, and Resolved counts aggregated from the API response
- [ ] Progress chart renders remediation trend visualization
- [ ] Loading state shows LoadingSpinner while data is being fetched
- [ ] Empty state shows EmptyStateCard when no vulnerability data is available
- [ ] Page layout uses PatternFly 5 components (Card, Grid, PageSection)
- [ ] Page includes placeholder area for the filterable vulnerability table (Task 6)

## Test Requirements
- [ ] Component renders summary cards with correct count values from mock data
- [ ] Component shows LoadingSpinner during data fetch
- [ ] Component shows EmptyStateCard when API returns empty dataset
- [ ] Progress chart renders without errors with valid data
- [ ] Summary cards correctly sum counts across severity groups per status

## Dependencies
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
