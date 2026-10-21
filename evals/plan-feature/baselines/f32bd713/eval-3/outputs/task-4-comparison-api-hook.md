## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript type definitions, API client function, and React Query hook for the SBOM comparison endpoint. This task creates the data-fetching layer that the comparison page UI (Task 5) will consume. This is an API-layer task and does not involve UI components.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for the comparison response types
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Follow the existing API type pattern in `src/api/models.ts` — add interfaces matching the backend response shape:
  - `SbomComparisonResult` with fields: `added_packages`, `removed_packages`, `version_changes`, `new_vulnerabilities`, `resolved_vulnerabilities`, `license_changes`
  - `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` — one interface per diff section item
- Per CONVENTIONS.md §API Layer: add the typed API function in `src/api/rest.ts` using the Axios client from `src/api/client.ts`, following the pattern of existing functions like `fetchSboms()`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.
- Per CONVENTIONS.md §State Management: create the React Query hook in `src/hooks/` using `useQuery` with a unique query key, following the pattern in `src/hooks/useSboms.ts`.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook scope.
- The hook should accept `leftId` and `rightId` parameters and only be enabled when both IDs are provided.
- Per CONVENTIONS.md §Naming: use camelCase for the hook (`useSbomComparison`) and API function (`compareSboms`).
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```json
  {
    "added_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": "number" }],
    "removed_packages": [{ "name": "string", "version": "string", "license": "string", "advisory_count": "number" }],
    "version_changes": [{ "name": "string", "left_version": "string", "right_version": "string", "direction": "string" }],
    "new_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "affected_package": "string" }],
    "resolved_vulnerabilities": [{ "advisory_id": "string", "severity": "string", "title": "string", "previously_affected_package": "string" }],
    "license_changes": [{ "name": "string", "left_license": "string", "right_license": "string" }]
  }
  ```
  See `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend for the endpoint definition.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API function pattern to follow for `compareSboms()`
- `src/hooks/useSboms.ts` — existing React Query hook pattern; follow its `useQuery` key structure and options
- `src/hooks/useSbomById.ts` — existing single-resource query pattern; similar to comparison which also returns a single result
- `src/api/client.ts` — Axios instance with base URL and auth interceptors; use for the comparison API call

## Acceptance Criteria
- [ ] `SbomComparisonResult` interface defined in `models.ts` with all six diff sections typed
- [ ] Each diff section item interface (AddedPackage, RemovedPackage, etc.) matches the backend response shape
- [ ] `compareSboms(leftId, rightId)` function added to `rest.ts` calling `GET /api/v2/sbom/compare`
- [ ] `useSbomComparison` hook created in `src/hooks/` using `useQuery`
- [ ] Hook is disabled when either `leftId` or `rightId` is not provided
- [ ] Hook exposes `data`, `isLoading`, `isError`, and `error` from React Query

## Test Requirements
- [ ] Unit test: `compareSboms()` calls the correct endpoint with left and right query parameters
- [ ] Unit test: `useSbomComparison` returns data from the API when both IDs are provided
- [ ] Unit test: `useSbomComparison` does not fire a request when either ID is missing

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison endpoint and integration tests
