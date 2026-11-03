# Task 4 — Add comparison API client, types, and React Query hook

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the data layer the SBOM comparison UI needs for TC-9003: TypeScript types for the comparison response, a typed REST function for `GET /api/v2/sbom/compare`, a React Query hook, and MSW mocks for tests. The comparison page (Task 6) and the export (Task 8) both use this layer.

## Files to Modify
- `src/api/models.ts` — add `SbomComparison`, `PackageDiff`, `VersionChange`, `NewVulnerability`, `ResolvedVulnerability`, and `LicenseChange` interfaces
- `src/api/rest.ts` — add `compareSboms(left: string, right: string): Promise<SbomComparison>`
- `tests/mocks/handlers.ts` — add an MSW handler for `GET /api/v2/sbom/compare`

## Files to Create
- `src/hooks/useSbomComparison.ts` — React Query `useQuery` hook keyed on `["sbom-compare", left, right]`, enabled only when both IDs are set
- `tests/mocks/fixtures/sbom-compare.json` — mock comparison response covering all six categories, including at least one `critical` new vulnerability and more than 100 added packages for virtualization tests

## Implementation Notes
- **Backend API contracts** (manual REST call; this endpoint is not covered by any generated client):
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}`
    - Query params: `left: string` and `right: string` (SBOM IDs)
    - 200 response: `SbomComparison`
      ```ts
      interface SbomComparison {
        added_packages: { name: string; version: string; license: string | null; advisory_count: number }[];
        removed_packages: { name: string; version: string; license: string | null; advisory_count: number }[];
        version_changes: { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }[];
        new_vulnerabilities: { advisory_id: string; severity: "critical" | "high" | "medium" | "low"; title: string; affected_package: string }[];
        resolved_vulnerabilities: { advisory_id: string; severity: "critical" | "high" | "medium" | "low"; title: string; previously_affected_package: string }[];
        license_changes: { name: string; left_license: string | null; right_license: string | null }[];
      }
      ```
    - Errors: 400 for a missing or invalid param, 404 when an SBOM is not found
    - Source: `modules/fundamental/src/sbom/endpoints/compare.rs` and `modules/fundamental/src/sbom/model/compare.rs` in trustify-backend (created by Tasks 2/3)
  - `GET /api/v2/sbom` (existing): returns `{ items: SbomSummary[], total: number }`. Source: `modules/fundamental/src/sbom/endpoints/list.rs`. Already wrapped by `fetchSboms()` / `useSboms`.
  - When you implement this task, verify these contracts against the trustify-backend repo using the implement-task cross-repo API verification step.
- Keep the snake_case field names in the TS interfaces so they mirror the API, following the existing interfaces in `src/api/models.ts`.
- Build `compareSboms` on the shared Axios instance from `src/api/client.ts`, following the existing functions in `src/api/rest.ts` such as `fetchSboms()`. Pass the IDs through Axios `params` rather than concatenating strings.
- Model `useSbomComparison` on `src/hooks/useSbomById.ts`:
  - Set `enabled: !!left && !!right`.
  - Surface 404/400 as `error` (do not swallow errors into empty data), so the page can tell "SBOM not found" apart from "no changes".
- Per CONVENTIONS.md §API layer: typed API functions go in `src/api/rest.ts` and React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's API layer scope. Example: `fetchSboms()` in `src/api/rest.ts` with `src/hooks/useSboms.ts`.
- Per CONVENTIONS.md §Naming: hooks and utilities use camelCase. Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hook naming scope. Example: `src/hooks/useSbomById.ts`.
- Per CONVENTIONS.md §Testing: use MSW for API mocking in Vitest tests. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW mock scope. Example: the existing SBOM handlers in `tests/mocks/handlers.ts` with `tests/mocks/fixtures/sboms.json`.
- Constraints (docs/constraints.md):
  - §2: commit format, Jira footer, `Assisted-by` trailer
  - §3: `gh pr create --base TC-9003`, and post the PR link to Jira
  - §5: scoped changes, reuse the existing client/hooks

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchSboms` — pattern for typed GET functions
- `src/hooks/useSbomById.ts` — `useQuery` hook pattern with a parameterized key
- `tests/mocks/handlers.ts` and `tests/mocks/fixtures/sboms.json` — MSW handler/fixture pattern

## Acceptance Criteria
- [ ] `SbomComparison` and the related interfaces in `src/api/models.ts` match the backend response shape exactly
- [ ] `compareSboms(left, right)` calls `GET /api/v2/sbom/compare` with `left`/`right` query params through the shared Axios client
- [ ] `useSbomComparison(left, right)` sends no request while either ID is empty
- [ ] `useSbomComparison` exposes 400/404 responses as errors, not as empty data
- [ ] An MSW handler and fixture exist for the compare endpoint

## Test Requirements
- [ ] Hook test: with both IDs set, the hook returns the fixture data
- [ ] Hook test: with one ID missing, no request is made (`enabled` false)
- [ ] Hook test: a 404 from MSW sets the hook into an error state with no data (fail-closed; no empty diff rendered)

## Verification Commands
- `npx vitest run src/hooks` — hook tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint
