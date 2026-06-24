## Repository
trustify-backend

## Target Branch
main

## Description
Implement relevance-based ranking for search results so that more relevant results appear first. The feature requirement states "results should be more relevant" but provides no definition of relevance criteria or ranking algorithm (see Ambiguity 2 in impact map). This task adds PostgreSQL `ts_rank` scoring with weighted fields so that matches on names/titles rank higher than matches on descriptions.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add `ts_rank` scoring to search queries. Weight fields so that entity name/title matches score higher than description matches. Order results by rank score descending. **Assumption (pending clarification):** Name/title fields are weighted at 'A' (highest) and description fields at 'B' — this weighting scheme is assumed since the feature provides no ranking criteria.
- `modules/search/src/endpoints/mod.rs` — Expose an optional `sort=relevance` query parameter on GET `/api/v2/search` to allow clients to explicitly request relevance-based ordering (default when a search query is present). Maintain backward compatibility with existing sort options.
- `common/src/db/query.rs` — Extend the `full_text_search` helper (from Task 2) to accept weight configuration and return rank scores alongside match conditions.

## Implementation Notes
- Use PostgreSQL `ts_rank(tsvector, tsquery)` to compute relevance scores: `SELECT *, ts_rank(to_tsvector('english', name), plainto_tsquery('english', $1)) AS rank FROM ... ORDER BY rank DESC`
- Apply `setweight(to_tsvector('english', name), 'A') || setweight(to_tsvector('english', COALESCE(description, '')), 'B')` to create weighted tsvectors — **Assumption (pending clarification):** exact column names for "name" and "description" across all three entity types need verification
- When no search term is provided (browsing mode), fall back to the existing sort order (e.g., created_at descending) to maintain backward compatibility
- Results should continue to use `PaginatedResults<T>` from `common/src/model/paginated.rs`
- **Assumption (pending clarification):** Relevance ranking applies uniformly to all entity types in search results. If different entity types need different ranking strategies, this would require further specification.

## Acceptance Criteria
- [ ] Search results are ordered by relevance score when a search query is provided
- [ ] Name/title matches rank higher than description-only matches
- [ ] Existing sort behavior is preserved when no search query is present
- [ ] `sort=relevance` query parameter is accepted on GET `/api/v2/search`
- [ ] Response format remains `PaginatedResults<T>` (backward compatible)

## Test Requirements
- [ ] Test that searching for an exact entity name returns that entity as the first result
- [ ] Test that a term appearing in an entity name ranks higher than the same term appearing only in a description
- [ ] Test that results without a search query maintain default ordering
- [ ] Test that `sort=relevance` parameter is accepted and does not error

## Dependencies
- Depends on: Task 2 — Optimize search queries (requires the `full_text_search` helper in `common/src/db/query.rs`)

## Digest
[sdlc-workflow] Description digest: sha256-md:08f89c24f33d9262d0c82b8083f24925c9a4d329ec89c997c60e60a40468323c
