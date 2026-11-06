# Task 4 — Add SBOM comparison API types, client function, and React Query hook

**Summary:** Add SbomComparison types, compareSboms() client, and useSbomComparison hook
**Epic:** TC-9003: SBOM comparison UI

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend data layer for the SBOM comparison view: TypeScript interfaces for the diff response, a typed REST function that calls the new backend endpoint, a React Query hook, and MSW mocks/fixtures for tests. The comparison page (Tasks 5–6) and export (Task 8) consume this layer.

## Files to Modify
- `src/api/models.ts` — add the `SbomComparison`, `PackageDiffEntry`, `VersionChangeEntry`, `NewVulnerabilityEntry`, `ResolvedVulnerabilityEntry`, and `LicenseChangeEntry` interfaces
- `src/api/rest.ts` — add `compareSboms(left: string, right: string): Promise<SbomComparison>`
- `tests/mocks/handlers.ts` — add an MSW handler for `GET /api/v2/sbom/compare`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query `useQuery` hook keyed on `["sbom-compare", left, right]`, enabled only when both IDs are set
- `tests/mocks/fixtures/sbom-compare.json` — mock comparison response covering all six categories, including at least one `critical` new vulnerability and more than 100 added packages (for virtualization tests in Task 6)

## Implementation Notes
**Backend API contracts** (this endpoint is new, created in Task 3; the frontend calls it manually through the Axios client):
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — query params `left: string`, `right: string` (SBOM IDs). Response 200:
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
  Errors: 400 for missing params, 404 for an unknown SBOM ID. Defined in `modules/fundamental/src/sbom/endpoints/compare.rs` (handler) and `modules/fundamental/src/sbom/model/compare.rs` (structs) in trustify-backend.
- `GET /api/v2/sbom` — existing list endpoint, returns `PaginatedResults<SbomSummary>` (`{ items, total }`). Defined in `modules/fundamental/src/sbom/endpoints/list.rs`. Already wrapped by `src/hooks/useSboms.ts`, so no new client is needed.

Verify these contracts against the backend repo at implementation time using the implement-task cross-repo API verification step. The backend task may still be in review on the `TC-9003` branch.

- Keep the interfaces snake_case so they match the JSON 1:1. Do not add a camelCase transform layer, consistent with the existing types in `src/api/models.ts`.
- `compareSboms` must use the shared Axios instance from `src/api/client.ts`, so base URL and auth interceptors apply. Follow the shape of existing functions such as `fetchSboms()` in `src/api/rest.ts`. Pass the IDs through Axios `params` rather than string concatenation.
- Model `useSbomComparison` on `src/hooks/useSbomById.ts`. Use `enabled: Boolean(left && right)` so no request fires until both sides are selected. Do not retry on 404.
- **Fail-closed:** surface a 404 or 400 as a query error (`isError`). Never map it to an empty `SbomComparison`, which the UI would render as "no differences".

**Conventions:**
- Per CONVENTIONS.md §API layer: add the typed function to `src/api/rest.ts` using the Axios client from `src/api/client.ts`, and put the React Query hook in `src/hooks/`. See `src/hooks/useSbomById.ts`.
  Applies: task modifies `src/api/rest.ts` matching the convention's API layer (`src/api/`, `src/hooks/`) scope.
- Per CONVENTIONS.md §Naming: the hook file and export use camelCase (`useSbomComparison.ts` / `useSbomComparison`).
  Applies: task modifies `src/hooks/useSbomComparison.ts` matching the convention's hooks/utilities naming scope.
- Per CONVENTIONS.md §Testing: mock the endpoint with MSW in `tests/mocks/handlers.ts` and put fixture data in `tests/mocks/fixtures/`.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW test (`tests/`) scope.
- Per CONVENTIONS.md §State management: use React Query for the comparison server state; do not add new global state.
  Applies: task modifies `src/hooks/useSbomComparison.ts` matching the convention's server-state (`src/hooks/*.ts`) scope.

**Project constraints (docs/constraints.md):**
- §2: Conventional Commits, `Implements TC-XXXX` footer, `Assisted-by:` trailer.
- §3: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5: Change only the listed files; reuse the existing client and hook patterns.

## Reuse Candidates
- `src/api/client.ts` — shared Axios instance (base URL, auth interceptors).
- `src/api/rest.ts::fetchSboms` — pattern for typed API functions.
- `src/hooks/useSbomById.ts` — pattern for a parameterized `useQuery` hook.
- `tests/mocks/handlers.ts` and `tests/mocks/fixtures/sboms.json` — existing MSW setup and SBOM fixtures. Reuse the fixture SBOM IDs in the compare fixture.

## Acceptance Criteria
- [ ] `SbomComparison` and the row interfaces in `src/api/models.ts` match the backend JSON contract exactly
- [ ] `compareSboms(left, right)` issues `GET /api/v2/sbom/compare` with `left` and `right` query params through the shared Axios client
- [ ] `useSbomComparison(left, right)` does not fire while either ID is missing
- [ ] A 404 or 400 response surfaces as a query error, not as an empty comparison (fail-closed)
- [ ] An MSW handler and fixture exist for the compare endpoint

## Test Requirements
- [ ] Hook test (Vitest + React Testing Library `renderHook`): with both IDs, it returns the fixture data
- [ ] Hook test: with one ID missing, no request is made
- [ ] Hook test: when MSW returns 404, `isError` is true and `data` is undefined (fail-closed path)

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/hooks` — new hook tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Expose GET /api/v2/sbom/compare endpoint (API contract; implementation can start against MSW mocks)
