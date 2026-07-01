## Repository
trustify-backend

## Target Branch
main

## Description
Implement PostgreSQL full-text search using `tsvector`/`tsquery` in the SearchService to replace or augment the current search implementation. This improves search relevance by supporting weighted field matching, partial matching, and ranked results.

**Ambiguity flag:** The feature states "results should be more relevant" without defining relevance criteria. This task assumes (Assumption A2) that relevance means PostgreSQL full-text search with field weighting (name fields weighted 'A', description fields weighted 'B'). The specific weighting scheme and whether fuzzy matching is required must be confirmed with the product owner.

**Assumption:** Search spans all three primary entity types: SBOMs, advisories, and packages (Assumption A5). If the product owner restricts the searchable entity scope, this task's scope will narrow accordingly.

## Files to Modify
- `modules/search/src/service/mod.rs` — update SearchService to use tsvector/tsquery for full-text search with ranking
- `modules/search/src/endpoints/mod.rs` — update search endpoint handler to pass through ranking/relevance parameters
- `common/src/db/query.rs` — add full-text search query builder helpers (ts_rank, plainto_tsquery)

## API Changes
- `GET /api/v2/search` — MODIFY: results now include a relevance score; ordering defaults to relevance-ranked when a search query is provided. Existing behavior (no query = list all) is preserved for backward compatibility.

## Implementation Notes
- Modify `SearchService` in `modules/search/src/service/mod.rs` to construct `tsquery` from user input using `plainto_tsquery()` or `websearch_to_tsquery()`
- Use `ts_rank()` to compute relevance scores and order results by rank descending
- Add weight classes to the tsvector: 'A' for name fields (highest weight), 'B' for description fields
- Extend `common/src/db/query.rs` with a helper function for full-text search query construction, following the existing pattern of shared query utilities
- Maintain backward compatibility: when no search query is provided, return results in the existing default order
- Follow the existing service pattern in `modules/fundamental/src/sbom/service/sbom.rs` for service method structure
- Return results wrapped in `PaginatedResults<T>` from `common/src/model/paginated.rs`, consistent with existing list endpoints
- Use `AppError` from `common/src/error.rs` for error handling with `.context()` wrapping
- Per docs/constraints.md §5.2: inspect existing search service code before modifying
- Per docs/constraints.md §5.4: reuse existing query builder helpers, do not duplicate

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; extend with full-text search support
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper used by all list endpoints
- `common/src/error.rs::AppError` — standard error handling enum
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference implementation for service method patterns

## Acceptance Criteria
- [ ] Search queries return results ranked by relevance (name matches rank higher than description-only matches)
- [ ] Empty search queries return results in the existing default order (backward compatible)
- [ ] Search supports multi-word queries with AND semantics
- [ ] Results include a relevance score field
- [ ] Existing search API consumers are not broken (optional parameters, backward-compatible defaults)

## Test Requirements
- [ ] Integration test: search for a known SBOM name returns it as the top result
- [ ] Integration test: search with no query returns paginated results in default order
- [ ] Integration test: multi-word search returns results matching all terms
- [ ] Integration test: search across entity types returns ranked results
- [ ] Verify existing tests in `tests/api/search.rs` still pass

## Verification Commands
- `cargo test -p search` — search module unit tests pass
- `cargo test --test search` — search integration tests pass

## Dependencies
- Depends on: Task 1 — Add database migration for search indexes

---

[sdlc-workflow] Description digest: sha256-md:cd3280ae0a54c29699d7de6c07808ebbf62df025870d9fd070fcd26405974168
