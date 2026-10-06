## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for remediation API response types, Axios API client functions, and React Query hooks for the remediation summary and by-product endpoints. This task establishes the data-fetching layer consumed by the remediation dashboard page (Tasks 6 and 7).

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces for RemediationSummary and ProductRemediation response types
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook wrapping fetchRemediationSummary()
- `src/hooks/useRemediationByProduct.ts` -- React Query hook wrapping fetchRemediationByProduct()

## Implementation Notes
Per CONVENTIONS.md "API layer": follow the Axios client pattern in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, and React Query hooks in `src/hooks/`. See `src/api/rest.ts::fetchSboms()` and `src/hooks/useSboms.ts` for reference implementations.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.

Per CONVENTIONS.md "State management": use React Query (TanStack Query) for server state. Each hook should use `useQuery` with appropriate query keys for cache management.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook scope.

Per CONVENTIONS.md "Naming": use camelCase for hooks and utility functions (e.g., `useRemediationSummary`, `fetchRemediationSummary`).
Applies: convention has no file-type restriction (broadly applicable).

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `RemediationSummary` with severity x status count matrix. Severity levels: Critical, High, Medium, Low. Status values: Open, In Progress, Resolved. See `modules/fundamental/src/remediation/model/summary.rs` in trustify-backend.
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `PaginatedResults<ProductRemediation>` with `{ items: ProductRemediation[], total: number }`. Each item has product identifier, total, open, and resolved counts. See `modules/fundamental/src/remediation/model/by_product.rs` in trustify-backend.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Relevant constraints from `docs/constraints.md`:
- Per SS5.3: Implementation must follow the patterns referenced in these Implementation Notes.
- Per SS5.4: Reuse existing API client infrastructure -- do not create a separate Axios instance.

## Reuse Candidates
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors (reuse for all API calls)
- `src/api/rest.ts::fetchSboms` -- reference implementation for a typed GET API function
- `src/api/models.ts` -- existing TypeScript interfaces to follow naming and structure patterns
- `src/hooks/useSboms.ts` -- reference implementation for a React Query useQuery hook
- `src/hooks/useAdvisories.ts` -- reference implementation for a list-based React Query hook

## Acceptance Criteria
- [ ] RemediationSummary TypeScript interface matches the backend response shape (severity x status counts)
- [ ] ProductRemediation TypeScript interface matches the backend per-product response shape
- [ ] fetchRemediationSummary() calls `GET /api/v2/remediation/summary` and returns typed data
- [ ] fetchRemediationByProduct() calls `GET /api/v2/remediation/by-product` with pagination params and returns typed data
- [ ] useRemediationSummary hook provides loading, error, and data states via React Query
- [ ] useRemediationByProduct hook provides loading, error, and data states with pagination support

## Test Requirements
- [ ] Unit test for fetchRemediationSummary() verifying correct URL and response parsing
- [ ] Unit test for fetchRemediationByProduct() verifying correct URL with pagination parameters
- [ ] Unit test for useRemediationSummary hook verifying React Query integration
- [ ] Unit test for useRemediationByProduct hook verifying React Query integration with pagination

## Dependencies
- Depends on: Task 2 -- Add remediation summary endpoint (backend API must exist)
- Depends on: Task 3 -- Add remediation by-product endpoint (backend API must exist)

## Parent Epic
TC-9008
