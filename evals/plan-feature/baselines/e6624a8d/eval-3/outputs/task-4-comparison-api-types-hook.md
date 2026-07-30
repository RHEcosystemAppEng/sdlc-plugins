## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend API layer for the SBOM comparison endpoint: TypeScript interfaces for the comparison response types, an Axios client function to call the endpoint, and a React Query hook for data fetching. This task establishes the data-fetching contract between the frontend and the new backend comparison endpoint without any UI components.

## Files to Modify
- `src/api/models.ts` -- add TypeScript interfaces for comparison response types
- `src/api/rest.ts` -- add `fetchSbomComparison()` function

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook wrapping the comparison API call

## Implementation Notes
Per CONVENTIONS.md API layer pattern: follow the established pattern of typed API functions in `src/api/rest.ts` with Axios client from `src/api/client.ts`, and React Query hooks in `src/hooks/`.
Applies: task modifies `src/api/rest.ts` matching the convention's `.ts` API file scope.

Per CONVENTIONS.md React Query hook pattern: create the hook following the existing pattern in `useSboms.ts` and `useSbomById.ts` -- use `useQuery` with a query key and the API function.
Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `.ts` hook file scope.

Per CONVENTIONS.md Naming conventions: use camelCase for the hook (`useSbomComparison`) and API function (`fetchSbomComparison`).
Applies: convention has no file-type restriction (broadly applicable).

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` -- response shape:
  ```typescript
  interface SbomComparisonResult {
    added_packages: PackageDiff[];
    removed_packages: PackageDiff[];
    version_changes: VersionChange[];
    new_vulnerabilities: VulnerabilityDiff[];
    resolved_vulnerabilities: VulnerabilityDiff[];
    license_changes: LicenseChange[];
  }

  interface PackageDiff {
    name: string;
    version: string;
    license: string;
    advisory_count: number;
  }

  interface VersionChange {
    name: string;
    left_version: string;
    right_version: string;
    direction: "upgrade" | "downgrade";
  }

  interface VulnerabilityDiff {
    advisory_id: string;
    severity: string;
    title: string;
    affected_package: string;
  }

  // For resolved_vulnerabilities, the field is previously_affected_package
  interface ResolvedVulnerabilityDiff {
    advisory_id: string;
    severity: string;
    title: string;
    previously_affected_package: string;
  }

  interface LicenseChange {
    name: string;
    left_license: string;
    right_license: string;
  }
  ```
  (See `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend for the source structs)

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**Hook usage pattern:**
```typescript
const { data, isLoading, error } = useSbomComparison(leftId, rightId, { enabled: !!leftId && !!rightId });
```

The hook should accept `leftId` and `rightId` as parameters and only execute the query when both are provided (using `enabled` option).

## Reuse Candidates
- `src/hooks/useSboms.ts` -- existing React Query hook; follow the same `useQuery` pattern for the comparison hook
- `src/hooks/useSbomById.ts` -- existing hook with parameter-based query key; reference for parameterized hook pattern
- `src/api/rest.ts::fetchSboms()` -- existing API function; follow the same Axios call pattern
- `src/api/models.ts` -- existing TypeScript interfaces; add comparison types alongside existing models
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors; import and use for the comparison API call

## Acceptance Criteria
- [ ] TypeScript interfaces for all comparison response types are defined in `models.ts`
- [ ] `fetchSbomComparison(leftId, rightId)` function is implemented in `rest.ts` using the Axios client
- [ ] `useSbomComparison` React Query hook is implemented with proper query key and enabled condition
- [ ] Hook only executes the query when both `leftId` and `rightId` are provided
- [ ] All types match the backend API response shape

## Test Requirements
- [ ] Unit test: `fetchSbomComparison` calls the correct endpoint with query parameters
- [ ] Unit test: `useSbomComparison` hook returns loading state initially and data after resolution
- [ ] Unit test: `useSbomComparison` does not fire when either ID is undefined (enabled: false)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- Add SBOM comparison REST endpoint with integration tests (API contract dependency)
