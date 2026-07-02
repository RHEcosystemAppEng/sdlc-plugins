# Task 4: Add remediation API types, client functions, and React Query hooks

Parent Epic: TC-9006: trustify-ui

## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the remediation API response types, Axios client functions for fetching remediation data, and React Query hooks that the dashboard page will consume. This establishes the data-fetching layer for the remediation dashboard.

## Files to Modify
- `src/api/models.ts` — add `RemediationSummary`, `SeverityStatusCount`, and `ProductRemediation` TypeScript interfaces
- `src/api/rest.ts` — add `fetchRemediationSummary()` and `fetchRemediationByProduct()` API client functions

## Files to Create
- `src/hooks/useRemediationSummary.ts` — React Query hook wrapping `fetchRemediationSummary()`
- `src/hooks/useRemediationByProduct.ts` — React Query hook wrapping `fetchRemediationByProduct()` with support for filter and pagination parameters

## Implementation Notes
- Per CONVENTIONS.md §API Layer: define typed API functions in `src/api/rest.ts` using the Axios client from `src/api/client.ts`, and wrap them in React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's .ts scope.
- Per CONVENTIONS.md §State Management: use React Query (TanStack Query) for server state; no Redux. Applies: task creates `src/hooks/useRemediationSummary.ts` matching the convention's .ts scope.
- Per CONVENTIONS.md §Naming: use camelCase for hook files and function names (e.g., `useRemediationSummary`, `fetchRemediationSummary`). Applies: convention has no file-type restriction (broadly applicable).
- Reference `src/hooks/useSboms.ts` for the React Query hook pattern — use `useQuery` with a query key array and the fetch function.
- Reference `src/hooks/useAdvisories.ts` for hooks that accept filter parameters.
- Reference `src/api/rest.ts` existing functions (e.g., `fetchSboms()`, `fetchAdvisories()`) for the Axios GET call pattern.
- `RemediationSummary` interface should contain `counts: SeverityStatusCount[]` where `SeverityStatusCount` has `severity: string`, `status: string`, `count: number`.
- `ProductRemediation` interface should contain `productName: string`, `total: number`, `open: number`, `inProgress: number`, `resolved: number`.
- The `fetchRemediationByProduct()` function should accept optional pagination params (`offset`, `limit`) and an optional `productName` filter.
- Use the Axios instance from `src/api/client.ts` which already has base URL and auth interceptors configured.

## Reuse Candidates
- `src/api/client.ts::client` — preconfigured Axios instance with base URL and auth interceptors; reuse for all API calls
- `src/api/rest.ts::fetchSboms` — reference pattern for typed GET requests with Axios
- `src/hooks/useSboms.ts` — reference pattern for React Query `useQuery` hook structure
- `src/hooks/useAdvisories.ts` — reference pattern for hooks with filter parameters

## Acceptance Criteria
- [ ] `RemediationSummary` and `ProductRemediation` TypeScript interfaces are defined in `src/api/models.ts`
- [ ] `fetchRemediationSummary()` calls `GET /api/v2/remediation/summary` and returns typed `RemediationSummary`
- [ ] `fetchRemediationByProduct()` calls `GET /api/v2/remediation/by-product` with optional query params and returns typed paginated `ProductRemediation[]`
- [ ] `useRemediationSummary` hook returns React Query result with loading, error, and data states
- [ ] `useRemediationByProduct` hook accepts filter/pagination parameters and returns React Query result
- [ ] All functions use the shared Axios client from `src/api/client.ts`

## Test Requirements
- [ ] Unit tests for `fetchRemediationSummary()` and `fetchRemediationByProduct()` verifying correct URL and parameter construction
