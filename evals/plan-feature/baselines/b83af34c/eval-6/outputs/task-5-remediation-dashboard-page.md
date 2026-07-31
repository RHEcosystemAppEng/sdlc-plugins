## Repository
trustify-ui

## Parent Epic
TC-9008 (TC-9006: trustify-ui)

## Priority
Major (inherited from Feature TC-9006)

## Fix Versions
RHTPA 1.5.0 (inherited from Feature TC-9006)

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing the remediation trend over the past 30 days. The page uses PatternFly 5 components and fetches data via the React Query hooks created in Task 4.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Main dashboard page component with layout, summary cards, and progress chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — PatternFly Card components displaying Open, In Progress, and Resolved counts by severity
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — Trend chart showing remediation progress over time

## Files to Modify
- `src/routes.tsx` — Add `/remediation` route pointing to RemediationDashboardPage (lazy-loaded)
- `src/App.tsx` — Add navigation entry for the remediation dashboard

## Implementation Notes
Follow the page directory structure pattern from `src/pages/SbomListPage/` — each page gets its own directory with a main component and a `components/` subdirectory for page-specific components.

Use PatternFly 5 components: `Card`, `CardBody`, `CardTitle` for summary cards, `Grid` and `GridItem` for layout. For the progress chart, use PatternFly's chart components or a compatible charting library.

Register the route in `src/routes.tsx` following the existing pattern with React Router v6 lazy-loaded components. Add a navigation link using the same pattern as existing pages (SbomListPage, AdvisoryListPage).

Use `src/components/SeverityBadge.tsx` for rendering severity levels in the summary cards. Use `src/components/LoadingSpinner.tsx` for loading states.

Use the severity ordering and color mapping from `src/utils/severityUtils.ts` for consistent severity display across the dashboard.

Per CONVENTIONS.md §Page structure: each page gets its own directory under src/pages/ with components/ subdirectory. Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page scope.

Per CONVENTIONS.md §Component library: all UI components use PatternFly 5. Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component scope.

Per CONVENTIONS.md §Routing: React Router v6 with lazy-loaded page components. Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` routing scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — Renders severity level badges (Critical/High/Medium/Low) with consistent styling
- `src/components/LoadingSpinner.tsx` — Loading indicator for data fetch states
- `src/components/EmptyStateCard.tsx` — Empty state placeholder when no remediation data exists
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping functions

## Acceptance Criteria
- [ ] Dashboard page renders at /remediation route
- [ ] Summary cards display total Open, In Progress, and Resolved counts
- [ ] Summary cards break down counts by severity level (Critical/High/Medium/Low)
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Page uses PatternFly 5 components for all UI elements
- [ ] Loading spinner displays while data is being fetched
- [ ] Empty state renders when no remediation data exists
- [ ] Navigation entry is added for the remediation dashboard

## Test Requirements
- [ ] Unit test verifying summary cards render correct counts from mock data
- [ ] Unit test verifying progress chart renders with trend data
- [ ] Unit test verifying loading state displays LoadingSpinner
- [ ] Unit test verifying empty state displays EmptyStateCard

## Dependencies
- Depends on: Task 4 — remediation-api-client-hooks (provides React Query hooks for data fetching)
