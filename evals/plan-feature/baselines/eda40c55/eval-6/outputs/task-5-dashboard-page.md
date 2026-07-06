## Repository
trustify-ui

## Target Branch
main

## Description
Add the remediation dashboard page at `/remediation` with summary cards and a progress chart. The summary cards display total counts for Open, In Progress, and Resolved vulnerabilities. The progress chart shows the remediation trend over the past 30 days. This page serves as the main entry point for the vulnerability remediation tracking feature (TC-9006).

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- Main dashboard page component that renders summary cards and progress chart using data from `useRemediationSummary` hook
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- Unit tests for the dashboard page component
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- Summary cards component displaying Open, In Progress, and Resolved counts using PatternFly Card components
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` -- Progress chart component showing remediation trend over the past 30 days

## Files to Modify
- `src/routes.tsx` -- Add route definition for `/remediation` pointing to lazy-loaded `RemediationDashboardPage`
- `src/App.tsx` -- Add navigation entry for the remediation dashboard (if the app uses a top-level navigation component)

## Implementation Notes
- Follow the page structure pattern: each page gets its own directory under `src/pages/` with a main component and `components/` subdirectory for page-specific components. See `src/pages/SbomListPage/` for the established pattern.
- Summary cards should use PatternFly 5 `Card` components. Reference `src/components/EmptyStateCard.tsx` for PatternFly card usage.
- The progress chart can use PatternFly's chart components or a compatible charting library. Group remediation summary data by status for the cards.
- Use `useRemediationSummary` hook (Task 4) for data fetching. Handle loading state with `LoadingSpinner` from `src/components/LoadingSpinner.tsx` and empty state with `EmptyStateCard` from `src/components/EmptyStateCard.tsx`.
- Route should use lazy loading per React Router v6 pattern. See `src/routes.tsx` for existing route definitions.
- Per CONVENTIONS.md §Page Structure: create the page directory under `src/pages/RemediationDashboardPage/` with main component and `components/` subdirectory. See `src/pages/SbomDetailPage/` for the pattern with sub-components.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's TypeScript/React page file scope.
- Per CONVENTIONS.md §Component Library: all UI components must use PatternFly 5 equivalents. See `src/components/SeverityBadge.tsx` for PatternFly component usage.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's TypeScript/React component file scope.
- Per CONVENTIONS.md §State Management: use React Query for server state (no Redux). Data fetching via hooks from `src/hooks/`. See `src/pages/SbomListPage/SbomListPage.tsx` for the pattern.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's TypeScript/React page file scope.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` -- Loading indicator; reuse for loading state while data fetches
- `src/components/EmptyStateCard.tsx` -- Empty state placeholder; reuse when no remediation data is available
- `src/components/SeverityBadge.tsx` -- Severity level badge; reuse for displaying severity indicators in summary cards
- `src/utils/severityUtils.ts` -- Severity level ordering and color mapping; reuse for chart color coding by severity
- `src/pages/SbomListPage/SbomListPage.tsx` -- Reference for page component structure with data fetching

## Acceptance Criteria
- [ ] Dashboard page is accessible at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart shows remediation trend visualization
- [ ] Page handles loading state with a loading spinner
- [ ] Page handles empty state when no remediation data exists
- [ ] Route is lazy-loaded per React Router v6 conventions

## Test Requirements
- [ ] Unit test: renders summary cards with correct counts from mock data
- [ ] Unit test: renders loading spinner while data is being fetched
- [ ] Unit test: renders empty state when no data is returned
- [ ] Unit test: progress chart renders without errors with valid data

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` -- Expected: all dashboard page tests pass

## Dependencies
- Depends on: Task 4 -- Add API client functions and React Query hooks for remediation endpoints
