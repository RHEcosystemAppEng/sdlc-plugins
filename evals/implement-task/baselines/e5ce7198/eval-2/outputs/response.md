# TC-9202: Incomplete Task Description -- Clarification Required

I cannot proceed with implementing this task. The task description for TC-9202 ("Add package search functionality") is incomplete and contains multiple gaps that prevent implementation. Per the implement-task workflow rules (constraint 1.6), I must stop execution immediately and request clarification rather than improvising or guessing implementation details. No branch will be created, no code will be written, and no Jira transitions will occur until these gaps are resolved.

---

## Identified Gaps

### 1. Implementation Notes -- MISSING

The task description contains no **Implementation Notes** section. This is a critical omission because Implementation Notes provide the code references, patterns, and architectural guidance necessary for implementation. Without this section, I cannot determine:

- Which existing patterns in `trustify-backend` to follow for the new search endpoint. The repository has a `modules/search/` module with its own `SearchService` (full-text search across entities) -- should the package search reuse this infrastructure, or should it be a standalone query within the `package` module?
- How to wire the new search route into the existing `endpoints/mod.rs` router registration -- what Axum extractors, middleware, or shared utilities to use.
- What service-layer method to add to `PackageService` (in `modules/fundamental/src/package/service/mod.rs`) and what query builder patterns from `common/src/db/query.rs` to apply.
- Whether a database migration is needed (e.g., adding a full-text search index on the `package` table).

Per constraint 5.3, implementation must follow patterns referenced in the task's Implementation Notes. Without this section, that requirement cannot be satisfied.

### 2. Acceptance Criteria -- Too Vague to Implement or Verify

The acceptance criteria as written are not specific enough to be pass/fail verifiable (per constraint 4.3):

- **"Users can search for packages"** -- Search by which fields? Package name? Version? Description? PURL (Package URL)? License? A combination? What query parameters should the search endpoint accept (e.g., `q`, `name`, `version`)? What HTTP method and path should be used -- `GET /api/v2/package/search?q=...`, or a query parameter added to the existing `GET /api/v2/package` list endpoint?

- **"Search results are relevant"** -- What defines "relevant"? Is this full-text search with ranking (e.g., PostgreSQL `ts_rank`), prefix matching, substring/`ILIKE` matching, exact matching, or fuzzy matching with a similarity threshold? Should results be ordered by relevance score, and if so, should that score be exposed in the response?

- **"Performance is acceptable"** -- What is the concrete performance target? Is there a maximum response time threshold (e.g., p95 < 200ms, p99 < 500ms)? Against what dataset size should performance be measured? Should database indexes be created to support search queries, and if so, what type (B-tree for exact/prefix, GIN for full-text, pg_trgm for fuzzy)?

Each criterion needs measurable, verifiable thresholds before implementation can begin.

### 3. Test Requirements -- Too Vague to Implement

The sole test requirement is:

- **"Test that search works correctly"** -- This does not specify what "correctly" means. To write tests, I need to know:
  - **Search scenarios**: What specific cases to cover -- exact name match, partial match, case-insensitive match, no results found, multiple results, special characters in query string, empty query?
  - **Response validation**: What response shape to assert against -- should results be wrapped in `PaginatedResults<PackageSummary>`? Should total count be included? Which fields must appear per result?
  - **Error cases**: How should the endpoint handle invalid inputs -- empty query string, excessively long query, unsupported query parameters? What HTTP status codes should be returned?
  - **Test type and location**: Should these be integration tests in `tests/api/` (following the existing pattern in `tests/api/search.rs`), unit tests within the module, or both?
  - **Test file**: Should a new `tests/api/package_search.rs` file be created, or should tests be added to an existing file?

---

## Additional Clarifying Questions

1. **Search infrastructure reuse**: The repository already has a `modules/search/` module with a `SearchService` that provides full-text search across entities. Should the package search endpoint delegate to this existing service, extend it, or implement search independently within the `package` module?

2. **API contract**: What should the endpoint path be? Should it follow the pattern `GET /api/v2/package/search?q=<term>` as a separate route, or should search be added as an optional query parameter on the existing `GET /api/v2/package` list endpoint? Should the response support pagination (using `PaginatedResults<T>`), sorting, and filtering consistent with other list endpoints?

3. **Response format**: Should search results return `PackageSummary` (as defined in `modules/fundamental/src/package/model/summary.rs`) or a different projection? Should a relevance score be included in the response?

4. **Files to Modify scope**: The task lists only `endpoints/mod.rs` to modify and `endpoints/search.rs` to create. Will changes also be needed in the service layer (`package/service/mod.rs`) and potentially the entity layer (`entity/package.rs`) for query support? Should `server/main.rs` be updated if new route mounting is required?

---

## Action Required

Please provide the missing **Implementation Notes** with code references to existing patterns, replace the vague **Acceptance Criteria** with specific and measurable requirements, and expand the **Test Requirements** with concrete test scenarios and expected behaviors. Once the task description is complete, I will proceed with implementation.
