<!-- Jira creation metadata (simulated; not part of the description body) -->
<!-- Summary: Add remediation API models, client functions, and React Query hooks | Simulated key: TC-9106 | Issue type: Task | Parent Epic: TC-9102 (TC-9006: trustify-ui) | Labels: ai-generated-jira | Priority: Major | fixVersions: RHTPA 1.5.0 -->

## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend data layer for the remediation dashboard (TC-9006): TypeScript response types, typed API client functions, React Query hooks, and MSW mocks for the three new backend endpoints (`/api/v2/remediation/summary`, `/api/v2/remediation/by-product`, `/api/v2/remediation/vulnerabilities`). Tasks 5 and 6 consume these hooks to render the dashboard. The auto-generated client does not cover these new endpoints, so calls are added manually to `src/api/rest.ts`.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `SeverityStatusCount`, `RemediationTrendPoint`, `ProductRemediation`, `RemediationVulnerability`, `RemediationVulnerabilityFilters` interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()`, `fetchRemediationByProduct()`, `fetchRemediationVulnerabilities()`
- `tests/mocks/handlers.ts` — add MSW handlers for the three remediation endpoints

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for the summary endpoint
- `src/hooks/useRemediationByProduct.ts` — React Query hook for the per-product breakdown
- `src/hooks/useRemediationVulnerabilities.ts` — React Query hook for the filtered vulnerability list (filters + pagination in the query key)
- `src/hooks/useRemediationHooks.test.ts` — unit tests for the three hooks against MSW
- `tests/mocks/fixtures/remediation-summary.json` — mock summary response
- `tests/mocks/fixtures/remediation-by-product.json` — mock per-product response
- `tests/mocks/fixtures/remediation-vulnerabilities.json` — mock vulnerability list response

## Implementation Notes
**Backend API contracts** (from trustify-backend Tasks 1–3):
- `GET /api/v2/remediation/summary?trend_days={number}` — response: `{ totals: { open: number, in_progress: number, resolved: number }, by_severity: { severity: "critical"|"high"|"medium"|"low", open: number, in_progress: number, resolved: number }[], trend: { date: string, open: number, in_progress: number, resolved: number }[] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={n}&limit={n}&sort={s}&severity={s}` — response: `{ items: { product: string, total: number, open: number, in_progress: number, resolved: number }[], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)
- `GET /api/v2/remediation/vulnerabilities?severity={s}&product={s}&status={s}&offset={n}&limit={n}&sort={s}` — response: `{ items: { advisory_id: string, title: string, severity: string, status: "open"|"in_progress"|"resolved", product: string, sbom_id: string }[], total: number }` (see `modules/fundamental/src/remediation/endpoints/list.rs`)

Verify these contracts against the trustify-backend repo during implementation using the implement-task cross-repo API verification step.

- Use the shared Axios instance from `src/api/client.ts`; follow the existing `fetchSboms()` / `fetchAdvisories()` function shape in `src/api/rest.ts`. List responses mirror the backend `PaginatedResults<T>` shape already modeled for SBOMs in `src/api/models.ts` — reuse that generic type rather than defining a new paginated interface.
- Hooks follow `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` (`useQuery` with a stable query key array, e.g., `["remediation", "vulnerabilities", filters]`). Use `keepPreviousData`/`placeholderData` for the paginated vulnerability hook so the table does not flash on page change.
- Hooks must surface `isError`/`error` from React Query unchanged — do not catch and convert failures into empty data, so the dashboard can show an error state instead of misleading zero counts.
- Status values from the API are snake_case (`in_progress`); add the display-label mapping `{ open: "Open", in_progress: "In Progress", resolved: "Resolved" }` alongside the models so Tasks 5 and 6 share it.
- Per CONVENTIONS.md §API layer: add typed API functions in `src/api/rest.ts` using the Axios client from `src/api/client.ts`, and wrap them in React Query hooks under `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope. Example: `src/hooks/useAdvisories.ts`.
- Per CONVENTIONS.md §State management: use React Query (TanStack Query) for server state; no Redux or local caches. Applies: task modifies `src/hooks/useRemediationSummary.ts` matching the convention's server-state hook scope. Example: `src/hooks/useSboms.ts`.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities (`useRemediationSummary`, `fetchRemediationSummary`). Applies: task modifies `src/hooks/useRemediationByProduct.ts` matching the convention's hook naming scope. Example: `src/hooks/useSbomById.ts`.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW for API mocking. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW mock scope. Example: `tests/mocks/fixtures/advisories.json`.
- Commit rules (docs/constraints.md §2), PR rules (§3: `gh pr create --base main`), and code change rules (§5) apply.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchAdvisories` — pattern for a typed list fetch function
- `src/hooks/useAdvisories.ts` — React Query list hook pattern
- `tests/mocks/handlers.ts` — existing MSW handler registration
- `tests/setup.ts` — test render helpers and MSW server setup

## Acceptance Criteria
- [ ] TypeScript interfaces for all three remediation responses exist in `src/api/models.ts` and match the backend contracts
- [ ] `fetchRemediationSummary`, `fetchRemediationByProduct`, `fetchRemediationVulnerabilities` call the correct paths with correctly serialized query parameters
- [ ] `useRemediationSummary`, `useRemediationByProduct`, `useRemediationVulnerabilities` hooks return typed data and include filters/pagination in their query keys
- [ ] Hook errors are exposed via React Query error state (not converted to empty data)
- [ ] MSW handlers and fixtures exist for all three endpoints
- [ ] `npm run build` type-checks without errors

## Test Requirements
- [ ] Unit test: each hook returns fixture data from the MSW handler
- [ ] Unit test: `useRemediationVulnerabilities` sends `severity`, `product`, `status`, `offset`, `limit` query parameters
- [ ] Unit test: a 500 response from the summary handler puts the hook into `isError` state with no data

## Verification Commands
- `npx vitest run src/hooks/useRemediationHooks.test.ts` — all hook tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Add remediation module with summary aggregation endpoint
- Depends on: Task 2 — Add per-product remediation breakdown endpoint
- Depends on: Task 3 — Add filterable remediation vulnerability list endpoint
