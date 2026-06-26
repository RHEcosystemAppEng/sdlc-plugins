# Impact Map — TC-9002: Improve search experience

## Feature Summary

Improve the search experience in the trustify-backend platform by making search faster, returning more relevant results, and adding filtering capabilities.

## Ambiguities and Open Questions

The feature description (TC-9002) is intentionally vague and contains several ambiguities that must be resolved before implementation can be considered complete. These are flagged below:

### Ambiguity 1: No specific performance targets for "Search should be faster"

The requirement states "Currently too slow" but provides no measurable targets. There is no indication of current latency, desired latency, throughput expectations, or which percentile (p50, p95, p99) should be measured. Without concrete targets, it is impossible to verify that the performance improvement is sufficient.

**Recommendation:** Clarify target search response time (e.g., "p95 latency under 200ms for queries returning up to 100 results").

### Ambiguity 2: No definition of relevance for "Results should be more relevant"

The requirement states "Users complain about irrelevant results" but provides no definition of what makes a result relevant. There are no ranking criteria, weighting rules, or examples of queries that currently return poor results. It is unclear whether relevance means text-match accuracy, recency, severity-based ordering, or some combination.

**Recommendation:** Define ranking criteria (e.g., "exact matches rank above partial matches; results with higher severity rank first within equal text relevance") and provide example queries with expected result ordering.

### Ambiguity 3: No specification for "Add filters"

The requirement says "Some kind of filtering capability" but does not specify which entity fields should be filterable, which filter operators to support (equality, range, multi-select), or whether filters apply to all searchable entities or only specific ones (SBOMs, advisories, packages).

**Recommendation:** Enumerate the filter fields (e.g., severity, date range, package name, license type) and operators (e.g., equals, contains, greater-than) that must be supported.

### Ambiguity 4: "Better UI" cannot be planned

The "Better UI" requirement has no design mockups, wireframes, or UI specifications. Additionally, only the backend repository (trustify-backend) is in scope. There is no frontend repository available to implement UI changes.

**Decision:** Exclude "Better UI" from this plan. It requires a frontend repository and design specifications before it can be planned.

### Ambiguity 5: Non-functional requirements are not measurable

The NFR "Should be fast enough" has no quantitative definition. "Don't break existing functionality" is reasonable but vague -- it does not specify regression test coverage expectations or backward compatibility guarantees for the search API.

**Recommendation:** Define measurable NFRs (e.g., "search latency p95 < 300ms", "zero breaking changes to existing GET /api/v2/search request/response schema", "all existing integration tests pass").

### Ambiguity 6: No acceptance criteria defined

The feature has no acceptance criteria whatsoever. There is no way to determine when the feature is "done" or to verify that the implementation meets stakeholder expectations.

**Recommendation:** Define explicit acceptance criteria for each requirement before implementation begins.

## Scope Decisions

| Requirement | In Scope? | Rationale |
|---|---|---|
| Search should be faster | Yes | Backend optimization can proceed with assumed targets |
| Results should be more relevant | Yes | Ranking logic can be added with assumed criteria |
| Add filters | Yes | Filter parameters can be added with assumed fields |
| Better UI | **No** | No frontend repo; no design specs; backend-only plan |

## Impacted Areas

### modules/search/
- `src/service/mod.rs` — SearchService: full-text search logic, ranking, and filtering
- `src/endpoints/mod.rs` — GET /api/v2/search endpoint: query parameters, response structure

### common/
- `src/db/query.rs` — Shared query builder helpers for filtering, pagination, sorting
- `src/model/paginated.rs` — PaginatedResults response wrapper (may need search metadata)

### entity/
- `src/sbom.rs`, `src/advisory.rs`, `src/package.rs` — Entity definitions consulted for filterable fields

### migration/
- New migration for search index — database-level full-text search index to improve performance

### tests/
- `api/search.rs` — Search integration tests: must be extended for new filters and ranking

## Task Breakdown

| Task | Title | Dependencies |
|---|---|---|
| 1 | Add database search index for full-text search performance | None |
| 2 | Implement search result ranking and relevance scoring | None |
| 3 | Add filter parameters to search endpoint | None |
| 4 | Extend search service to support filtering | Task 3 |
| 5 | Add search performance and filter integration tests | Tasks 1, 2, 4 |

## Assumptions (Pending Clarification)

All assumptions below are labeled as pending clarification from the product owner:

1. **Performance target assumed as p95 < 500ms** for search queries returning up to 100 results.
2. **Relevance ranking assumed as:** exact match > prefix match > partial match, with severity as a secondary sort for advisories.
3. **Filter fields assumed as:** severity (advisory), date range (all entities), package name (package/SBOM), license (package).
4. **Filter operators assumed as:** equality, contains (text fields), range (date fields), multi-value (severity).
5. **Backward compatibility assumed:** existing search API query parameters continue to work; new parameters are additive.
