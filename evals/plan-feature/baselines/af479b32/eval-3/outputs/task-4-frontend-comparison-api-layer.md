## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces, API client function, and React Query hook for the SBOM comparison endpoint. This establishes the data-fetching layer that the comparison page (Task 5) will consume. The API response types match the backend contract defined in the feature requirements and implemented in Tasks 2-3.

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces for SbomComparisonResult and its sub-types (AddedPackage, RemovedPackage, VersionChange, NewVulnerability, ResolvedVulnerability, LicenseChange)
- `src/api/rest.ts` -- add fetchSbomComparison(leftId: string, rightId: string) function that calls GET /api/v2/sbom/compare?left={leftId}&right={rightId}

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook wrapping fetchSbomComparison with proper query key, enabled flag (only when both IDs are provided), and error handling

## Implementation Notes

Per CONVENTIONS.md §API Layer: follow the established pattern of typed API functions in `src/api/rest.ts` and React Query hooks in `src/hooks/`. See `src/api/rest.ts::fetchSboms()` and `src/hooks/useSboms.ts` for the existing patterns.
Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope.

Per CONVENTIONS.md §Naming: use camelCase for the hook file name (`useSbomComparison.ts`) and function name (`useSbomComparison`). See `src/hooks/useSbomById.ts` for naming reference.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape:
  ```typescript
  interface SbomComparisonResult {
    added_packages: AddedPackage[];
    removed_packages: RemovedPackage[];
    version_changes: VersionChange[];
    new_vulnerabilities: NewVulnerability[];
    resolved_vulnerabilities: ResolvedVulnerability[];
    license_changes: LicenseChange[];
  }
  ```
  See `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend for the definitive response shape.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

The React Query hook should:
1. Accept `leftId` and `rightId` as parameters.
2. Use a query key like `["sbom-comparison", leftId, rightId]`.
3. Set `enabled: !!(leftId && rightId)` to prevent firing when selectors are empty.
4. Return the standard React Query result object with `data`, `isLoading`, `isError`, etc.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- existing API function; follow its Axios call pattern with the client instance from `src/api/client.ts`
- `src/hooks/useSboms.ts` -- existing React Query hook; follow its query key structure and options pattern
- `src/hooks/useSbomById.ts` -- existing hook for fetching a single SBOM; similar parameter passing pattern
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; use for the comparison API call

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in models.ts
- [ ] fetchSbomComparison() correctly calls GET /api/v2/sbom/compare with left and right query parameters
- [ ] useSbomComparison() hook returns comparison data when both SBOM IDs are provided
- [ ] Hook does not fire API call when either SBOM ID is missing (enabled: false)
- [ ] Types match the backend API contract exactly

## Test Requirements
- [ ] Unit test: useSbomComparison hook returns data when API responds successfully (using MSW mock)
- [ ] Unit test: useSbomComparison hook does not fire when IDs are missing
- [ ] Unit test: useSbomComparison hook handles API error response gracefully

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- Add SBOM comparison endpoint and integration tests (defines the API contract)
