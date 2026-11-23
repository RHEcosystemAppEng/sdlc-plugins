# Task 4 — Add SBOM comparison API types, client function, and React Query hook

**Summary:** Add SBOM comparison API client and useSbomComparison hook
**Epic:** TC-9003: SBOM comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003; fixVersion scope = both)

---

## Repository
trustify-ui

## Target Branch
TC-9003

## Description
Add the frontend data layer for the SBOM comparison view (TC-9003): TypeScript types for the diff response, a typed REST function calling the new backend endpoint, a React Query hook used by the comparison page, and MSW mocks so page-level tests (Tasks 5–8) can run without a backend. The auto-generated/typed client in `src/api/rest.ts` does not cover the new endpoint, so this task adds a manual REST call against the backend contract below.

## Files to Modify
- `src/api/models.ts` — add `SbomComparison`, `PackageDiffEntry`, `VersionChange`, `VersionDirection`, `VulnerabilityDiffEntry` (new/resolved), `LicenseChange` interfaces
- `src/api/rest.ts` — add `compareSboms(left: string, right: string): Promise<SbomComparison>`
- `tests/mocks/handlers.ts` — add an MSW handler for `GET /api/v2/sbom/compare` (200 fixture, 404 for an unknown ID)

## Files to Create
- `src/hooks/useSbomComparison.ts` — `useQuery` hook keyed on `["sbom-compare", left, right]`, `enabled` only when both IDs are present
- `src/hooks/useSbomComparison.test.ts` — hook tests using MSW
- `tests/mocks/fixtures/sbom-compare.json` — mock diff response covering all six sections, including at least one `critical` new vulnerability and >100 added packages for virtualization tests

## Implementation Notes
**Backend API contracts:**
- `GET /api/v2/sbom/compare?left={id1}&right={id2}` — query params `left: string`, `right: string` (SBOM IDs). Response `200`:
  ```ts
  {
    added_packages: { name: string; version: string; license: string; advisory_count: number }[];
    removed_packages: { name: string; version: string; license: string; advisory_count: number }[];
    version_changes: { name: string; left_version: string; right_version: string; direction: "upgrade" | "downgrade" }[];
    new_vulnerabilities: { advisory_id: string; severity: string; title: string; affected_package: string }[];
    resolved_vulnerabilities: { advisory_id: string; severity: string; title: string; previously_affected_package: string }[];
    license_changes: { name: string; left_license: string; right_license: string }[];
  }
  ```
  `400` when a param is missing; `404` when either SBOM does not exist. Defined in `modules/fundamental/src/sbom/endpoints/compare.rs` and `modules/fundamental/src/sbom/model/compare.rs` (trustify-backend, Tasks 2–3).
- `GET /api/v2/sbom` — existing list endpoint (`modules/fundamental/src/sbom/endpoints/list.rs`), returns `PaginatedResults<SbomSummary>` (`{ items, total }`); already wrapped by `fetchSboms()` in `src/api/rest.ts` and `useSboms` in `src/hooks/useSboms.ts` — reuse, do not duplicate.

Verify these contracts against the backend repo during implementation using the implement-task cross-repo API verification step (the backend task lands on the same `TC-9003` branch).

- Keep API field names snake_case in `models.ts` to match the wire format (follow how existing interfaces in `src/api/models.ts` mirror backend field names); do not rename in the transport layer.
- Implement `compareSboms` with the shared Axios instance from `src/api/client.ts` (base URL + auth interceptors), mirroring `fetchSboms()` / the SBOM-detail fetch function in `src/api/rest.ts`; pass IDs via `params: { left, right }` rather than string concatenation.
- Model the hook on `src/hooks/useSbomById.ts` (single-resource `useQuery` with an ID-based key and `enabled` guard).
- Fail-closed: a `404`/`400` must surface as the hook's `error` state — do not catch the error and return an empty `SbomComparison`, which would render as "no changes". The guard site is `compareSboms` in `src/api/rest.ts` (must not swallow Axios errors) and `useSbomComparison` (must not set `placeholderData`/fallback to an empty diff).

**Conventions:**
- Per CONVENTIONS.md §API layer: Axios client in `src/api/client.ts`, typed functions in `src/api/rest.ts`, React Query hooks in `src/hooks/`. Applies: task modifies `src/api/rest.ts` matching the convention's `src/api/` and `src/hooks/` scope. Example: `fetchSboms()` in `src/api/rest.ts` with `src/hooks/useSboms.ts`.
- Per CONVENTIONS.md §State management: server state via React Query only (no Redux / local caches of the diff). Applies: task modifies `src/hooks/useSbomComparison.ts` matching the convention's React Query hook (`.ts`) scope. Example: `src/hooks/useSbomById.ts`.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities. Applies: task modifies `src/hooks/useSbomComparison.ts` matching the convention's hook/utility naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW for API mocking. Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW mocking scope. Example: existing handlers in `tests/mocks/handlers.ts` and fixtures in `tests/mocks/fixtures/sboms.json`.

**Project constraints (docs/constraints.md):**
- §2 Commit rules: Conventional Commits, `Implements <task-key>` footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base TC-9003`; post the PR link on the Jira task.
- §5 Code change rules: scope to listed files; inspect `rest.ts`/hooks before modifying; reuse the Axios instance; doc comments on every test function.

## Reuse Candidates
- `src/api/client.ts` — shared Axios instance (base URL, auth interceptors)
- `src/api/rest.ts::fetchSboms` — pattern for typed REST functions
- `src/hooks/useSbomById.ts` — pattern for an ID-keyed `useQuery` hook with `enabled` guard
- `src/hooks/useSboms.ts` — existing SBOM list hook, to be reused by the selectors in Task 5 (not re-implemented)
- `tests/mocks/handlers.ts`, `tests/mocks/fixtures/sboms.json` — MSW handler and fixture patterns

## Acceptance Criteria
- [ ] `SbomComparison` and row types in `src/api/models.ts` match the backend contract field-for-field
- [ ] `compareSboms(left, right)` calls `GET /api/v2/sbom/compare` with `left` and `right` query params via the shared Axios client
- [ ] `useSbomComparison(left, right)` does not fire a request until both IDs are defined
- [ ] Fail-closed: backend `404`/`400` responses surface as the hook's `error` state, never as an empty diff
- [ ] MSW handler and fixture exist for success and not-found cases

## Test Requirements
- [ ] Hook test: with both IDs, returns fixture data with all six sections
- [ ] Hook test: with one ID undefined, no request is made (`isFetching` false, MSW handler not called)
- [ ] Fail-closed hook test: MSW returns `404` → hook exposes `isError === true` and `data` is `undefined` (not an empty `SbomComparison`)

## Verification Commands
- `npx tsc --noEmit` — no type errors
- `npx vitest run src/hooks/useSbomComparison.test.ts` — tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9003 from main
- Depends on: Task 3 — Expose GET /api/v2/sbom/compare endpoint
