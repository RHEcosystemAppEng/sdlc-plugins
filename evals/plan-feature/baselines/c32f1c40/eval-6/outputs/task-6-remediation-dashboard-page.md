## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Create the remediation dashboard page at `/remediation` with summary cards showing total Open, In Progress, and Resolved vulnerability counts, and a progress chart showing remediation trend over the past 30 days. This is the primary entry point for security managers tracking remediation SLAs and engineering leads prioritizing fix work.

## Files to Create
- `src/pages/RemediationDashboard/RemediationDashboard.tsx` -- main dashboard page component with summary cards and progress chart
- `src/pages/RemediationDashboard/components/SummaryCards.tsx` -- summary card components displaying open, in-progress, and resolved counts by severity
- `src/pages/RemediationDashboard/components/ProgressChart.tsx` -- progress chart component showing remediation trend over time

## Files to Modify
- `src/routes.tsx` -- add route definition for /remediation path pointing to RemediationDashboard (lazy-loaded)
- `src/App.tsx` -- add navigation link for the remediation dashboard in the app navigation

## Implementation Notes
- Per frontend conventions: each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components. Follow the pattern in `src/pages/SbomListPage/`.
- Per frontend conventions: PatternFly 5 for all UI components. Use PF5 Card components for summary cards, PF5 Grid/Gallery for layout.
- Per frontend conventions: React Router v6 with lazy-loaded page components. Add a lazy import in `src/routes.tsx` following the existing pattern.
- Per frontend conventions: naming uses PascalCase for components, kebab-case for directories (but existing pages use PascalCase directories -- follow the existing pattern: `SbomListPage/`, `AdvisoryListPage/`).
- Use the `useRemediationSummary` hook (from Task 5) to fetch summary data for the cards.
- Use the existing `SeverityBadge` component (`src/components/SeverityBadge.tsx`) for displaying severity levels in the summary cards.
- Use the existing `LoadingSpinner` component (`src/components/LoadingSpinner.tsx`) for loading states.
- Use the existing `EmptyStateCard` component (`src/components/EmptyStateCard.tsx`) for empty data states.
- For the progress chart, use a charting library compatible with PatternFly (e.g., PatternFly Charts or Victory). Show remediation counts over the past 30 days.
- Constraints: per docs/constraints.md section 2, commit messages must follow Conventional Commits format and reference TC-9006. Per section 5, changes must be scoped to the files listed.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` -- SBOM list page. Reference for page structure, PatternFly layout, and data-fetching patterns.
- `src/components/SeverityBadge.tsx` -- severity level badge component. Reuse directly for displaying severity indicators in summary cards.
- `src/components/LoadingSpinner.tsx` -- loading indicator. Reuse for loading states while data is being fetched.
- `src/components/EmptyStateCard.tsx` -- empty state placeholder. Reuse when no remediation data is available.
- `src/utils/severityUtils.ts` -- severity level ordering and color mapping. Reuse for ordering severity levels in summary cards.

## Acceptance Criteria
- [ ] Dashboard page is accessible at /remediation route
- [ ] Summary cards display total Open, In Progress, and Resolved vulnerability counts
- [ ] Summary cards break down counts by severity level (Critical, High, Medium, Low)
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Page shows loading state while data is being fetched
- [ ] Page shows empty state when no remediation data exists
- [ ] Navigation includes a link to the remediation dashboard
- [ ] Page is lazy-loaded following existing routing pattern

## Test Requirements
- [ ] Unit test verifying summary cards render with correct counts from mock data
- [ ] Unit test verifying progress chart renders with trend data
- [ ] Unit test verifying loading spinner displays while data is loading
- [ ] Unit test verifying empty state displays when no data is available

## Verification Commands
- `npx tsc --noEmit` -- TypeScript compilation succeeds
- `npx vitest run --reporter=verbose -- RemediationDashboard` -- dashboard tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 5 -- Add remediation API types, client functions, and React Query hooks
