# Task 6 — Add /remediation dashboard page with summary cards and progress chart

**Summary:** Add /remediation dashboard page with summary cards and remediation progress chart
**Parent Epic:** TC-9006: trustify-ui (Epic group "trustify-ui")

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the remediation dashboard page at `/remediation` (TC-9006 requirement 3, UC-1). The page shows:
- Summary cards for total Open, In Progress, and Resolved vulnerabilities (from `GET /api/v2/remediation/summary`)
- A remediation progress chart that breaks down status per severity (Critical/High/Medium/Low) from the same summary data
- A layout slot for the filterable vulnerability table (Task 7)

The 30-day trend over time is excluded from this task. No backend data source for historical status exists, and the NFR forbids new tables (see impact map "Excluded requirements"). The chart component should be easy to extend with a time-series once a data source is agreed.

## Files to Modify
- `src/routes.tsx` — add a lazy-loaded `/remediation` route to `RemediationDashboardPage`
- `src/App.tsx` — add a "Remediation" navigation entry if navigation items are defined in the root component (inspect first)

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — page component: layout, loading/error/empty states
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page tests
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — Open / In Progress / Resolved PatternFly cards
- `src/pages/RemediationDashboardPage/components/RemediationProgressChart.tsx` — status-by-severity progress chart

## Implementation Notes
- Page structure follows `src/pages/SbomListPage/` and `src/pages/SbomDetailPage/` (main component, test file, and `components/` subdirectory for page-specific components).
- Register the route in `src/routes.tsx` with React Router v6 lazy loading, like the existing page routes.
- Get data with `useRemediationSummary` from Task 5 (`src/hooks/useRemediationSummary.ts`). Do not call Axios directly from components.
- Cards: PatternFly 5 `Card` / `CardTitle` / `CardBody` in a `Gallery` or `Grid`. Chart: PatternFly charts (`@patternfly/react-charts`, e.g., `ChartBar` stacked by status, grouped by severity). Get severity colors and ordering from `src/utils/severityUtils.ts`. Do not hardcode colors.
- Loading state: `src/components/LoadingSpinner.tsx`. Empty state (all counts 0): `src/components/EmptyStateCard.tsx`. Error state: show an error, not zero counts, so a failed fetch never looks like "nothing to remediate".
- Display text vs API value mapping: the API returns `in_progress` / `open` / `resolved` and lowercase severities. Map them to "In Progress" / "Open" / "Resolved" and "Critical"/"High"/"Medium"/"Low" for display. Reuse `src/components/SeverityBadge.tsx` / `src/utils/severityUtils.ts` for severity labels.
- **Backend API contracts:**
  - `GET /api/v2/remediation/summary` — response `{ totals: { open: number, in_progress: number, resolved: number }, by_severity: { severity: string, open: number, in_progress: number, resolved: number }[] }` (see trustify-backend `modules/fundamental/src/remediation/endpoints/summary.rs`)
  - Verify the contract against the trustify-backend `TC-9006` branch during implementation using the implement-task cross-repo API verification step.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, a test file, and `components/`. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page (`src/pages/**/*.tsx`) scope. Example: `src/pages/SbomDetailPage/`.
- Per CONVENTIONS.md §Component library: all UI components use PatternFly 5 equivalents. Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` matching the convention's React component (`.tsx`) scope. Example: `src/pages/SbomDetailPage/components/SbomMetadata.tsx`.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's routing (`.tsx`) scope. Example: existing page entries in `src/routes.tsx`.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's unit-test (`.test.tsx`) scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx`.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.3 `gh pr create --base TC-9006`; §5.1–5.8 code change rules; §1.4–1.6 implement-task scope rules.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity label/badge rendering
- `src/utils/severityUtils.ts` — severity ordering and color mapping for chart series
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/hooks/useRemediationSummary.ts` (Task 5) — data hook

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the dashboard page (lazy-loaded route)
- [ ] Summary cards show total Open, In Progress, and Resolved counts from the summary endpoint
- [ ] The progress chart shows status counts per severity in severity rank order with colors from `severityUtils`
- [ ] Loading, empty, and error states are rendered distinctly (an error never shows zero counts)
- [ ] Status and severity API values are shown with human-readable labels

## Test Requirements
- [ ] Page test: renders the three cards with fixture counts
- [ ] Page test: the chart renders one group per severity
- [ ] Page test: shows a loading spinner while fetching and an error state when the summary endpoint returns 500
- [ ] Page test: all-zero summary shows the empty state
- [ ] Route test: `/remediation` resolves to `RemediationDashboardPage`

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — page tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 5 — Add remediation API client functions, models, and React Query hooks
