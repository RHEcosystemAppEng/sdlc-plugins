# Repository Impact Map — TC-9002: Improve search experience

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators identified. Each planned change is independently mergeable:
- Filter parameters are additive to the existing search API (no breaking change)
- Full-text ranking is a backend-only enhancement that does not break existing consumers
- Caching is an infrastructure concern with no cross-task data dependency
No coordinated schema migrations, breaking API changes, cross-cutting refactors, or tightly coupled components were detected.

## Type-to-Role Mapping

Issue type discovery would be performed via `jira.get_project_issue_types`. The project's Hierarchy Configuration specifies `Default epic grouping strategy: by-sub-feature`.

## Epic Grouping (by-sub-feature)

If a level-1 issue type (Epic) is discovered:

- **Epic 1: TC-9002: Search filtering and relevance** — Tasks 1, 2
- **Epic 2: TC-9002: Search performance** — Task 3

## additional_fields (applied to all created issues)

```json
{
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

- **priority**: Inherited from Feature TC-9002 (priority: Normal, not "Undefined")
- **fixVersions**: Inherited from Feature TC-9002 (fixVersions: ["RHTPA 1.6.0"]). No `fixVersion scope` setting found in `### Jira Field Defaults` under `## Jira Configuration` in CLAUDE.md, so defaulting to "both" (propagate to tasks).

## Repository Changes

### trustify-backend

**Changes:**
- Add entity-type and field-value filter query parameters to the search endpoint (`modules/search/endpoints/mod.rs`)
- Implement filter application logic in SearchService using existing `common/src/db/query.rs` helpers (`modules/search/service/mod.rs`)
- Create database migration for B-tree indexes on filterable columns (`migration/src/m0002_search_filter_indexes/mod.rs`)
- Implement PostgreSQL full-text search with tsvector columns and GIN indexes (`migration/src/m0003_fulltext_search_indexes/mod.rs`)
- Add ts_rank-based relevance scoring to SearchService query results (`modules/search/service/mod.rs`)
- Add sort-by-relevance parameter to the search endpoint (`modules/search/endpoints/mod.rs`)
- Configure tower-http response caching for the search endpoint (`modules/search/endpoints/mod.rs`)
- Add integration tests for filtering, relevance ranking, and caching (`tests/api/search.rs`)

## Reuse Candidates Identified

- `common/src/db/query.rs` — Shared query builder helpers (filtering, pagination, sorting). Reuse for constructing filtered search queries instead of writing new filter logic.
- `common/src/model/paginated.rs` — PaginatedResults<T> response wrapper. Reuse for paginated, filtered search results.
- `common/src/error.rs` — AppError enum with IntoResponse. Reuse for error handling in modified search endpoints.
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService includes a search method. Reference as a pattern for implementing filtered search in SearchService.
- `modules/fundamental/src/sbom/endpoints/list.rs` — GET /api/v2/sbom list endpoint. Reference as a pattern for query parameter extraction and paginated response.

## Excluded Requirements

The Feature description (TC-9002) contains significant ambiguities that prevent precise task planning. The following gaps were identified:

| Requirement | Ambiguity | Missing Input |
|---|---|---|
| "Search should be faster" | No quantifiable performance target (e.g., p95 latency < 200ms, query time reduction %). | Specific latency or throughput targets needed to size optimization work and define acceptance criteria. |
| "Results should be more relevant" | No definition of relevance — no ranking criteria, field weighting, or relevance benchmark specified. | Relevance definition (e.g., title matches weighted higher than description, exact matches before partial) needed for ranking algorithm design. |
| "Add filters" — "Some kind of filtering capability" | No specification of which fields should be filterable, what filter types are needed (exact match, range, multi-select), or which entity types should support filtering. | List of filterable fields and filter semantics (e.g., filter by entity type, date range, severity, license) needed. |
| "Should be fast enough" (NFR) | No quantifiable non-functional requirement. Cannot plan or verify. | Specific performance targets (latency, throughput, concurrency) needed. |
| "Don't break existing functionality" (NFR) | Generic backward compatibility requirement. Addressed via test requirements in each task. | No action needed — covered by standard test practices. |
| "Better UI" — "Make it look nicer" (non-MVP) | No frontend repository in scope. Only trustify-backend is configured in the Repository Registry. | A frontend repository must be added to the Repository Registry and the Feature re-planned to include UI tasks. |

**Recommendation:** Before proceeding with implementation, the feature owner should clarify the ambiguities above — specifically the performance targets, relevance criteria, and filterable fields. The tasks below are planned with reasonable defaults but may need revision once requirements are clarified.

## Documentation Signals

No "Documentation Considerations" section found in the Feature description. Documentation task generation skipped.

## Testing Readiness

No `docs/testing-readiness.md` template found in trustify-backend. Testing task generation skipped.
