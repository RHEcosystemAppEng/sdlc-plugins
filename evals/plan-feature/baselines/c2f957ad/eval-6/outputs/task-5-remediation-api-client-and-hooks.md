## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend API layer for the TC-9006 remediation dashboard: TypeScript response types, typed REST client functions, and React Query hooks for the four new backend remediation endpoints, plus MSW mock handlers and fixtures so dashboard components can be developed and tested without a live backend. The auto-generated/typed client in `src/api/rest.ts` does not cover these new endpoints, so they are added manually following the existing pattern.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `SeverityStatusCounts`, `ProductRemediation`, `RemediationVulnerability`, `RemediationTrend`, `TrendPoint`, `RemediationStatus`, `RemediationFilters` types
- `src/api/rest.ts` — add `fetchRemediationSummary()`, `fetchRemediationByProduct()`, `fetchRemediationVulnerabilities()`, `fetchRemediationTrend()`
- `tests/mocks/handlers.ts` — add MSW handlers for `/api/v2/remediation/*`

## Files to Create
- `src/hooks/useRemediationSummary.ts` — `useQuery` hook for the summary (optional product filter)
- `src/hooks/useRemediationByProduct.ts` — `useQuery` hook for the per-product breakdown (used to populate the product filter)
- `src/hooks/useRemediationVulnerabilities.ts` — `useQuery` hook for the filterable vulnerability list (filters, sort, pagination in the query key)
- `src/hooks/useRemediationTrend.ts` — `useQuery` hook for the trend series
- `tests/mocks/fixtures/remediation.json` — mock remediation summary, by-product, vulnerability list, and trend data

## Implementation Notes
- Follow `src/api/rest.ts::fetchSboms` / `fetchAdvisories` for client functions using the shared Axios instance in `src/api/client.ts` (auth interceptors and base URL already configured — do not create a new Axios instance).
- Follow `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` for hook structure and query-key conventions; include all filter/sort/pagination params in the query key so filter changes refetch.
- Backend API contracts (planned in trustify-backend Tasks 2–4; source files to be created under `modules/fundamental/src/remediation/endpoints/`):
  - `GET /api/v2/remediation/summary?product={product}` — response `{ total: number, by_status: { open: number, in_progress: number, resolved: number }, by_severity: { severity: "critical"|"high"|"medium"|"low", open: number, in_progress: number, resolved: number, total: number }[] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
  - `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` — response `{ items: { product_id: string, product_name: string, total: number, open: number, in_progress: number, resolved: number }[], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)
  - `GET /api/v2/remediation/vulnerabilities?severity={csv}&product={product}&status={csv}&sort={field:dir}&offset={offset}&limit={limit}` — response `{ items: { advisory_id: string, identifier: string, title: string, severity: string, status: "open"|"in_progress"|"resolved", affected_products: string[], affected_sbom_count: number }[], total: number }` (see `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs`)
  - `GET /api/v2/remediation/trend?days={days}&product={product}` — response `{ points: { date: string, open: number, in_progress: number, resolved: number }[] }` (see `modules/fundamental/src/remediation/endpoints/trend.rs`)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- Per CONVENTIONS.md §API layer: typed API functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`, Axios client from `src/api/client.ts`.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API-layer (`src/api/*.ts`, `src/hooks/*.ts`) scope.
- Per CONVENTIONS.md §Naming: hooks and utilities use camelCase file names (`useRemediationSummary.ts`).
  Applies: task modifies `src/hooks/useRemediationSummary.ts` matching the convention's TypeScript hook/utility (`.ts`) scope.
- Per CONVENTIONS.md §Testing: API mocking via MSW handlers in `tests/mocks/handlers.ts` with fixtures in `tests/mocks/fixtures/`.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW test-mock scope.
- Constraints (docs/constraints.md): §5.1 scope to listed files; §5.2 inspect `rest.ts` and existing hooks before writing; §5.4 reuse the shared Axios client; §2.1–2.3 commit rules; §3.3 PR `--base main`.

## Reuse Candidates
- `src/api/client.ts` — shared Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchAdvisories` — pattern for list fetch functions with query params
- `src/hooks/useAdvisories.ts` — React Query list hook pattern
- `tests/mocks/handlers.ts` — existing MSW handler registration

## Acceptance Criteria
- [ ] Types in `src/api/models.ts` match the backend response shapes listed above
- [ ] Four fetch functions exist in `src/api/rest.ts` and use the shared Axios client
- [ ] Four hooks exist in `src/hooks/` and include filter/pagination params in their query keys
- [ ] MSW handlers return fixture data for all four endpoints

## Test Requirements
- [ ] Unit test (Vitest + MSW): each hook returns fixture data on success
- [ ] Unit test: `useRemediationVulnerabilities` refetches when filters change (distinct query keys)
- [ ] Unit test: hooks surface an error state when the endpoint returns 500

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/hooks` — hook tests pass

## Dependencies
- Depends on: Task 2 — Remediation summary and by-product endpoints
- Depends on: Task 3 — Remediation vulnerability list endpoint
- Depends on: Task 4 — Remediation trend endpoint
