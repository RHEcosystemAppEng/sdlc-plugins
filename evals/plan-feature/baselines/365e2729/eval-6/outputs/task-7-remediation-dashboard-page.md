# Task 7 — Add /remediation dashboard page with summary cards and progress chart

**Parent Epic:** TC-9006: trustify-ui (<EPIC-UI>)
**Issue type:** Task
**Labels:** ai-generated-jira
**Priority:** Major
**fixVersions:** RHTPA 1.5.0

---

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the remediation dashboard page at `/remediation` (TC-9006, UC-1):
- Summary cards for total Open, In Progress, and Resolved vulnerabilities
- A remediation progress chart that shows the status breakdown per severity

The page provides the layout container that Task 8's vulnerability table is placed in.

**Scope note:** the "trend over the past 30 days" view is excluded from this task. No historical status data source exists yet (see "Excluded requirements" in the TC-9006 impact map). The chart shows the current status distribution from `/summary`.

## Files to Modify
- `src/routes.tsx` — add a lazy-loaded `/remediation` route pointing to `RemediationDashboardPage`
- `src/App.tsx` — add a "Remediation" navigation entry if nav items are defined there (check during implementation)

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — page component (header, summary cards, chart, table slot)
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — page unit tests
- `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` — three PF5 `Card`s (Open / In Progress / Resolved)
- `src/pages/RemediationDashboardPage/components/RemediationProgressChart.tsx` — PF5 stacked bar chart (`@patternfly/react-charts` `ChartStack`/`ChartBar`), with severity on the x-axis and stacks by status

## Implementation Notes
- Data: use `useRemediationSummary()` from Task 6 (`src/hooks/useRemediationSummary.ts`). The cards read `by_status.open`, `by_status.in_progress`, and `by_status.resolved`. The chart reads `by_severity[]`.
- Map API values to display labels: `open` → "Open", `in_progress` → "In Progress", `resolved` → "Resolved"; `critical|high|medium|low` → "Critical|High|Medium|Low". Order the severities and color them with `src/utils/severityUtils.ts` instead of hard-coding them.
- **Data component rendering scope:** the summary cards and progress chart are **aggregated** (portfolio-wide) and are not affected by the table filters in Task 8, matching UC-1. Do not pass the table filter state into `useRemediationSummary`.
- Loading state: `src/components/LoadingSpinner.tsx`. Empty state (total == 0): `src/components/EmptyStateCard.tsx`.
- **Fail-closed rendering:** when `useRemediationSummary` reports `isError`, render an error state (PF5 `Alert` or `EmptyState` with an error variant). Never render the cards with `0` counts on failure, because a zero count on error would wrongly tell security managers that nothing is open.
- No Figma design is available, so use the standard PF5 `PageSection`, `Gallery`/`Grid` with `Card`, and `@patternfly/react-charts`.
- Per CONVENTIONS.md §Page structure: each page gets its own directory under `src/pages/` with a main component, a test file, and a `components/` subdirectory. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's page structure scope. Example: `src/pages/SbomDetailPage/`.
- Per CONVENTIONS.md §Routing: use React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's route definition scope. Example: the existing `SbomListPage` route in `src/routes.tsx`.
- Per CONVENTIONS.md §Component library: all UI uses PatternFly 5 equivalents. Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationSummaryCards.tsx` matching the convention's UI component scope. Example: `src/components/EmptyStateCard.tsx`.
- Per CONVENTIONS.md §Naming: PascalCase for components and kebab-case for directories. Applies: task modifies `src/pages/RemediationDashboardPage/components/RemediationProgressChart.tsx` matching the convention's component naming scope. Example: `src/pages/SbomDetailPage/components/PackageTable.tsx`. (Follow the existing page-directory casing used by `SbomListPage/`.)
- Per CONVENTIONS.md §Testing: use Vitest + RTL with MSW. Applies: task modifies `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` matching the convention's unit test scope. Example: `src/pages/SbomListPage/SbomListPage.test.tsx`.
- Constraints (docs/constraints.md):
  - §2: commit rules.
  - §3: the PR is created with `--base TC-9006` in trustify-ui.
  - §5: changes stay limited to the listed files, and shared components are reused.

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` — loading indicator
- `src/components/EmptyStateCard.tsx` — empty state placeholder
- `src/components/SeverityBadge.tsx` — severity visuals for the chart legend
- `src/utils/severityUtils.ts` — severity ordering and color mapping for chart series
- `src/pages/SbomListPage/SbomListPage.tsx` — page layout pattern

## Acceptance Criteria
- [ ] Navigating to `/remediation` renders the dashboard page (route is lazy-loaded)
- [ ] Three summary cards show the Open, In Progress, and Resolved counts from `/api/v2/remediation/summary`
- [ ] The progress chart shows, for each of Critical/High/Medium/Low, the stacked Open/In Progress/Resolved counts, in severity order
- [ ] A loading spinner is shown while the data loads, and an empty state is shown when total == 0
- [ ] Fail-closed: when the API fails, an error state is shown and no zero-count cards are rendered
- [ ] The page has a clearly marked region where Task 8's vulnerability table is mounted

## Test Requirements
- [ ] Unit test: with MSW fixture data, the cards display the exact fixture counts
- [ ] Unit test: the chart receives four severity groups in the order Critical, High, Medium, Low
- [ ] Unit test: an MSW 500 for `/summary` renders the error state, and the cards with "0" are not present
- [ ] Unit test: a total of 0 renders `EmptyStateCard`
- [ ] Unit test: the `/remediation` route resolves to `RemediationDashboardPage`

## Verification Commands
- `npx vitest run src/pages/RemediationDashboardPage` — tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 6 — Add remediation API models, REST functions and React Query hooks
