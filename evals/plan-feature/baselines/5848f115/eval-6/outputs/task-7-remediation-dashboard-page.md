# Task 7 — Add remediation dashboard page with summary cards, progress chart, and filterable table

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Implement the main remediation dashboard page at `/remediation` with three sections: summary cards showing total Open, In Progress, and Resolved counts; a progress chart showing remediation trend over the past 30 days; and a filterable vulnerability table with severity, product, and status filters. The page uses PatternFly 5 components and consumes the React Query hooks created in Task 6.

## Files to Create
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` — Main dashboard page component with summary cards, progress chart, and filterable vulnerability table
- `src/pages/RemediationDashboardPage/RemediationDashboardPage.test.tsx` — Unit tests for the dashboard page
- `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` — Summary cards component showing Open, In Progress, Resolved counts using PatternFly Card components
- `src/pages/RemediationDashboardPage/components/RemediationChart.tsx` — Progress chart component showing 30-day remediation trend
- `src/pages/RemediationDashboardPage/components/VulnerabilityTable.tsx` — Filterable vulnerability table component with severity, product, and status filter dropdowns

## Files to Modify
- `src/routes.tsx` — Add route definition for `/remediation` mapping to RemediationDashboardPage with lazy loading

## Implementation Notes
- Follow the page structure pattern from `src/pages/SbomListPage/SbomListPage.tsx`: main page component in a named directory with a `components/` subdirectory for page-specific components.
- Use PatternFly 5 components throughout:
  - `Card`, `CardTitle`, `CardBody` for summary cards
  - `Table`, `Thead`, `Tbody`, `Tr`, `Th`, `Td` for the vulnerability table
  - `Toolbar`, `ToolbarContent`, `ToolbarItem` with filter dropdowns for table filtering
  - `Select` / `SelectOption` for filter dropdowns (severity, product, status)
- For the progress chart, use a PatternFly-compatible charting library or a lightweight chart component. The chart shows remediation status counts over a 30-day period.
- The filterable vulnerability table should use the `FilterToolbar` component from `src/components/FilterToolbar.tsx` as a reference for filter implementation.
- Use the `SeverityBadge` component from `src/components/SeverityBadge.tsx` to render severity levels in the table.
- Use `LoadingSpinner` from `src/components/LoadingSpinner.tsx` while data is loading.
- Use `EmptyStateCard` from `src/components/EmptyStateCard.tsx` when no data is available.
- Severity values (Critical/High/Medium/Low) ordering and color mapping should use the utilities from `src/utils/severityUtils.ts`.
- Route definition in `src/routes.tsx` should use lazy loading following the pattern of existing routes (React Router v6 with `React.lazy`).
- The dashboard must handle up to 10,000 tracked vulnerabilities without performance degradation per the non-functional requirements.
- Per Key Conventions (Component library): all UI components use PatternFly 5 equivalents.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` file scope.
- Per Key Conventions (Page structure): each page gets its own directory under `src/pages/` with a main component, optional test file, and `components/` subdirectory for page-specific components.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` page file scope.
- Per Key Conventions (Naming): PascalCase for components.
  Applies: task creates `src/pages/RemediationDashboardPage/components/SummaryCards.tsx` matching the convention's `.tsx` file scope.
- Per Key Conventions (State management): React Query (TanStack Query) for server state; no Redux.
  Applies: task creates `src/pages/RemediationDashboardPage/RemediationDashboardPage.tsx` matching the convention's `.tsx` file scope.

## Reuse Candidates
- `src/pages/SbomListPage/SbomListPage.tsx` — Page layout and structure pattern with table and filters
- `src/components/FilterToolbar.tsx` — Reusable filter toolbar pattern with PatternFly
- `src/components/SeverityBadge.tsx` — Severity level badge for rendering in the vulnerability table
- `src/components/EmptyStateCard.tsx` — Empty state placeholder for no-data case
- `src/components/LoadingSpinner.tsx` — Loading indicator while data is being fetched
- `src/utils/severityUtils.ts` — Severity level ordering and color mapping utilities

## Acceptance Criteria
- [ ] Dashboard page renders at `/remediation` with summary cards showing Open, In Progress, and Resolved counts
- [ ] Progress chart displays remediation trend over the past 30 days
- [ ] Filterable vulnerability table renders with columns for vulnerability details
- [ ] Filter dropdowns for severity, product, and status filter the table correctly
- [ ] Loading state shows a spinner while data is being fetched
- [ ] Empty state is displayed when no vulnerability data is available
- [ ] Page handles up to 10,000 vulnerabilities without visible performance degradation

## Test Requirements
- [ ] Test: dashboard page renders summary cards with correct counts from mock data
- [ ] Test: filter dropdowns update the displayed vulnerability table
- [ ] Test: loading state is shown while hooks are fetching data
- [ ] Test: empty state is shown when no data is returned
- [ ] Test: severity badges render with correct colors for each severity level

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 6 — Add remediation API layer (types, client, hooks)

## Parent Epic
TC-9006: trustify-ui
