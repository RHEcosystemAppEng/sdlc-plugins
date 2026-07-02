## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards displaying total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing remediation trend over time. Register the route and add a navigation entry so users can access the dashboard from the main navigation.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component composing summary cards and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards displaying aggregate counts by status (Open, In Progress, Resolved)
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — progress chart showing remediation trend over time

## Files to Modify
- `src/routes.tsx` — add `/remediation` route pointing to RemediationDashboardPage (lazy-loaded)
- `src/App.tsx` — add remediation dashboard entry to the navigation menu

## Implementation Notes
- Follow the page directory structure pattern: each page gets its own directory under `src/pages/` with a main component and a `components/` subdirectory for page-specific sub-components.
  Per CONVENTIONS.md: each page gets its own directory under src/pages/ with main component and components/ subdirectory.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's .tsx page file scope.
- Use PatternFly 5 components throughout — `Card`, `CardTitle`, `CardBody` for summary cards, `Grid`/`GridItem` for layout.
  Per CONVENTIONS.md: all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's .tsx component file scope.
- Consume data from the `useRemediationSummary` hook created in Task 4.
- Use the existing `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` for loading states and `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no data is available.
- Use the existing `SeverityBadge` component from `src/components/SeverityBadge.tsx` and severity color mapping from `src/utils/severityUtils.ts` for consistent severity presentation.
- Register the route in `src/routes.tsx` following the existing pattern — use React Router v6 lazy loading for the page component.
- The progress chart can use a PatternFly chart component or a lightweight charting approach consistent with the existing frontend stack.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity level badge for consistent severity display
- `src/components/LoadingSpinner.tsx` — loading indicator for async data states
- `src/components/EmptyStateCard.tsx` — empty state placeholder when no data exists
- `src/utils/severityUtils.ts` — severity level ordering and color mapping
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page component structure and hook consumption
- `src/routes.tsx` — reference for lazy-loaded route registration pattern

## Acceptance Criteria
- [ ] `/remediation` route renders the RemediationDashboardPage
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Progress chart renders remediation trend visualization
- [ ] Navigation menu includes a link to the remediation dashboard
- [ ] Loading and empty states are handled gracefully using existing shared components

## Test Requirements
- [ ] Component renders summary cards with data from useRemediationSummary hook (verified in Task 7)
- [ ] Component renders empty state when no data is available (verified in Task 7)
- [ ] Route is registered and navigable (verified in Task 7's E2E test)

## Dependencies
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks

[sdlc-workflow] Description digest: sha256-md:637253659a669220021fbc84268d08e77716615bee7a72a666895a3ea86afcf1
