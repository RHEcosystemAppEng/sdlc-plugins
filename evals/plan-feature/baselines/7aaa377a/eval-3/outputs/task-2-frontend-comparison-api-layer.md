# Task 2 — Add comparison API types, client function, and React Query hook

## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend API layer for the SBOM comparison feature: TypeScript interfaces for the comparison response, an Axios client function to call the comparison endpoint, and a React Query hook for data fetching. This provides the data-fetching foundation that the comparison page (Task 3) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison API response types (SbomComparisonResult, AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `src/api/rest.ts` — add `fetchSbomComparison(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping `fetchSbomComparison` with `useQuery`, enabled only when both SBOM IDs are provided

## Implementation Notes
- Follow the existing TypeScript interface pattern in `src/api/models.ts` for naming and structure.
- Follow the existing API client function pattern in `src/api/rest.ts` (e.g., `fetchSboms()`) for Axios call structure using the shared `client.ts` instance.
- Follow the existing React Query hook pattern in `src/hooks/useSbomById.ts` for query key naming, return type, and enabled condition.
- The hook should accept `leftId` and `rightId` parameters and only enable the query when both are non-empty strings.
- Use a descriptive query key like `["sbom-comparison", leftId, rightId]` so React Query caches and deduplicates requests correctly.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": 0 }],
    "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "upgrade|downgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "string", "severity": "critical|high|medium|low", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```
  Defined in backend `modules/fundamental/src/sbom/model/comparison.rs` (created in Task 1).

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API client function pattern demonstrating Axios GET call with the shared client instance
- `src/api/models.ts` — existing TypeScript interfaces for SBOM and Advisory types; follow the same naming and export pattern
- `src/hooks/useSbomById.ts` — existing React Query hook pattern with query key naming, conditional enabling, and typed return values
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; import and use for the comparison request

## Acceptance Criteria
- [ ] `SbomComparisonResult` interface is defined in `models.ts` matching the backend response shape with all six diff category arrays
- [ ] `fetchSbomComparison(leftId, rightId)` function exists in `rest.ts` and calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`
- [ ] `useSbomComparison(leftId, rightId)` hook exists and returns typed React Query result
- [ ] Hook is disabled (does not fire a request) when either SBOM ID is empty or undefined
- [ ] Hook uses a query key that includes both SBOM IDs for correct caching

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` constructs the correct URL with query parameters
- [ ] Unit test: `useSbomComparison` hook does not trigger a request when leftId is undefined
- [ ] Unit test: `useSbomComparison` hook does not trigger a request when rightId is undefined
- [ ] Unit test: `useSbomComparison` hook returns comparison data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 1 — Add SBOM comparison diff endpoint (backend API contract must be finalized)
