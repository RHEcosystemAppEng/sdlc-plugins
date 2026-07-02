## Repository
trustify-ui

## Target Branch
main

## Description
Add TypeScript interfaces for the SBOM comparison API response, the REST client function to call the backend comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This establishes the data layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` -- Add TypeScript interfaces for comparison response types (`SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`)
- `src/api/rest.ts` -- Add `fetchSbomComparison(leftId: string, rightId: string)` function

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook for fetching SBOM comparison results

## Implementation Notes
- Add the following TypeScript interfaces to `src/api/models.ts`, matching the backend API response shape exactly:
  ```typescript
  export interface PackageDiff {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  export interface VersionChange {
    name: string;
    left_version: string;
    right_version: string;
    direction: "upgrade" | "downgrade";
  }

  export interface VulnerabilityDiff {
    advisory_id: string;
    severity: string;
    title: string;
    affected_package: string;
  }

  export interface LicenseChange {
    name: string;
    left_license: string;
    right_license: string;
  }

  export interface SbomComparisonResult {
    added_packages: PackageDiff[];
    removed_packages: PackageDiff[];
    version_changes: VersionChange[];
    new_vulnerabilities: VulnerabilityDiff[];
    resolved_vulnerabilities: VulnerabilityDiff[];
    license_changes: LicenseChange[];
  }
  ```
- Add `fetchSbomComparison` to `src/api/rest.ts` following the established pattern of `fetchSboms()` and other API functions in that file. Use the Axios instance from `src/api/client.ts`:
  ```typescript
  export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
    client.get("/api/v2/sbom/compare", { params: { left: leftId, right: rightId } }).then((res) => res.data);
  ```
- Create `src/hooks/useSbomComparison.ts` following the pattern of `src/hooks/useSbomById.ts`. Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`. The hook should accept `leftId` and `rightId` as optional string parameters and only enable the query when both are provided:
  ```typescript
  export const useSbomComparison = (leftId?: string, rightId?: string) =>
    useQuery({
      queryKey: ["sbom-comparison", leftId, rightId],
      queryFn: () => fetchSbomComparison(leftId!, rightId!),
      enabled: !!leftId && !!rightId,
    });
  ```
- Per CONVENTIONS.md section API layer: Axios client in `src/api/client.ts`, typed API functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API layer scope.
- Per CONVENTIONS.md section Naming: camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook naming scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- Response shape: `SbomComparisonResult` with fields `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]` (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- Existing API function pattern using Axios client; follow for `fetchSbomComparison`
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; import for API calls
- `src/hooks/useSbomById.ts` -- Existing React Query hook for single SBOM fetch; follow pattern for `useSbomComparison`
- `src/hooks/useSboms.ts` -- Existing React Query hook for SBOM list; reference for query key naming convention

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types (`SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`) are defined in `src/api/models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` function calls `GET /api/v2/sbom/compare` with correct query parameters using the Axios client
- [ ] `useSbomComparison` hook returns `{ data, isLoading, isError, error }` with proper TypeScript typing (`SbomComparisonResult`)
- [ ] Hook query is disabled (does not fire the API call) when either `leftId` or `rightId` is undefined or empty
- [ ] All types compile without errors (`npx tsc --noEmit`)

## Test Requirements
- [ ] Unit test: `useSbomComparison` hook returns comparison data when both IDs are provided (using MSW mock handler for `/api/v2/sbom/compare`)
- [ ] Unit test: hook does not fire when `leftId` is undefined
- [ ] Unit test: hook does not fire when `rightId` is undefined
- [ ] Type check: interfaces match the expected backend response shape (verified by TypeScript compilation)

## Verification Commands
- `npx tsc --noEmit` -- verify TypeScript compilation with no type errors

## Dependencies
- Depends on: Task 2 -- Add SBOM comparison endpoint and integration tests

---
sha256-md:37f0381be8801fe930fcc8e446bf4c6cbcf9d9bd19f1a4c35a13890d04439b5c
