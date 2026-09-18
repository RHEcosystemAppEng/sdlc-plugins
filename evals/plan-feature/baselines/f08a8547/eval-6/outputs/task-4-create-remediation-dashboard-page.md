## Repository
trustify-ui

## Target Branch
main

## Description
Create the main remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. Register the page route in the application router with lazy loading. This page serves as the central view for security managers tracking remediation SLAs across the portfolio.

## Files to Modify
- `src/routes.tsx` — add /remediation route with lazy-loaded RemediationDashboardPage component

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with layout
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page component tests
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards component displaying Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — progress chart component showing remediation trend over 30 days

## Implementation Notes
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. See `src/pages/SbomListPage/` for the established pattern.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's .tsx page component scope.

- Per CONVENTIONS.md §Component library: use PatternFly 5 components for all UI elements — cards, page layout, and chart components.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's .tsx component scope.

- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. See existing route definitions in `src/routes.tsx`.
  Applies: task modifies `src/routes.tsx` matching the convention's .tsx route file scope.

- Per CONVENTIONS.md §Naming: use PascalCase for component names and files.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's .tsx file scope.

- Per CONVENTIONS.md §Testing: use Vitest + React Testing Library for component tests. Use MSW for API mocking in tests. See `src/pages/SbomListPage/SbomListPage.test.tsx` for the established test pattern.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's .tsx test file scope.

- Consume data from `useRemediationSummary` hook (from Task 3).
- Use existing `LoadingSpinner` component from `src/components/LoadingSpinner.tsx` for loading states.
- Use existing `EmptyStateCard` component from `src/components/EmptyStateCard.tsx` for empty states.
- Use `SeverityBadge` color mapping from `src/utils/severityUtils.ts` for consistent severity coloring in summary cards.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator for data-fetching states
- `src/components/EmptyStateCard.tsx` — empty state placeholder when no remediation data exists
- `src/hooks/useRemediationSummary.ts` — React Query hook for summary data (from Task 3)
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page component structure with data fetching and loading/error states
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for summary card styling

## Acceptance Criteria
- [ ] RemediationDashboardPage renders at `/remediation` route
- [ ] Route is registered in `src/routes.tsx` with lazy loading
- [ ] Summary cards display total Open, In Progress, and Resolved counts from the remediation summary API
- [ ] Progress chart renders remediation trend data over the past 30 days
- [ ] Page shows LoadingSpinner while data is being fetched
- [ ] Page shows EmptyStateCard when no remediation data exists

## Test Requirements
- [ ] Component test verifying summary cards render correct counts from mock data
- [ ] Component test verifying progress chart renders with mock trend data
- [ ] Test that loading state is shown during data fetch using MSW delay
- [ ] Test that empty state is shown when API returns no data

## Dependencies
- Depends on: Task 3 — Add remediation API types, client functions, and React Query hooks
