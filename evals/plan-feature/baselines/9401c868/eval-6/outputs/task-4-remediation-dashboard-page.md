## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards and a progress chart. The page displays total Open, In Progress, and Resolved vulnerability counts as summary cards, and a progress chart showing the remediation trend over the past 30 days. This is the primary landing page for security managers tracking remediation SLAs.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with summary cards and progress chart layout
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — unit tests for dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary card components showing Open, In Progress, Resolved counts
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` — progress chart showing remediation trend over time

## Files to Modify
- `src/routes.tsx` — add route definition for `/remediation` pointing to `RemediationDashboardPage`
- `src/App.tsx` — add lazy-loaded import for the remediation dashboard page

## Implementation Notes
- Per CONVENTIONS.md §Page Structure: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. See `src/pages/SbomListPage/` for the established pattern.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page directory scope.
- Per CONVENTIONS.md §Component Library: all UI components must use PatternFly 5 equivalents. Use PF5 `Card`, `CardTitle`, `CardBody`, `Gallery`, and `Grid` for summary card layout.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component scope.
- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. See `src/routes.tsx` for existing route definitions.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing file scope.
- Per CONVENTIONS.md §Naming: PascalCase for components, kebab-case for directories. The page directory should follow existing naming pattern.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` file scope.
- Summary cards: use PatternFly `Card` components to display three counts (Open, In Progress, Resolved) with appropriate color coding
- Progress chart: use a chart library compatible with PatternFly (PatternFly Charts or a compatible alternative) for the 30-day trend line
- Use `useRemediationSummary` hook from Task 3 for data fetching
- Handle loading state with `LoadingSpinner` from `src/components/LoadingSpinner.tsx`
- Handle empty state with `EmptyStateCard` from `src/components/EmptyStateCard.tsx`

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator for data fetch states
- `src/components/EmptyStateCard.tsx` — empty state placeholder when no data
- `src/components/SeverityBadge.tsx` — severity level badge for color-coding severity labels
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page structure with data fetching and table/card layout
- `src/utils/severityUtils.ts` — severity level ordering and color mapping for consistent severity display

## Acceptance Criteria
- [ ] Dashboard page accessible at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart shows remediation trend over the past 30 days
- [ ] Page handles loading state with loading spinner
- [ ] Page handles empty state when no remediation data exists
- [ ] Route registered in `src/routes.tsx` with lazy loading
- [ ] Page uses PatternFly 5 components for layout and styling

## Test Requirements
- [ ] Unit test verifying summary cards render with correct counts from mock data
- [ ] Unit test verifying progress chart renders with trend data
- [ ] Unit test verifying loading state displays spinner
- [ ] Unit test verifying empty state displays placeholder when no data
- [ ] Add MSW handler for remediation summary endpoint in test mocks

## Verification Commands
- `npx tsc --noEmit` — TypeScript type checking passes
- `npx vitest run --reporter=verbose` — unit tests pass

## Dependencies
- Depends on: Task 3 — Add API client functions and React Query hooks for remediation endpoints
