## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript API types, client function, and React Query hook for the SBOM comparison endpoint. This establishes the data-fetching layer that the comparison page (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces for the comparison response types
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- **TypeScript interfaces** (in `src/api/models.ts`): Define interfaces matching the backend response shape:
  - `SbomComparisonResult` with fields: `added_packages: PackageDiff[]`, `removed_packages: PackageDiff[]`, `version_changes: VersionChange[]`, `new_vulnerabilities: VulnerabilityDiff[]`, `resolved_vulnerabilities: VulnerabilityDiff[]`, `license_changes: LicenseChange[]`
  - `PackageDiff`: `name: string`, `version: string`, `license: string`, `advisory_count: number`
  - `VersionChange`: `name: string`, `left_version: string`, `right_version: string`, `direction: "upgrade" | "downgrade"`
  - `VulnerabilityDiff`: `advisory_id: string`, `severity: string`, `title: string`, `affected_package: string`
  - `LicenseChange`: `name: string`, `left_license: string`, `right_license: string`
- **API client function** (in `src/api/rest.ts`): Follow the existing pattern of `fetchSboms()` and `fetchAdvisories()`. The function should use the Axios instance from `src/api/client.ts` and call `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`.
- **React Query hook** (in `src/hooks/useSbomComparison.ts`): Follow the pattern in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`. Use `useQuery` with a query key like `["sbom", "compare", leftId, rightId]`. The hook should:
  - Accept `leftId: string | undefined` and `rightId: string | undefined`
  - Only enable the query when both IDs are defined (`enabled: !!leftId && !!rightId`)
  - Return the standard React Query result object

### Backend API contracts
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` (see above interfaces). Defined in `modules/fundamental/src/sbom/endpoints/compare.rs`.
- `GET /api/v2/sbom` — existing endpoint for SBOM list, used by SBOM selectors. Response shape: `PaginatedResults<SbomSummary>`. Defined in `modules/fundamental/src/sbom/endpoints/list.rs`.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — Existing API client function pattern to follow for `compareSboms()`
- `src/api/client.ts` — Axios instance with base URL and auth interceptors (import and use directly)
- `src/hooks/useSboms.ts` — React Query hook pattern to follow for `useSbomComparison`
- `src/hooks/useSbomById.ts` — React Query hook with single-resource query key pattern

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend comparison response shape exactly
- [ ] `compareSboms()` function correctly calls the comparison endpoint with left/right query params
- [ ] `useSbomComparison` hook enables the query only when both SBOM IDs are provided
- [ ] Hook returns loading, error, and data states correctly

## Test Requirements
- [ ] Unit test: `compareSboms()` calls the correct endpoint URL with query parameters
- [ ] Unit test: `useSbomComparison` does not fire when either ID is undefined
- [ ] Unit test: `useSbomComparison` returns comparison data when both IDs are provided (use MSW mock)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
