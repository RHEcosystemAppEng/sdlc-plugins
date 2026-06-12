# Task 4 — Add comparison API types, client function, and React Query hook

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript type definitions for the SBOM comparison API response, the Axios client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This provides the data layer that the comparison page component will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add fetchSbomComparison() client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for the comparison endpoint

## Implementation Notes
- Add TypeScript interfaces matching the backend response contract. Define interfaces for each diff category:
  - `SbomComparisonResult` — top-level response with six arrays
  - `AddedPackage` — `{ name: string; version: string; license: string; advisory_count: number }`
  - `RemovedPackage` — same shape as AddedPackage
  - `VersionChange` — `{ name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }`
  - `NewVulnerability` — `{ advisory_id: string; severity: string; title: string; affected_package: string }`
  - `ResolvedVulnerability` — `{ advisory_id: string; severity: string; title: string; previously_affected_package: string }`
  - `LicenseChange` — `{ name: string; left_license: string; right_license: string }`
- Follow the existing pattern in `src/api/models.ts` for type definitions.
- Add `fetchSbomComparison(leftId: string, rightId: string)` to `src/api/rest.ts` following the pattern of existing functions like `fetchSboms()`. Use the Axios instance from `src/api/client.ts`.
- The React Query hook should follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. Use `useQuery` with appropriate query key including both SBOM IDs. The hook should accept both IDs as parameters and only enable the query when both are provided.
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` (see Task 2 for the full struct definition, defined in `modules/fundamental/src/sbom/model/comparison.rs`)
  - Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/models.ts` — existing TypeScript interfaces demonstrating the type definition pattern
- `src/api/rest.ts::fetchSboms` — existing API client function demonstrating the Axios call pattern with typed responses
- `src/api/client.ts` — Axios instance with base URL and auth interceptors, used by all API functions
- `src/hooks/useSbomById.ts` — existing React Query hook demonstrating the single-resource query pattern with ID parameter

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in models.ts
- [ ] `fetchSbomComparison()` correctly calls `GET /api/v2/sbom/compare` with left and right query parameters
- [ ] `useSbomComparison()` hook returns loading, error, and data states
- [ ] Hook is disabled (does not fetch) when either SBOM ID is missing
- [ ] All types are exported and available for use by the comparison page component

## Test Requirements
- [ ] Unit test: useSbomComparison hook returns comparison data when both IDs are provided (using MSW mock)
- [ ] Unit test: useSbomComparison hook does not fetch when left ID is missing
- [ ] Unit test: useSbomComparison hook does not fetch when right ID is missing
- [ ] Unit test: useSbomComparison hook handles error response correctly

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint (API contract must be finalized)
