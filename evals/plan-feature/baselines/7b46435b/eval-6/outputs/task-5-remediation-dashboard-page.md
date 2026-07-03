## Repository
trustify-ui

## Target Branch
main

## Description
Create the main remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. The page uses PatternFly 5 components and consumes data from the React Query hooks created in Task 4. This implements UC-1 from the Feature specification (View remediation summary).

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` -- main dashboard page component
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` -- unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` -- summary cards component displaying Open, In Progress, and Resolved counts
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` -- remediation trend chart showing 30-day progress

## Files to Modify
- `src/routes.tsx` -- add /remediation route definition with lazy-loaded RemediationDashboardPage component
- `src/App.tsx` -- add navigation entry for the remediation dashboard (if navigation menu is managed here)

## Implementation Notes
- Follow the page directory structure convention: each page gets its own directory under `src/pages/` with a main component file, an optional test file, and a `components/` subdirectory for page-specific child components.
  Per CONVENTIONS.md section "Page structure": each page gets its own directory under `src/pages/` with main component, test file, and `components/` subdirectory.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page directory scope.

- Use PatternFly 5 components for all UI elements: `Card`, `CardTitle`, `CardBody` for summary cards; `Grid` and `GridItem` for responsive layout; `PageSection` for page structure.
  Per CONVENTIONS.md section "Component library": all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` scope.

- Add a lazy-loaded route in `src/routes.tsx` following the React Router v6 pattern used for existing pages (SbomListPage, AdvisoryListPage).
  Per CONVENTIONS.md section "Routing": React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` scope.

- Consume data from the `useRemediationSummary` hook created in Task 4 for summary card values.

- Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` for loading states while data is fetched.

- Use `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no remediation data is available.

- For the progress chart (ProgressChart.tsx), use PatternFly Charts or a compatible charting library to show the 30-day remediation trend with data points for Open, In Progress, and Resolved counts over time.

- Use `SeverityBadge` from `src/components/SeverityBadge.tsx` if severity indicators appear in the summary section.

- Reference `src/pages/SbomListPage/SbomListPage.tsx` as the established page component pattern showing data fetching, loading states, and error handling.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` -- loading indicator for async data fetch states
- `src/components/EmptyStateCard.tsx` -- empty state placeholder when no remediation data exists
- `src/components/SeverityBadge.tsx` -- severity level badge (Critical/High/Medium/Low) for severity-related displays
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping (useful for chart color coding by severity)
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference page component pattern with data fetching, loading, and error states

## Acceptance Criteria
- [ ] Dashboard page renders at `/remediation` route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Progress chart shows remediation trend over the past 30 days
- [ ] Page handles loading state with LoadingSpinner while data is fetched
- [ ] Page handles empty state with EmptyStateCard when no remediation data exists
- [ ] Navigation entry links to `/remediation` from the main navigation
- [ ] Page is lazy-loaded via React Router for bundle optimization

## Test Requirements
- [ ] Unit test verifying summary cards render correct count values from mock data
- [ ] Unit test verifying LoadingSpinner appears during data fetch
- [ ] Unit test verifying EmptyStateCard renders when no remediation data is returned
- [ ] Unit test verifying the /remediation route renders the RemediationDashboardPage component

## Verification Commands
- `npm run test` -- run unit tests
- `npm run build` -- verify production build succeeds with new page

## Dependencies
- Depends on: Task 4 -- Add remediation API types, client functions, and React Query hooks
