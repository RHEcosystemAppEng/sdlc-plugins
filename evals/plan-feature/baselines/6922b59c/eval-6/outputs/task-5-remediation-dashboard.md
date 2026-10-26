## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add the remediation dashboard page at `/remediation` with summary cards showing
total Open, In Progress, and Resolved vulnerability counts, and a progress chart
displaying the remediation trend over the past 30 days. Register the route and add
a navigation entry so users can access the dashboard.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component that composes summary cards and progress chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards component showing Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — line/area chart component showing 30-day remediation trend

## Files to Modify
- `src/routes.tsx` — add `/remediation` route definition pointing to `RemediationDashboardPage` with lazy loading
- `src/App.tsx` — add navigation entry for the remediation dashboard in the app navigation

## Implementation Notes
- Follow the page directory structure pattern: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory. See `src/pages/SbomListPage/` for the reference layout.
  Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page component scope.
- Use PatternFly 5 components for all UI elements: `Card` for summary cards, `PageSection` for layout.
  Per CONVENTIONS.md §Component Library: all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component scope.
- Use the `useRemediationSummary` hook (from Task 4) for data fetching in the dashboard page.
- Summary cards should display three key metrics: total Open (warning color), In Progress (info color), Resolved (success color). Use PatternFly `Card` with `CardTitle` and `CardBody`.
- Progress chart should show a 30-day trend. Consider using a charting library compatible with PatternFly (e.g., Victory or Recharts) or PatternFly Charts if available.
- Handle loading states with `LoadingSpinner` from `src/components/LoadingSpinner.tsx`.
- Handle empty states with `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no remediation data exists.
- Use React Router v6 lazy loading for the route definition.
  Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` route file scope.
- Use PascalCase for component names.
  Per CONVENTIONS.md §Naming: PascalCase for components.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` component scope.
- Non-functional requirement: dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation. Summary cards render aggregated counts (not individual items), so performance concern is primarily on the chart rendering.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator component for async data states
- `src/components/EmptyStateCard.tsx` — empty state placeholder for when no data exists
- `src/components/SeverityBadge.tsx` — severity level badge for displaying severity indicators
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page component structure with data fetching
- `src/utils/severityUtils.ts` — severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] `RemediationDashboardPage` renders at the `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved counts from `useRemediationSummary`
- [ ] Progress chart displays a 30-day remediation trend visualization
- [ ] Loading spinner is shown while data is being fetched
- [ ] Empty state is shown when no remediation data exists
- [ ] Navigation entry for "Remediation" is visible in the app navigation
- [ ] Route uses lazy loading for the page component

## Test Requirements
- [ ] Test that `RemediationDashboardPage` renders summary cards with mocked data
- [ ] Test that loading state displays `LoadingSpinner`
- [ ] Test that empty state displays `EmptyStateCard` when no data
- [ ] Test that the page renders without errors with valid mock data
- [ ] Add MSW handler for `GET /api/v2/remediation/summary` in `tests/mocks/handlers.ts`

## Verification Commands
- `npx vitest run --reporter=verbose src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — run dashboard page tests
- `npm run build` — verify production build succeeds with the new page

## Dependencies
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks
