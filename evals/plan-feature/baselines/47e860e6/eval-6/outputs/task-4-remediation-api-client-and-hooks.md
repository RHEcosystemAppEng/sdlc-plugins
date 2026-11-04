## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend API layer for the remediation dashboard (TC-9006): TypeScript
response types, typed REST client functions, React Query hooks for the three new
backend endpoints, and MSW mocks/fixtures for tests.

Parent Epic: TC-9006: trustify-ui

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `ProductRemediation`, `RemediationItem`, `RemediationStatus`, and filter param types
- `src/api/rest.ts` — add `fetchRemediationSummary()`, `fetchRemediationByProduct(params)`, `fetchRemediationVulnerabilities(params)`
- `tests/mocks/handlers.ts` — add MSW handlers for the three remediation endpoints

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for the summary endpoint
- `src/hooks/useRemediationByProduct.ts` — React Query hook for the per-product breakdown
- `src/hooks/useRemediationVulnerabilities.ts` — React Query hook for the filterable vulnerability list (filters/pagination in the query key)
- `tests/mocks/fixtures/remediation.json` — mock summary, by-product and vulnerability list data

## Implementation Notes
- **Backend API contracts** (manual REST calls; there is no generated client for these endpoints):
  - `GET /api/v2/remediation/summary` — response `{ total: { open: number, in_progress: number, resolved: number }, by_severity: Array<{ severity: "critical"|"high"|"medium"|"low", open: number, in_progress: number, resolved: number }> }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`, Task 1)
  - `GET /api/v2/remediation/by-product?offset&limit&sort` — response `{ items: Array<{ product: string, total: number, open: number, in_progress: number, resolved: number }>, total: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`, Task 2)
  - `GET /api/v2/remediation/vulnerabilities?severity&product&status&offset&limit&sort` — response `{ items: Array<{ advisory_id: string, title: string, severity: string, sbom_id: string, product: string, status: "open"|"in_progress"|"resolved" }>, total: number }` (see `modules/fundamental/src/remediation/endpoints/list.rs`, Task 3)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.
- Use the shared Axios instance from `src/api/client.ts`; follow the shape of `fetchAdvisories()` in `src/api/rest.ts`.
- Hooks follow `src/hooks/useAdvisories.ts` / `src/hooks/useSboms.ts`: `useQuery` with a stable query key array (`["remediation", "vulnerabilities", filters]`). Use `placeholderData: keepPreviousData` on the list hook so the table does not flash while filters change.
- Per CONVENTIONS.md §API layer: typed API functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope. Example: `src/hooks/useAdvisories.ts`.
- Per CONVENTIONS.md §Naming: camelCase for hooks (`useRemediationSummary`). Applies: task modifies `src/hooks/useRemediationSummary.ts` matching the convention's hook/utility naming scope. Example: `src/hooks/useSbomById.ts`.
- Per CONVENTIONS.md §Testing: MSW for API mocking. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's test mock scope. Example: `tests/mocks/fixtures/advisories.json`.
- Constraints (docs/constraints.md): §2 commit rules (Conventional Commits, Jira footer, `Assisted-by: Claude Code` trailer); §3 PR `--base main` and Jira PR link; §5 scope to listed files, inspect before modifying, reuse existing client/hooks patterns.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchAdvisories` — pattern for typed list fetch with params
- `src/hooks/useAdvisories.ts` — React Query list hook pattern
- `tests/mocks/handlers.ts` — existing MSW handler registration

## Acceptance Criteria
- [ ] Types in `src/api/models.ts` match the backend response shapes listed above
- [ ] `fetchRemediationSummary`, `fetchRemediationByProduct`, `fetchRemediationVulnerabilities` call the correct paths with correctly serialized query params
- [ ] Three hooks expose `data`, `isLoading`, `error` and include filters/pagination in their query keys
- [ ] HTTP errors propagate to the hook `error` state (not swallowed into empty data)
- [ ] MSW handlers and fixtures exist for all three endpoints

## Test Requirements
- [ ] Unit test (Vitest + MSW): each hook returns fixture data on success
- [ ] Unit test: list hook sends `severity`, `product`, `status`, `offset`, `limit` query params as provided
- [ ] Unit test: a 500 response surfaces as `error` in the hook

## Verification Commands
- `npm run test -- remediation` — hook tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Add remediation module and GET /api/v2/remediation/summary endpoint
- Depends on: Task 2 — Add GET /api/v2/remediation/by-product endpoint
- Depends on: Task 3 — Add GET /api/v2/remediation/vulnerabilities filterable list endpoint
