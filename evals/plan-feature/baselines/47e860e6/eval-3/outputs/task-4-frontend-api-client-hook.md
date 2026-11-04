# Task 4 — Frontend: comparison API types, client function, React Query hook and mocks

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the data layer the SBOM comparison view (TC-9003) needs to call the new backend diff endpoint: TypeScript response types, a typed API client function, a React Query hook, and MSW mocks for tests. The page and section components (Tasks 5 and 6) consume this hook.

## Files to Modify
- `src/api/models.ts`: add `SbomComparison`, `PackageDiffEntry`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` interfaces and a `VersionChangeDirection` type
- `src/api/rest.ts`: add `fetchSbomComparison(left: string, right: string): Promise<SbomComparison>`
- `tests/mocks/handlers.ts`: add an MSW handler for `GET /api/v2/sbom/compare`, covering the success, 404 and 400 cases

## Files to Create
- `src/hooks/useSbomComparison.ts`: React Query `useQuery` hook for the comparison
- `tests/mocks/fixtures/sbom-comparison.json`: mock comparison response with entries in every category, including at least one `critical` new vulnerability and more than 100 added packages (for the virtualization tests in Task 5)

## Implementation Notes
- **Backend API contracts** (manual REST call; there is no generated client for this endpoint):
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}`. Query params are `left: string` and `right: string` (SBOM IDs). The response is:
    ```ts
    interface SbomComparison {
      added_packages: { name: string; version: string; license: string; advisory_count: number }[];
      removed_packages: { name: string; version: string; license: string; advisory_count: number }[];
      version_changes: { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }[];
      new_vulnerabilities: { advisory_id: string; severity: string; title: string; affected_package: string }[];
      resolved_vulnerabilities: { advisory_id: string; severity: string; title: string; previously_affected_package: string }[];
      license_changes: { name: string; left_license: string; right_license: string }[];
    }
    ```
    Errors are `400` (missing params) and `404` (unknown SBOM). Defined in `modules/fundamental/src/sbom/endpoints/compare.rs` (new, Task 3), with the model in `modules/fundamental/src/sbom/model/compare.rs` (Task 2).
  - `GET /api/v2/sbom` returns `{ items: SbomSummary[], total: number }` (`modules/fundamental/src/sbom/endpoints/list.rs`). It is already wrapped by `fetchSboms()` and `useSboms`, and the selectors (Task 6) will use it.
  - Verify these contracts against the `trustify-backend` repo during implementation using the implement-task cross-repo API verification step.
- Keep API field names in snake_case to match the backend JSON. Do not rename them in the types.
- **Hook:** `useSbomComparison(left?: string, right?: string)` calls `useQuery({ queryKey: ["sbom-compare", left, right], queryFn: () => fetchSbomComparison(left!, right!), enabled: !!left && !!right })`. Surface errors from the hook so a 404 renders an error state, not an empty diff.
- Per CONVENTIONS.md §API layer: put the call in `src/api/rest.ts` using the Axios instance from `src/api/client.ts`, the types in `src/api/models.ts`, and the hook in `src/hooks/`. Follow `fetchSboms()` in `src/api/rest.ts` and `src/hooks/useSbomById.ts`.
  Applies: task modifies `src/api/rest.ts` matching the convention's API layer (`src/api/*.ts`, `src/hooks/*.ts`) scope.
- Per CONVENTIONS.md §State management: use React Query `useQuery` for this server state, with no local caching layer. See `src/hooks/useSboms.ts`.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's React Query hook (`src/hooks/*.ts`) scope.
- Per CONVENTIONS.md §Naming: use camelCase for the hook and function names (`useSbomComparison`, `fetchSbomComparison`).
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hooks/utilities (`.ts`) naming scope.
- Per CONVENTIONS.md §Testing: mock the API with MSW in `tests/mocks/handlers.ts`, with fixtures under `tests/mocks/fixtures/`, following `sboms.json`.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW mocking (`tests/mocks/*`) scope.
- Constraints (docs/constraints.md): §1.4/§5.1 scope to the listed files; §5.2 inspect `rest.ts`, `models.ts` and `useSbomById.ts` before changes; §5.4 reuse the Axios client and do not create a new instance; §2.1–2.3 commit format; §3.3 open the PR with `--base TC-9003`.

## Reuse Candidates
- `src/api/client.ts`: the Axios instance with base URL and auth interceptors. Must be reused.
- `src/api/rest.ts::fetchSboms`: pattern for typed API functions
- `src/hooks/useSbomById.ts`: pattern for a parameterized `useQuery` hook
- `tests/mocks/handlers.ts` and `tests/mocks/fixtures/sboms.json`: MSW handler and fixture patterns

## Acceptance Criteria
- [ ] `SbomComparison` and related types match the backend contract field-for-field
- [ ] `fetchSbomComparison(left, right)` calls `GET /api/v2/sbom/compare?left=..&right=..` via the shared Axios client
- [ ] `useSbomComparison` does not fire a request until both IDs are set
- [ ] A `404` or `400` from the endpoint surfaces as a query error and is never resolved as an empty comparison
- [ ] MSW handler and fixture are available for page and component tests

## Test Requirements
- [ ] Hook test: with both IDs, the hook returns the fixture data
- [ ] Hook test: with one ID missing, no request is made
- [ ] Hook test (fail-closed): when the MSW handler returns `404`, the hook is in an error state and `data` is undefined

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Backend: GET /api/v2/sbom/compare endpoint and integration tests
