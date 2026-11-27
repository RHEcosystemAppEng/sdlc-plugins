## Repository
trustify-backend

## Target Branch
main

## Description
Improve the latency of the unified search endpoint (`GET /api/v2/search`) by adding
database-level full-text search support: a migration that adds indexed full-text
search vectors for the entities `SearchService` queries (SBOMs, advisories, packages),
and an update to `SearchService` so its queries use those indexes instead of
unindexed pattern matching.

This addresses the MVP requirement "Search should be faster" from TC-9002.

**Ambiguity flagged (pending clarification on TC-9002):** the Feature gives no baseline
latency, no target latency, no dataset size, and no statement of which endpoints are
"slow" ("Should be fast enough" is the only NFR). The assumptions below fill these gaps
and must be confirmed or corrected by the Feature owner before or during implementation.

**Assumptions pending clarification:**
- ASSUMPTION A1: "Search" refers to the unified search endpoint `GET /api/v2/search`
  (`modules/search/`), not the per-entity list endpoints (`GET /api/v2/sbom`,
  `GET /api/v2/advisory`, `GET /api/v2/package`).
- ASSUMPTION A2: the main source of slowness is unindexed text matching in
  `SearchService`; the fix is PostgreSQL full-text search (`tsvector` + GIN index).
  This must be validated by capturing `EXPLAIN ANALYZE` output for the current search
  query before implementing.
- ASSUMPTION A3: no numeric latency target is defined; the acceptance bar is "measurably
  faster than the current baseline on the same dataset, with the query plan using the new
  index". If the Feature owner supplies a target (e.g., p95 < N ms), add it to the
  Acceptance Criteria.
- ASSUMPTION A4: the searchable fields are the ones already searched by `SearchService`
  today (no new fields are added to the search scope).

## Files to Modify
- `migration/src/lib.rs` — register the new search-index migration in the migrator list
- `modules/search/src/service/mod.rs` — change `SearchService` queries to match against the indexed `tsvector` columns (`@@` with `websearch_to_tsquery`/`plainto_tsquery`) instead of unindexed pattern matching
- `entity/src/sbom.rs` — expose the new search vector column on the SBOM entity (if it must be selected/filtered via SeaORM)
- `entity/src/advisory.rs` — expose the new search vector column on the Advisory entity
- `entity/src/package.rs` — expose the new search vector column on the Package entity
- `tests/api/search.rs` — add regression and index-usage tests for the search endpoint

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — migration adding generated, weighted `tsvector` columns and GIN indexes on the `sbom`, `advisory`, and `package` tables

## Implementation Notes
- Follow the existing migration module layout in `migration/src/m0001_initial/mod.rs`
  (one directory per migration with a `mod.rs`) and register it in `migration/src/lib.rs`
  after `m0001_initial`.
- Use **stored generated columns** (`GENERATED ALWAYS AS (...) STORED`) for the search
  vectors. This keeps the search vector in sync for every writer of these tables without
  modifying them — the SBOM ingestion path (`modules/ingestor/src/graph/sbom/mod.rs`), the
  advisory ingestion path (`modules/ingestor/src/graph/advisory/mod.rs`), and
  `IngestorService` (`modules/ingestor/src/service/mod.rs`) continue to work unchanged.
  If generated columns are rejected in review, the ingestion writers must be added to this
  task's scope (see shared-artifact analysis in the impact map).
- Build each vector with `setweight` per field (identifier/name fields weight `A`,
  title/description fields weight `B`/`C`) so Task 2 can rank by relevance without another
  schema change.
- Add a GIN index on each new `tsvector` column in the same migration and include the
  `down` migration that drops indexes and columns.
- In `modules/search/src/service/mod.rs`, keep the existing public signature of
  `SearchService` methods so `modules/search/src/endpoints/mod.rs` does not need to change;
  only the query construction changes.
- Reuse the shared pagination helpers in `common/src/db/query.rs` and keep returning
  `PaginatedResults<T>` from `common/src/model/paginated.rs` — do not hand-roll
  offset/limit logic.
- Error handling: return `Result<T, AppError>` (`common/src/error.rs`) with `.context()`
  wrapping, as all other services do.
- Before changing code, capture `EXPLAIN ANALYZE` for the current search query on a
  representative dataset and record it in the PR description, then capture it again after
  the change (validates ASSUMPTION A2/A3).
- Per CONVENTIONS.md §Module pattern: keep search logic in `service/` and routing in `endpoints/`; do not move query logic into the endpoint handler.
  Applies: task modifies modules/search/src/service/mod.rs matching the convention's `modules/*/src/{model,service,endpoints}` Rust module scope.
- Per CONVENTIONS.md §Error handling: all new/changed service functions return `Result<T, AppError>` and wrap database errors with `.context()`.
  Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust handler/service (`.rs`) scope.
- Per CONVENTIONS.md §Query helpers: use `common/src/db/query.rs` for pagination and sorting of search results.
  Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust database-query (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` against the real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern; see `tests/api/sbom.rs` for an example.
  Applies: task modifies tests/api/search.rs matching the convention's `tests/api/*.rs` integration-test scope.
- Constraints (docs/constraints.md): commits must use Conventional Commits, reference
  the Jira task ID in the footer, and include an `Assisted-by:` trailer (§2.1–2.3); the PR
  must target `main` via `gh pr create --base main` and its link must be posted on the Jira
  task (§3.2, §3.3); changes must stay within Files to Modify / Files to Create, inspect
  code before modifying it, and reuse existing helpers (§5.1, §5.2, §5.4).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers; use for paging search results
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper the search endpoint must keep returning
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — already implements an advisory "search" operation; inspect it for existing text-matching logic to align with (or reuse) rather than duplicating a second advisory text query
- `migration/src/m0001_initial/mod.rs` — reference for migration structure

## Acceptance Criteria
- [ ] A new migration `m0002_search_indexes` adds a weighted `tsvector` search column and a GIN index to each entity table searched by `SearchService` (sbom, advisory, package), with a working `down` migration
- [ ] The migration applies cleanly on an existing database populated with data, and the search vectors are populated for pre-existing rows (generated columns)
- [ ] `SearchService` queries use the new indexes — `EXPLAIN` of the search query shows a GIN index scan rather than a sequential scan on the searched tables
- [ ] Search latency on the same representative dataset is measurably lower than the pre-change baseline (baseline and post-change measurements recorded in the PR) — numeric target pending clarification (ASSUMPTION A3)
- [ ] `GET /api/v2/search` request/response contract is unchanged (same query parameters, same `PaginatedResults<T>` shape)
- [ ] Newly ingested SBOMs and advisories are searchable immediately after ingestion without any extra indexing step
- [ ] Existing search tests in `tests/api/search.rs` continue to pass ("Don't break existing functionality")

## Test Requirements
- [ ] Integration test in `tests/api/search.rs`: searching for a term present in an SBOM, an advisory, and a package returns all three, matching pre-change behavior
- [ ] Integration test: an entity ingested after the migration is returned by search (verifies the generated column covers the ingestion write path)
- [ ] Integration test: an empty/blank query and a query with no matches return `200 OK` with an empty `PaginatedResults` (no 500s from tsquery parsing of special characters such as `&`, `|`, `!`, `:`)
- [ ] Migration test: apply `up` then `down` then `up` on the test database without error
- [ ] All existing tests in `tests/api/` pass

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass
- `cargo run -p migration -- up` — migration applies without error

## Dependencies
- None
