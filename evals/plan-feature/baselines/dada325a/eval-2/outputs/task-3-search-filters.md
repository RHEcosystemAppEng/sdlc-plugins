**Summary:** Add filter parameters to GET /api/v2/search

**Labels:** ai-generated-jira | **Priority:** Normal | **Fix Versions:** RHTPA 1.6.0

## Repository
trustify-backend

## Target Branch
main

## Description
Part of TC-9002 ("Improve search experience"), MVP requirement "Add filters".

The Feature only asks for "some kind of filtering capability", so this task is scoped
under planning assumption A4 (see the TC-9002 impact map): the MVP filters are those
backed by attributes already exposed in the model layer:

- `type` — entity type: `sbom`, `advisory`, `package` (multi-value)
- `severity` — advisory severity (from `AdvisorySummary`)
- `license` — package license (from `PackageSummary`)

The filter set must be confirmed with the Feature owner (clarification question 3)
before implementation starts; additional filters (e.g. date ranges) are out of scope
for this task.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — parse and validate `type`, `severity`, `license` query parameters; return 400 for invalid values
- `modules/search/src/service/mod.rs` — apply filters to the search query using the shared filter helpers
- `tests/api/search.rs` — add filter tests

## API Changes
- `GET /api/v2/search` — MODIFY: new optional query parameters `type` (repeatable: `sbom|advisory|package`), `severity` (advisory severity value), `license` (package license identifier). Omitting all filters keeps current behaviour. Invalid values return `400 Bad Request`.

## Implementation Notes
- Builds on Task 1 (indexed, paginated query). Filters must be applied in SQL before limit/offset so `total` reflects the filtered set.
- Entity-type filter: skip the sub-query for excluded entity types rather than post-filtering in Rust.
- `severity` applies only to advisories and `license` only to packages: define and document whether supplying `severity` implicitly restricts results to advisories (recommended) — confirm with the Feature owner.
- Severity values: reuse the severity type used by `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs`; license: join via `entity/src/package_license.rs` as `PackageService` does.
- Unknown or malformed filter values must be rejected with `AppError` → 400, never silently ignored — silently dropping a filter would return an unfiltered result that looks like a successful filtered search.
- Per CONVENTIONS.md §Query helpers: build filter predicates with the shared filtering helpers in `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's database query scope.
- Per CONVENTIONS.md §Error handling: validation failures return `AppError` from `common/src/error.rs` via `Result<T, AppError>`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's handler scope.
- Per CONVENTIONS.md §Response types: keep returning `PaginatedResults<T>` with `total` computed after filtering. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md §Testing: integration tests against a real PostgreSQL test database using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope.
- Constraints (docs/constraints.md): §2 commit rules (Conventional Commits, `Implements TC-<task>` footer, `Assisted-by:` trailer); §3 PR rules (task-ID branch, `--base main`, PR link on Jira task); §5 code change rules (scope to listed files, inspect first, reuse helpers).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — severity field/type to reuse for validation
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — license field
- `modules/fundamental/src/package/service/mod.rs::PackageService` — existing package/license join logic
- `entity/src/package_license.rs` — package-license mapping entity

## Acceptance Criteria
- [ ] `type=advisory` returns only advisories; repeated `type` values return the union of those types
- [ ] `severity=<value>` returns only advisories with that severity
- [ ] `license=<value>` returns only packages with that license
- [ ] Filters combine with `q` and with each other (AND semantics), and `total` reflects the filtered count
- [ ] Requests with no filter parameters return the same results as before this change
- [ ] An unknown `type`, invalid `severity`, or malformed filter value returns `400 Bad Request` with an error message — the filter is never silently ignored

## Test Requirements
- [ ] Integration test per filter (`type`, `severity`, `license`) asserting only matching entities are returned
- [ ] Integration test: combined filters plus `q`, verifying AND semantics and `total`
- [ ] Integration test: no filters — results identical to the unfiltered baseline
- [ ] Integration test: invalid `type` / `severity` value returns 400 (fail-closed), not an unfiltered 200
- [ ] Integration test: filtered pagination returns correct slices and `total`

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass

## Documentation Updates
- `README.md` — document the new `type`, `severity` and `license` filter parameters if the search API is documented there

## Dependencies
- Depends on: Task 1 — Add full-text indexes and paginated querying to SearchService
