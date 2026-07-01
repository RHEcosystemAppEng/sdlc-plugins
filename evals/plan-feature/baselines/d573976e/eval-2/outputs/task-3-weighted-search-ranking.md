# Task 3 — Implement weighted full-text search ranking in SearchService

## Repository
trustify-backend

## Target Branch
main

## Description
Enhance the `SearchService` to use PostgreSQL's full-text search capabilities with weighted ranking (`ts_rank`) to return results ordered by relevance. This replaces the current unranked search with a scoring model that prioritizes title/name matches over description matches, directly addressing the user complaint that "search doesn't return useful results."

## Files to Modify
- `modules/search/src/service/mod.rs` — rewrite search queries to use `ts_rank` with `tsvector` columns created by Task 1's migration, apply weight configuration (A for name/title, B for description), and populate the `relevance_score` field in `SearchResultSummary` (from Task 2)
- `common/src/db/query.rs` — add a shared helper for constructing `ts_query` from user search input (tokenization, prefix matching, boolean operators)

## Implementation Notes
- Use PostgreSQL `to_tsquery` or `plainto_tsquery` to convert user search input into a `tsquery`, and `ts_rank` to score matches against the `tsvector` columns indexed in Task 1.
- Weight configuration: assign weight A (highest) to name/title fields and weight B to description fields. This ensures that an exact name match ranks higher than a description mention.
- The `ts_query` helper in `common/src/db/query.rs` should handle:
  - Basic tokenization (splitting on whitespace)
  - Prefix matching for partial terms (append `:*` to each token)
  - Combining terms with `&` (AND) semantics by default
- Order results by `ts_rank` descending. When relevance scores are equal, fall back to entity name alphabetically.
- Populate the `SearchResultSummary.relevance_score` field with the `ts_rank` output.
- Follow the existing query builder patterns in `common/src/db/query.rs` for composability with pagination and sorting.
- Error handling: wrap database errors with `.context("Full-text search query failed")` per the project's `AppError` convention.

## Reuse Candidates
- `common/src/db/query.rs` — existing query builder helpers for filtering, pagination, and sorting; extend rather than replace
- `modules/search/src/service/mod.rs::SearchService` — existing search implementation to be enhanced
- `common/src/error.rs::AppError` — error type with `.context()` wrapping pattern

## Acceptance Criteria
- [ ] Search results are ordered by relevance score (highest first)
- [ ] Title/name matches rank higher than description-only matches
- [ ] Partial search terms return results (prefix matching)
- [ ] Relevance score is populated in `SearchResultSummary`
- [ ] Existing search queries that currently return results continue to return results (no regressions)

## Test Requirements
- [ ] Integration test: search for a term that appears in both SBOM name and advisory description — SBOM result ranks higher
- [ ] Integration test: search for a partial term returns matching results
- [ ] Integration test: search for a non-existent term returns empty results with no errors

## Verification Commands
- `cargo test -p search -- --test-threads=1` — search module tests pass
- `cargo test -p tests -- search --test-threads=1` — integration tests pass

## Dependencies
- Depends on: Task 1 — Add full-text search indexes via database migration (requires GIN indexes to exist)
- Depends on: Task 2 — Add search result model types with relevance scoring (requires SearchResultSummary type)
