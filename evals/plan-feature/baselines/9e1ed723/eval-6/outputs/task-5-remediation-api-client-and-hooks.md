# Task 5 — Add remediation API client functions, models, and React Query hooks

**Summary:** Add remediation API models, REST functions, and React Query hooks
**Parent Epic:** TC-9006: trustify-ui (Epic group "trustify-ui")

## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add the frontend data layer for the remediation dashboard (TC-9006): TypeScript response types, typed Axios REST functions, and React Query hooks for the three remediation endpoints added in trustify-backend (Tasks 2–4). Also add MSW mock handlers and fixtures so the dashboard components (Tasks 6–7) can be tested without the backend.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `SeverityStatusCounts`, `ProductRemediation`, `RemediationItem`, `RemediationFilters` interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()`, `fetchRemediationByProduct(params)`, `fetchRemediationVulnerabilities(filters, params)`
- `tests/mocks/handlers.ts` — add MSW handlers for `/api/v2/remediation/summary`, `/api/v2/remediation/by-product`, `/api/v2/remediation/vulnerabilities`

## Files to Create
- `src/hooks/useRemediationSummary.ts` — `useQuery` hook for the summary endpoint
- `src/hooks/useRemediationByProduct.ts` — `useQuery` hook for the by-product breakdown
- `src/hooks/useRemediationVulnerabilities.ts` — `useQuery` hook for the filtered vulnerability list (filters and pagination in the query key)
- `tests/mocks/fixtures/remediation.json` — mock summary, by-product, and vulnerability list data

## Implementation Notes
- Manual REST calls are needed: the endpoints are new and not covered by any generated client. Add the functions to `src/api/rest.ts` alongside `fetchSboms()` / `fetchAdvisories()`, using the shared Axios instance in `src/api/client.ts` (base URL and auth interceptors). Do not create a new Axios instance.
- Hooks follow the pattern in `src/hooks/useAdvisories.ts` / `src/hooks/useSboms.ts`. Use query keys such as `["remediation", "summary"]`, `["remediation", "by-product", params]`, and `["remediation", "vulnerabilities", filters, params]` so a filter change refetches.
- MSW handlers follow the existing entries in `tests/mocks/handlers.ts`. Fixtures follow `tests/mocks/fixtures/advisories.json`.
- **Backend API contracts** (from trustify-backend Tasks 2–4, defined in `modules/fundamental/src/remediation/endpoints/`):
  - `GET /api/v2/remediation/summary` — response `{ totals: { open: number, in_progress: number, resolved: number }, by_severity: { severity: "critical"|"high"|"medium"|"low", open: number, in_progress: number, resolved: number }[] }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`, model `modules/fundamental/src/remediation/model/summary.rs`)
  - `GET /api/v2/remediation/by-product?offset={number}&limit={number}` — response `{ items: { product: string, total: number, open: number, in_progress: number, resolved: number }[], total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)
  - `GET /api/v2/remediation/vulnerabilities?severity={string}&product={string}&status={string}&sort={string}&offset={number}&limit={number}` — response `{ items: { advisory_id: string, identifier: string, title: string, severity: string, status: string, product: string, sbom_id: string }[], total: number }` (see `modules/fundamental/src/remediation/endpoints/list.rs`)
  - These contracts come from the backend tasks in the same feature branch. Verify them against the trustify-backend `TC-9006` branch during implementation using the implement-task cross-repo API verification step.
- Per CONVENTIONS.md §API layer: typed API functions go in `src/api/rest.ts` on the `src/api/client.ts` Axios instance, with React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's API-layer (`src/api/*.ts`) scope. Example: `src/hooks/useAdvisories.ts`.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities. Applies: task modifies `src/hooks/useRemediationSummary.ts` matching the convention's hook (`.ts`) scope. Example: `src/hooks/useSbomById.ts`.
- Per CONVENTIONS.md §Testing: use MSW for API mocking. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's test-mock (`tests/**/*.ts`) scope. Example: `tests/mocks/handlers.ts` existing SBOM/advisory handlers.
- Constraints (docs/constraints.md): §2.1–2.3 commit rules; §3.3 `gh pr create --base TC-9006`; §5.1–5.8 code change rules; §1.4–1.6 implement-task scope rules.

## Reuse Candidates
- `src/api/client.ts` — shared Axios instance with auth interceptors
- `src/api/rest.ts::fetchAdvisories` — pattern for typed, paginated REST calls
- `src/hooks/useAdvisories.ts` — React Query list hook pattern
- `tests/mocks/handlers.ts` — existing MSW handler set to extend

## Acceptance Criteria
- [ ] TypeScript interfaces for all three remediation responses are in `src/api/models.ts` and match the backend contracts
- [ ] `fetchRemediationSummary`, `fetchRemediationByProduct`, and `fetchRemediationVulnerabilities` call the correct paths through the shared Axios client
- [ ] Hooks `useRemediationSummary`, `useRemediationByProduct`, and `useRemediationVulnerabilities` expose data/loading/error states, and filter changes trigger a refetch
- [ ] MSW handlers and fixtures exist for all three endpoints
- [ ] `tsc` type check passes

## Test Requirements
- [ ] Unit test: each hook returns fixture data from the MSW handlers
- [ ] Unit test: `useRemediationVulnerabilities` sends the severity/product/status filters as query params
- [ ] Unit test: a hook surfaces an error state when the endpoint returns 500

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/hooks` — hook tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
- Depends on: Task 2 — Add remediation module and GET /api/v2/remediation/summary endpoint
- Depends on: Task 3 — Add GET /api/v2/remediation/by-product endpoint
- Depends on: Task 4 — Add filterable GET /api/v2/remediation/vulnerabilities list endpoint
