# Task 3 — Add SBOM comparison API types, client function and React Query hook

**Summary:** TC-9003: Add SBOM comparison API client and useSbomComparison hook
**Issue type:** Task
**Parent (Epic):** Epic 2 — TC-9003: SBOM comparison UI
**Labels:** ai-generated-jira
**Priority:** Critical (inherited from TC-9003)
**Fix Versions:** RHTPA 1.5.0 (inherited from TC-9003)

---

## Repository
trustify-ui

## Target Branch
main

## Description
Add the frontend data layer for the SBOM comparison view (TC-9003): TypeScript types for the
`GET /api/v2/sbom/compare` response, a typed REST function, a React Query hook, and MSW mocks
and fixtures so the comparison page (Task 4) and diff sections (Task 5) can be developed and
tested. The endpoint is new (Task 2) and is not covered by any existing client function, so
this is a manual REST call through the existing Axios client.

## Files to Modify
- `src/api/models.ts` — add `SbomComparison`, `AddedPackage`, `RemovedPackage`, `VersionChange`, `VersionChangeDirection`, `NewVulnerability`, `ResolvedVulnerability`, `LicenseChange` interfaces
- `src/api/rest.ts` — add `fetchSbomComparison(left: string, right: string): Promise<SbomComparison>`
- `tests/mocks/handlers.ts` — add an MSW handler for `GET /api/v2/sbom/compare` (success, 400 for missing param, 404 for unknown ID)

## Files to Create
- `src/hooks/useSbomComparison.ts` — `useSbomComparison(left?: string, right?: string)` React Query `useQuery` hook, `enabled` only when both IDs are present
- `tests/mocks/fixtures/sbom-compare.json` — mock comparison response with entries in all six categories, including at least one `critical` new vulnerability and >100 added packages variant (or a generator) for virtualization tests
- `src/hooks/useSbomComparison.test.ts` — hook unit tests

## Implementation Notes
- **Backend API contracts:**
  - `GET /api/v2/sbom/compare?left={id1}&right={id2}` — NEW (Task 2). Query params: `left: string`, `right: string` (SBOM IDs). Response `200`:
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
    Errors: `400` missing/malformed param, `404` unknown SBOM. Defined in `modules/fundamental/src/sbom/endpoints/compare.rs` and `modules/fundamental/src/sbom/model/comparison.rs` (trustify-backend, created by Tasks 1–2).
  - `GET /api/v2/sbom` — EXISTING, returns `PaginatedResults<SbomSummary>` = `{ items: SbomSummary[], total: number }` (see `modules/fundamental/src/sbom/endpoints/list.rs` and `common/src/model/paginated.rs` in trustify-backend). Already consumed by `fetchSboms()` / `useSboms`; no change needed here.
  - Verify these contracts against the backend repo at implementation time using the implement-task cross-repo API verification step (Task 2 may adjust field types, e.g. the SBOM ID type).
- Keep API field names snake_case in the TypeScript interfaces to match the wire format, consistent with existing interfaces in `src/api/models.ts`.
- Follow the existing `fetchSboms()` / SBOM-detail function pattern in `src/api/rest.ts` (uses the Axios instance from `src/api/client.ts` with auth interceptors). Pass params via Axios `params: { left, right }` rather than string concatenation.
- Hook: mirror `src/hooks/useSbomById.ts` — query key `["sbomComparison", left, right]`, `enabled: Boolean(left && right)`. Errors (400/404) must surface as `isError` so the page can show an error state rather than an empty comparison.
- Per CONVENTIONS.md §API layer: typed API functions live in `src/api/rest.ts` and React Query hooks in `src/hooks/`; see `src/hooks/useSbomById.ts`.
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's `src/hooks/*.ts` scope.
- Per CONVENTIONS.md §Naming: camelCase for hooks and utilities (`useSbomComparison`, `fetchSbomComparison`).
  Applies: task creates `src/hooks/useSbomComparison.ts` matching the convention's hook/utility `.ts` naming scope.
- Per CONVENTIONS.md §Testing: Vitest + React Testing Library with MSW for API mocking; register the new handler in `tests/mocks/handlers.ts` alongside existing SBOM handlers.
  Applies: task modifies `tests/mocks/handlers.ts` matching the convention's MSW mock `.ts` scope.
- Constraints (docs/constraints.md): §5.1 scope to listed files; §5.4 reuse `client.ts` Axios instance, do not create a new HTTP client; §2.1–2.3 commit rules; §3.3 PR `--base main`.

## Reuse Candidates
- `src/api/client.ts` — Axios instance with base URL and auth interceptors
- `src/api/rest.ts::fetchSboms` — pattern for typed REST functions
- `src/hooks/useSbomById.ts` — pattern for a parameterized `useQuery` hook
- `tests/mocks/handlers.ts` / `tests/mocks/fixtures/sboms.json` — existing MSW handler and fixture patterns

## Acceptance Criteria
- [ ] `SbomComparison` and item interfaces in `src/api/models.ts` match the backend contract field-for-field
- [ ] `fetchSbomComparison(left, right)` issues `GET /api/v2/sbom/compare` with `left` and `right` query params via the shared Axios client
- [ ] `useSbomComparison` does not fire a request unless both IDs are provided
- [ ] `useSbomComparison` exposes 400/404 responses as an error state (not as an empty successful result)
- [ ] MSW handler and fixture exist for success, 400 and 404 cases

## Test Requirements
- [ ] Hook test: with both IDs, returns the fixture data from the MSW handler
- [ ] Hook test: with one ID missing, no request is made
- [ ] Hook test: 404 response results in `isError === true`

## Dependencies
- Depends on: Task 2 — Add GET /api/v2/sbom/compare endpoint (contract source of truth)
