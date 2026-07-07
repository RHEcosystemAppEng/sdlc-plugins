## Repository
trustify-ui

## Target Branch
main

## Description
Create the main remediation dashboard page component with summary cards and a progress chart for the vulnerability remediation tracking dashboard (TC-9006). The page displays:

- Summary cards showing total Open, In Progress, and Resolved vulnerability counts
- A progress chart showing the remediation trend over the past 30 days

This is the primary page component at `/remediation` that security managers will use to track remediation SLAs and engineering leads will use to prioritize fix work.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — main dashboard page component with layout for summary cards and chart
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — summary cards component displaying Open, In Progress, and Resolved counts using PatternFly Card components
- `src/pages/RemediationDashboardPage/components/ProgressChart.tsx` — progress chart component showing remediation trend over the past 30 days

## Implementation Notes
- Follow the page structure convention: each page gets its own directory under `src/pages/` with a main component and a `components/` subdirectory for page-specific components. Reference `src/pages/SbomListPage/` for the established pattern.
- Use PatternFly 5 components for all UI elements:
  - `Card`, `CardTitle`, `CardBody` for summary cards
  - `Grid`, `GridItem` for responsive card layout
  - `PageSection` for page content areas
- Use the `useRemediationSummary` hook from Task 4 to fetch summary data.
- Display loading state using `LoadingSpinner` from `src/components/LoadingSpinner.tsx`.
- Display empty state using `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no vulnerability data exists.
- Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` to render severity levels with appropriate color coding.
- For the progress chart, use a PatternFly-compatible charting library or a simple bar/line chart showing daily remediation counts over 30 days.
- The dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation (NFR).

Per CONVENTIONS.md Section "Component library": all UI components use PatternFly 5 equivalents.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` component file scope.

Per CONVENTIONS.md Section "Page structure": each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page file scope.

Per CONVENTIONS.md Section "Naming": PascalCase for components.
Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` component file scope.

## Reuse Candidates
- `src/components/SeverityBadge.tsx` — severity level badge with color mapping; reuse for severity indicators in summary cards
- `src/components/EmptyStateCard.tsx` — empty state placeholder; reuse when no vulnerability data is available
- `src/components/LoadingSpinner.tsx` — loading indicator; reuse while data is being fetched
- `src/pages/SbomListPage/SbomListPage.tsx` — reference for page structure with data fetching, loading, and empty states
- `src/utils/severityUtils.ts` — severity level ordering and color mapping; reuse for chart color coding

## Acceptance Criteria
- [ ] RemediationDashboardPage renders summary cards showing total Open, In Progress, and Resolved counts
- [ ] ProgressChart shows remediation trend over the past 30 days
- [ ] Page displays loading state while data is being fetched
- [ ] Page displays empty state when no vulnerability data exists
- [ ] Summary cards use PatternFly 5 Card components with responsive grid layout
- [ ] Page handles up to 10,000 vulnerabilities without visible performance degradation
- [ ] Severity indicators use the existing SeverityBadge component

## Test Requirements
- [ ] Verify summary cards render correct counts from API response
- [ ] Verify loading spinner displays while data is loading
- [ ] Verify empty state displays when API returns no data
- [ ] Verify progress chart renders with trend data

## Dependencies
- Depends on: Task 4 — Add remediation API types, client functions, and React Query hooks
