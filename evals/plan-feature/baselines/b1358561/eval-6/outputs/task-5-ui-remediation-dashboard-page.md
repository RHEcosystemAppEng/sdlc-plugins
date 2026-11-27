**Summary:** Add /remediation dashboard page with summary cards and remediation trend chart
**Parent Epic:** TC-9102 (TC-9006: trustify-ui)
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Major | **fixVersions:** RHTPA 1.5.0

## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` (TC-9006, UC-1). The page shows summary cards for total Open, In Progress, and Resolved vulnerabilities and a progress chart with the remediation trend over the past 30 days. The filterable vulnerability table is added in Task 6 and will be placed below these components.

No Figma design is attached to TC-9006; layout follows the Feature description and existing PatternFly page patterns.

## Files to Modify
- `src/routes.tsx` — add lazy-loaded route `/remediation` -> `RemediationDashboardPage`

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — page component composing cards and chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page tests
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — Open / In Progress / Resolved cards
- `src/pages/RemediationDashboardPage/components/RemediationTrendChart.tsx` — 30-day trend chart

## Implementation Notes
- Data: `useRemediationSummary()` for cards (`totals.open`, `totals.in_progress`, `totals.resolved`) and `useRemediationTrend(30)` for the chart, both from Task 4 (`src/hooks/`).
- Use PatternFly 5 `Card`/`Gallery` for summary cards and `@patternfly/react-charts` (`Chart`, `ChartLine` or `ChartArea`, `ChartAxis`) for the trend chart. Check `package.json` for `@patternfly/react-charts`; if missing, add it (it is the PF5 equivalent charting package).
- Loading/empty states: reuse `src/components/LoadingSpinner.tsx` and `src/components/EmptyStateCard.tsx`, matching `src/pages/SbomListPage/SbomListPage.tsx`.
- Status labels: map API values `open`/`in_progress`/`resolved` to "Open"/"In Progress"/"Resolved" (mapping introduced in Task 4).
- Data component rendering scope: summary cards and trend chart are **aggregated** across all products (portfolio-wide); when the product filter from Task 6 is applied, cards/chart remain portfolio-wide unless the backend adds product scoping — note this in the PR.
- Per CONVENTIONS.md §Page structure: page directory `src/pages/RemediationDashboardPage/` with main component, test file, and `components/` subdirectory, like `src/pages/SbomDetailPage/`.
  Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `src/pages/` page directory scope.
- Per CONVENTIONS.md §Routing: register a lazy-loaded route in `src/routes.tsx` (React Router v6), matching existing entries.
  Applies: task modifies `src/routes.tsx` matching the convention's routing `.tsx` scope.
- Per CONVENTIONS.md §Component library: use PF5 components only (Card, Gallery, Title, PF charts).
  Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` matching the convention's `.tsx` UI component scope.
- Per CONVENTIONS.md §Naming: PascalCase component files.
  Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationTrendChart.tsx` matching the convention's component `.tsx` naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW handlers from Task 4; follow `src/pages/SbomListPage/SbomListPage.test.tsx`.
  Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's Vitest `.test.tsx` scope.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/components/EmptyStateCard.tsx` — empty state when no vulnerabilities are tracked
- `src/pages/SbomListPage/SbomListPage.tsx` — page layout and loading/error handling pattern
- `src/utils/formatDate.ts` — format trend chart x-axis dates

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders `RemediationDashboardPage` (lazy-loaded)
- [ ] Three summary cards display Open, In Progress, and Resolved totals from the summary endpoint
- [ ] Trend chart renders 30 daily points with Open / In Progress / Resolved series
- [ ] Loading and error/empty states are shown using existing shared components
- [ ] Only PatternFly 5 components are used

## Test Requirements
- [ ] Page test: cards render the fixture counts for Open, In Progress, Resolved
- [ ] Page test: chart renders with trend fixture data
- [ ] Page test: loading spinner shown while pending; error state shown when summary endpoint returns 500
- [ ] Route test: `/remediation` resolves to the dashboard page

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — tests pass

## Dependencies
- Depends on: Task 4 — Add remediation API types, REST client functions, React Query hooks and MSW mocks
