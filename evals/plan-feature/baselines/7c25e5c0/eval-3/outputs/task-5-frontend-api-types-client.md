## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the SBOM comparison API response and a typed API client function for calling the comparison endpoint. This task extends the existing API layer with the types and function needed by the comparison hook and page.

## Files to Modify
- `src/api/models.ts` — add `SbomComparisonResult`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` interfaces
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Implementation Notes
Follow the existing API layer patterns:
- `src/api/models.ts` defines TypeScript interfaces matching backend response types — add interfaces matching the `SbomComparisonResult` JSON shape from the backend
- `src/api/rest.ts` defines API client functions using the Axios instance from `src/api/client.ts` — add `compareSboms` following the same pattern as `fetchSboms()` and `fetchAdvisories()`
- The `compareSboms` function calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}` using the shared Axios client

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape:
  ```
  {
    added_packages: AddedPackage[],
    removed_packages: RemovedPackage[],
    version_changes: VersionChange[],
    new_vulnerabilities: NewVulnerability[],
    resolved_vulnerabilities: ResolvedVulnerability[],
    license_changes: LicenseChange[]
  }
  ```
  (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's API client scope.

## Acceptance Criteria
- [ ] `SbomComparisonResult` interface defined with all six section arrays
- [ ] Each section item type (`AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`) is defined with correct fields
- [ ] `compareSboms(leftId, rightId)` function uses the shared Axios client
- [ ] Function constructs the correct URL with query parameters

## Test Requirements
- [ ] Type definitions compile without TypeScript errors
- [ ] `compareSboms` function signature matches the expected API contract

## Dependencies
- Depends on: Task 3 — Backend comparison endpoint
