# Task 5 — Add remediation dashboard page with summary cards and progress chart

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Create the `/remediation` dashboard page with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart displaying the remediation trend over the past 30 days. This is the main page component and its core sub-components (summary cards and progress chart). The filterable vulnerability table is handled in Task 6.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with layout for summary cards, progress chart, and vulnerability table
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — component displaying Open, In Progress, and Resolved counts as PatternFly cards
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — component displaying the 30-day remediation trend chart

## Files to Modify
- `src/routes.tsx` — add route definition for `/remediation` path pointing to `RemediationDashboardPage`
- `src/App.tsx` — add navigation entry for the Remediation Dashboard (if navigation is managed here)

## Implementation Notes
- Follow the existing page structure pattern: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory (see `src/pages/SbomListPage/` for reference).
- Use PatternFly 5 components for all UI elements: `Card`, `CardTitle`, `CardBody` for summary cards; `Grid`/`GridItem` for layout.
- Use React Query hooks from Task 4 (`useRemediationSummary`) to fetch data.
- Add lazy-loaded route following the React Router v6 pattern in `src/routes.tsx`.
- Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` for loading states.
- Use `EmptyStateCard` from `src/components/EmptyStateCard.tsx` for empty data states.
- Use `SeverityBadge` from `src/components/SeverityBadge.tsx` for displaying severity levels in the summary.
- Use severity ordering and color mapping utilities from `src/utils/severityUtils.ts`.
- The dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation (non-functional requirement).

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page component structure with table and filters
- `src/components/SeverityBadge.tsx` — severity level badge component (Critical/High/Medium/Low)
- `src/components/LoadingSpinner.tsx` — loading indicator for async data
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/utils/severityUtils.ts` — severity level ordering and color mapping
- `src/utils/formatDate.ts` — date formatting helpers for chart axis labels

## Acceptance Criteria
- [ ] Dashboard page renders at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Loading state is shown while data is being fetched
- [ ] Empty state is shown when no remediation data exists
- [ ] Route is registered in `src/routes.tsx`
- [ ] Page handles up to 10,000 vulnerabilities without visible performance degradation

## Test Requirements
- [ ] Unit test verifying the dashboard page renders with mock data
- [ ] Unit test verifying summary cards display correct counts from mock data
- [ ] Unit test verifying loading state is shown before data arrives
- [ ] Unit test verifying empty state when no data is returned
- [ ] Tests use MSW mock handlers and React Testing Library following `src/pages/SbomListPage/SbomListPage.test.tsx` pattern

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 4 — Add remediation API client, TypeScript models, and React Query hooks
