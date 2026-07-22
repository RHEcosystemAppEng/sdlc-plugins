## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types and create API client functions to fetch data from the new backend endpoints. Also create React Query hooks that wrap these client functions for use in dashboard components.

## Files to Modify
- `src/api/models.ts` — add RemediationSummary, SeverityStatusCount, ProductRemediation, and PaginatedProductRemediation interfaces
- `src/api/rest.ts` — add fetchRemediationSummary() and fetchRemediationByProduct() API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook for GET /api/v2/remediation/summary
- `src/hooks/useRemediationByProduct.ts` — React Query hook for GET /api/v2/remediation/by-product with filter parameters

## Implementation Notes
Add TypeScript interfaces to `src/api/models.ts` following the existing pattern (e.g., interfaces for SBOM and Advisory response types already defined there). Create API client functions in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`, following the pattern of existing functions like `fetchSboms()` and `fetchAdvisories()`. Create React Query hooks in `src/hooks/` following the pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` — use `useQuery` with typed return values and query key arrays.

Per CONVENTIONS.md §API layer: Axios client in src/api/client.ts, typed functions in src/api/rest.ts, React Query hooks in src/hooks/.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` file scope.

Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` file scope.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchSboms()` — reference for API client function pattern
- `src/hooks/useSboms.ts` — reference for React Query hook pattern with useQuery
- `src/api/models.ts` — existing interfaces to follow for type definition style

## Acceptance Criteria
- [ ] RemediationSummary interface matches the backend response structure (severity x status counts)
- [ ] ProductRemediation interface includes total, open, and resolved count fields
- [ ] API client functions use the Axios instance and return typed responses
- [ ] React Query hooks expose loading, error, and data states
- [ ] By-product hook accepts filter parameters (product, severity, status)

## Test Requirements
- [ ] Unit tests for API client functions with mocked Axios responses
- [ ] Unit tests for React Query hooks using renderHook with mock data

## Dependencies
- Depends on: Task 3 — Create remediation API endpoints (API contract must be defined)
