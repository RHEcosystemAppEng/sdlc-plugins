## Repository
trustify-ui

## Parent Epic
TC-9008 (TC-9006: trustify-ui)

## Priority
Major (inherited from Feature TC-9006)

## Fix Versions
RHTPA 1.5.0 (inherited from Feature TC-9006)

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types, client functions for calling the backend remediation endpoints, and React Query hooks for data fetching. This establishes the data layer that the remediation dashboard page will consume.

## Files to Modify
- `src/api/models.ts` — Add RemediationSummary, SeverityStatusCount, RemediationByProduct, and ProductRemediation TypeScript interfaces
- `src/api/rest.ts` — Add fetchRemediationSummary() and fetchRemediationByProduct() client functions using the Axios instance

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping fetchRemediationSummary()
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping fetchRemediationByProduct() with pagination parameters

## Implementation Notes
Follow the existing API layer pattern: typed interfaces in `src/api/models.ts`, Axios-based client functions in `src/api/rest.ts` using the shared client from `src/api/client.ts`, and React Query hooks in `src/hooks/`.

Model the hooks after `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` — use `useQuery` with typed generics and query keys. The by-product hook should accept pagination parameters similar to the SBOM list hook pattern.

The RemediationSummary interface should model the severity-by-status matrix returned by the backend. The RemediationByProduct interface should extend or follow the pattern used by PaginatedResults on the backend, with a paginated list of ProductRemediation entries.

Per CONVENTIONS.md §API layer: typed API functions in src/api/rest.ts with React Query hooks in src/hooks/. Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` scope.

Per CONVENTIONS.md §State management: React Query for server state, no Redux. Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` hook scope.

## Acceptance Criteria
- [ ] RemediationSummary and RemediationByProduct TypeScript interfaces match the backend API response shapes
- [ ] fetchRemediationSummary() calls GET /api/v2/remediation/summary using the shared Axios client
- [ ] fetchRemediationByProduct() calls GET /api/v2/remediation/by-product with pagination parameters
- [ ] useRemediationSummary hook returns typed query result with loading, error, and data states
- [ ] useRemediationByProduct hook accepts pagination parameters and returns typed paginated results

## Test Requirements
- [ ] Unit test for useRemediationSummary hook with MSW handler returning mock summary data
- [ ] Unit test for useRemediationByProduct hook with MSW handler returning paginated mock data
- [ ] Verify hooks handle loading and error states correctly

## Dependencies
- Depends on: Task 2 — remediation-endpoints (backend API must be defined for type alignment)
