# Task 5: Create remediation dashboard page with summary cards and progress chart

Parent Epic: TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
main

## Description
Create the main remediation dashboard page at `/remediation`. The page displays summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend. Register the page route in the application router. This task establishes the page structure; the filterable vulnerability table is added in Task 6.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component that composes summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary card components showing Open, In Progress, and Resolved counts by severity
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — progress chart component showing remediation trend over time

## Files to Modify
- `src/routes.tsx` — add `/remediation` route pointing to `RemediationDashboardPage` with lazy loading

## Implementation Notes
- Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components. Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's .tsx scope.
- Per CONVENTIONS.md §Component Library: use PatternFly 5 components for all UI elements — `Card`, `CardTitle`, `CardBody` for summary cards, `Grid` and `GridItem` for layout. Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's .tsx scope.
- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. Add the route in `src/routes.tsx` using `React.lazy()` for code splitting. Applies: task modifies `src/routes.tsx` matching the convention's .tsx scope.
- Per CONVENTIONS.md §Naming: use PascalCase for component files and names (e.g., `RemediationDashboardPage`, `SummaryCards`). Applies: convention has no file-type restriction (broadly applicable).
- Reference `src/pages/SbomListPage/SbomListPage.tsx` for the page component structure pattern — how it uses hooks for data fetching and composes child components.
- The `RemediationDashboardPage` component should call `useRemediationSummary()` from Task 4 to fetch summary data.
- Use `src/components/LoadingSpinner.tsx` for loading states and `src/components/EmptyStateCard.tsx` for empty data scenarios.
- Use `src/utils/severityUtils.ts` for severity level ordering and color mapping in summary cards.
- Use `src/components/SeverityBadge.tsx` to display severity levels in the summary cards.
- The progress chart should use a charting approach compatible with PatternFly (e.g., PatternFly Charts or a lightweight chart library).
- Summary cards should display one card per status (Open, In Progress, Resolved) with a breakdown by severity level within each card.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity level badge component with Critical/High/Medium/Low styling; reuse in summary cards
- `src/components/LoadingSpinner.tsx` — loading indicator; reuse for loading state while data fetches
- `src/components/EmptyStateCard.tsx` — empty state placeholder; reuse when no remediation data exists
- `src/utils/severityUtils.ts` — severity level ordering and color mapping; reuse for chart and card color coding
- `src/pages/SbomListPage/SbomListPage.tsx` — page component pattern; reference for hook usage and component composition

## Acceptance Criteria
- [ ] `/remediation` route is registered in `src/routes.tsx` with lazy loading
- [ ] `RemediationDashboardPage` renders and fetches data via `useRemediationSummary` hook
- [ ] Summary cards display total Open, In Progress, and Resolved counts with severity breakdown
- [ ] Progress chart renders remediation trend visualization
- [ ] Loading spinner displays while data is fetching
- [ ] Empty state card displays when no remediation data is available
- [ ] All components use PatternFly 5 components

## Dependencies
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks
