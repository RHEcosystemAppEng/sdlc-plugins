## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9008 (TC-9006: trustify-ui)

## Description
Add the remediation dashboard page at `/remediation` with summary cards and a progress chart. The summary cards display total Open, In Progress, and Resolved vulnerability counts. The progress chart shows the remediation trend over the past 30 days. This page serves as the primary view for security managers tracking remediation SLAs across the portfolio. The page uses the React Query hooks from Task 4 to fetch data from the backend aggregation endpoints.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Main dashboard page component composing summary cards and progress chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — Unit tests for dashboard page rendering and data states
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — Summary cards component displaying Open, In Progress, and Resolved counts by severity
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — Progress chart component showing remediation trend over the past 30 days
- `tests/mocks/fixtures/remediation.json` — Mock remediation data for MSW handlers

## Files to Modify
- `src/routes.tsx` — Add /remediation route pointing to RemediationDashboardPage with lazy loading
- `tests/mocks/handlers.ts` — Add MSW request handlers for remediation API endpoints

## Implementation Notes
Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` file scope.

Per CONVENTIONS.md §Component library: all UI components must use PatternFly 5 equivalents. Use PF5 Card for summary cards, PF5 Grid/Gallery for layout.
Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` file scope.

Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. Add the /remediation route definition in `src/routes.tsx`.
Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` file scope.

Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for unit tests; MSW for API mocking. Add mock handlers in `tests/mocks/handlers.ts`.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.tsx` test file scope.

Per CONVENTIONS.md §Naming: use PascalCase for components (RemediationDashboardPage, SummaryCards, ProgressChart), kebab-case for directories.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` file scope.

For the summary cards, use PatternFly 5 `Card` components arranged in a `Grid` layout. Each card should show a count with a label (e.g., "Open: 142") and optionally color-code by severity using the existing `SeverityBadge` component pattern from `src/components/SeverityBadge.tsx`.

For the progress chart, use a line chart or area chart showing remediation trend over time. Consider using a charting library compatible with PatternFly (e.g., PatternFly Charts or a lightweight alternative).

Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` for loading states and `EmptyStateCard` from `src/components/EmptyStateCard.tsx` for empty data states.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Severity level badge component; reuse for severity indicators in summary cards
- `src/components/LoadingSpinner.tsx` — Loading indicator; use while remediation data is being fetched
- `src/components/EmptyStateCard.tsx` — Empty state placeholder; use when no remediation data is available
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping; reuse for chart color coding
- `src/pages/SbomListPage/SbomListPage.tsx` — Reference for page component structure with data fetching and rendering patterns
- `src/hooks/useRemediationSummary.ts` — React Query hook for summary data (created in Task 4)

## Acceptance Criteria
- [ ] Dashboard page renders at /remediation route
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Summary cards show breakdown by severity (Critical, High, Medium, Low)
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Loading spinner displays while data is being fetched
- [ ] Empty state card displays when no remediation data is available
- [ ] Page is lazy-loaded via React Router

## Test Requirements
- [ ] Unit test: RemediationDashboardPage renders summary cards with mock data
- [ ] Unit test: RemediationDashboardPage shows loading spinner during data fetch
- [ ] Unit test: RemediationDashboardPage shows empty state when no data is returned
- [ ] Unit test: SummaryCards component displays correct counts for each severity-status combination
- [ ] Unit test: ProgressChart component renders without errors with valid data

## Dependencies
- Depends on: Task 4 — Add remediation API client and React Query hooks
