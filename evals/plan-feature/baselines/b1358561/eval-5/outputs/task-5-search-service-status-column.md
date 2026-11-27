**Summary:** Use advisory.status column in SearchService
**Epic:** TC-9005: Advisory status query and ingestion updates

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
`SearchService` performs full-text search across entities, including advisories. Any advisory search query that joins `advisory_status` (to return or filter by status) must be switched to `advisory.status`, so that the "eliminate the join from all advisory queries" goal of TC-9005 covers the search path and the search module compiles against the new entity.

## Files to Modify
- `modules/search/src/service/mod.rs` — replace any `advisory_status` join/relation with `advisory::Column::Status`
- `tests/api/search.rs` — cover advisory search results/status after the schema change

## Implementation Notes
- Search `modules/search/src/service/mod.rs` for `advisory_status`, `status_id`, and `Relation::AdvisoryStatus`; replace each with `entity::advisory::Column::Status` / `AdvisoryStatus` from Task 3. If the search service never touched status, this task reduces to verifying compilation and adding the regression test — record that in the PR.
- Use `AdvisoryStatus` `Display` for any status string in search results; do not introduce a separate mapping.
- `GET /api/v2/search` (`modules/search/src/endpoints/mod.rs`) response shape must not change.
- Per CONVENTIONS.md §Query helpers: use `common/src/db/query.rs` for any filtering. Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust (`.rs`) service scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against real PostgreSQL using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/search.rs matching the convention's Rust (`.rs`) integration test scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR `--base TC-9005`, PR link posted to Jira; §5 scope limited to listed files, inspect before modifying, no duplicated functionality.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatus` — enum from Task 3
- `common/src/db/query.rs` — shared query helpers

## Acceptance Criteria
- [ ] `modules/search` contains no reference to `advisory_status` or `status_id`
- [ ] `GET /api/v2/search` returns advisories (with unchanged status string values, if status is part of the result) after the migration
- [ ] `cargo build -p search` succeeds

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: ingest an advisory, search for it, assert `StatusCode::OK` and the advisory is returned (with correct status string if exposed)

## Verification Commands
- `grep -rn "advisory_status\|status_id" modules/search/src` — no matches
- `cargo test -p tests --test search` (or workspace equivalent) — search tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity for status enum column
