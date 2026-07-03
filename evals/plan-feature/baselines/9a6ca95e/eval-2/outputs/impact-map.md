# Impact Map — TC-9002: Improve search experience

## Feature Scope

This impact map covers the MVP requirements for TC-9002. The non-MVP requirement "Better UI" is explicitly excluded from scope (see below).

## Ambiguities and Clarifications Needed

The feature description TC-9002 is underspecified in several critical areas. The following ambiguities were identified and must be resolved with the product owner before or during implementation:

### Ambiguity 1: No performance targets defined

The requirement states search is "too slow" and the NFR says it should be "fast enough," but no quantitative targets are provided. There are no baseline metrics (current latency), no target metrics (desired latency), and no specification of measurement methodology (p50, p95, p99, throughput). **Assumption:** This plan targets adding database indexes and query optimizations. Measurable improvement will be verified via integration test timing and EXPLAIN ANALYZE, but without defined thresholds, "done" is subjective.

### Ambiguity 2: No relevance criteria specified

The requirement says results should be "more relevant" and users "complain about irrelevant results," but there is no definition of what constitutes a relevant result. No ranking factors are specified (text match quality, recency, entity importance, severity). No examples of "irrelevant" results are provided. **Assumption:** This plan implements PostgreSQL full-text search ranking (`ts_rank`) based on term frequency and match proximity. Domain-specific ranking factors (e.g., prioritizing critical advisories) are not included without explicit guidance.

### Ambiguity 3: Filter dimensions not specified

The requirement says "Add filters" with the note "Some kind of filtering capability" but does not enumerate which fields or dimensions should be filterable. **Assumption:** This plan implements filters based on the existing entity model attributes: entity type (sbom/advisory/package), date range, advisory severity, and package license. Additional filters may be needed but are not discoverable from the requirements.

### Ambiguity 4: Search scope undefined

The feature does not specify which entities the search improvement covers. The existing SearchService operates across SBOMs, advisories, and packages. **Assumption:** All three entity types are in scope for performance, relevance, and filtering improvements.

### Ambiguity 5: Non-functional requirements are vague

"Should be fast enough" and "Don't break existing functionality" are not actionable NFRs. There are no load/concurrency requirements, no backward compatibility guarantees for API contracts, and no mention of search result limits or pagination behavior changes. **Assumption:** Existing API contracts and response formats are preserved. Performance improvements are additive (indexes, query optimization) rather than breaking changes.

## "Better UI" — Excluded from Scope

The "Better UI" requirement is marked as non-MVP and **cannot be planned** for the following reasons:

1. **No frontend repository available.** The planning scope covers only `trustify-backend`. UI changes require a frontend repository that is not part of this planning context.
2. **No design mockups or specifications.** "Make it look nicer" provides no actionable design direction. UI work requires design mockups, wireframes, or at minimum a description of specific UI problems to address.
3. **No Figma context provided.** No design artifacts are available for this feature.

This requirement should be planned separately once a frontend repository is in scope and design specifications are available.

## Affected Modules

| Module | Impact | Tasks |
|---|---|---|
| `modules/search/` | Primary — search service, endpoint, and model changes | 1, 2, 3 |
| `common/src/db/` | Extended — new query builder helpers for full-text search and filtering | 1, 3 |
| `common/src/model/` | Minor — potential response wrapper extension | 2 |
| `migration/` | New migration — search indexes | 1 |
| `entity/` | Read-only — verify entity column annotations | 1 |
| `tests/api/` | Extended — new integration tests for all tasks | 1, 2, 3 |

## Task Dependency Graph

```
Task 1: Optimize search performance (indexes, query optimization)
  └── Task 2: Search relevance scoring (depends on tsvector indexes from Task 1)
        └── Task 3: Add search filters (depends on SearchResult model from Task 2)
```

## Risk Assessment

- **Medium risk:** Without defined performance targets, there is no clear "done" criterion for Task 1. Recommend establishing baseline metrics before implementation begins.
- **Low risk:** Relevance scoring (Task 2) uses well-understood PostgreSQL full-text search ranking. The main risk is that the default ranking may not match user expectations of "relevant."
- **Low risk:** Filtering (Task 3) follows established patterns in the codebase (query builder helpers, list endpoint parameters).
