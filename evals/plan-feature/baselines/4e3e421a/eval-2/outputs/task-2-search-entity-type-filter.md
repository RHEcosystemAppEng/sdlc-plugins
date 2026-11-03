## Repository
trustify-backend

## Target Branch
main

## Description
Part of TC-9002 (Improve search experience), requirement "Add filters" (MVP).

The Feature only asks for "some kind of filtering capability". `SearchService` searches across several entity types (SBOMs, advisories, packages), so the most basic and lowest-risk filter is narrowing results by entity type. This task adds an optional `type` filter to `GET /api/v2/search` and sets up the filter parameter handling that Task 3 extends.

**Assumption pending confirmation:** the filter dimension (entity type) was inferred from repository evidence, not stated in the Feature (see the TC-9002 impact map, clarification question 3). If the Feature owner chooses different dimensions, update this task before implementation starts.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — parse and validate the optional `type` query parameter (one or more of `sbom`, `advisory`, `package`) and pass it to the service
- `modules/search/src/service/mod.rs` — restrict the search to the requested entity types
- `tests/api/search.rs` — add filter and backward-compatibility tests

## API Changes
- `GET /api/v2/search` — MODIFY: new optional query parameter `type` (repeatable or comma-separated; values `sbom`, `advisory`, `package`). If omitted, all entity types are searched (current behavior).

## Implementation Notes
- Build the filter with the shared filtering helpers in `common/src/db/query.rs` rather than hand-written SQL conditions.
- Model the allowed values as a typed enum that deserializes from the query string. An unknown value (e.g., `type=foo`) must return 400 via `AppError` (`common/src/error.rs`). It must **not** be silently ignored, because that would quietly return unfiltered results.
- Keep the pagination from Task 1 intact. `total` must reflect the filtered count.
- Entity definitions to scope against: `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`.
- Per CONVENTIONS.md §Query helpers: filtering goes through `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service/query scope. Example: `modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService` list/search).
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's handler scope. Example: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Testing: use real PostgreSQL integration tests with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md):
  - §2 commits: Conventional Commits, `Implements <task-key>` footer, Assisted-by trailer.
  - §3 PRs: `--base main`, and post the PR link on the Jira task.
  - §5 code changes: change only the listed files, inspect code first, reuse the shared helpers.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing list/search implementation with filtering to use as a pattern
- `common/src/error.rs::AppError` — 400 responses for invalid filter values

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=<term>&type=advisory` returns only advisory results
- [ ] Multiple types (e.g., `type=sbom&type=package` or `type=sbom,package`) return results from only those types
- [ ] An omitted `type` returns results from all entity types, the same as before this change
- [ ] An unknown `type` value returns 400 with a descriptive error. It never returns unfiltered results.
- [ ] Pagination `total` reflects the filtered result count
- [ ] Existing tests in `tests/api/search.rs` pass

## Test Requirements
- [ ] Integration test: seed one SBOM, one advisory, and one package that all match a term. Filtering by each type returns only that entity.
- [ ] Integration test: a multi-type filter returns the union of the selected types
- [ ] Integration test: no `type` parameter returns all three entities (backward compatibility)
- [ ] Integration test: `type=invalid` returns 400
- [ ] Integration test: filtered `total` matches the number of filtered items across pages

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass

## Documentation Updates
- `README.md` — document the `type` filter parameter of `GET /api/v2/search`, if the README documents the API

## Dependencies
- Depends on: Task 1 — Paginate and cache GET /api/v2/search, and add a latency baseline
