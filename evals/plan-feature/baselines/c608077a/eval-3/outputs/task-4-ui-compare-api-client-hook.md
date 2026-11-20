# Task 4 — Add SBOM comparison API types, REST function, and React Query hook

**Summary:** Add SbomComparison types, fetchSbomComparison() and useSbomComparison hook with MSW mocks
**Epic:** TC-9003: Comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend data layer for the SBOM comparison view (TC-9003): TypeScript types for the diff response, a typed REST function that calls the new backend endpoint, a React Query hook, and MSW mock data for tests. The UI tasks (Task 5, Task 6, Task 8) consume this layer. The project has no auto-generated client for the new endpoint, so this is a manual REST call and must match the backend contract exactly.

## Files to Modify
- `src/api/models.ts` — add the `SbomComparison`, `PackageDiffEntry`, `VersionChangeEntry`, `VulnerabilityDiffEntry`, `ResolvedVulnerabilityEntry`, and `LicenseChangeEntry` interfaces and the `VersionDirection` type
- `src/api/rest.ts` — add `fetchSbomComparison(leftId: string, rightId: string): Promise<SbomComparison>`
- `tests/mocks/handlers.ts` — add an MSW handler for `GET /api/v2/sbom/compare` that returns the new fixture. Return 404 when the ID is `missing`, so error paths can be tested.

## Files to Create
- `src/hooks/useSbomComparison.ts` — `useSbomComparison(leftId?: string, rightId?: string)` React Query hook, enabled only when both IDs are set
- `src/hooks/useSbomComparison.test.ts` — unit tests for the hook
- `tests/mocks/fixtures/sbom-compare.json` — mock diff response with at least one entry per category, including one `critical` new vulnerability and enough entries to exercise rendering

## Implementation Notes
- **Backend API contracts.**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` returns `SbomComparison`. Errors: 400 for a missing or invalid param, 404 for an unknown SBOM ID. Defined in `trustify-backend`:
    - handler: `modules/fundamental/src/sbom/endpoints/compare.rs` (Task 3)
    - route registration: `modules/fundamental/src/sbom/endpoints/mod.rs`
    - model: `modules/fundamental/src/sbom/model/compare.rs` (Task 2)
  - `SbomComparison`:
    ```ts
    interface SbomComparison {
      added_packages: PackageDiffEntry[];
      removed_packages: PackageDiffEntry[];
      version_changes: VersionChangeEntry[];
      new_vulnerabilities: VulnerabilityDiffEntry[];
      resolved_vulnerabilities: ResolvedVulnerabilityEntry[];
      license_changes: LicenseChangeEntry[];
    }
    interface PackageDiffEntry { name: string; version: string; license: string | null; advisory_count: number; }
    interface VersionChangeEntry { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade"; }
    interface VulnerabilityDiffEntry { advisory_id: string; severity: string; title: string; affected_package: string; }
    interface ResolvedVulnerabilityEntry { advisory_id: string; severity: string; title: string; previously_affected_package: string; }
    interface LicenseChangeEntry { name: string; left_license: string | null; right_license: string | null; }
    ```
  - `GET /api/v2/sbom` (existing; used by the selectors in Task 5) returns `PaginatedResults<SbomSummary>`. Defined in `modules/fundamental/src/sbom/endpoints/list.rs`; consumed through the existing `useSboms` hook.
  - Keep the field names in snake_case exactly as the backend returns them. Do not add a camelCase transform layer; check the existing interfaces in `src/api/models.ts` and follow their casing convention.
  - Verify these contracts against the `trustify-backend` repo at implementation time, using the implement-task cross-repo API verification step. Task 3 may still be in review on the `TC-9003` branch.
- **Axios client.** Implement `fetchSbomComparison` with the shared Axios instance in `src/api/client.ts` (base URL and auth interceptors). Pass the IDs through `params: { left, right }` rather than string concatenation, so they are URL-encoded.
- **Query key and caching.** Use the query key `["sbomComparison", leftId, rightId]`. Set `enabled: Boolean(leftId && rightId)`. A comparison of two fixed IDs is stable, so a moderate `staleTime` is fine. This is a read-only query, so the mutation and invalidation pattern does not apply.
- **Error handling.** Do not catch and swallow errors in `fetchSbomComparison`. A 404 or 400 must surface as React Query `error`, so the page can show an error state instead of an empty "no changes" diff.
- Per CONVENTIONS.md §API layer: add typed functions to `src/api/rest.ts` using the client from `src/api/client.ts`, and put React Query hooks in `src/hooks/`. See `src/api/rest.ts::fetchSboms` and `src/hooks/useSbomById.ts` for the established pattern.
  Applies: task modifies `src/api/rest.ts` matching the convention's `src/api/` + `src/hooks/` API-layer scope.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities, so name the hook `useSbomComparison.ts`.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hook naming scope.
- Per CONVENTIONS.md §Testing: use Vitest with MSW for API mocking; register the handler in `tests/mocks/handlers.ts` and the fixture in `tests/mocks/fixtures/`. See `tests/mocks/fixtures/sboms.json`.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW test scope.
- Constraints (docs/constraints.md):
  - §2 Commit rules: Conventional Commits format, a `Implements TC-<task-key>` footer, and an `Assisted-by:` trailer.
  - §3 PR rules: use `--base TC-9003` and post the PR link on the Jira task.
  - §5 Code change rules: stay within the listed files; inspect before modifying; reuse existing helpers.
  - §1.4/§1.5: no unrelated refactoring.

## Reuse Candidates
- `src/api/client.ts` — shared Axios instance; must be used for the request
- `src/api/rest.ts::fetchSboms` — pattern for a typed GET with query params
- `src/hooks/useSbomById.ts` — pattern for a parameterised `useQuery` hook with `enabled` gating
- `tests/mocks/handlers.ts` / `tests/mocks/fixtures/sboms.json` — existing MSW handler and fixture structure

## Acceptance Criteria
- [ ] `src/api/models.ts` exports interfaces matching the backend `SbomComparison` contract field-for-field (snake_case)
- [ ] `fetchSbomComparison(left, right)` issues `GET /api/v2/sbom/compare` with `left` and `right` query params through the shared Axios client
- [ ] `useSbomComparison` does not fire a request until both IDs are defined
- [ ] A 404 from the backend surfaces as the hook's `error` state, not as an empty comparison
- [ ] The MSW handler and fixture for the compare endpoint are available to all tests

## Test Requirements
- [ ] Hook test: with both IDs set, the hook returns the fixture data
- [ ] Hook test: with one ID undefined, no request is made (`fetchStatus` is `idle`)
- [ ] Hook test: when the MSW handler returns 404, the hook reports `isError` and `data` stays undefined

## Verification Commands
- `npx vitest run src/hooks/useSbomComparison.test.ts` — all tests pass
- `npx tsc --noEmit` — no type errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Add GET /api/v2/sbom/compare endpoint with integration tests (API contract source)
