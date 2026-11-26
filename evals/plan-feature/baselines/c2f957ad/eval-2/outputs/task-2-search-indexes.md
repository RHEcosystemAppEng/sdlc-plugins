# Task 2 — Add database indexes for search queries

**Jira:** Task, parent EPIC-1 ("TC-9002: Search performance"), labels `ai-generated-jira`, priority `Normal`, fixVersions `RHTPA 1.6.0`

## Repository
trustify-backend

## Target Branch
main

## Description
Speed up `GET /api/v2/search` by adding PostgreSQL indexes that support the full-text queries `SearchService` runs against the `sbom`, `advisory` and `package` tables. The schema currently has only `migration/src/m0001_initial/mod.rs`, with no search-specific indexes.

**Assumptions (pending clarification on TC-9002, open question 1):**
- `SearchService` queries text columns in a way an index can serve (full-text `to_tsvector` / `ILIKE` patterns). The implementer must check the actual query shapes in `modules/search/src/service/mod.rs` before choosing between GIN full-text indexes and `pg_trgm` trigram indexes.
- No numeric target is defined. Success is measured as an improvement over the Task 1 baseline.

## Files to Modify
- `migration/src/lib.rs` — register the new migration
- `modules/search/src/service/mod.rs` — change query expressions only where needed so they exactly match the indexed expressions and the planner can use the indexes
- `tests/api/search.rs` — add tests confirming search results are unchanged and index-backed

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration that creates the search indexes on `sbom`, `advisory` and `package`, with a matching `down()` that drops them

## Implementation Notes
- **Shared artifact (searchable entity tables):** these tables are populated by `modules/ingestor/src/graph/sbom/mod.rs` (SBOMs and linked packages), `modules/ingestor/src/graph/advisory/mod.rs` (advisories) and the ingest path in `modules/fundamental/src/sbom/service/sbom.rs`. Use **expression indexes or generated columns** so no producer code changes. Do **not** add stored columns that ingestion must populate. If that turns out to be necessary, stop and raise a scope change, because every producer above would then need to change.
- Index expressions must exactly match the expressions `SearchService` uses. Otherwise PostgreSQL will not use the index.
- Follow the structure of `migration/src/m0001_initial/mod.rs` for the `MigrationTrait` `up`/`down` implementation.
- Check the speedup with `EXPLAIN ANALYZE` on the queries timed in Task 1, and compare against the Task 1 baseline.
- Per CONVENTIONS.md §Module pattern: domain logic stays in `service/`. Change only the query construction in `SearchService` and leave the endpoints alone. Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust module (`model/ + service/ + endpoints/`) scope.
- Per CONVENTIONS.md §Query helpers: shared filtering, pagination and sorting go through `common/src/db/query.rs`. Keep using these helpers in any query you touch, and do not rewrite them by hand. Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust query construction (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` against the real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/search.rs matching the convention's integration test (`tests/api/*.rs`) scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md): §1.4 and §5.1 scope limits. §5.2 inspect before modifying. §5.4 no duplication. §5.6 trace the data flow (ingest → index → search). §2.1–2.3 commit rules. §3.1–3.3 PR rules. §5.11–5.12 test documentation.

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration structure to copy
- `common/src/db/query.rs` — shared query builder used by search and list queries
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — has its own advisory search. Check whether its query expressions should use the same indexes, so you don't create a second, differently shaped index

## Acceptance Criteria
- [ ] A new migration creates the search indexes on the `sbom`, `advisory` and `package` text columns used by `SearchService`, and `down()` removes them
- [ ] The migration is registered in `migration/src/lib.rs` and applies cleanly on a database migrated to `m0001_initial`
- [ ] `EXPLAIN` for each search query shows the new index being used (recorded in the PR description)
- [ ] Measured search latency improves against the Task 1 baseline on the same dataset (before and after numbers in the PR description)
- [ ] No ingestion code (`modules/ingestor/**`, `SbomService` ingest) needs changes. Data ingested after the migration is searchable without extra steps
- [ ] Search results (the set of matching entities) are unchanged for the existing test queries

## Test Requirements
- [ ] Existing `tests/api/search.rs` tests pass unchanged
- [ ] Test: an SBOM ingested through the SBOM ingestion path **after** the migration is returned by search
- [ ] Test: an advisory ingested through the advisory ingestion path **after** the migration is returned by search
- [ ] Test: the migration runs `up` then `down` then `up` without error

## Verification Commands
- `cargo test --test api search` — all search tests pass
- `cargo run -p migration -- up` — the migration applies without error

## Dependencies
- Depends on: Task 1 — Instrument search and establish a latency baseline
