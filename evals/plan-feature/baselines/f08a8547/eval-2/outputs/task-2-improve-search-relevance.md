## Repository
trustify-backend

## Target Branch
main

## Description
Improve the relevance scoring of search results returned by the SearchService. The feature description states users complain about "irrelevant results" but provides no specific ranking criteria or relevance definition (see Ambiguity A2 in the impact map). This task focuses on enhancing PostgreSQL's full-text search scoring: implementing weighted tsvector columns, applying ts_rank or ts_rank_cd for result ordering, and ensuring search across multiple entity types (SBOMs, advisories, packages) returns meaningfully ranked results.

**Ambiguity note:** "More relevant" is not defined. The implementer should establish a relevance baseline by documenting the current search behavior (e.g., unranked or simple keyword match) and then implement standard full-text search ranking as the improvement. Consider title/name matches ranking higher than description/body matches.

## Files to Modify
- `modules/search/src/service/mod.rs` -- implement relevance scoring using ts_rank or ts_rank_cd, add weighted tsvector queries
- `modules/search/src/endpoints/mod.rs` -- ensure search results are returned ordered by relevance score

## Implementation Notes
- Use PostgreSQL `ts_rank()` or `ts_rank_cd()` functions to score search results
- Implement weighted tsvector: assign higher weight (A) to title/name fields, lower weight (D) to description/body fields
- Ensure search results across entity types (SBOMs, advisories, packages) are scored consistently so cross-entity search returns meaningful rankings
- Review existing SearchService implementation to understand current search behavior before modifying
- Per CONVENTIONS.md §Error Handling: all service methods must return `Result<T, AppError>` with `.context()` wrapping for any new error paths.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's .rs handler/service scope.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs` -- search results must use this wrapper.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's .rs endpoint scope.
- Per CONVENTIONS.md §Module Pattern: each domain module follows `model/ + service/ + endpoints/` structure -- any new types should be placed accordingly.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's module directory scope.

**Constraints (docs/constraints.md):**
- §2 Commit Rules: every commit must reference the Jira task ID in the footer, follow Conventional Commits, and include `--trailer="Assisted-by: Claude Code"`
- §3 PR Rules: branch must be named after the Jira task ID; after opening PR, post link as Jira comment; `gh pr create` must specify `--base main`
- §5 Code Change Rules: changes scoped to listed files; inspect code before modifying; follow patterns in Implementation Notes; do not duplicate existing functionality

## Reuse Candidates
- `modules/search/src/service/mod.rs::SearchService` -- existing search implementation to extend with relevance scoring
- `common/src/db/query.rs` -- shared query helpers that may already support ordering/sorting; check before implementing custom sort logic
- `common/src/model/paginated.rs::PaginatedResults` -- response wrapper for list/search endpoints

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (most relevant first)
- [ ] Title/name matches rank higher than description/body matches
- [ ] Cross-entity search returns meaningfully ranked results across SBOMs, advisories, and packages
- [ ] Search endpoint response contract is backward-compatible (existing clients unaffected)
- [ ] Existing search integration tests in `tests/api/search.rs` continue to pass

## Test Requirements
- [ ] Add integration test verifying search results are returned in relevance-ranked order (e.g., exact title match ranks above partial body match)
- [ ] Add test verifying cross-entity search returns results from all matching entity types
- [ ] Verify existing search tests pass with relevance scoring enabled

## Verification Commands
- `cargo test --test search` -- verify search integration tests pass
- `cargo build` -- verify compilation succeeds

## Dependencies
- Depends on: Task 1 -- Optimize search query performance (search indexes from Task 1 support relevance scoring)
