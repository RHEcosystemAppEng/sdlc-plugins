## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering capability to the unified search endpoint `GET /api/v2/search` so users
can narrow search results by entity type and by a small set of entity attributes that
already exist in the data model.

This addresses the MVP requirement "Add filters — some kind of filtering capability"
from TC-9002.

**Ambiguity flagged (pending clarification on TC-9002):** the Feature says only "some
kind of filtering capability". It does not specify which fields are filterable, which
entity types the filters apply to, whether filters combine with AND or OR, or whether
filters are exposed in a UI (the UI requirement is excluded — see impact map). The
assumptions below fill these gaps and must be confirmed by the Feature owner.

**Assumptions pending clarification:**
- ASSUMPTION C1: filters are added to the backend API only (query parameters on
  `GET /api/v2/search`); no frontend work is planned.
- ASSUMPTION C2: initial filter set, chosen because the fields already exist in the model:
  - `type` — restrict to one or more entity types (`sbom`, `advisory`, `package`)
  - `severity` — advisory severity (field exists on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`)
  - `license` — package license (field exists on `PackageSummary` in `modules/fundamental/src/package/model/summary.rs`; mapping in `entity/src/package_license.rs`)
- ASSUMPTION C3: multiple values for the same filter combine with OR; different filters
  combine with AND. Attribute filters apply only to the entity type that owns the attribute
  (e.g., `severity` restricts advisories and excludes SBOM/package results).
- ASSUMPTION C4: unknown filter names or invalid values are rejected with `400 Bad Request`
  rather than silently ignored (silently ignoring would return unfiltered results that look
  like a successful filtered search).

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — accept and validate the new filter query parameters on `GET /api/v2/search`
- `modules/search/src/service/mod.rs` — apply the filters to the search query
- `common/src/db/query.rs` — extend the shared filtering helpers only if the needed filter operators (multi-value IN on enum/text) are not already supported
- `tests/api/search.rs` — add filter tests

## API Changes
- `GET /api/v2/search` — MODIFY: add optional query parameters `type` (multi-value: `sbom|advisory|package`), `severity` (multi-value, advisory severities), `license` (multi-value, SPDX identifier). Response shape (`PaginatedResults<T>`) unchanged. Invalid filter values return `400 Bad Request`.

## Implementation Notes
- Parse filter parameters in `modules/search/src/endpoints/mod.rs` using the same Axum
  query-extraction style the endpoint already uses for its search/pagination parameters, and
  pass a typed filter struct to `SearchService` in `modules/search/src/service/mod.rs`.
- Validate values against the known set: entity types are a fixed enum; severity values
  must match the values stored for `AdvisorySummary.severity`
  (`modules/fundamental/src/advisory/model/summary.rs`). Return `AppError`
  (`common/src/error.rs`) mapped to `400` on invalid input — this is the fail-closed guard
  for ASSUMPTION C4 and belongs in the endpoint parameter-parsing code in
  `modules/search/src/endpoints/mod.rs`.
- License filtering joins through the package-license mapping in
  `entity/src/package_license.rs`; inspect how `PackageService`
  (`modules/fundamental/src/package/service/mod.rs`) exposes `license` on `PackageSummary`
  and reuse the same join rather than writing a new one.
- Apply filters via the shared filtering helpers in `common/src/db/query.rs`. Only extend
  that file if a needed operator is missing; any extension must remain generic so the
  `fundamental` list endpoints can use it later.
- Filters must compose with the full-text match (Task 1) and relevance ordering (Task 2):
  filter in the WHERE clause, keep the `@@` index predicate, and keep ordering unchanged.
- Per CONVENTIONS.md §Module pattern: parameter parsing stays in `endpoints/`, query logic in `service/`.
  Applies: task modifies modules/search/src/endpoints/mod.rs matching the convention's `modules/*/src/{model,service,endpoints}` Rust module scope.
- Per CONVENTIONS.md §Error handling: invalid filters surface as `AppError` from a handler returning `Result<T, AppError>`, with `.context()` on DB errors.
  Applies: task modifies modules/search/src/endpoints/mod.rs matching the convention's Rust handler/service (`.rs`) scope.
- Per CONVENTIONS.md §Endpoint registration: routes remain registered in `modules/search/src/endpoints/mod.rs`; no change to `server/src/main.rs` mounting is expected.
  Applies: task modifies modules/search/src/endpoints/mod.rs matching the convention's `endpoints/mod.rs` route-registration scope.
- Per CONVENTIONS.md §Query helpers: implement filtering through `common/src/db/query.rs`.
  Applies: task modifies common/src/db/query.rs matching the convention's shared query-helper (`common/src/db/query.rs`) scope.
- Per CONVENTIONS.md §Response types: the filtered list keeps returning `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies modules/search/src/endpoints/mod.rs matching the convention's list-endpoint (`endpoints/*.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/search.rs` against the real PostgreSQL test DB using `assert_eq!(resp.status(), StatusCode::OK)`; see `tests/api/advisory.rs`.
  Applies: task modifies tests/api/search.rs matching the convention's `tests/api/*.rs` integration-test scope.
- Constraints (docs/constraints.md): Conventional Commits with Jira ID footer and
  `Assisted-by:` trailer (§2.1–2.3); PR targets `main` and is linked on the Jira task
  (§3.2, §3.3); stay within listed files, inspect before modifying, reuse existing helpers
  (§5.1, §5.2, §5.4).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers; primary mechanism for applying filters
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — defines the `severity` field and its value set
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — defines the `license` field
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package/license join logic to reuse
- `entity/src/package_license.rs` — Package-License mapping entity

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=<term>&type=advisory` returns only advisories
- [ ] `type` accepts multiple values (e.g., `type=sbom&type=package`) and returns the union of those types
- [ ] `severity=<value>` returns only advisories with that severity
- [ ] `license=<spdx-id>` returns only packages with that license
- [ ] Different filters combine with AND; multiple values of one filter combine with OR (ASSUMPTION C3)
- [ ] An unknown filter value (e.g., `type=foo`, invalid severity) returns `400 Bad Request` with an error message, never an unfiltered `200` result (fail-closed)
- [ ] Requests without any filter parameter behave exactly as before (backward compatible)
- [ ] Filtered results remain paginated via `PaginatedResults<T>` and `total` reflects the filtered count

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: `type=advisory` returns only advisories
- [ ] Integration test: multi-value `type` returns union of types
- [ ] Integration test: `severity` filter returns only matching advisories
- [ ] Integration test: `license` filter returns only matching packages
- [ ] Integration test: combined `type` + `severity` filters apply AND semantics
- [ ] Integration test: invalid `type` / `severity` value returns `400` (asserts the response is not `200` with unfiltered results)
- [ ] Integration test: no filters returns the same results as before the change
- [ ] Integration test: `total` in the paginated response equals the filtered count
- [ ] All existing tests in `tests/api/` pass

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass
- `curl -s -o /dev/null -w '%{http_code}' 'http://localhost:8080/api/v2/search?q=test&type=foo'` — returns `400`

## Documentation Updates
- `README.md` — document the new `GET /api/v2/search` filter parameters if the README lists API endpoints/parameters

## Dependencies
- Depends on: Task 1 — Add full-text search indexes and use them in SearchService
