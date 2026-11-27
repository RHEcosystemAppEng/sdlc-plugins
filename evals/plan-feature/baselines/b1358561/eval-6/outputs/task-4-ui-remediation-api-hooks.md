**Summary:** Add remediation API types, REST client functions, React Query hooks and MSW mocks
**Parent Epic:** TC-9102 (TC-9006: trustify-ui)
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Major | **fixVersions:** RHTPA 1.5.0

## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend data layer for the TC-9006 remediation dashboard: TypeScript types for the new backend responses, typed REST functions, React Query hooks, and MSW handlers/fixtures for tests. The remediation endpoints are new, so they are not covered by any generated client and must be called manually through the existing Axios client.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `SeverityStatusCounts`, `ProductRemediation`, `RemediationVulnerability`, `RemediationTrend`, `RemediationFilters` interfaces and `RemediationStatus` type
- `src/api/rest.ts` — add `fetchRemediationSummary()`, `fetchRemediationByProduct()`, `fetchRemediationVulnerabilities(filters)`, `fetchRemediationTrend(days)`
- `tests/mocks/handlers.ts` — add MSW handlers for the four remediation endpoints

## Files to Create
- `src/hooks/useRemediationSummary.ts` — `useQuery` hook for the summary
- `src/hooks/useRemediationByProduct.ts` — `useQuery` hook for per-product breakdown
- `src/hooks/useRemediationVulnerabilities.ts` — `useQuery` hook for the filterable list (filters in the query key)
- `src/hooks/useRemediationTrend.ts` — `useQuery` hook for the trend
- `tests/mocks/fixtures/remediation.json` — mock data for summary, by-product, vulnerabilities and trend

## Implementation Notes
- **Backend API contracts** (from Tasks 2 and 3 in trustify-backend; endpoints are new):
  - `GET /api/v2/remediation/summary` — response `{ totals: { open: number, in_progress: number, resolved: number, total: number }, by_severity: { severity: "critical"|"high"|"medium"|"low", open: number, in_progress: number, resolved: number, total: number }[] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
  - `GET /api/v2/remediation/by-product?offset={number}&limit={number}` — response `{ items: { product_name: string, total: number, open: number, in_progress: number, resolved: number }[], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)
  - `GET /api/v2/remediation/vulnerabilities?severity={string}&product={string}&status={string}&sort={string}&offset={number}&limit={number}` — response `{ items: { advisory_id: string, identifier: string, title: string, severity: string, status: "open"|"in_progress"|"resolved", product_name: string, sbom_id: string }[], total: number }` (see `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs`)
  - `GET /api/v2/remediation/trend?days={number}` — response `{ points: { date: string, open: number, in_progress: number, resolved: number }[] }` (see `modules/fundamental/src/remediation/endpoints/trend.rs`)
  - Verify these contracts against the trustify-backend repo at implementation time using the implement-task cross-repo API verification step.
- **Display text vs API value:** API returns `snake_case` enum values. Frontend label mapping needed: status `{ open: "Open", in_progress: "In Progress", resolved: "Resolved" }`; severity `{ critical: "Critical", high: "High", medium: "Medium", low: "Low" }` — reuse/extend `src/utils/severityUtils.ts` for severity labels and ordering rather than adding a new map.
- Follow the existing pattern: `fetchAdvisories()` in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`, and `src/hooks/useAdvisories.ts` / `src/hooks/useSboms.ts` for hook shape and query keys.
- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`, typed functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API layer (`src/api/`, `src/hooks/`) scope.
- Per CONVENTIONS.md §State management: server state only via React Query; no Redux or local caches.
  Applies: task modifies `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook scope.
- Per CONVENTIONS.md §Naming: camelCase for hooks (`useRemediationSummary.ts`) and utilities.
  Applies: task modifies `src/hooks/useRemediationVulnerabilities.ts` matching the convention's hook/utility `.ts` naming scope.
- Per CONVENTIONS.md §Testing: MSW for API mocking; add handlers in `tests/mocks/handlers.ts` and fixtures under `tests/mocks/fixtures/` like `advisories.json`.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW test mock scope.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR rules (`--base main`); §5 code change rules.

## Reuse Candidates
- `src/api/client.ts` — configured Axios instance with auth interceptors
- `src/api/rest.ts::fetchAdvisories` — typed REST function pattern
- `src/hooks/useAdvisories.ts` — React Query list hook pattern
- `src/utils/severityUtils.ts` — severity ordering and labels/colors
- `tests/mocks/handlers.ts` / `tests/mocks/fixtures/advisories.json` — MSW handler and fixture pattern

## Acceptance Criteria
- [ ] TypeScript interfaces in `src/api/models.ts` match the backend response shapes above
- [ ] Four REST functions in `src/api/rest.ts` call the correct paths via the shared Axios client
- [ ] Four hooks exist; `useRemediationVulnerabilities` includes filters in its query key so filter changes refetch
- [ ] MSW handlers and fixtures cover all four endpoints
- [ ] `npm run build` / `tsc` passes with no type errors

## Test Requirements
- [ ] Unit test (Vitest + MSW): each hook returns fixture data on success
- [ ] Unit test: `useRemediationVulnerabilities` sends severity/product/status query params from its filters argument
- [ ] Unit test: hooks expose error state when the endpoint returns 500

## Verification Commands
- `npx vitest run src/hooks` — hook tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/remediation/summary and /api/v2/remediation/by-product endpoints
- Depends on: Task 3 — Add filterable remediation vulnerability list and 30-day trend endpoints
