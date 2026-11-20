## Repository
trustify-ui

## Target Branch
main

## Description
Create the TC-9006 remediation dashboard page at `/remediation` with summary cards (total Open, In Progress, Resolved) and a progress chart showing the remediation trend over the past 30 days (UC-1 steps 1–3). The filterable vulnerability table that sits below the cards/chart is delivered in Task 6; this task renders a placeholder slot for it.

## Files to Modify
- `src/routes.tsx` — add a lazy-loaded `/remediation` route pointing to `RemediationDashboardPage`
- `src/App.tsx` — add a "Remediation" navigation entry alongside existing pages (if navigation is defined in the root component)

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — page component composing summary cards, trend chart, and the table slot
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page unit tests
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — PF5 `Card`s for Open / In Progress / Resolved totals
- `src/pages/RemediationDashboardPage/components/RemediationTrendChart.tsx` — 30-day trend chart (PatternFly charts) of open / in-progress / resolved counts

## Implementation Notes
- No Figma design was provided for TC-9006; use standard PatternFly 5 layout (`PageSection`, `Gallery`/`Grid` of `Card`s, PatternFly `Chart` line/area chart) and keep components simple so they can be adjusted when a design arrives.
- Data: `useRemediationSummary()` for cards (use `totals.open`, `totals.in_progress`, `totals.resolved`) and `useRemediationTrend(30)` for the chart — both from Task 4. Map API status keys to labels using the constant added in Task 4 (`in_progress` -> "In Progress").
- Rendering scope: summary cards and trend chart are **aggregated** across all products (portfolio-wide), per UC-1; they are not affected by the table's product filter in Task 6 unless the product owner decides otherwise.
- Loading/empty/error states: reuse `src/components/LoadingSpinner.tsx` while loading and `src/components/EmptyStateCard.tsx` when there are no tracked vulnerabilities; show a PF5 error `Alert` on request failure — never render zero counts on an error response (avoid a silently "green" dashboard).
- Use `src/utils/formatDate.ts` for chart axis labels and `src/utils/severityUtils.ts` color mapping if severity breakdown is shown on cards.
- Follow `src/pages/SbomListPage/SbomListPage.tsx` for page-level structure and `src/pages/SbomDetailPage/components/` for the page-specific components subdirectory layout.
- Performance: dashboard must handle up to 10,000 tracked vulnerabilities; all aggregation is server-side, so the page only renders aggregate numbers and ~30 chart points.
- Per CONVENTIONS.md §Page structure: page gets its own directory under `src/pages/` with main component, test file, and `components/` subdirectory. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `src/pages/` scope. Example: `src/pages/SbomDetailPage/`.
- Per CONVENTIONS.md §Component library: all UI built with PatternFly 5 equivalents. Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` matching the convention's `.tsx` component scope. Example: `src/components/FilterToolbar.tsx`.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route definition scope. Example: existing page entries in `src/routes.tsx`.
- Per CONVENTIONS.md §Naming: PascalCase for components, kebab-case directories per convention. Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationTrendChart.tsx` matching the convention's component naming scope. Example: `src/pages/SbomDetailPage/components/SbomMetadata.tsx`.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW mocks. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's `.test.tsx` scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx`.
- Constraints (docs/constraints.md): §5.1 scope; §5.2 inspect before modifying; §5.4 reuse shared components; §5.8 parity with sibling pages (loading/empty/error handling); §2.1–2.3 commit rules; §3.1–3.3 PR rules (`--base main`).

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/utils/formatDate.ts` — date formatting for chart axis
- `src/utils/severityUtils.ts` — severity ordering and color mapping
- `src/pages/SbomListPage/SbomListPage.tsx` — page layout pattern

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the dashboard page (lazy-loaded route)
- [ ] Three summary cards show total Open, In Progress, and Resolved counts from the summary endpoint
- [ ] The trend chart displays 30 daily points for open / in-progress / resolved
- [ ] Loading state shows `LoadingSpinner`; empty dataset shows `EmptyStateCard`; API failure shows an error alert, not zero counts
- [ ] A navigation entry links to `/remediation`

## Test Requirements
- [ ] Page test: with MSW fixture data, cards render the expected Open / In Progress / Resolved numbers
- [ ] Page test: trend chart renders with fixture data points
- [ ] Page test: when the summary endpoint returns 500, an error alert is displayed and no zero-count cards are shown
- [ ] Page test: empty fixture renders the empty state

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 4 — Add remediation API client, types and React Query hooks
