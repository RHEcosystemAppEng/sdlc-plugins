<!-- Jira creation metadata (simulated; not part of the description body) -->
<!-- Summary: Add remediation dashboard page with summary cards and progress chart | Simulated key: TC-9107 | Issue type: Task | Parent Epic: TC-9102 (TC-9006: trustify-ui) | Labels: ai-generated-jira | Priority: Major | fixVersions: RHTPA 1.5.0 -->

## Repository
trustify-ui

## Target Branch
main

## Description
Add the remediation dashboard page at `/remediation` (TC-9006, UC-1) with summary cards showing total Open, In Progress, and Resolved counts, and a progress chart showing the remediation trend over the past 30 days. Data comes from `useRemediationSummary` (Task 4). The filterable vulnerability table is added to this page in Task 6.

## Files to Modify
- `src/routes.tsx` — add a lazy-loaded `/remediation` route pointing to `RemediationDashboardPage`

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — page component: layout, loading/error/empty states, summary cards, chart
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page unit tests
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — three PatternFly cards (Open / In Progress / Resolved) with per-severity breakdown
- `src/pages/RemediationDashboardPage/components/RemediationProgressChart.tsx` — 30-day trend chart (open / in progress / resolved series)

## Implementation Notes
**Backend API contracts:**
- `GET /api/v2/remediation/summary?trend_days=30` — response: `{ totals: { open, in_progress, resolved }, by_severity: [...], trend: [{ date, open, in_progress, resolved }] }` (see trustify-backend `modules/fundamental/src/remediation/endpoints/summary.rs`). Consumed via `useRemediationSummary` from `src/hooks/useRemediationSummary.ts` (Task 4) — do not call Axios directly from the page.

Verify this contract against the trustify-backend repo during implementation using the implement-task cross-repo API verification step.

- Page structure mirrors `src/pages/SbomListPage/` and `src/pages/SbomDetailPage/` (main component + `components/` subdirectory + co-located test). Existing page directories use PascalCase (`SbomListPage`), so follow that established pattern for `RemediationDashboardPage`.
- Register the route in `src/routes.tsx` with `React.lazy` like the existing page routes.
- Use PatternFly 5 `Card`, `CardTitle`, `CardBody`, `Gallery`/`Grid` for the summary cards. For the chart use PatternFly charts (`@patternfly/react-charts` `ChartArea`/`ChartLine` + `ChartGroup`); check `package.json` — if `@patternfly/react-charts` is not yet a dependency, add it (and list `package.json` in the PR).
- Reuse `src/components/LoadingSpinner.tsx` for loading, `src/components/EmptyStateCard.tsx` when all counts are zero, and `src/utils/severityUtils.ts` for severity colors/order in the per-severity breakdown. Use `src/utils/formatDate.ts` for chart axis labels.
- Use the status label mapping added in Task 4 (`in_progress` → "In Progress").
- **Error vs empty:** when `useRemediationSummary` is in `isError` state, render an error alert — never render cards with `0` counts on failure. Render the empty state only on a successful response with all-zero totals. (Remediation status depends on advisory correlation being current; zeros shown on failure would mislead SLA reporting.)
- Per CONVENTIONS.md §Page structure: create `src/pages/RemediationDashboardPage/` with a main component, test file, and `components/` subdirectory. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page directory scope. Example: `src/pages/SbomDetailPage/`.
- Per CONVENTIONS.md §Component library: build all UI with PatternFly 5 components (Card, Gallery, Alert, charts). Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` matching the convention's `.tsx` UI component scope. Example: `src/components/FilterToolbar.tsx`.
- Per CONVENTIONS.md §Routing: add a lazy-loaded React Router v6 route. Applies: task modifies `src/routes.tsx` matching the convention's route definition scope. Example: existing page routes in `src/routes.tsx`.
- Per CONVENTIONS.md §Naming: PascalCase for components (`RemediationSummaryCards`, `RemediationProgressChart`). Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationProgressChart.tsx` matching the convention's component naming scope. Example: `src/pages/SbomDetailPage/components/SbomMetadata.tsx`.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's unit test scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx`.
- Commit rules (docs/constraints.md §2), PR rules (§3: `gh pr create --base main`), and code change rules (§5) apply.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/components/SeverityBadge.tsx` — severity badge for the per-severity breakdown in cards
- `src/utils/severityUtils.ts` — severity ordering and color mapping
- `src/utils/formatDate.ts` — date formatting for chart axis
- `src/pages/SbomDetailPage/SbomDetailPage.tsx` — page layout pattern

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders `RemediationDashboardPage` (lazy-loaded)
- [ ] Three summary cards show total Open, In Progress, and Resolved counts from the summary endpoint
- [ ] Progress chart renders 30 daily points for open / in progress / resolved
- [ ] A loading spinner shows while data loads
- [ ] On API error, an error alert is shown and no zero-count cards are rendered
- [ ] On a successful all-zero response, the empty state card is shown
- [ ] All UI uses PatternFly 5 components

## Test Requirements
- [ ] Unit test: page renders the three cards with fixture totals
- [ ] Unit test: chart receives 30 trend points from the fixture
- [ ] Unit test: MSW 500 response renders the error alert and does not render "0" counts
- [ ] Unit test: all-zero fixture renders the empty state
- [ ] Unit test: `/remediation` route resolves to the dashboard page

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — page tests pass
- `npm run build` — build succeeds

## Dependencies
- Depends on: Task 4 — Add remediation API models, client functions, and React Query hooks
