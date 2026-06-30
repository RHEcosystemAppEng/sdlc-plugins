# Plan Summary: TC-9002 — Improve Search Experience

## Tasks

| # | Task | Repository | Key Files | Dependencies |
|---|---|---|---|---|
| 1 | Add Full-Text Search Indexes via Database Migration | trustify-backend | `migration/src/m0002_search_indexes/mod.rs`, `entity/src/*.rs` | None |
| 2 | Implement Search Relevance Ranking in SearchService | trustify-backend | `modules/search/src/service/mod.rs`, `common/src/db/query.rs` | Task 1 |
| 3 | Add Search Filter Parameters to Search Endpoint | trustify-backend | `modules/search/src/endpoints/mod.rs`, `common/src/db/query.rs` | Task 2 |
| 4 | Add Integration Tests for Search Improvements | trustify-backend | `tests/api/search.rs` | Task 3 |

## Repositories Affected
- **trustify-backend** — All 4 tasks target this repository

## Architecture Summary

The plan addresses three MVP requirements from TC-9002 through a linear dependency chain:

1. **Database layer (Task 1):** Add PostgreSQL tsvector columns and GIN indexes to sbom, advisory, and package tables via a new SeaORM migration. This provides the foundation for fast full-text search.

2. **Service layer (Task 2):** Refactor `SearchService` to use `ts_rank` scoring against the new tsvector columns, replacing LIKE/ILIKE pattern matching. Adds shared full-text query helpers to `common/src/db/query.rs`.

3. **API layer (Task 3):** Extend the `GET /api/v2/search` endpoint with filter query parameters (entity_type, severity, date_from, date_to, license) using AND combination logic.

4. **Validation layer (Task 4):** Comprehensive integration tests covering full-text search, relevance ranking, all filter parameters, edge cases, and backward compatibility.

## Scope Exclusions

- **"Better UI" (Non-MVP):** Excluded from scope. Cannot be planned without design mockups or access to a frontend repository. The trustify-backend repository contains only the REST API. UI work should be planned separately with UX design input.

## Ambiguities Flagged

The feature description is intentionally vague. The following ambiguities were identified and documented with assumptions in the task descriptions and impact map:

1. **No performance targets** — "search should be faster" lacks baseline or target latency metrics
2. **No relevance criteria** — "results should be more relevant" lacks a definition of relevance or ranking rules
3. **No filter specification** — "add filters" lacks specific filter types, combination logic, or facet requirements
4. **No entity scope** — does not specify which entity types (SBOMs, advisories, packages) need improvement
5. **Non-quantitative NFRs** — "should be fast enough" provides no measurable acceptance criteria

All assumptions are labeled "assumptions pending clarification" in the task descriptions.

## Inherited Fields

Inherited fields propagated to tasks: priority=Normal, fixVersion=RHTPA 1.6.0
