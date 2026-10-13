## Repository
trustify-ui

## Target Branch
main

## Parent Epic
TC-9006: trustify-ui

## Description
Add TypeScript interfaces for the remediation API response types, Axios client functions to call the two new backend endpoints, and React Query hooks for data fetching. This establishes the frontend data layer that the dashboard page components will consume.

## Files to Modify
- `src/api/models.ts` — Add `RemediationSummary`, `RemediationStatusCount`, `ProductRemediation`, and related TypeScript interfaces matching the backend response shapes
- `src/api/rest.ts` — Add `fetchRemediationSummary()` and `fetchRemediationByProduct()` client functions using the Axios instance from `src/api/client.ts`

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()` with appropriate query key and stale time
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()` with pagination parameter support and query key including page/filter params

## Implementation Notes
Follow the existing API layer pattern: typed interfaces in `models.ts`, Axios functions in `rest.ts`, React Query hooks in `src/hooks/`.

- Model interfaces should match the backend `RemediationSummary` and `ProductRemediation` struct shapes. Reference existing interfaces in `src/api/models.ts` for naming and structure conventions
- Client functions should use the shared Axios instance from `src/api/client.ts` which already has base URL and auth interceptors configured
- Hook naming follows camelCase convention: `useRemediationSummary`, `useRemediationByProduct`
- Follow the hook pattern in `src/hooks/useSboms.ts` and `src/hooks/useAdvisories.ts` for query key structure and error handling
- The `useRemediationByProduct` hook should accept pagination parameters (page, perPage) and optional filter parameters (severity, status), including them in the query key so React Query refetches when filters change
- Set `staleTime` to 60 seconds for the summary hook since remediation data changes infrequently

Per CONVENTIONS.md §API Layer: use Axios client in `src/api/client.ts`, typed functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` scope.

Per CONVENTIONS.md §Naming: use camelCase for hooks and utilities. Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's `.ts` scope.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for all API calls
- `src/api/models.ts` — Existing TypeScript interfaces; follow same patterns for new remediation types
- `src/hooks/useSboms.ts` — React Query hook pattern with query key and options; replicate for remediation hooks
- `src/hooks/useAdvisories.ts` — React Query hook with filtering support; reference for by-product hook filter params

## Acceptance Criteria
- [ ] `RemediationSummary` interface models severity-by-status matrix with counts
- [ ] `ProductRemediation` interface models per-product breakdown with total, open, in-progress, and resolved counts
- [ ] `fetchRemediationSummary()` calls `GET /api/v2/remediation/summary` and returns typed response
- [ ] `fetchRemediationByProduct()` calls `GET /api/v2/remediation/by-product` with pagination parameters and returns typed paginated response
- [ ] `useRemediationSummary` hook returns query result with loading, error, and data states
- [ ] `useRemediationByProduct` hook accepts pagination and filter parameters, refetches on parameter changes

## Test Requirements
- [ ] Unit test for `useRemediationSummary` hook verifying data fetching with MSW mock handler
- [ ] Unit test for `useRemediationByProduct` hook verifying pagination parameter forwarding
- [ ] MSW handlers added to `tests/mocks/handlers.ts` for both remediation endpoints

## Dependencies
- Depends on: Task 2 — Add remediation REST endpoints for summary and by-product breakdown
