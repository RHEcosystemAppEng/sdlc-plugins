# Task 1 — Add full-text search indexes migration

**Summary:** TC-9002: Add full-text search indexes migration
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Normal | **Fix Versions:** RHTPA 1.6.0

## Repository
trustify-backend

## Target Branch
main

## Description
Users report that search is slow (TC-9002, requirement "Search should be faster"). The global search (`SearchService` in `modules/search/src/service/mod.rs`) runs full-text matching across SBOMs, advisories and packages. This task adds a SeaORM migration that creates PostgreSQL full-text search support for the columns that search reads. That support is either stored generated `tsvector` columns or expression GIN indexes. Task 2 then moves the queries onto these indexes.

**Planning assumption (A1 in the impact map, still to be confirmed):** the slowness comes from un-indexed text matching. Before writing the migration, the implementer should capture `EXPLAIN ANALYZE` output for today's search query to confirm this. If the bottleneck is somewhere else, stop and report back on TC-9002.

## Files to Modify
- `migration/src/lib.rs` — register the new migration in the `Migrator` migrations list after `m0001_initial`

## Files to Create
- `migration/src/m0002_search_fulltext_indexes/mod.rs` — migration with `up` (creates tsvector/GIN indexes on the searchable columns of `sbom`, `advisory` and `package`) and `down` (drops them)

## Implementation Notes
- Follow the existing migration module layout in `migration/src/m0001_initial/mod.rs` (one directory per migration containing `mod.rs`, registered in `migration/src/lib.rs`).
- Find the searchable columns in `SearchService` (`modules/search/src/service/mod.rs`) and in the entity definitions: `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs`. Index exactly the columns that the search query filters on. Do not guess the column names.
- Prefer `GENERATED ALWAYS AS (to_tsvector('english', coalesce(<col>, ''))) STORED` columns with `USING GIN` indexes. PostgreSQL then keeps the index up to date for every write path, including SBOM and advisory ingestion in `modules/ingestor/src/graph/sbom/mod.rs` and `modules/ingestor/src/graph/advisory/mod.rs`, with no ingestor changes. If generated columns are used, add the matching fields to the SeaORM entities (`entity/src/*.rs`) in Task 2, not here, so this migration stays standalone.
- Create the indexes `CONCURRENTLY` where the migration framework allows it, so large existing tables are not locked during upgrade.
- The migration must be purely additive. Existing queries must keep working unchanged, so the task can merge to `main` on its own (direct-to-main mode).
- Constraints (docs/constraints.md): changes stay within the files listed above (§5.1). Inspect the code before modifying it (§5.2). Do not duplicate existing helpers (§5.4). Commits follow Conventional Commits, reference this Jira task in the footer and include the `Assisted-by: Claude Code` trailer (§2.1–2.3). The PR targets `main` with `--base main`, and its link is posted on the Jira task (§3.2–3.3).

## Reuse Candidates
- `migration/src/m0001_initial/mod.rs` — existing migration showing the `MigrationTrait` `up`/`down` structure to copy
- `migration/src/lib.rs::Migrator` — migration registry to extend

## Acceptance Criteria
- [ ] A new migration `m0002_search_fulltext_indexes` is registered in `migration/src/lib.rs`
- [ ] `up` creates full-text (GIN) indexes covering every text column that `SearchService` matches on for the `sbom`, `advisory` and `package` tables
- [ ] `down` removes everything `up` created, leaving the schema identical to before
- [ ] Data that exists before the migration, and data ingested after it, is covered by the indexes
- [ ] Existing search behavior and existing tests in `tests/api/search.rs` are unchanged

## Test Requirements
- [ ] The migration applies cleanly on an empty test database and on one seeded with SBOM, advisory and package rows
- [ ] Running the migration down and then up again succeeds (reversibility)
- [ ] An integration test confirms that an SBOM ingested after the migration can be found through search (index maintained on write)
- [ ] The existing `tests/api/search.rs` suite passes unchanged

## Verification Commands
- `cargo test -p migration` — passes
- `cargo test --test api search` — existing search integration tests pass

## Dependencies
- None
