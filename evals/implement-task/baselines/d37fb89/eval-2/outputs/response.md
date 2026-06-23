# TC-9202 — Task Description Incomplete

I fetched and parsed the task description for TC-9202 ("Add package search functionality") and found that several required sections are missing or insufficiently specified. Per the implement-task skill rules, I must stop execution immediately and ask for clarification before proceeding with any implementation steps.

## Missing Sections

The following sections required by the structured description template are absent:

1. **API Changes** — The task mentions adding a search route and endpoint handler, but there is no API Changes section specifying the endpoint path, HTTP method, query parameters, request/response shapes, or status codes. For a REST endpoint in this codebase (which follows `/api/v2/<entity>` conventions), this section is essential.

2. **Implementation Notes** — There is no Implementation Notes section. This section should reference the specific code patterns to follow, existing utilities to reuse (e.g., the shared query helpers in `common/src/db/query.rs`, the `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs`, or the existing `SearchService` in `modules/search/`), and any architectural decisions about how search should be implemented for the package module.

3. **Dependencies** — No Dependencies section is present. It is unclear whether this task depends on any other tasks under TC-9001.

## Vague Sections

The following sections exist but are too vague to implement against:

4. **Acceptance Criteria** — All three criteria are ambiguous:
   - "Users can search for packages" — which fields should be searchable (name, version, license, namespace/ecosystem, PURL)? Should this be full-text search, prefix matching, exact match, or a combination?
   - "Search results are relevant" — what does "relevant" mean concretely? Is there a relevance ranking algorithm to follow? Should results be sorted by relevance score, and if so, how is relevance computed?
   - "Performance is acceptable" — what is the performance threshold? Is there a maximum response time (e.g., p95 < 200ms)? A maximum result set size? Does the endpoint need pagination?

5. **Test Requirements** — The single entry "Test that search works correctly" provides no actionable detail. What specific scenarios should be tested? What constitutes "correctly"?

6. **Files to Modify / Files to Create** — Only one file to modify and one file to create are listed. Given the repository's module pattern (`model/ + service/ + endpoints/`), a search feature likely also requires changes to:
   - `modules/fundamental/src/package/service/mod.rs` (adding a search method to `PackageService`)
   - `modules/fundamental/src/package/model/` (possibly a search result or search query model)
   - `server/src/main.rs` (if route mounting needs updating)
   - `tests/api/` (integration test file for the package search endpoint)

## Clarifying Questions

Before I can proceed, I need answers to the following:

1. **Which fields should be searchable?** The `PackageSummary` struct includes at minimum a `license` field. Should users be able to search by package name, version, license, ecosystem/namespace, PURL, or some combination? Should this be a single query string parameter that searches across multiple fields, or separate filter parameters per field?

2. **What does "relevant" mean for search results, and how should they be ranked?** Should this use the existing `SearchService` in `modules/search/` (which provides full-text search across entities), or should it be a new SQL-based search within the package module? If full-text, should results be ranked by a relevance score? What ordering should be applied — relevance, alphabetical, most recently ingested?

3. **What is the concrete performance requirement?** Is there a specific latency threshold (e.g., queries must return within 200ms at p95)? Should results be paginated using the existing `PaginatedResults<T>` pattern? Is there a maximum page size? Should caching be applied (the project uses `tower-http` caching middleware)?

4. **What are the specific test scenarios required?** For example: search with matching results, search with no results, search with special characters, search with pagination, search with relevance ordering — which of these are in scope?

5. **Should the search endpoint integrate with the existing `modules/search/` module** (which already provides `GET /api/v2/search` via `SearchService` for full-text search across entities), or should this be an independent search capability scoped only to the package module (e.g., `GET /api/v2/package/search` or query parameters on `GET /api/v2/package`)?

I have stopped execution and will not proceed with branching, implementation planning, or code changes until these gaps are resolved. Please provide the missing information or update the task description in Jira, and I will re-run the skill.
