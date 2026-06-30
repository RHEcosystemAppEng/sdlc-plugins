# Impact Map: TC-9002 — Improve Search Experience

## Feature Overview

Improve the search experience across the Trustify platform by adding full-text search indexes, relevance-based ranking, and filter capabilities to the search endpoint.

## Ambiguities Identified

The feature description TC-9002 contains several significant ambiguities that required assumptions to proceed with planning. These are documented here and flagged in individual task descriptions.

### Ambiguity 1: No Performance Targets
**Feature says:** "Search should be faster" / "Should be fast enough"
**What is missing:** No baseline latency measurements, no target latency (e.g., p95 < 200ms), no specific queries or dataset sizes to benchmark against.
**Assumption pending clarification:** The primary bottleneck is lack of full-text search indexes. Target is sub-200ms p95 query latency for typical searches. PostgreSQL tsvector/GIN indexes are the appropriate solution.

### Ambiguity 2: No Relevance Criteria
**Feature says:** "Results should be more relevant" / "Users complain about irrelevant results"
**What is missing:** No definition of "relevant," no ranking criteria, no user research data, no examples of bad vs. good search results.
**Assumption pending clarification:** Relevance is defined as PostgreSQL ts_rank scoring with title matches weighted above description matches. Weighting scheme: title=A, description=B, other fields=C/D.

### Ambiguity 3: No Filter Specification
**Feature says:** "Add filters — some kind of filtering capability"
**What is missing:** No specific filter types, no filter UI requirements, no indication of AND vs OR combination logic, no requirement for faceted counts.
**Assumption pending clarification:** Filters include entity type (sbom/advisory/package), severity (for advisories), date range (created/modified), and license (for packages). Filters combine with AND logic.

### Ambiguity 4: No Entity Scope
**Feature says:** "Make the search better" (applies globally)
**What is missing:** No specification of which entity types (SBOMs, advisories, packages) need improvement, or whether all are equally important.
**Assumption pending clarification:** All three entity types require equal search improvement, based on the existing SearchService's cross-entity search design.

### Ambiguity 5: Non-Functional Requirements Are Non-Quantitative
**Feature says:** "Should be fast enough" / "Don't break existing functionality"
**What is missing:** No latency SLAs, no throughput targets, no concurrency requirements, no degradation budget.
**Assumption pending clarification:** Backward compatibility is maintained (no breaking API changes). Performance target is sub-200ms p95 for typical search queries on datasets up to 100K documents.

## Excluded from Scope

**"Better UI" (Non-MVP requirement):** The feature lists "Better UI — Make it look nicer" as a non-MVP requirement. This cannot be planned without design mockups, UX specifications, or access to a frontend repository. The trustify-backend repository contains only the REST API backend. UI improvements are excluded from this plan and should be planned separately once design assets and a frontend repository are available.

## Impact by Repository

### trustify-backend

| Area | Files Affected | Change Type |
|---|---|---|
| Database migrations | `migration/src/m0002_search_indexes/mod.rs` (new), `migration/src/lib.rs` | New migration for tsvector columns and GIN indexes |
| Entity definitions | `entity/src/sbom.rs`, `entity/src/advisory.rs`, `entity/src/package.rs` | Add search_vector tsvector columns |
| Search service | `modules/search/src/service/mod.rs` | Refactor to use full-text search with ts_rank |
| Search endpoint | `modules/search/src/endpoints/mod.rs` | Add filter query parameters |
| Shared query helpers | `common/src/db/query.rs` | Add full-text search and filter builder helpers |
| Integration tests | `tests/api/search.rs` | Extend with full-text search, ranking, and filter tests |

## Task Dependency Chain

```
Task 1: Full-Text Search Indexes (migration + entities)
    |
    v
Task 2: Search Relevance Ranking (SearchService refactor)
    |
    v
Task 3: Search Filters (endpoint + service extension)
    |
    v
Task 4: Integration Tests (end-to-end validation)
```

## Task Summary

| Task | Title | Repository | Key Files |
|---|---|---|---|
| 1 | Add Full-Text Search Indexes via Database Migration | trustify-backend | migration/, entity/ |
| 2 | Implement Search Relevance Ranking in SearchService | trustify-backend | modules/search/src/service/, common/src/db/query.rs |
| 3 | Add Search Filter Parameters to Search Endpoint | trustify-backend | modules/search/src/endpoints/, common/src/db/query.rs |
| 4 | Add Integration Tests for Search Improvements | trustify-backend | tests/api/search.rs |
