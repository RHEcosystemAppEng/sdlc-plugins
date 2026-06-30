## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the TypeScript interfaces for the SBOM comparison API response, the API client function to call the comparison endpoint, and a React Query hook to manage comparison data fetching. This task establishes the frontend data layer for the comparison feature without any UI components.

## Files to Modify
- `src/api/models.ts` — Add TypeScript interfaces: `SbomComparisonResult`, `PackageDiff`, `VersionChange`, `VulnerabilityDiff`, `LicenseChange`
- `src/api/rest.ts` — Add `compareSboms(leftId: string, rightId: string): Promise<SbomComparisonResult>` function

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query hook: `useSbomComparison(leftId: string | undefined, rightId: string | undefined)` that calls `compareSboms` and returns the query result

## Implementation Notes
- TypeScript interfaces should match the backend response shape exactly:
  ```
  SbomComparisonResult {
    added_packages: PackageDiff[]
    removed_packages: PackageDiff[]
    version_changes: VersionChange[]
    new_vulnerabilities: VulnerabilityDiff[]
    resolved_vulnerabilities: VulnerabilityDiff[]
    license_changes: LicenseChange[]
  }
  ```
- Follow the existing API client pattern in `src/api/rest.ts` — use the Axios instance from `src/api/client.ts` with typed response generics (e.g., `client.get<SbomComparisonResult>(...)`).
- Follow the existing hook pattern in `src/hooks/useSboms.ts` — use `useQuery` from React Query with a query key like `["sbom-comparison", leftId, rightId]`.
- The hook should be disabled when either `leftId` or `rightId` is undefined (use the `enabled` option: `enabled: !!leftId && !!rightId`).
- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`; typed API functions in `src/api/rest.ts`; React Query hooks in `src/hooks/`.
  Applies: task modifies `src/api/rest.ts` matching the convention's TypeScript API file scope.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's TypeScript file scope.

**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — response shape: `SbomComparisonResult` with fields as listed above (see `modules/fundamental/src/sbom/endpoints/compare.rs` in trustify-backend)
- Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step.

## Reuse Candidates
- `src/api/rest.ts::fetchSboms` — existing API function pattern to follow for `compareSboms`
- `src/api/models.ts` — existing TypeScript interface patterns for API response types
- `src/hooks/useSboms.ts` — existing React Query hook pattern to follow for `useSbomComparison`
- `src/hooks/useSbomById.ts` — demonstrates the single-resource query hook pattern with dynamic query keys
- `src/api/client.ts` — Axios instance with base URL and auth interceptors

## Acceptance Criteria
- [ ] `SbomComparisonResult` and supporting interfaces are defined in `models.ts` with correct field types
- [ ] `compareSboms` function makes a GET request to `/api/v2/sbom/compare` with `left` and `right` query parameters
- [ ] `useSbomComparison` hook returns React Query result and is disabled when either ID is undefined
- [ ] TypeScript compilation succeeds with no type errors

## Test Requirements
- [ ] Unit test: `compareSboms` constructs the correct URL with query parameters
- [ ] Unit test: `useSbomComparison` hook is disabled when leftId or rightId is undefined
- [ ] Add MSW handler in `tests/mocks/handlers.ts` for `GET /api/v2/sbom/compare` returning mock comparison data

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 4 — Backend comparison endpoint (API contract dependency)

<!-- [sdlc-workflow] Description digest: sha256-md:9f29f5fbcfabf50a6c369c332112b7a0475f258bd474973b72edb44cbb8eddaa -->
