## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering to the unified search endpoint `GET /api/v2/search` (TC-9002 requirement "Add filters", MVP).

The Feature only asks for "some kind of filtering capability". It does not say which fields can be filtered, which operators to support, or whether filters apply to the unified search or to the per-entity list endpoints. This task adds a small, conservative set of optional filter parameters based on fields that already exist in the domain models.

**Assumptions (pending clarification on TC-9002):**
- ASSUMPTION C1: Filters apply to the unified search endpoint `GET /api/v2/search` only, not to the per-entity list endpoints.
- ASSUMPTION C2: The initial filter set is limited to fields that already exist in the models:
  - entity type (`sbom`, `advisory`, `package`)
  - advisory `severity`, from `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`)
  - package `license`, from `PackageSummary` (`modules/fundamental/src/package/model/summary.rs`)

  The product owner must confirm or replace this set.
- ASSUMPTION C3: Filters are optional query parameters that combine with AND semantics. Omitting every filter must return exactly the same results as today.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — accept optional filter query parameters (`type`, `severity`, `license`) on `GET /api/v2/search` and validate their values
- `modules/search/src/service/mod.rs` — apply the filters to the `SearchService` query using the shared filtering helpers
- `tests/api/search.rs` — add filter tests

## API Changes
- `GET /api/v2/search` — MODIFY: adds optional query parameters `type` (sbom|advisory|package), `severity` (advisory severity values), and `license` (package license identifier). Invalid values return a 400 through `AppError`. With no filters, behavior is unchanged.

## Implementation Notes
- Parse the filter parameters in the search handler in `modules/search/src/endpoints/mod.rs`, following how the other modules' endpoint handlers extract query parameters (for example `modules/fundamental/src/advisory/endpoints/list.rs` and `modules/fundamental/src/package/endpoints/list.rs`).
- Apply the filters in `SearchService` (`modules/search/src/service/mod.rs`) through the shared filtering helpers in `common/src/db/query.rs`. Do not build ad-hoc SQL fragments.
- Severity filter: use the `severity` field defined on `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`) and the advisory entity in `entity/src/advisory.rs`.
- License filter: use the license field on `PackageSummary` (`modules/fundamental/src/package/model/summary.rs`) and the `entity/src/package_license.rs` mapping.
- A type-specific filter only narrows results of its own entity type. For example, `severity` excludes non-advisory results only when combined with `type=advisory`. Document the chosen semantics in the PR, because the Feature does not define them.
- Per CONVENTIONS.md §Error handling: every handler returns `Result<T, AppError>` (`common/src/error.rs`) and wraps fallible calls with `.context()`. Invalid filter values map to a 400 `AppError` variant.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: use the shared filtering helpers in `common/src/db/query.rs`.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust database-query (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/`, run against the real PostgreSQL test database, and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): changes stay within the files listed above (§5.1). Inspect code before modifying it (§5.2). Reuse rather than duplicate (§5.4). Commits use Conventional Commits with a Jira footer and an `Assisted-by:` trailer (§2.1–2.3). The PR targets `main` via `--base main` and its link is posted to the Jira task (§3.2, §3.3).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers used by the list endpoints. Reuse them for the search filters.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — source of the `severity` field and its value set.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — source of the `license` field.
- `modules/fundamental/src/advisory/endpoints/list.rs` — existing query-parameter extraction pattern for list endpoints.

## Acceptance Criteria
- [ ] `GET /api/v2/search?type=advisory` returns only advisory results
- [ ] `GET /api/v2/search?type=advisory&severity=<value>` returns only advisories with that severity
- [ ] `GET /api/v2/search?type=package&license=<id>` returns only packages with that license
- [ ] Multiple filters combine with AND semantics
- [ ] Invalid filter values return HTTP 400 through `AppError`
- [ ] A request with no filter parameters returns the same results as before this change (backward compatible)
- [ ] The filter set is confirmed with the product owner, or ASSUMPTION C2 is explicitly accepted on TC-9002, before merge

## Test Requirements
- [ ] Integration test in `tests/api/search.rs` for each filter (`type`, `severity`, `license`) asserting that only matching results are returned
- [ ] Integration test for a combined filter (AND semantics)
- [ ] Integration test asserting HTTP 400 for an invalid `type` or `severity` value
- [ ] Integration test asserting that a request without filters returns the same result set as an unfiltered baseline query
- [ ] Filtered results keep correct `total` and pagination in the `PaginatedResults<T>` response

## Verification Commands
- `cargo test --test search` (run from `tests/`) — all search integration tests pass

## Documentation Updates
- `README.md` — document the new optional filter query parameters on `GET /api/v2/search`, if the README lists API endpoints

## Dependencies
- Depends on: Task 1 — Search performance baseline and optimization (shares `modules/search/src/service/mod.rs` query construction and pagination changes)
