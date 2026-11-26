## Repository
trustify-backend

## Target Branch
main

## Description
Add optional filter query parameters to `GET /api/v2/search` so users can narrow results. This addresses the TC-9002 MVP requirement "Add filters" ("Some kind of filtering capability").

**Assumptions pending clarification (TC-9002):**
- ASSUMPTION: The Feature does not say which filters are wanted. This task proposes the filters that map to fields already present in the backend models:
  - `type` — entity type (`sbom`, `advisory`, `package`)
  - `severity` — advisory severity (from `AdvisorySummary.severity` in `modules/fundamental/src/advisory/model/summary.rs`)
  - `license` — package license (from `PackageSummary.license` in `modules/fundamental/src/package/model/summary.rs`, backed by `entity/src/package_license.rs`)
  The Feature owner must confirm or replace this list before implementation starts.
- ASSUMPTION: Filters are backend query parameters only. Frontend filter controls are out of scope (no frontend repository or design was provided; see the "Better UI" exclusion in the impact map).
- ASSUMPTION: Multiple filters combine with AND; multiple values of the same filter (comma-separated) combine with OR.
- ASSUMPTION: Filters are optional and additive — omitting them preserves current behavior.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — accept and validate `type`, `severity`, and `license` query parameters
- `modules/search/src/service/mod.rs` — apply the filters in the search SQL
- `tests/api/search.rs` — add filter tests
- `README.md` — document the new search filter parameters

## API Changes
- `GET /api/v2/search` — MODIFY: new optional query parameters `type`, `severity`, `license`. Unknown filter values return 400. Response body shape unchanged.

## Implementation Notes
- Apply filters inside the SQL built by `SearchService` (`modules/search/src/service/mod.rs`) so `total` in `PaginatedResults<T>` reflects the filtered count — do not filter after pagination.
- Use the shared filtering helpers in `common/src/db/query.rs` rather than building ad-hoc `WHERE` clauses.
- `severity` filter: join or filter on the advisory entity (`entity/src/advisory.rs`); the field is exposed as `AdvisorySummary.severity` in `modules/fundamental/src/advisory/model/summary.rs` — reuse its type/enum for parameter parsing.
- `license` filter: use the package-license mapping in `entity/src/package_license.rs` (exposed as `PackageSummary.license` in `modules/fundamental/src/package/model/summary.rs`).
- Validation: invalid `type` or `severity` values must produce `AppError` (400) from `common/src/error.rs`, not be silently ignored. A silently ignored filter would return unfiltered (or empty) results and look like success.
- Per CONVENTIONS.md §Query helpers: use the shared filtering, pagination, and sorting helpers from `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust database query scope.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Response types: list-style responses return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's endpoint handler scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against the PostgreSQL test database, using `assert_eq!(resp.status(), StatusCode::OK)`.
  Applies: task modifies `tests/api/search.rs` matching the convention's `tests/api/` scope.

Constraints (docs/constraints.md):
- §2 Commit rules: Conventional Commits format, Jira task ID in footer, `Assisted-by:` trailer.
- §3 PR rules: `gh pr create --base main`; post the PR link on the Jira task.
- §5 Code change rules: scope changes to the listed files; inspect before modifying; reuse `common/src/db/query.rs` filtering instead of duplicating it.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — `severity` field and its type for parsing the `severity` filter
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — `license` field
- `modules/fundamental/src/advisory/endpoints/list.rs` / `modules/fundamental/src/package/endpoints/list.rs` — existing list endpoints; check whether they already accept filter parameters and mirror their naming/parsing

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=...&type=advisory` returns only advisories
- [ ] `GET /api/v2/search?q=...&severity=critical` returns only advisories with that severity
- [ ] `GET /api/v2/search?q=...&license=Apache-2.0` returns only packages with that license
- [ ] Combining filters applies AND semantics; comma-separated values within one filter apply OR semantics
- [ ] `total` in the response reflects the filtered count
- [ ] An invalid filter value (e.g., `type=foo`) returns 400 with an error body, instead of silently returning unfiltered or empty results
- [ ] Requests without filter parameters behave exactly as before
- [ ] `README.md` documents the new parameters

## Test Requirements
- [ ] Integration test for each filter (`type`, `severity`, `license`) returning only matching entities
- [ ] Integration test for combined filters (AND) and multi-value filters (OR)
- [ ] Integration test asserting `total` equals the filtered count
- [ ] Integration test: invalid filter value returns 400 (fail-closed, not an empty 200)
- [ ] Integration test: no filters returns the same results as before this change
- [ ] Existing tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test api search` — search integration tests pass
- `curl -i "http://localhost:8080/api/v2/search?q=openssl&type=foo"` — returns 400

## Documentation Updates
- `README.md` — add the `type`, `severity`, and `license` query parameters for `GET /api/v2/search`, with allowed values and combination semantics

## Dependencies
- Depends on: Task 2 — Optimize search queries and add response caching
