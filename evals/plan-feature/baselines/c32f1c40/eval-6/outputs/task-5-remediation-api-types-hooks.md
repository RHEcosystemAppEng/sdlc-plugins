## Repository
trustify-ui

## Target Branch
TC-9006

## Description
Add TypeScript interfaces for the remediation API response types, API client functions for fetching remediation data, and React Query hooks for the remediation summary and by-product endpoints. This provides the data-fetching layer that the remediation dashboard page components will consume.

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook for fetching remediation summary data from GET /api/v2/remediation/summary
- `src/hooks/useRemediationByProduct.ts` -- React Query hook for fetching per-product remediation data from GET /api/v2/remediation/by-product with pagination support

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces: RemediationSummaryEntry (severity, status, count), RemediationSummaryResponse (entries array, totals object), ProductRemediation (productName, total, open, resolved), PaginatedProductRemediation
- `src/api/rest.ts` -- add API client functions: fetchRemediationSummary() and fetchRemediationByProduct(params) using the Axios client

## Implementation Notes
- Per frontend conventions: API layer follows Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`. Follow the existing pattern exactly.
- Per frontend conventions: React Query (TanStack Query) for server state. See `src/hooks/useSboms.ts` for the useQuery hook pattern with query keys and options.
- Per frontend conventions: use camelCase for hooks and utility functions, PascalCase for type interfaces.
- Per frontend conventions: mutation pattern uses React Query mutations with `onSuccess` and `queryClient.invalidateQueries()` for cache invalidation. For this task, only read hooks are needed (no mutations).
- The by-product hook should accept pagination parameters (offset, limit) and return paginated results. Follow the pattern in `src/hooks/useSboms.ts` for paginated data fetching.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `{ entries: RemediationSummaryEntry[], totals: { open: number, in_progress: number, resolved: number } }`. Entry shape: `{ severity: string, status: string, count: number }`. Defined in `modules/fundamental/src/remediation/endpoints/summary.rs`.
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `{ items: ProductRemediation[], total: number }` (PaginatedResults). Item shape: `{ product_name: string, total: number, open: number, resolved: number }`. Defined in `modules/fundamental/src/remediation/endpoints/by_product.rs`.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

- Constraints: per docs/constraints.md section 2, commit messages must follow Conventional Commits format and reference TC-9006. Per section 5, changes must be scoped to the files listed.

## Reuse Candidates
- `src/api/rest.ts` -- existing API client functions (fetchSboms, fetchAdvisories). Follow the same pattern for remediation functions.
- `src/api/models.ts` -- existing TypeScript interfaces (SbomSummary, AdvisorySummary). Follow the same typing pattern.
- `src/hooks/useSboms.ts` -- React Query hook for SBOM list with pagination. Reference for useRemediationByProduct implementation.
- `src/hooks/useAdvisories.ts` -- React Query hook for advisory list. Reference for useRemediationSummary implementation.
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors. Use for all API calls.

## Acceptance Criteria
- [ ] TypeScript interfaces for RemediationSummaryEntry, RemediationSummaryResponse, and ProductRemediation are defined in src/api/models.ts
- [ ] fetchRemediationSummary() function is added to src/api/rest.ts
- [ ] fetchRemediationByProduct(params) function with pagination support is added to src/api/rest.ts
- [ ] useRemediationSummary hook fetches and returns summary data via React Query
- [ ] useRemediationByProduct hook fetches and returns paginated product data via React Query
- [ ] All TypeScript types compile without errors

## Test Requirements
- [ ] Unit test for useRemediationSummary hook verifying it calls the correct endpoint and returns typed data
- [ ] Unit test for useRemediationByProduct hook verifying pagination parameter handling
- [ ] Test that hooks handle loading and error states correctly

## Verification Commands
- `npx tsc --noEmit` -- TypeScript compilation succeeds
- `npx vitest run --reporter=verbose -- remediation` -- all remediation hook tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
- Depends on: Task 3 -- Add remediation summary and by-product REST endpoints (API contract dependency)
