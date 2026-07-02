## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response types, a REST client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This provides the data layer that the comparison page components (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for comparison response types (SbomComparisonResult, PackageDiff, VersionChange, VulnerabilityDiff, LicenseChange)
- `src/api/rest.ts` — Add fetchSbomComparison(leftId, rightId) function calling GET /api/v2/sbom/compare

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping fetchSbomComparison with query key and conditional enabling

## Implementation Notes
- Add interfaces to `src/api/models.ts` following the existing pattern (see SbomSummary, AdvisorySummary interfaces in that file):
  - `SbomComparisonResult` — top-level response with six array fields
  - `PackageDiff` — { name: string, version: string, license: string, advisory_count: number }
  - `VersionChange` — { name: string, left_version: string, right_version: string, direction: "upgrade" | "downgrade" }
  - `VulnerabilityDiff` — { advisory_id: string, severity: string, title: string, affected_package: string } (also used for resolved with previously_affected_package)
  - `LicenseChange` — { name: string, left_license: string, right_license: string }
- `fetchSbomComparison` in `src/api/rest.ts` should use the Axios instance from `src/api/client.ts`, following the pattern of `fetchSboms()` and other existing API functions.
- `useSbomComparison` hook in `src/hooks/useSbomComparison.ts`:
  - Query key: `["sbom-comparison", leftId, rightId]`
  - `enabled: !!leftId && !!rightId` — only fire the request when both IDs are provided
  - Follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "removed_packages": [{ "name": "...", "version": "...", "license": "...", "advisory_count": 0 }],
    "version_changes": [{ "name": "...", "left_version": "...", "right_version": "...", "direction": "upgrade" }],
    "new_vulnerabilities": [{ "advisory_id": "...", "severity": "critical", "title": "...", "affected_package": "..." }],
    "resolved_vulnerabilities": [{ "advisory_id": "...", "severity": "...", "title": "...", "previously_affected_package": "..." }],
    "license_changes": [{ "name": "...", "left_license": "...", "right_license": "..." }]
  }
  ```
  (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**Convention references:**
- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API layer scope.
- Per CONVENTIONS.md §State management: React Query (TanStack Query) for server state; no Redux.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript hook scope.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — API function pattern to follow for fetchSbomComparison
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (import and use directly)
- `src/hooks/useSboms.ts` — React Query hook pattern to follow for useSbomComparison
- `src/hooks/useSbomById.ts` — example of a hook that takes an ID parameter and conditionally enables the query
- `src/api/models.ts` — existing interface definitions to follow for naming and structure

## Acceptance Criteria
- [ ] SbomComparisonResult and all sub-type interfaces are defined in models.ts
- [ ] fetchSbomComparison(leftId, rightId) calls GET /api/v2/sbom/compare with correct query parameters
- [ ] useSbomComparison hook returns { data, isLoading, isError, error } with correct types
- [ ] Hook is disabled (does not fire request) when either leftId or rightId is undefined/empty
- [ ] Hook fires request when both IDs are provided

## Test Requirements
- [ ] Unit test: fetchSbomComparison calls the correct URL with left and right query parameters
- [ ] Unit test: useSbomComparison hook returns loading state initially, then data on success (using MSW mock)
- [ ] Unit test: useSbomComparison hook does not fire when leftId is undefined
- [ ] Unit test: useSbomComparison hook does not fire when rightId is undefined

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests

[sdlc-workflow] Description digest: sha256-md:05f7bd0d8dd30c1f4e09d6abaefeead90b1e3e28972c685ca94cd34bee6ffbaf
