## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes that support the full-text search performed by `SearchService` so that `GET /api/v2/search` stops doing sequential scans over the SBOM, advisory, and package tables. This addresses the TC-9002 MVP requirement "Search should be faster".

**Assumptions pending clarification (TC-9002):**
- ASSUMPTION: "Search" refers to the unified `GET /api/v2/search` endpoint (`modules/search/`), not the per-entity list endpoints. Pending confirmation from the Feature owner.
- ASSUMPTION: The slowness is caused (at least partly) by missing full-text/trigram indexes on the searched columns. No profiling data, slow-query logs, or latency baseline were provided in the Feature; the implementer must confirm with `EXPLAIN ANALYZE` before choosing index types.
- ASSUMPTION: No numeric latency target exists ("fast enough" in the NFRs is not measurable). This task records a before/after measurement rather than asserting a specific threshold until a target is agreed.

## Files to Modify
- `migration/src/lib.rs` — register the new search-index migration in the migrator list

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration creating (and dropping in `down`) the indexes on columns queried by `SearchService`

## Implementation Notes
- Inspect `modules/search/src/service/mod.rs` (`SearchService`) first to determine exactly which entity columns are matched (e.g., SBOM name, advisory title/identifier, package name). Index only those columns; do not guess.
- Entities whose tables are searched are defined in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` (SeaORM). Use their column definitions for index targets.
- Follow the existing migration structure in `migration/src/m0001_initial/mod.rs` (a `Migration` struct implementing `MigrationTrait` with `up`/`down`) and register the new module in `migration/src/lib.rs` the same way `m0001_initial` is registered.
- If `SearchService` uses `ILIKE '%term%'`, a `pg_trgm` GIN index is appropriate; if it uses `to_tsvector`/`plainto_tsquery`, a GIN index over the matching `tsvector` expression is appropriate. The index expression must match the query expression exactly or PostgreSQL will not use it.
- The `down` migration must drop every index created in `up` so the migration is reversible.
- Regression coverage relies on the existing integration tests in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs`, which run against a real PostgreSQL test database.

Constraints (docs/constraints.md):
- §2 Commit rules: Conventional Commits format, reference the Jira task ID in the footer, include an `Assisted-by:` trailer.
- §3 PR rules: open the PR with `--base main`; post the PR link on the Jira task.
- §5 Code change rules: change only the files listed above; inspect code before modifying it; do not duplicate existing helpers.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration to copy for structure (`MigrationTrait`, `up`/`down`)
- `migration/src/lib.rs` — existing migrator registration list to extend

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` is registered in `migration/src/lib.rs` and applies cleanly on a fresh database and on a database already at `m0001_initial`
- [ ] The migration's `down` step removes every index it created
- [ ] `EXPLAIN` for the query issued by `SearchService` shows an index scan (not a sequential scan) on each searched table
- [ ] Existing search behavior is unchanged: `tests/api/search.rs` passes without modification
- [ ] Before/after latency for a representative `GET /api/v2/search?q=...` request is recorded in the PR description (no fixed threshold until TC-9002 defines one)

## Test Requirements
- [ ] Migration up/down round-trip test (apply, roll back, re-apply) succeeds against the PostgreSQL test database
- [ ] Existing integration tests in `tests/api/search.rs` continue to pass
- [ ] Existing integration tests in `tests/api/sbom.rs` and `tests/api/advisory.rs` continue to pass ("Don't break existing functionality")

## Verification Commands
- `cargo test -p migration` — migration tests pass
- `cargo test --test api search` — search integration tests pass

## Dependencies
- None
