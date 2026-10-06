## Repository
trustify-backend

## Target Branch
main

## Description
Improve the relevance ranking of search results returned by the `SearchService` so that users receive more useful results for their queries. The current full-text search in `modules/search/src/service/mod.rs` returns results but users report that results are often irrelevant to their search intent.

**Assumption (pending clarification):** In the absence of specified relevance criteria, this task assumes the following ranking strategy: (1) exact matches rank higher than partial matches, (2) matches in entity names/titles rank higher than matches in descriptions or metadata fields, (3) more recent entities receive a slight ranking boost. This ranking strategy should be validated with the product owner.

**Assumption (pending clarification):** The relevance ranking applies uniformly across all searchable entity types (SBOMs, advisories, packages). If different entity types require different ranking strategies, this needs clarification.

## Files to Modify
- `modules/search/src/service/mod.rs` — implement weighted full-text search scoring with field-level ranking priorities across SBOM, advisory, and package entities
- `modules/search/src/endpoints/mod.rs` — expose relevance score in search results if not already present

## Implementation Notes
- The existing `SearchService` in `modules/search/src/service/mod.rs` performs full-text search across entities. Modify the search query to use PostgreSQL `ts_rank` or `ts_rank_cd` functions for weighted ranking.
- Apply field-level weights: entity name/title fields should receive higher weight (e.g., weight A) than description fields (weight B) and metadata fields (weight C/D). Use PostgreSQL's `setweight()` function on `tsvector` columns.
- The search endpoint at `GET /api/v2/search` registered in `modules/search/src/endpoints/mod.rs` should order results by relevance score descending.
- Reference the entity definitions in `entity/src/sbom.rs`, `entity/src/advisory.rs`, and `entity/src/package.rs` to understand which fields are available for weighting.
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a `severity` field — consider whether severity should influence ranking for advisory results.
- The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a `license` field — this is a metadata field that should receive lower ranking weight.
- Per docs/constraints.md §2 (Commit Rules): every commit must reference TC-9002 in the footer, follow Conventional Commits, and include the `Assisted-by: Claude Code` trailer.
- Per docs/constraints.md §3 (PR Rules): the feature branch must be named after the Jira issue ID, and the PR link must be posted as a comment on the Jira task.
- Per docs/constraints.md §5 (Code Change Rules): changes must be scoped to the files listed above, code must be inspected before modification, and implementation must follow referenced patterns.

**Convention-aware enrichment:**

- Per CONVENTIONS.md §Error Handling: all new or modified handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust handler file scope.

- Per CONVENTIONS.md §Response Types: list endpoints must return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust endpoint file scope.

- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database; use `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/search.rs` matching the convention's Rust test file scope.

## Reuse Candidates
- `modules/search/src/service/mod.rs::SearchService` — existing full-text search implementation to extend with ranking logic rather than rewriting
- `common/src/db/query.rs::query builder helpers` — shared query utilities for constructing the ranked search query
- `common/src/model/paginated.rs::PaginatedResults<T>` — response wrapper to preserve for ranked results

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (highest relevance first)
- [ ] Exact matches in entity name/title fields rank higher than partial matches
- [ ] Matches in name/title fields rank higher than matches in description or metadata fields
- [ ] Relevance ranking works consistently across all searchable entity types (SBOMs, advisories, packages)
- [ ] Existing search API contract (`GET /api/v2/search`) is preserved — no breaking changes to response shape
- [ ] All existing search integration tests continue to pass

## Test Requirements
- [ ] Add integration tests in `tests/api/search.rs` verifying that exact name matches rank higher than partial matches
- [ ] Add integration tests verifying that matches in title fields rank higher than matches in description fields
- [ ] Verify existing search integration tests in `tests/api/search.rs` continue to pass without modification
- [ ] Test ranking consistency across entity types (SBOM, advisory, package search results)

## Verification Commands
- `cargo test --test search` — run search integration tests and verify all pass
- `cargo build` — verify the project compiles without errors after changes

## Dependencies
- None
