## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Create the remediation dashboard page at `/remediation` with summary cards and a progress chart. The page shows three summary cards (total Open, In Progress, and Resolved vulnerability counts) and a progress chart displaying the remediation trend over time. This page serves as the primary entry point for security managers to monitor portfolio-wide remediation progress.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page component tests
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards component showing Open, In Progress, Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — progress chart component showing remediation trend over time

## Files to Modify
- `src/routes.tsx` — add `/remediation` route pointing to `RemediationDashboardPage`
- `src/App.tsx` — add navigation link to the remediation dashboard in the app navigation

## Implementation Notes
- Follow the existing page structure: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory.
  Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page directory scope.
- Use PatternFly 5 components for all UI elements: `Card`, `CardTitle`, `CardBody` for summary cards, `PageSection` and `Title` for page layout.
  Per CONVENTIONS.md §Component Library: PatternFly 5 — all UI components use PF5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component file scope.
- Use PascalCase for component names.
  Per CONVENTIONS.md §Naming: PascalCase for components.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` component file scope.
- Consume the `useRemediationSummary` hook from Task 4 for data fetching. Handle loading and error states using `LoadingSpinner` and `EmptyStateCard` shared components.
- Use React Router v6 lazy loading for the page component in `src/routes.tsx`, following the existing route definition pattern.
- The progress chart should show remediation trend over the past 30 days (per UC-1). Use a PatternFly-compatible charting approach or a lightweight chart library.
- Summary cards layout: three cards in a row showing Open (red/warning), In Progress (blue/info), and Resolved (green/success) counts.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx::LoadingSpinner` — reuse for loading state display
- `src/components/EmptyStateCard.tsx::EmptyStateCard` — reuse for empty state when no remediation data exists
- `src/components/SeverityBadge.tsx::SeverityBadge` — reference for PatternFly badge/label usage pattern
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page layout structure with PatternFly components
- `src/routes.tsx` — reference for route definition pattern with lazy loading

## Acceptance Criteria
- [ ] `/remediation` route is registered and navigable from the app navigation
- [ ] Dashboard page loads and displays three summary cards: Open, In Progress, Resolved counts
- [ ] Summary cards show correct counts from the remediation summary API
- [ ] Progress chart renders remediation trend data over the past 30 days
- [ ] Loading state is displayed while data is fetching
- [ ] Error state is displayed if the API call fails
- [ ] Empty state is displayed when no remediation data exists
- [ ] Page uses PatternFly 5 components exclusively

## Test Requirements
- [ ] Unit test verifying RemediationDashboardPage renders summary cards with mock data (MSW)
- [ ] Unit test verifying loading spinner appears during data fetch
- [ ] Unit test verifying error state is displayed on API failure
- [ ] Unit test verifying empty state when API returns zero counts

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — verify page component tests pass

## Dependencies
- Depends on: Task 4 — Add remediation API client, TypeScript models, and React Query hooks
