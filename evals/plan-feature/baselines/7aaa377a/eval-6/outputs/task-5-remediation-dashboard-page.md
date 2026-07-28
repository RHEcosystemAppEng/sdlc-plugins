## Repository
trustify-ui

## Target Branch
main

## Description
Create the remediation dashboard page at `/remediation` with summary cards and a progress chart. The summary cards display total Open, In Progress, and Resolved vulnerability counts. The progress chart shows the remediation trend over the past 30 days. This implements Use Case UC-1 (View remediation summary) from the feature specification.

## Files to Create
- `src/pages/RemediationPage/RemediationPage.tsx` -- main dashboard page component composing SummaryCards and ProgressChart
- `src/pages/RemediationPage/components/SummaryCards.tsx` -- summary cards showing Open, In Progress, and Resolved counts
- `src/pages/RemediationPage/components/ProgressChart.tsx` -- chart showing remediation trend over the past 30 days

## Files to Modify
- `src/routes.tsx` -- add /remediation route definition with lazy-loaded RemediationPage component

## Implementation Notes
- Per CONVENTIONS.md (Key Conventions -- Page structure): each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/RemediationPage/RemediationPage.tsx` matching the convention's `.tsx` file scope.
- Per CONVENTIONS.md (Key Conventions -- Component library): all UI components must use PatternFly 5 equivalents. Use PF5 Card, CardTitle, CardBody for summary cards. Use a PF5-compatible charting solution for the progress chart.
  Applies: task creates `src/pages/RemediationPage/components/SummaryCards.tsx` matching the convention's `.tsx` file scope.
- Per CONVENTIONS.md (Key Conventions -- Routing): use React Router v6 with lazy-loaded page components. Follow the pattern in existing route definitions in `src/routes.tsx`.
  Applies: task modifies `src/routes.tsx` matching the convention's `.tsx` file scope.
- Per CONVENTIONS.md (Key Conventions -- Naming): use PascalCase for components (RemediationPage, SummaryCards, ProgressChart).
  Applies: task creates `src/pages/RemediationPage/RemediationPage.tsx` matching the convention's `.tsx` file scope.
- Use the `useRemediationSummary` hook from Task 4 to fetch summary data.
- Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` for loading states.
- Use `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no data is available.
- Follow the page layout pattern from `src/pages/SbomListPage/SbomListPage.tsx` for overall page structure.
- The dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation (NFR).

## Reuse Candidates
- `src/components/LoadingSpinner.tsx` -- existing loading indicator component; use for data loading states
- `src/components/EmptyStateCard.tsx` -- existing empty state placeholder; use when no remediation data is available
- `src/pages/SbomListPage/SbomListPage.tsx` -- reference page component; follow the same layout structure and data-fetching pattern
- `src/pages/AdvisoryListPage/AdvisoryListPage.tsx` -- another reference page; demonstrates PatternFly page layout conventions
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping; reuse for severity-based visual indicators in summary cards

## Acceptance Criteria
- [ ] /remediation route is registered and loads the RemediationPage
- [ ] Summary cards display total Open, In Progress, and Resolved counts from the API
- [ ] Progress chart shows remediation trend over the past 30 days
- [ ] Loading state is shown while data is being fetched
- [ ] Empty state is shown when no remediation data exists
- [ ] Page handles up to 10,000 vulnerabilities without performance degradation

## Test Requirements
- [ ] RemediationPage renders summary cards with correct counts from mock data
- [ ] RemediationPage shows loading state while data is being fetched
- [ ] RemediationPage shows empty state when API returns no data
- [ ] Progress chart renders with mock trend data

## Dependencies
- Depends on: Task 4 -- Add API types and React Query hooks for remediation endpoints
