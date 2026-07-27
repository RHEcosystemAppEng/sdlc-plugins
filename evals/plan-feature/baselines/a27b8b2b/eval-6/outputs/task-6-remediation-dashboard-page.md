# Task 6: Create remediation dashboard page with summary cards and progress chart

**Epic:** TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Create the RemediationDashboardPage at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. This is the main entry point for the remediation tracking dashboard feature (UC-1: View remediation summary).

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards component showing Open, In Progress, Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — trend chart showing remediation progress over the past 30 days

## Implementation Notes
- Follow the page directory structure convention: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory for page-specific components. Reference `src/pages/SbomListPage/` for the established pattern.
- Use PatternFly 5 components for all UI elements:
  - `Card` components for summary cards
  - `Grid` / `GridItem` for card layout
  - A charting library compatible with PF5 for the progress trend chart (e.g., Victory or Recharts)
- Consume data from the `useRemediationSummary()` hook created in Task 5.
- Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` for loading states.
- Use `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no remediation data is available.
- Use PascalCase for component names per project naming conventions.
- The dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation per the non-functional requirements. Use React.memo or useMemo for expensive computations if needed.
- Summary cards should display counts by aggregating across all severity levels from the summary response.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator; use for data loading states
- `src/components/EmptyStateCard.tsx` — empty state placeholder; use when no remediation data exists
- `src/components/SeverityBadge.tsx` — severity level badge component; use to display severity indicators in cards
- `src/utils/severityUtils.ts` — severity level ordering and color mapping; reuse for consistent severity display
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page structure with data fetching and PatternFly layout

## Acceptance Criteria
- [ ] RemediationDashboardPage renders summary cards with total Open, In Progress, and Resolved counts
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Loading state is displayed while data is being fetched
- [ ] Empty state is displayed when no remediation data exists
- [ ] Dashboard handles up to 10,000 vulnerabilities without performance degradation
- [ ] All UI components use PatternFly 5

## Test Requirements
- [ ] Unit test verifying summary cards render with correct count values from mock data
- [ ] Unit test verifying loading spinner is shown during data fetch
- [ ] Unit test verifying empty state is shown when summary data is empty
- [ ] Unit test verifying the progress chart renders with trend data

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — run dashboard page tests
- `npx tsc --noEmit` — verify TypeScript compilation

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 5 — Add remediation API types, client functions, and hooks
