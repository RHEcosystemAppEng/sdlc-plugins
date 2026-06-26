## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add TypeScript interfaces for the SBOM comparison API response, an API client function to call the comparison endpoint, and a React Query hook to manage the comparison data fetching lifecycle. This establishes the data layer that the comparison page UI will consume.

## Files to Modify
- `src/api/models.ts` -- Add TypeScript interfaces: `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange`
- `src/api/rest.ts` -- Add `fetchSbomComparison(leftId: string, rightId: string)` function that calls `GET /api/v2/sbom/compare?left={leftId}&right={rightId}`

## Files to Create
- `src/hooks/useSbomComparison.ts` -- React Query hook `useSbomComparison(leftId, rightId)` that wraps `fetchSbomComparison` with `useQuery`, enabled only when both IDs are provided

## Implementation Notes
The TypeScript interfaces in `src/api/models.ts` must match the backend response shape exactly:

```typescript
interface SbomComparison {
  added_packages: AddedPackage[];
  removed_packages: RemovedPackage[];
  version_changes: VersionChange[];
  new_vulnerabilities: NewVulnerability[];
  resolved_vulnerabilities: ResolvedVulnerability[];
  license_changes: LicenseChange[];
}
```

Follow the API client pattern in `src/api/rest.ts` where existing functions like `fetchSboms()` use the Axios instance from `src/api/client.ts`. The new function should use `client.get<SbomComparison>()` with query parameters.

The React Query hook in `src/hooks/useSbomComparison.ts` should follow the pattern established by `src/hooks/useSbomById.ts` -- using `useQuery` with a descriptive query key (e.g., `["sbom-comparison", leftId, rightId]`) and the `enabled` option set to `!!leftId && !!rightId` so the query only fires when both SBOM IDs are available.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` -- Pattern reference for API client function using Axios
- `src/api/client.ts` -- Axios instance with base URL and auth interceptors
- `src/hooks/useSbomById.ts` -- Pattern reference for React Query hook with conditional enabling
- `src/api/models.ts` -- Existing interface patterns for API response types

## Acceptance Criteria
- [ ] `SbomComparison` and all sub-interfaces are defined in `src/api/models.ts` matching the backend response contract
- [ ] `fetchSbomComparison()` in `src/api/rest.ts` correctly calls the comparison endpoint with query parameters
- [ ] `useSbomComparison` hook returns `{ data, isLoading, isError }` and only fetches when both SBOM IDs are provided
- [ ] All new types are exported and available for import by the comparison page

## Test Requirements
- [ ] Unit test: `useSbomComparison` does not fire a request when either SBOM ID is undefined
- [ ] Unit test: `useSbomComparison` returns comparison data when both IDs are provided (using MSW mock)

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9003 from main
- Depends on: Task 3 -- Implement comparison endpoint and integration tests (for API contract)

[sdlc-workflow] Description digest: sha256-md:d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2b3c4d5e6
