# Repository Impact Map -- TC-9002: Improve search experience

## Workflow Mode: direct-to-main

**Rationale:** No atomicity indicators identified. All changes are within a single repository (trustify-backend) and can be delivered incrementally:
- Search performance optimization, relevance improvements, and filter additions are independent changes that each leave main in a working state
- No coordinated schema migrations requiring all-or-nothing delivery
- No breaking API changes between tasks (the search endpoint is extended, not replaced)
- No cross-cutting refactors spanning multiple tasks

## Field Inheritance

- **Priority:** Normal (inherited from Feature TC-9002, propagated to all tasks -- not "Undefined", so propagation applies)
- **Fix Versions:** RHTPA 1.6.0 (inherited from Feature TC-9002, propagated to all tasks -- fixVersion scope defaults to "both" as no Jira Field Defaults section is configured in CLAUDE.md)

All tasks will be created with:
```
additional_fields: {
  "labels": ["ai-generated-jira"],
  "priority": {"name": "Normal"},
  "fixVersions": [{"name": "RHTPA 1.6.0"}]
}
```

## Impact

### trustify-backend

**changes:**
- Optimize search query performance in SearchService (`modules/search/src/service/mod.rs`) -- add database indexes, optimize query structure, evaluate caching strategy
- Improve search result relevance scoring in SearchService (`modules/search/src/service/mod.rs`) -- enhance PostgreSQL full-text search ranking with weighted tsvector and ts_rank
- Add filtering capability to search endpoint (`modules/search/src/endpoints/mod.rs`, `modules/search/src/service/mod.rs`, `common/src/db/query.rs`) -- extend `GET /api/v2/search` with filter query parameters (entity_type, name, date range)
- Create search model types (`modules/search/src/model/`) -- define SearchFilter struct and related types following module pattern
- Add database migration for search indexes (`migration/src/m0002_search_indexes/`) -- GIN indexes on tsvector columns
- Update integration tests (`tests/api/search.rs`) -- add tests for performance, relevance ordering, and filter behavior

## Ambiguities and Assumptions

The following ambiguities were identified in the feature description. Assumptions are documented for each; these should be validated with the product owner before implementation begins.

| # | Ambiguity | Source | Assumption |
|---|---|---|---|
| A1 | "Search should be faster" -- no quantitative performance target (current latency unknown, target latency unspecified) | Requirements table | Performance optimization will focus on database query optimization (indexing, query plan analysis) and caching within the existing SearchService. Success will be measured by relative improvement over current baseline. |
| A2 | "Results should be more relevant" -- no definition of relevance or ranking criteria specified | Requirements table | Relevance improvement will enhance PostgreSQL full-text search scoring (ts_rank, weighted tsvector columns). No external search engine (Elasticsearch, etc.) is assumed. Title/name matches will rank higher than body/description matches. |
| A3 | "Add filters" described only as "Some kind of filtering capability" -- no specification of filterable fields, filter operations, or UI integration | Requirements table | Filters will follow the existing query helper pattern in `common/src/db/query.rs` and support filtering by entity type (SBOM, advisory, package), name substring, and date range. |
| A4 | "Should be fast enough" (NFR) -- no specific latency, throughput, or concurrency requirements | Non-Functional Requirements | Interpreted as: search queries should complete within reasonable bounds and not degrade under normal load. |
| A5 | "Don't break existing functionality" (NFR) -- no specific regression criteria defined | Non-Functional Requirements | Interpreted as: existing search endpoint contract is preserved (backward-compatible), existing integration tests continue to pass. |

## Excluded Requirements

| Requirement | Is MVP? | Reason for Exclusion |
|---|---|---|
| Better UI -- "Make it look nicer" | No | Requires a frontend repository and design mockups. No frontend repository is listed in the Repository Registry, and no Figma designs are available. This requirement cannot be decomposed into actionable tasks without these inputs. |

## CONVENTIONS.md

A `CONVENTIONS.md` file exists at the trustify-backend repository root. The following conventions were identified and applied to tasks where file-type applicability rules are satisfied:

- §Module Pattern (scope: module directories, .rs files)
- §Error Handling (scope: .rs handler/service files)
- §Endpoint Registration (scope: .rs endpoint files)
- §Response Types (scope: .rs endpoint files)
- §Query Helpers (scope: .rs query files)
- §Testing (scope: broadly applicable)
- §Caching (scope: .rs endpoint route builders)

## Documentation and Testing

- **Documentation task:** Not generated -- no "Documentation Considerations" section exists in the Feature description (per constraint §1.84).
- **Testing tasks:** Not generated -- no testing readiness template found at `docs/testing-readiness.md` in the target repository (per constraint §1.86).
