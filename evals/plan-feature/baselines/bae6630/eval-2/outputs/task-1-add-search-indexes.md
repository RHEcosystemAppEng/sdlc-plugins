## Repository
trustify-backend

## Target Branch
main

## Description
Add database indexes to support faster full-text search queries across SBOMs, advisories, and packages. The feature requirement states search is "currently too slow" but provides no specific latency targets (see Ambiguity 1 in impact map). This task creates the foundational indexes that Tasks 2 and 3 depend on for query optimization and relevance ranking.

## Files to Create
- `migration/src/m0002_search_indexes/mod.rs` — New SeaORM migration adding GIN indexes for full-text search on SBOM, advisory, and package tables, plus B-tree indexes on commonly filtered columns (created_at, severity)

## Files to Modify
- `migration/src/lib.rs` — Register the new m0002_search_indexes migration module
- `entity/src/sbom.rs` — Add `tsvector` column annotation for SBOM search fields (assumption: name and description columns exist based on SbomSummary struct in `modules/fundamental/src/sbom/model/summary.rs`)
- `entity/src/advisory.rs` — Add `tsvector` column annotation for advisory search fields (assumption: title/description and severity columns exist based on AdvisorySummary struct in `modules/fundamental/src/advisory/model/summary.rs`)
- `entity/src/package.rs` — Add `tsvector` column annotation for package search fields (assumption: name and license columns exist based on PackageSummary struct in `modules/fundamental/src/package/model/summary.rs`)

## Implementation Notes
- Follow the existing migration pattern in `migration/src/m0001_initial/mod.rs` for migration structure
- Create GIN indexes on `tsvector` columns for full-text search performance: `CREATE INDEX idx_sbom_fts ON sbom USING GIN (to_tsvector('english', name || ' ' || COALESCE(description, '')))` — exact column names are an **assumption pending clarification** since entity structs are not fully visible
- Create B-tree indexes on `advisory.severity` and timestamp columns used for filtering
- Use SeaORM migration API (`manager.create_index(...)`) consistent with the project's ORM conventions
- **Assumption (pending clarification):** The specific columns available for indexing are inferred from the model summary structs (`SbomSummary`, `AdvisorySummary`, `PackageSummary`). Actual column names must be verified against the entity definitions before implementation.

## Acceptance Criteria
- [ ] New migration m0002_search_indexes is created and registered in `migration/src/lib.rs`
- [ ] GIN indexes exist for full-text search on sbom, advisory, and package tables
- [ ] B-tree indexes exist on severity and date columns used for filtering
- [ ] Migration runs successfully against a clean database
- [ ] Migration is reversible (down migration drops indexes)
- [ ] Existing tests in `tests/api/` continue to pass (backward compatibility)

## Test Requirements
- [ ] Migration applies cleanly on a fresh database (verified via migration test or manual run)
- [ ] Migration rolls back cleanly without errors
- [ ] Existing integration tests in `tests/api/search.rs`, `tests/api/sbom.rs`, and `tests/api/advisory.rs` continue to pass

## Dependencies
- None (this is the foundation task)

## Digest
[sdlc-workflow] Description digest: sha256-md:4c8524b9b0bd6a199050394a4e3ffb37ac5c56eb9cfa979df54fa16e37e18c55
