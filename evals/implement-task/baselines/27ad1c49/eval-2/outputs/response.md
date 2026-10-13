# TC-9202 -- Task Description Incomplete

I cannot proceed with implementing TC-9202. The task description is missing required sections and contains vague criteria that do not meet the structured template requirements. I need clarification before any implementation work can begin.

## Gaps Identified

### 1. Missing: Implementation Notes section

The task description has no **Implementation Notes** section. This section is required and should specify:
- Which existing code patterns to follow (e.g., how sibling search functionality is implemented in `modules/search/` or how `advisory/` implements its search)
- References to concrete types, traits, or helper functions to reuse (e.g., whether to use the shared `query.rs` query builder, how to integrate with `SearchService` in `modules/search/`)
- How the search endpoint should integrate with existing infrastructure (e.g., full-text PostgreSQL search vs. in-memory filtering, use of SeaORM query builders)

Without Implementation Notes, I would be guessing at the implementation approach, which violates the skill's constraint against proceeding without complete information.

### 2. Missing: API Changes section

The task description has no **API Changes** section. This section is required and should describe the endpoints to create or modify, including:
- The HTTP method and path (e.g., `GET /api/v2/package/search?q=...` or a query parameter on the existing `GET /api/v2/package`)
- Request parameters (query string, path params, request body)
- Response shape and status codes
- Whether this extends the existing list endpoint or creates a new dedicated search route

### 3. Vague Acceptance Criteria

The acceptance criteria lack measurable, verifiable definitions:

- **"Search results are relevant"** -- What does "relevant" mean in this context? Does it mean exact match on package name? Substring match? Full-text search across multiple fields? Fuzzy matching? There is no definition of relevance that I can verify against.
- **"Performance is acceptable"** -- What is the performance threshold? Is there a maximum response time (e.g., < 200ms for 95th percentile)? A maximum result set size? A pagination requirement? Without a concrete threshold, this criterion cannot be verified in Step 8.
- **"Users can search for packages"** -- This is broad. Which fields should be searchable? Package name only? Name and version? Name, version, and license? The `PackageSummary` struct includes a `license` field -- should that be searchable too?

### 4. Vague Test Requirements

The single test requirement -- **"Test that search works correctly"** -- provides no actionable guidance:

- What test cases are expected? (e.g., exact match, partial match, no results, special characters, empty query)
- What assertions should be made? (e.g., assert specific packages are returned, assert result ordering, assert pagination behavior)
- Should there be negative test cases? (e.g., search with no matches returns empty results, malformed query returns 400)
- Should there be performance/load tests?

## Clarifying Questions

Before I can proceed, I need answers to the following:

1. **Which fields should be searchable?** The `PackageSummary` struct includes at minimum a name and a `license` field. Should the search match against the package name only, or also against version, license, and/or other fields? Should it support multi-field queries?

2. **What does "relevant" mean for search results?** Should this be an exact match, a substring/prefix match (SQL `LIKE`/`ILIKE`), PostgreSQL full-text search (`tsvector`/`tsquery`), or integration with the existing `SearchService` in `modules/search/`? Should results be ranked by relevance score, or is simple filtering sufficient?

3. **What is the performance threshold for "acceptable"?** Is there a target response time (e.g., p95 < 500ms)? Should results be paginated using the existing `PaginatedResults<T>` wrapper? Is there a maximum result set size?

4. **Should this be a new endpoint or a query parameter on the existing list endpoint?** The repository has both a pattern of dedicated search endpoints (`modules/search/`) and list endpoints with query filtering (`common/src/db/query.rs`). Which pattern should this follow? What should the API path and method be?

5. **What test scenarios are required?** At minimum I would expect tests for: successful search with results, search with no matches, empty/missing query parameter, and pagination. Are there additional scenarios (e.g., special characters, SQL injection prevention, case sensitivity)?

6. **Should the search use the existing `SearchService` from `modules/search/`?** That module already provides full-text search across entities. Should the package search delegate to it, extend it, or implement search independently within the `package` module?

**Stopping execution.** I will not create a branch, draft an implementation plan, or make any code changes until these gaps are resolved. Please update the task description with the missing sections and clarify the vague criteria, then re-run this skill.
