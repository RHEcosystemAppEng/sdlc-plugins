**Summary:** Add full-text indexes and paginated querying to SearchService

**Labels:** ai-generated-jira | **Priority:** Normal | **Fix Versions:** RHTPA 1.6.0

## Repository
trustify-backend

## Target Branch
main

## Description
Part of TC-9002 ("Improve search experience"), MVP requirement "Search should be faster".

The Feature does not give a latency baseline or target, so this task is scoped under
planning assumptions A1/A2 (see the TC-9002 impact map): `GET /api/v2/search` is the
search users mean, and it is slow because full-text matching is not indexed and results
are not bounded. This task adds PostgreSQL full-text indexes for the entities
`SearchService` searches (SBOM, advisory, package) and makes `SearchService` query
through those indexes with pagination enforced.

**Open question (blocks sign-off of the performance criterion):** the target latency
for "fast enough" is not defined. The benchmark criterion below uses a placeholder
that must be replaced with the value agreed with the Feature owner.

## Files to Modify
- `migration/src/lib.rs` — register the new search-index migration after `m0001_initial`
- `entity/src/sbom.rs` — add the generated `search_vector` column to the SBOM entity model
- `entity/src/advisory.rs` — add the generated `search_vector` column to the Advisory entity model
- `entity/src/package.rs` — add the generated `search_vector` column to the Package entity model
- `modules/search/src/service/mod.rs` — query `search_vector` with `plainto_tsquery` through the GIN index; apply limit/offset via shared query helpers
- `modules/search/src/endpoints/mod.rs` — accept `offset`/`limit` query parameters and return `PaginatedResults<T>`
- `tests/api/search.rs` — add indexing, pagination and backward-compatibility tests

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — add stored generated `tsvector` columns and GIN indexes on `sbom`, `advisory`, `package`

## API Changes
- `GET /api/v2/search` — MODIFY: accepts optional `offset` and `limit` query parameters (default limit applied when absent); response wrapped in `PaginatedResults<T>` with `total`. Existing `q` parameter behaviour unchanged.

## Implementation Notes
- Use a **stored generated column** (`GENERATED ALWAYS AS (to_tsvector('english', ...)) STORED`) so that every write path keeps the index current without code changes. Searchable rows are produced by:
  - `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion (writes SBOM rows and links packages via `entity/src/sbom_package.rs`)
  - `modules/ingestor/src/graph/advisory/mod.rs` — advisory ingestion
  - `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` ingest path (on-demand/API)
  - the migration itself, which back-fills all pre-existing rows
  Each of these paths needs a test (see Test Requirements); do not assume the primary ingestor alone is sufficient.
- Follow the migration structure of `migration/src/m0001_initial/mod.rs` and register the new module in `migration/src/lib.rs`.
- Pagination must reuse the shared helpers in `common/src/db/query.rs` and the response wrapper in `common/src/model/paginated.rs` — do not hand-roll limit/offset handling.
- Text sources for the vectors: confirm against the entity definitions which name/title/identifier columns exist (e.g. SBOM name, advisory identifier/title, package name) before writing the generated expression.
- Per CONVENTIONS.md §Response types: list-style endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md §Query helpers: use the shared filtering/pagination/sorting helpers in `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's database query scope.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` (`common/src/error.rs`) with `.context()` wrapping on database errors. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's handler scope.
- Per CONVENTIONS.md §Framework: SeaORM for database access — add the generated columns to the SeaORM entity models and keep raw SQL limited to the migration. Applies: task modifies `entity/src/sbom.rs` matching the convention's SeaORM entity scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` run against a real PostgreSQL test database and assert with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope.
- Constraints (docs/constraints.md): §2 commit rules — Conventional Commits, `Implements TC-<task>` footer, `Assisted-by:` trailer; §3 PR rules — branch named after the task issue ID, `gh pr create --base main`, PR link posted to the Jira task; §5 code change rules — stay within Files to Modify/Create, inspect before modifying, reuse existing helpers, trace the data flow (ingest → index → search) end to end before committing.

## Reuse Candidates
- `common/src/db/query.rs` — shared pagination/filtering/sorting helpers; use for limit/offset
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper
- `modules/fundamental/src/sbom/endpoints/list.rs` — existing paginated list endpoint to mirror for parameter parsing
- `migration/src/m0001_initial/mod.rs` — existing migration structure to follow

## Acceptance Criteria
- [ ] New migration adds stored generated `tsvector` columns and GIN indexes on `sbom`, `advisory` and `package`, and its `down` migration removes them
- [ ] `SearchService` matches using the indexed `search_vector` columns (verified via `EXPLAIN` showing a GIN index scan for a representative query)
- [ ] Rows that existed before the migration are returned by search after it runs
- [ ] An SBOM (and its linked packages) ingested via `modules/ingestor/src/graph/sbom/mod.rs` is searchable immediately after ingestion
- [ ] An advisory ingested via `modules/ingestor/src/graph/advisory/mod.rs` is searchable immediately after ingestion
- [ ] An SBOM ingested via `SbomService` in `modules/fundamental/src/sbom/service/sbom.rs` is searchable immediately after ingestion
- [ ] `GET /api/v2/search` applies a default page size when `limit` is absent and honours `offset`/`limit` when present, returning `PaginatedResults<T>` with a correct `total`
- [ ] Existing requests to `GET /api/v2/search?q=...` keep returning the same matching entities (no regression)
- [ ] p95 latency of `GET /api/v2/search` on the agreed benchmark dataset meets the agreed target (**placeholder — target to be supplied by Feature owner**)

## Test Requirements
- [ ] Integration test: seed data, run migration, assert previously existing rows are found by `q`
- [ ] Integration test: ingest an SBOM through the ingestor graph path and assert the SBOM and a linked package are returned by search
- [ ] Integration test: ingest an advisory through the ingestor graph path and assert it is returned by search
- [ ] Integration test: ingest an SBOM through `SbomService` and assert it is returned by search
- [ ] Integration test: pagination — `limit`/`offset` return the expected slice and `total`; absent `limit` uses the default
- [ ] Integration test: existing search tests in `tests/api/search.rs` continue to pass unchanged
- [ ] Migration test: `up` then `down` leaves the schema in its original state

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass
- `cargo run -p migration -- up` followed by `EXPLAIN ANALYZE` of the search query — plan shows a Bitmap Index Scan on the new GIN index

## Documentation Updates
- `README.md` — mention the new `offset`/`limit` parameters on `GET /api/v2/search` if the API is documented there
