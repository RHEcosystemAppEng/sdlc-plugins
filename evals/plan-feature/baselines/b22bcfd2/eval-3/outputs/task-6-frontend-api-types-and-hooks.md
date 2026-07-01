## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching. This API layer is needed before the comparison page UI can be built.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add fetchSbomComparison() API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook for the comparison endpoint

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — CONSUME: add client function and hook for the new backend endpoint

## Implementation Notes
In `src/api/models.ts`, add interfaces matching the backend response shape:
- `SbomComparisonResult` with fields: added_packages, removed_packages, version_changes, new_vulnerabilities, resolved_vulnerabilities, license_changes
- `AddedPackage` with fields: name, version, license, advisory_count
- `RemovedPackage` with fields: name, version, license, advisory_count
- `VersionChange` with fields: name, left_version, right_version, direction
- `NewVulnerability` with fields: advisory_id, severity, title, affected_package
- `ResolvedVulnerability` with fields: advisory_id, severity, title, previously_affected_package
- `LicenseChange` with fields: name, left_license, right_license

In `src/api/rest.ts`, add a function following the pattern of existing functions like `fetchSboms()`:
```typescript
export const fetchSbomComparison = (leftId: string, rightId: string): Promise<SbomComparisonResult> =>
  client.get(`/api/v2/sbom/compare`, { params: { left: leftId, right: rightId } }).then(res => res.data);
```

In `src/hooks/useSbomComparison.ts`, create a React Query hook following the pattern of `src/hooks/useSbomById.ts`:
```typescript
export const useSbomComparison = (leftId: string | undefined, rightId: string | undefined) =>
  useQuery({
    queryKey: ['sbom-comparison', leftId, rightId],
    queryFn: () => fetchSbomComparison(leftId!, rightId!),
    enabled: !!leftId && !!rightId,
  });
```

Use the Axios instance from `src/api/client.ts` which handles base URL and auth interceptors.

## Reuse Candidates
- `src/api/models.ts` — existing interface patterns (e.g., SBOM-related types)
- `src/api/rest.ts::fetchSboms` — pattern for API client functions using Axios
- `src/hooks/useSbomById.ts` — pattern for React Query hooks with parameters
- `src/api/client.ts` — Axios instance with auth interceptors

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend response shape exactly
- [ ] fetchSbomComparison() calls the correct endpoint with left/right query params
- [ ] useSbomComparison hook is disabled when either ID is undefined
- [ ] useSbomComparison hook returns typed SbomComparisonResult data
- [ ] All types are properly exported

## Test Requirements
- [ ] Unit test: useSbomComparison returns data when both IDs are provided (using MSW mock)
- [ ] Unit test: useSbomComparison does not fire when an ID is undefined
- [ ] Verify TypeScript interfaces compile correctly with sample data

## Dependencies
- Depends on: Task 4 — Backend comparison endpoint
