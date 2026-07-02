# Repository Impact Map — TC-9002: Improve search experience

## Ambiguities Identified

The feature description contains several ambiguities that must be clarified before
implementation can proceed with full confidence. The following assumptions have been
made to enable planning; each is labeled as **pending clarification** from the
product owner.

### Ambiguity 1: "Search should be faster" — No performance targets defined

The requirement states search is "currently too slow" but provides no baseline
metrics, no target latency (e.g., p95 < 200ms), and no indication of which search
operations are slow (full-text search, filtered queries, autocomplete). Without
quantitative targets, there is no way to verify the requirement is met.

**Assumption (pending clarification):** Focus on database-level optimizations
(indexes on commonly searched columns) and query-path optimization in the
SearchService. Target sub-500ms p95 response time for typical search queries as
an interim benchmark until the product owner provides specific SLAs.

### Ambiguity 2: "Results should be more relevant" — No relevance criteria defined

The requirement says users complain about "irrelevant results" but provides no
definition of relevance, no examples of bad results, no information about the
current ranking algorithm, and no user research to inform a relevance model.

**Assumption (pending clarification):** Implement text-match scoring with
field-weight boosting (title matches ranked higher than description matches).
This is a common baseline relevance strategy. The product owner should clarify
whether specific relevance criteria (recency, severity, user role context) are
needed.

### Ambiguity 3: "Add filters" — No filter specification

The requirement says "some kind of filtering capability" but does not specify which
fields should be filterable, what filter types to support (dropdown, multi-select,
free-text, range), which entities support filtering, or how filters compose (AND
vs OR logic).

**Assumption (pending clarification):** Add filtering by entity type (SBOM,
advisory, package), date range, and severity level. These filters are based on
existing entity fields visible in the repository data model. The product owner
should confirm which filters are desired and their composition logic.

### Ambiguity 4: "Should be fast enough" — Non-functional requirement lacks quantification

The non-functional requirement "should be fast enough" is not actionable without
specific targets. No p95/p99 latency requirements, no throughput targets, no
concurrent user load specifications are provided.

**Assumption (pending clarification):** Apply standard backend performance practices
(database indexing, query optimization, connection pooling via existing limiter).
Specific performance targets should be provided by the product owner or SRE team.

### Ambiguity 5: "Don't break existing functionality" — No regression baseline

This non-functional requirement lacks specificity. No backward compatibility
requirements are stated for the search API contract, no regression test baseline is
defined, and no specific integrations to protect are identified.

**Assumption (pending clarification):** The existing search API contract
(GET /api/v2/search) must remain backward compatible. New filter parameters will be
additive (optional query parameters). Existing response shape (PaginatedResults) is
preserved. Existing integration tests in tests/api/search.rs must continue to pass.

### Exclusion: "Better UI" — Out of scope

The "Better UI" requirement is marked as non-MVP and cannot be planned:
- No design mockups or Figma designs are provided
- No frontend repository is in scope (only trustify-backend is available)
- UI improvements require design input and a frontend codebase

This requirement is **excluded** from the current plan. It should be revisited when
design mockups are available and a frontend repository is identified.

---

## Workflow Mode

**Mode:** `direct-to-main`

**Rationale:** No atomicity indicators are present. Each search improvement (indexing,
query optimization, relevance scoring, filtering) can land independently on main
without breaking existing functionality. The changes are additive — new filter
parameters are optional, relevance scoring augments existing results, and index
additions are transparent to the application layer. No coordinated schema migrations,
breaking API changes, cross-cutting refactors, or tightly coupled cross-repo
components are identified.

---

## Impact Map

```
trustify-backend:
  changes:
    - Add database migration with indexes on commonly searched columns to improve search query performance
    - Optimize SearchService query execution for full-text search operations
    - Add relevance scoring model and ranking logic to search results
    - Add filter parameters (entity type, date range, severity) to GET /api/v2/search endpoint
    - Extend search integration tests to cover performance, relevance ranking, and filtering
```
