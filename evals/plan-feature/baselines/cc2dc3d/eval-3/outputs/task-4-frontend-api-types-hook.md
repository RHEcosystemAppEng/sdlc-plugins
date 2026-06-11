## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage comparison data fetching. This provides the data layer that the comparison page UI (Task 5) will consume.

## Files to Modify
- `src/api/models.ts` — add TypeScript interfaces for comparison response types
- `src/api/rest.ts` — add `compareSboms(leftId: string, rightId: string)` API client function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook wrapping the comparison API call

## Implementation Notes
- Add the following TypeScript interfaces to `src/api/models.ts`, matching the backend response shape:
  - `AddedPackage` — `{ name: string; version: string; license: string; advisory_count: number }`
  - `RemovedPackage` — `{ name: string; version: string; license: string; advisory_count: number }`
  - `VersionChange` — `{ name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }`
  - `NewVulnerability` — `{ advisory_id: string; severity: string; title: string; affected_package: string }`
  - `ResolvedVulnerability` — `{ advisory_id: string; severity: string; title: string; previously_affected_package: string }`
  - `LicenseChange` — `{ name: string; left_license: string; right_license: string }`
  - `SbomComparisonResult` — `{ added_packages: AddedPackage[]; removed_packages: RemovedPackage[]; version_changes: VersionChange[]; new_vulnerabilities: NewVulnerability[]; resolved_vulnerabilities: ResolvedVulnerability[]; license_changes: LicenseChange[] }`
- Add the client function in `src/api/rest.ts` following the existing pattern (see `fetchSboms()`, `fetchAdvisories()` for examples). Use the Axios instance from `src/api/client.ts`.
- The hook in `src/hooks/useSbomComparison.ts` should follow the React Query hook pattern used in `src/hooks/useSboms.ts` and `src/hooks/useSbomById.ts`:
  - Use `useQuery` with a query key like `["sbom-comparison", leftId, rightId]`
  - Only enable the query when both `leftId` and `rightId` are provided (`enabled: !!leftId && !!rightId`)
  - Return the query result typed as `SbomComparisonResult`

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` (see `modules/fundamental/src/sbom/model/comparison.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

**Reuse Candidates:**
- `src/api/client.ts` — reuse the configured Axios instance for the API call
- `src/api/rest.ts::fetchSboms` — follow the same function pattern for the new comparison client function
- `src/hooks/useSboms.ts` — follow the same React Query hook pattern (useQuery with typed response)
- `src/hooks/useSbomById.ts` — follow the same single-resource query pattern with ID-based query key

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend response shape exactly
- [ ] API client function calls the correct endpoint with left/right query parameters
- [ ] React Query hook returns typed comparison data and handles loading/error states
- [ ] Hook only fires the query when both SBOM IDs are provided

## Test Requirements
- [ ] Unit test: `compareSboms` client function constructs the correct URL with query parameters
- [ ] Unit test: `useSbomComparison` hook returns data when both IDs are provided
- [ ] Unit test: `useSbomComparison` hook does not fire when an ID is missing
- [ ] Use MSW to mock the comparison endpoint in tests (follow pattern in `tests/mocks/handlers.ts`)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add SBOM comparison endpoint (API contract dependency)
