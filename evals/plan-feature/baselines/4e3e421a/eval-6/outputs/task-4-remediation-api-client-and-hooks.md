## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend data layer for the TC-9006 remediation dashboard: TypeScript response types, typed REST client functions, React Query hooks, and MSW mock handlers/fixtures for the three new remediation endpoints. The dashboard page (Task 5) and vulnerability table (Task 6) consume these hooks.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `SeverityStatusCounts`, `ProductRemediation`, `RemediationVulnerability`, `RemediationStatus` types
- `src/api/rest.ts` — add `fetchRemediationSummary()`, `fetchRemediationByProduct(params)`, `fetchRemediationVulnerabilities(params)`
- `tests/mocks/handlers.ts` — add MSW handlers for the three remediation endpoints

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query `useQuery` hook for the summary endpoint
- `src/hooks/useRemediationByProduct.ts` — React Query hook for the per-product breakdown (paginated)
- `src/hooks/useRemediationVulnerabilities.ts` — React Query hook for the filtered vulnerability list; filter values are part of the query key
- `tests/mocks/fixtures/remediation.json` — mock data for summary, by-product, and vulnerability list responses

## Implementation Notes
- Follow the API layering in this repo: Axios instance in `src/api/client.ts` → typed functions in `src/api/rest.ts` (pattern: `fetchSboms()`, `fetchAdvisories()`) → hooks in `src/hooks/` (pattern: `src/hooks/useSboms.ts`, `src/hooks/useAdvisories.ts`).
- Query keys: `["remediation", "summary"]`, `["remediation", "by-product", params]`, `["remediation", "vulnerabilities", filters]` so filter changes refetch and the cache is shared across components.
- These are manual REST calls (no generated client covers the new endpoints).

**Backend API contracts** (defined by trustify-backend Tasks 1–3, which are NEW endpoints; contracts come from those task definitions):
- `GET /api/v2/remediation/summary` — response: `{ total: number, by_status: { open: number, in_progress: number, resolved: number }, by_severity: Array<{ severity: "critical" | "high" | "medium" | "low", open: number, in_progress: number, resolved: number, total: number }> }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`, `model/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={number}&limit={number}&sort={string}` — response: `{ items: Array<{ product_id: string, product_name: string, total: number, open: number, in_progress: number, resolved: number }>, total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`, `model/product.rs`)
- `GET /api/v2/remediation/vulnerabilities?severity={string}&product={string}&status={string}&offset={number}&limit={number}&sort={string}` — response: `{ items: Array<{ advisory_id: string, identifier: string, title: string, severity: string, status: "open" | "in_progress" | "resolved", product_id: string, product_name: string, sbom_id: string }>, total: number }` (see `modules/fundamental/src/remediation/endpoints/vulnerabilities.rs`, `model/vulnerability.rs`)

Verify these contracts against the trustify-backend repo during implementation using the implement-task cross-repo API verification step — the backend tasks may have adjusted field names.

- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's `src/api/` and `src/hooks/` scope. Example: `src/hooks/useAdvisories.ts`.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities. Applies: task modifies `src/hooks/useRemediationSummary.ts` matching the convention's hooks (`.ts`) scope. Example: `src/hooks/useSbomById.ts`.
- Per CONVENTIONS.md §Testing: MSW for API mocking. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's test mock scope. Example: `tests/mocks/fixtures/advisories.json`.
- Constraints (docs/constraints.md): Conventional Commits with Jira footer and `Assisted-by: Claude Code` trailer (§2.1–2.3); PR with `--base main`, PR link posted to Jira (§3.2–3.3); scope changes to listed files and reuse existing helpers (§5.1–5.4).

## Reuse Candidates
- `src/api/client.ts` — existing Axios instance with base URL and auth interceptors; must be reused, not re-created
- `src/hooks/useAdvisories.ts` — list `useQuery` hook pattern to copy for the paginated hooks
- `src/hooks/useSbomById.ts` — single-resource `useQuery` pattern for the summary hook
- `tests/mocks/handlers.ts` — existing MSW handler registration

## Acceptance Criteria
- [ ] Types for all three remediation responses exist in `src/api/models.ts` and match the backend contracts
- [ ] `rest.ts` exposes one typed function per endpoint using the shared Axios client
- [ ] Three hooks exist; filter/pagination parameters are included in query keys
- [ ] MSW handlers return fixture data for all three endpoints
- [ ] API errors surface through the hook's `error` state (no swallowed errors returning empty data)

## Test Requirements
- [ ] Unit tests (Vitest) for each hook using MSW: successful fetch returns typed data
- [ ] Unit test: changing filters in `useRemediationVulnerabilities` triggers a new request with the expected query string
- [ ] Unit test: a 500 response from MSW yields the hook's error state

## Verification Commands
- `npm run test -- useRemediation` — hook tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Add remediation module and summary endpoint
- Depends on: Task 2 — Add remediation by-product endpoint
- Depends on: Task 3 — Add remediation vulnerability list endpoint
