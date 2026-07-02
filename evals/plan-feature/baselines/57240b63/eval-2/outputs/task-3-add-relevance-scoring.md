## Repository
trustify-backend

## Target Branch
main

## Description
Add relevance scoring to search results so that more relevant matches appear first.
The current search returns results without meaningful ranking (see Ambiguity 2 in
the impact map — no relevance criteria are defined by the product owner). This task
introduces a scoring model that weights matches by field importance and exposes the
score in the search response.

**Assumption (pending clarification):** Relevance scoring will use field-weight boosting:
title/name matches are weighted higher than description/body matches. The specific
weights and any additional relevance signals (recency, severity, user context) should
be confirmed by the product owner. The current implementation uses a simple weighting
scheme that can be tuned later.

## Files to Modify
- `modules/search/src/service/mod.rs` — Add relevance scoring logic to the search query: compute a score per result based on field-match weights, order results by score descending

## Files to Create
- `modules/search/src/model/mod.rs` — New model module for search-specific types; re-exports SearchResult
- `modules/search/src/model/search_result.rs` — SearchResult struct wrapping the matched entity with a `relevance_score: f64` field

## API Changes
- `GET /api/v2/search` — MODIFY: response items now include a `relevance_score` field (additive, backward compatible). Results are ordered by relevance score descending by default.

## Implementation Notes
- Follow the module pattern established in other modules (e.g., `modules/fundamental/src/sbom/model/`):
  each domain module has a `model/` directory with a `mod.rs` re-exporting types and
  individual type files.
- The `SearchResult` struct should wrap the existing entity summary types (SbomSummary,
  AdvisorySummary, PackageSummary) with an additional `relevance_score: f64` field.
  Inspect these summary types:
  - `modules/fundamental/src/sbom/model/summary.rs` — SbomSummary
  - `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary (includes severity)
  - `modules/fundamental/src/package/model/summary.rs` — PackageSummary (includes license)
- For PostgreSQL full-text search scoring, use `ts_rank()` or `ts_rank_cd()` functions
  if the search uses `tsvector`/`tsquery`. If the search uses LIKE/ILIKE patterns,
  implement application-level scoring based on match position and field weights.
- Suggested initial field weights (tunable):
  - Name/title match: weight 3.0
  - Description match: weight 1.0
  - Identifier/version exact match: weight 5.0
- The search endpoint in `modules/search/src/endpoints/mod.rs` will need to serialize
  the new SearchResult type. Ensure it implements `serde::Serialize`.
- The response still uses `PaginatedResults<T>` from `common/src/model/paginated.rs`,
  now parameterized with `SearchResult` instead of the raw entity type.
- Per docs/constraints.md section 5 (Code Change Rules): inspect existing code patterns
  before implementing.

**Conventions (from Key Conventions):**

Per Key Conventions §Module pattern: follow `model/ + service/ + endpoints/` structure for the search module.
Applies: task creates `modules/search/src/model/mod.rs` matching the convention's Rust module structure scope.

Per Key Conventions §Response types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's Rust service file scope.

## Reuse Candidates
- `modules/fundamental/src/sbom/model/summary.rs` — SbomSummary struct pattern to follow for SearchResult design
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct; the severity field can inform relevance weighting
- `common/src/model/paginated.rs` — PaginatedResults<T> wrapper; SearchResult must be compatible with this response type

## Acceptance Criteria
- [ ] SearchResult struct is created with a relevance_score field
- [ ] Search results are ordered by relevance score descending by default
- [ ] Title/name matches rank higher than description-only matches
- [ ] Existing search API contract is backward compatible (relevance_score is an additive field)
- [ ] Response continues to use PaginatedResults wrapper

## Test Requirements
- [ ] Integration test that verifies a title match scores higher than a description-only match
- [ ] Integration test that verifies results are returned in descending relevance order
- [ ] Existing search tests in `tests/api/search.rs` continue to pass

## Verification Commands
- `cargo test --test search` — All search integration tests pass

## Dependencies
- None (can be developed independently, but benefits from Task 1 indexes)

## additional_fields
- priority: Normal
- fixVersions: ["RHTPA 1.6.0"]
- labels: ["ai-generated-jira"]
---

[sdlc-workflow] Description digest: sha256-md:3ff60daa85bc96fd5b592f8569c6da09019eb7c42faeb5d0867ec5c691c30009
