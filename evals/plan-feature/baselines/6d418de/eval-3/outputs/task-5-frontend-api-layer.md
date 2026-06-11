# Task 5 — Add frontend API types, client function, and React Query hook for SBOM comparison

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, a REST client function to call the comparison endpoint, and a React Query hook for fetching comparison data. This establishes the frontend data layer that the comparison page will consume.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `fetchSbomComparison` and returns query result. Only enabled when both IDs are defined.

## API Changes
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — consumed by `fetchSbomComparison` in `rest.ts`

## Implementation Notes
- **TypeScript interfaces** — match the backend response shape exactly:
  ```
  PackageDiff: { name: string; version: string; license: string | null; advisory_count: number }
  VersionChange: { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }
  VulnerabilityDiff: { advisory_id: string; severity: string; title: string; affected_package: string }
  LicenseChange: { name: string; left_license: string; right_license: string }
  SbomComparisonResult: { added_packages: PackageDiff[]; removed_packages: PackageDiff[]; version_changes: VersionChange[]; new_vulnerabilities: VulnerabilityDiff[]; resolved_vulnerabilities: VulnerabilityDiff[]; license_changes: LicenseChange[] }
  ```
- Follow the existing API client pattern in `src/api/rest.ts` — use the Axios instance from `src/api/client.ts`. Example: `return client.get<SbomComparisonResult>("/api/v2/sbom/compare", { params: { left: leftId, right: rightId } }).then(res => res.data);`
- Follow the existing hook pattern in `src/hooks/useSboms.ts` — use `useQuery` from React Query with a query key like `["sbom-comparison", leftId, rightId]`. Set `enabled: !!leftId && !!rightId` to prevent fetching when selectors are empty.
- Use `staleTime` of 30 seconds since comparison results are deterministic for given SBOM IDs.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` as defined above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend). Returns 400 if either parameter is missing, 404 if either SBOM is not found.
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — reference for the API client function pattern using Axios
- `src/api/models.ts` — reference for TypeScript interface naming and field conventions
- `src/hooks/useSboms.ts` — reference for React Query hook structure with `useQuery`
- `src/hooks/useSbomById.ts` — reference for hooks with conditional `enabled` flag

## Acceptance Criteria
- [ ] TypeScript interfaces match the backend API response shape exactly
- [ ] `fetchSbomComparison` sends GET request with `left` and `right` query parameters
- [ ] `useSbomComparison` hook returns loading, error, and data states
- [ ] Hook only fires request when both SBOM IDs are provided (enabled flag)

## Test Requirements
- [ ] Unit test: `useSbomComparison` returns data on successful fetch (use MSW to mock endpoint)
- [ ] Unit test: `useSbomComparison` does not fire when either ID is undefined
- [ ] Unit test: `useSbomComparison` returns error state on 404 response

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Add GET /api/v2/sbom/compare endpoint (API contract dependency)
