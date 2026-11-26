## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` for TC-9006 with summary cards (total Open, In Progress, Resolved) and a progress chart showing the remediation trend over the past 30 days (UC-1). The page also hosts a product filter (UC-2) that scopes the cards and chart to a single product. The filterable vulnerability table is added to this page in Task 7.

## Files to Modify
- `src/routes.tsx` — add the lazy-loaded `/remediation` route
- `src/App.tsx` — add a "Remediation" navigation entry if navigation is defined here (inspect before modifying)

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — page component: product filter, summary cards, progress chart, table slot
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page tests
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — PF5 `Card`s for Open / In Progress / Resolved totals
- `src/pages/RemediationDashboardPage/components/RemediationTrendChart.tsx` — 30-day trend chart (PatternFly Charts)

## Implementation Notes
- No Figma design is attached to TC-9006; build with standard PatternFly 5 layout (`PageSection`, `Gallery`/`Grid`, `Card`, `CardTitle`, `CardBody`) and `@patternfly/react-charts` (`Chart`, `ChartLine` or `ChartStack`/`ChartArea`) for the trend.
- Data: `useRemediationSummary(product)` and `useRemediationTrend({ days: 30, product })` from Task 5; product dropdown options from `useRemediationByProduct()`.
- Display text vs API values: the API returns snake_case status keys (`open`, `in_progress`, `resolved`) and lowercase severities. Frontend label mapping needed: `{ open: "Open", in_progress: "In Progress", resolved: "Resolved" }`. For severities reuse `src/utils/severityUtils.ts` ordering/colors and `src/components/SeverityBadge.tsx` rather than redefining them.
- Loading/empty/error states: reuse `src/components/LoadingSpinner.tsx` and `src/components/EmptyStateCard.tsx`. When a query errors, show an error state — do not render zeros as if there were no vulnerabilities.
- Store the selected product in URL search params so the filtered view is shareable and consumed by the table in Task 7.
- Data component rendering scope: summary cards and trend chart are **aggregated** across the portfolio when no product is selected and **per-context** (filtered by `product`) when a product is selected — pass the `product` param to the API; do not filter client-side.
- Per CONVENTIONS.md §Page structure: page lives in its own directory under `src/pages/` with main component, test file, and `components/` subdirectory; see `src/pages/SbomDetailPage/`.
  Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `src/pages/*` page-component (`.tsx`) scope.
- Per CONVENTIONS.md §Component library: use PatternFly 5 equivalents for all UI components.
  Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` matching the convention's React component (`.tsx`) scope.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components.
  Applies: task modifies `src/routes.tsx` matching the convention's route-definition (`.tsx`) scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW mocks.
  Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.test.tsx` unit-test scope.
- Constraints (docs/constraints.md): §5.1, §5.2 (inspect `routes.tsx`, `App.tsx`, `SbomListPage` before writing), §5.4 (reuse shared components), §5.8 (parity with sibling pages on loading/error states), §2.1–2.3, §3.3 PR `--base main`.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/components/EmptyStateCard.tsx` — empty state
- `src/utils/severityUtils.ts` — severity ordering and color mapping (chart colors)
- `src/pages/SbomListPage/SbomListPage.tsx` — page layout and filter pattern
- `src/hooks/useRemediationSummary.ts`, `src/hooks/useRemediationTrend.ts`, `src/hooks/useRemediationByProduct.ts` — from Task 5

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the dashboard page (lazy-loaded route)
- [ ] Three summary cards show total Open, In Progress, Resolved from the summary endpoint
- [ ] Trend chart renders 30 daily points for Open / In Progress / Resolved
- [ ] Selecting a product updates cards and chart to that product
- [ ] Loading, empty, and error states render with the shared components; API errors are never shown as zero counts

## Test Requirements
- [ ] RTL test: page renders summary card values from MSW fixture
- [ ] RTL test: chart renders with fixture trend data
- [ ] RTL test: selecting a product triggers requests with the `product` param and updates cards
- [ ] RTL test: summary endpoint 500 shows the error state, not zeros

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — page tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 5 — Remediation API client and hooks
