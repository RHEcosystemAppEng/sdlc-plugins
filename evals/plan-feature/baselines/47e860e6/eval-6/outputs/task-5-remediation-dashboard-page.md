## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards (total
Open, In Progress, Resolved) and a remediation progress chart (TC-9006, UC-1 steps
1–3). The page provides the layout container into which the filterable vulnerability
table (Task 6) is placed.

Note: the Feature asks for the chart to show a trend over the past 30 days. The
backend has no historical status data and the Feature forbids new tables, so the
30-day trend is an open question on TC-9006 (see impact map). This task renders the
current status distribution per severity (stacked bar) from the summary endpoint;
the trend view will be added once a data source is agreed.

Parent Epic: TC-9006: trustify-ui

## Files to Modify
- `src/routes.tsx` — add lazy-loaded `/remediation` route
- `src/App.tsx` — add navigation entry for the remediation dashboard (if nav is defined here)

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — page component (summary cards + chart + table slot)
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page tests
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — Open/In Progress/Resolved cards
- `src/pages/RemediationDashboardPage/components/RemediationProgressChart.tsx` — status-by-severity progress chart

## Implementation Notes
- Data from `useRemediationSummary()` (Task 4, `src/hooks/useRemediationSummary.ts`). Show `LoadingSpinner` (`src/components/LoadingSpinner.tsx`) while loading and `EmptyStateCard` (`src/components/EmptyStateCard.tsx`) when all counts are zero. On fetch error show a PatternFly error state — never render zero-valued cards for a failed request.
- Cards: PatternFly 5 `Card` in a `Gallery`/`Flex` layout. Chart: `@patternfly/react-charts` `ChartBar` / `ChartStack` with severity colors from `src/utils/severityUtils.ts` and ordering via its severity ordering helper.
- **Backend API contract:** `GET /api/v2/remediation/summary` — `{ total: { open, in_progress, resolved }, by_severity: [{ severity, open, in_progress, resolved }] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`). Verify against the backend repo during implementation using the implement-task cross-repo API verification step.
- API status keys are snake_case (`in_progress`); map to display labels in the UI: `{ open: "Open", in_progress: "In Progress", resolved: "Resolved" }`.
- Per CONVENTIONS.md §Page structure: page directory under `src/pages/` with main component, test file, and `components/` subdirectory. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `src/pages/` scope. Example: `src/pages/SbomDetailPage/`.
- Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route definition scope. Example: existing page entries in `src/routes.tsx`.
- Per CONVENTIONS.md §Component library: use PatternFly 5 components for all UI. Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` matching the convention's `.tsx` UI component scope. Example: `src/pages/SbomDetailPage/components/SbomMetadata.tsx`.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's unit test scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx`.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR `--base main` and Jira PR link; §5 scope, inspect-before-modify, reuse shared components.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading state
- `src/components/EmptyStateCard.tsx` — empty state
- `src/components/SeverityBadge.tsx` — severity labelling in chart legend
- `src/utils/severityUtils.ts` — severity ordering and color mapping

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the dashboard page (lazy-loaded route)
- [ ] Three summary cards display total Open, In Progress, and Resolved counts from the summary endpoint
- [ ] Progress chart shows Open/In Progress/Resolved per severity in Critical→Low order with severity colors
- [ ] Loading, empty, and error states render correctly; a failed request shows an error state, not zero counts
- [ ] Page is reachable from the application navigation

## Test Requirements
- [ ] Page test: renders card counts from MSW fixture data
- [ ] Page test: shows loading spinner before data resolves
- [ ] Page test: shows empty state when all counts are zero
- [ ] Page test: shows error state when the summary endpoint returns 500

## Verification Commands
- `npm run test -- RemediationDashboardPage` — page tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 4 — Add remediation API client functions, types, and React Query hooks
