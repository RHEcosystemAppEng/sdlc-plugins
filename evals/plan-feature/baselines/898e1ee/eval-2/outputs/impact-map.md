# Repository Impact Map -- TC-9002: Improve search experience

## Feature Summary

TC-9002 requests improvements to the search experience: faster search, more relevant results, and filtering capability. The feature description is intentionally vague and requires significant clarification before detailed implementation can proceed.

## Identified Ambiguities

The following ambiguities were identified in the TC-9002 feature description. Each is flagged for product owner clarification before implementation begins.

### Ambiguity 1: "Search should be faster" -- No performance baseline or target

The requirement states search is "currently too slow" but provides no quantitative baseline (current p50/p95 latency) or target (e.g., "under 200ms for 95th percentile"). The non-functional requirement "should be fast enough" is equally undefined.

**Assumption pending clarification:** We assume the goal is to reduce search latency by adding database indexes on commonly queried columns and optimizing the existing full-text search query in `modules/search/src/service/mod.rs`. We target a measurable improvement but cannot commit to a specific SLA without baseline metrics.

### Ambiguity 2: "Results should be more relevant" -- No definition of relevance

The requirement does not define what "relevant" means. There is no ranking specification, no description of what users expect to find, no indication of which entity types (SBOMs, advisories, packages) are most important in search results, and no weighting criteria.

**Assumption pending clarification:** We assume relevance means implementing PostgreSQL `ts_rank` scoring on the existing full-text search, with title/name fields weighted higher than description/body fields. The exact weighting is subject to tuning after initial implementation.

### Ambiguity 3: "Add filters" -- No specification of which filters

The requirement says "some kind of filtering capability" without specifying which fields should be filterable, which entity types support filters, or what the filter UX should be (since this is a backend, this means query parameter design).

**Assumption pending clarification:** We assume filters should cover the most obvious domain-relevant fields: entity type (SBOM, advisory, package), severity (for advisories), and date range (created/modified). Additional filters can be added in follow-up work.

### Ambiguity 4: "Better UI" -- Excluded from scope

The "Better UI" requirement is marked non-MVP and cannot be planned without design mockups or a frontend repository. The target repository `trustify-backend` is a Rust backend service with no frontend code. **This requirement is explicitly excluded from scope.** It should be addressed in a separate feature targeting the frontend repository once designs are available.

### Ambiguity 5: "Don't break existing functionality" -- No regression test baseline

The non-functional requirement to "not break existing functionality" does not specify which existing behaviors are critical or how regression will be measured. Existing integration tests in `tests/api/search.rs` provide some coverage, but the extent of that coverage is unknown.

**Assumption pending clarification:** We assume all existing integration tests in `tests/api/search.rs` must continue to pass, and new tests must cover added functionality.

## Workflow Mode

**Direct-to-main.** There are no atomicity constraints (no linked issues requiring coordinated deployment). Each task can be merged independently.

## Scope Determination

**In scope (MVP):**
1. Search performance optimization (indexing, query optimization)
2. Search relevance improvements (ranking/scoring)
3. Search filtering capability (query parameter filters)
4. Integration tests for all new functionality

**Out of scope:**
- "Better UI" -- requires frontend repository and design mockups (see Ambiguity 4)
- Any frontend changes -- `trustify-backend` is a backend-only repository
- Search infrastructure changes (e.g., Elasticsearch/Meilisearch) -- not mentioned and would be a separate architectural decision

## Repository Impact

### trustify-backend

| Area | Files | Change Type |
|---|---|---|
| Search service | `modules/search/src/service/mod.rs` | Modify -- optimize queries, add ranking, add filter logic |
| Search endpoints | `modules/search/src/endpoints/mod.rs` | Modify -- add filter query parameters, update response to include relevance score |
| Search module | `modules/search/src/lib.rs` | Modify -- re-export new types if needed |
| Database migrations | `migration/src/` | Create -- new migration for search indexes |
| Common query helpers | `common/src/db/query.rs` | Modify -- add full-text search index helpers if needed |
| Entity definitions | `entity/src/advisory.rs`, `entity/src/sbom.rs`, `entity/src/package.rs` | Potentially modify -- add index annotations |
| Integration tests | `tests/api/search.rs` | Modify -- add tests for filters, relevance, performance |

## Task Breakdown

| Task | Title | Dependencies |
|---|---|---|
| Task 1 | Add database indexes for search performance | None |
| Task 2 | Implement search relevance ranking | Task 1 |
| Task 3 | Add search filter query parameters | Task 1 |
| Task 4 | Add integration tests for search improvements | Tasks 2, 3 |
