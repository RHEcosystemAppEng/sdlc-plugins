## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards (total Open, In Progress, Resolved) and a progress chart of remediation status by severity, fulfilling the TC-9006 MVP requirement "Dashboard page at `/remediation` with summary cards and progress chart" (UC-1 steps 1–3). The page hosts the vulnerability table added in Task 6.

## Files to Modify
- `src/routes.tsx` — add a lazy-loaded `/remediation` route pointing to `RemediationDashboardPage`

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — page component: layout, summary cards, chart, table slot
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page unit tests
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — three PF5 cards (Open / In Progress / Resolved)
- `src/pages/RemediationDashboardPage/components/RemediationProgressChart.tsx` — stacked bar chart of status per severity
- `tests/e2e/remediation-dashboard.spec.ts` — Playwright E2E for navigating to `/remediation`

## Implementation Notes
- Page structure mirrors `src/pages/SbomListPage/` and `src/pages/SbomDetailPage/` (main component + test file + `components/` subdirectory).
- Register the route in `src/routes.tsx` using the same lazy-loading pattern as existing pages (React Router v6).
- Data: use `useRemediationSummary()` from Task 4 (`src/hooks/useRemediationSummary.ts`). Show `LoadingSpinner` while loading and `EmptyStateCard` when `total === 0`; show an error state (not zeroed cards) when the request fails, so an outage is never rendered as "0 open vulnerabilities".
- Cards: PF5 `Card` / `CardTitle` / `CardBody`; values from `summary.by_status.open|in_progress|resolved`.
- Chart: PF5 Charts (`@patternfly/react-charts`, `ChartStack` + `ChartBar`) stacking open/in_progress/resolved per severity from `summary.by_severity`. Use `src/utils/severityUtils.ts` for severity ordering and colors.
- Display-label mapping: the API returns lowercase keys (`critical`, `in_progress`); map to "Critical" / "In Progress" etc. Reuse `severityUtils.ts` for severity labels and add a status label map (`open` → "Open", `in_progress` → "In Progress", `resolved` → "Resolved").
- 30-day trend: the feature asks for a trend over time, but no backend data source for historical status exists (see impact map "Open questions"). Implement the chart against current status-by-severity data and leave the trend view for a follow-up once the data source is agreed.
- Backend API contracts used: `GET /api/v2/remediation/summary` — `{ total, by_status: { open, in_progress, resolved }, by_severity: [{ severity, open, in_progress, resolved, total }] }` (see trustify-backend `modules/fundamental/src/remediation/endpoints/summary.rs`). Verify against the backend repo during implementation using the implement-task cross-repo API verification step.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, test file, and `components/` subdirectory. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `src/pages/` scope. Example: `src/pages/SbomDetailPage/`.
- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents. Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` matching the convention's `.tsx` component scope. Example: `src/pages/SbomDetailPage/components/SbomMetadata.tsx`.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route definition scope. Example: existing entries in `src/routes.tsx`.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library for unit tests, Playwright for E2E, MSW for mocking. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's test file scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx`.
- Constraints (docs/constraints.md): Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer (§2.1–2.3); PR with `--base main`, PR link posted to Jira (§3.2–3.3); scope changes to listed files and reuse existing helpers (§5.1–5.4).

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/components/EmptyStateCard.tsx` — empty state when no vulnerabilities are tracked
- `src/components/SeverityBadge.tsx` — severity badge for chart legend / card accents
- `src/utils/severityUtils.ts` — severity ordering and color mapping for the chart
- `src/pages/SbomListPage/SbomListPage.tsx` — page layout reference

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders `RemediationDashboardPage` (lazy-loaded)
- [ ] Three summary cards show Open, In Progress and Resolved counts from the summary endpoint
- [ ] Progress chart shows open/in-progress/resolved per severity in Critical → Low order with severity colors from `severityUtils.ts`
- [ ] Loading, empty, and error states render distinctly; a failed request shows an error, not zero counts
- [ ] API keys are rendered as human-readable labels

## Test Requirements
- [ ] Unit test: page renders three cards with counts from MSW fixture data
- [ ] Unit test: chart receives series ordered by severity rank
- [ ] Unit test: loading spinner while pending; empty state when `total` is 0; error state on 500
- [ ] Playwright E2E (`tests/e2e/remediation-dashboard.spec.ts`): navigate to `/remediation`, assert cards and chart are visible

## Verification Commands
- `npm run test -- RemediationDashboardPage` — page tests pass
- `npx playwright test tests/e2e/remediation-dashboard.spec.ts` — E2E passes

## Dependencies
- Depends on: Task 4 — Add remediation API client types and React Query hooks
