## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend data layer for the TC-9006 remediation dashboard: TypeScript response types, typed REST client functions, and React Query hooks for the four remediation endpoints delivered by the backend (Tasks 2 and 3), plus MSW mock handlers and fixtures so the dashboard page and table (Tasks 5 and 6) can be developed and tested without a live backend.

## Files to Modify
- `src/api/models.ts` — add `RemediationStatus`, `RemediationSummary`, `ProductRemediation`, `RemediationVulnerability`, `RemediationTrendPoint`, and `RemediationVulnerabilityFilters` interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()`, `fetchRemediationByProduct(params)`, `fetchRemediationVulnerabilities(params)`, `fetchRemediationTrend(days)`
- `tests/mocks/handlers.ts` — add MSW handlers for the four `/api/v2/remediation/*` routes

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query `useQuery` hook for the summary endpoint
- `src/hooks/useRemediationByProduct.ts` — React Query hook for the per-product breakdown (paginated)
- `src/hooks/useRemediationVulnerabilities.ts` — React Query hook for the filterable vulnerability list; filters and pagination included in the query key
- `src/hooks/useRemediationTrend.ts` — React Query hook for the trend series
- `tests/mocks/fixtures/remediation.json` — mock summary, by-product, vulnerabilities, and trend data

## Implementation Notes
- Add client functions to `src/api/rest.ts` next to `fetchSboms()` / `fetchAdvisories()`, using the shared Axios instance from `src/api/client.ts` (do not create a new Axios instance).
- Model hooks on `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` (query key structure, `enabled` handling, return shape).
- Include filter values (`severity`, `product`, `status`), `offset`, `limit` and `sort` in the `useRemediationVulnerabilities` query key so filter changes refetch automatically.
- API values are snake_case keys (`open`, `in_progress`, `resolved`); keep the raw API values in the types and expose the display-label mapping (`open` -> "Open", `in_progress` -> "In Progress", `resolved` -> "Resolved") as a typed constant for Tasks 5/6. Severity values must align with `src/utils/severityUtils.ts`.
- Backend API contracts (from trustify-backend analysis — Tasks 2 and 3):
  - `GET /api/v2/remediation/summary` — response `RemediationSummary`: `{ by_severity: { [severity: "critical"|"high"|"medium"|"low"]: { open: number, in_progress: number, resolved: number } }, totals: { open: number, in_progress: number, resolved: number } }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`, model `modules/fundamental/src/remediation/model/summary.rs`)
  - `GET /api/v2/remediation/by-product?offset={number}&limit={number}` — response `{ items: ProductRemediation[], total: number }` where `ProductRemediation = { product: string, total: number, open: number, in_progress: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)
  - `GET /api/v2/remediation/vulnerabilities?severity={string}&product={string}&status={string}&sort={string}&offset={number}&limit={number}` — response `{ items: RemediationVulnerability[], total: number }` where `RemediationVulnerability = { id: string, identifier: string, title: string, severity: string, product: string, status: "open"|"in_progress"|"resolved", affected_sboms: number }` (see `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs`)
  - `GET /api/v2/remediation/trend?days={number}` — response `RemediationTrendPoint[]` = `{ date: string (ISO-8601), open: number, in_progress: number, resolved: number }[]` (see `modules/fundamental/src/remediation/endpoints/trend.rs`)
  - Verify these contracts against the trustify-backend repo during implementation using the implement-task cross-repo API verification step; field names must match the final Rust structs.
- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's API layer (`src/api/*.ts`, `src/hooks/*.ts`) scope. Example: `src/hooks/useAdvisories.ts`.
- Per CONVENTIONS.md §State management: use React Query for server state; no Redux or ad-hoc global stores. Applies: task modifies `src/hooks/useRemediationSummary.ts` matching the convention's hook `.ts` scope. Example: `src/hooks/useSboms.ts`.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities. Applies: task modifies `src/hooks/useRemediationVulnerabilities.ts` matching the convention's hooks/utilities naming scope. Example: `src/hooks/useSbomById.ts`.
- Per CONVENTIONS.md §Testing: use MSW for API mocking with fixtures under `tests/mocks/fixtures/`. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW mock scope. Example: `tests/mocks/fixtures/advisories.json`.
- Constraints (docs/constraints.md): §5.1 scope; §5.2 inspect before modifying; §5.4 reuse the shared Axios client and hook patterns; §2.1–2.3 commit rules; §3.1–3.3 PR rules (`--base main`).

## Reuse Candidates
- `src/api/client.ts` — shared Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchAdvisories` — typed client function pattern
- `src/hooks/useAdvisories.ts` — list query hook pattern
- `src/hooks/useSbomById.ts` — single-object query hook pattern
- `tests/mocks/handlers.ts` — existing MSW handler registration

## Acceptance Criteria
- [ ] TypeScript interfaces for all four remediation responses exist in `src/api/models.ts` and match the backend contracts
- [ ] `src/api/rest.ts` exposes one typed client function per remediation endpoint using the shared Axios client
- [ ] Four React Query hooks exist in `src/hooks/`; `useRemediationVulnerabilities` refetches when filters or pagination change
- [ ] MSW handlers and `tests/mocks/fixtures/remediation.json` serve all four endpoints
- [ ] `tsc` type-check passes

## Test Requirements
- [ ] Hook test: `useRemediationSummary` returns MSW fixture data
- [ ] Hook test: `useRemediationVulnerabilities` sends `severity`, `product`, `status` query params and refetches when they change
- [ ] Hook test: error responses surface as React Query `error` state (not swallowed as empty data)

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/hooks` — hook tests pass

## Dependencies
- Depends on: Task 2 — Add remediation summary and by-product endpoints
- Depends on: Task 3 — Add remediation vulnerabilities list and trend endpoints
