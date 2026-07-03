## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Create the RemediationDashboardPage component with summary cards displaying total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. This is the main dashboard page that users navigate to at /remediation.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- page component tests
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- summary cards component showing Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` -- remediation trend chart component

## Implementation Notes
- Follow the page directory structure pattern: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory. See `src/pages/SbomListPage/` for the established pattern.
- Use PatternFly 5 components for all UI elements -- cards (`Card`, `CardTitle`, `CardBody`), grid layout (`Grid`, `GridItem`), and page structure (`PageSection`).
- Summary cards should display three cards in a row: Open (count), In Progress (count), Resolved (count). Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` for severity-colored indicators where applicable.
- Use the `useRemediationSummary` hook from Task 4 to fetch summary data.
- Handle loading states with `src/components/LoadingSpinner.tsx` and empty states with `src/components/EmptyStateCard.tsx`.
- The progress chart should show a line or bar chart of remediation counts over the past 30 days. Choose a charting approach consistent with the project's existing dependencies.
- The page layout should accommodate the filterable vulnerability table (Task 6) below the summary section.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` -- severity level badge for color-coded severity indicators
- `src/components/LoadingSpinner.tsx` -- loading indicator for async data
- `src/components/EmptyStateCard.tsx` -- empty state placeholder when no data is available
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference pattern for page component structure with data fetching
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping

## Acceptance Criteria
- [ ] RemediationDashboardPage renders summary cards showing total Open, In Progress, and Resolved counts
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Loading state is shown while data is being fetched
- [ ] Empty state is shown when no remediation data is available
- [ ] All UI components use PatternFly 5
- [ ] Page layout reserves space for the filterable table (Task 6)

## Test Requirements
- [ ] Component test verifying summary cards render with correct counts from mocked data
- [ ] Component test verifying progress chart renders with trend data
- [ ] Test loading state is displayed during data fetch
- [ ] Test empty state is displayed when API returns no data
- [ ] Test uses MSW handlers for API mocking (following pattern in tests/setup.ts)

## Dependencies
- Depends on: Task 4 -- Add remediation API client functions and React Query hooks
