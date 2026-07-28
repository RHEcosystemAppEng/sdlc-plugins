## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces, API client functions, and React Query hooks for the remediation backend endpoints. This task establishes the frontend data layer that the dashboard page components will consume in subsequent tasks.

## Files to Create
- `src/hooks/useRemediationSummary.ts` -- React Query hook wrapping fetchRemediationSummary
- `src/hooks/useRemediationByProduct.ts` -- React Query hook wrapping fetchRemediationByProduct

## Files to Modify
- `src/api/models.ts` -- add RemediationSummary and ProductRemediation TypeScript interfaces
- `src/api/rest.ts` -- add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Implementation Notes
- Per CONVENTIONS.md (Key Conventions -- API layer): follow the established pattern of Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, and React Query hooks in `src/hooks/`.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.
- Per CONVENTIONS.md (Key Conventions -- State management): use React Query (TanStack Query) for server state. Do not introduce Redux or other state management.
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.
- Per CONVENTIONS.md (Key Conventions -- Naming): use camelCase for hooks and utilities (e.g., `useRemediationSummary`, `fetchRemediationSummary`).
  Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.
- Model the React Query hooks after existing hooks like `src/hooks/useAdvisories.ts` and `src/hooks/useSboms.ts` for consistent query key naming, error handling, and caching behavior.

**Backend API contracts:**
- `GET /api/v2/remediation/summary` -- response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }` (see `modules/fundamental/src/remediation/endpoints/summary.rs`)
- `GET /api/v2/remediation/by-product?offset={offset}&limit={limit}` -- response shape: `{ items: ProductRemediation[], total: number }` where ProductRemediation = `{ product_name: string, product_id: string, total: number, open: number, resolved: number }` (see `modules/fundamental/src/remediation/endpoints/by_product.rs`)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/hooks/useAdvisories.ts` -- reference React Query hook; follow the same useQuery pattern for query keys, options, and return types
- `src/hooks/useSboms.ts` -- reference React Query hook; follow the same pattern for list-based data fetching
- `src/api/rest.ts::fetchAdvisories()` -- reference API client function; follow the same Axios call pattern with typed response
- `src/api/models.ts` -- existing TypeScript interfaces for API types; follow the same interface naming and structure conventions

## Acceptance Criteria
- [ ] RemediationSummary and ProductRemediation TypeScript interfaces are defined in models.ts
- [ ] fetchRemediationSummary() and fetchRemediationByProduct() functions are implemented in rest.ts
- [ ] useRemediationSummary hook returns summary data using React Query
- [ ] useRemediationByProduct hook returns paginated product data using React Query
- [ ] All types match the backend API response shapes

## Test Requirements
- [ ] Hooks return data correctly when API responds successfully
- [ ] Hooks handle loading and error states properly
- [ ] TypeScript interfaces compile without errors and match expected API shapes

## Dependencies
- Depends on: Task 1 -- Add remediation summary aggregation endpoint (backend API must be defined)
- Depends on: Task 2 -- Add per-product remediation breakdown endpoint (backend API must be defined)
