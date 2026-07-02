# implement-task TC-9202 -- Execution Halted: Incomplete Task Description

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains the required sections:

- **Repository Registry** -- present, maps `trustify-backend` to Serena instance `serena_backend`
- **Jira Configuration** -- present with Project key (TC), Cloud ID, and Feature issue type ID
- **Code Intelligence** -- present, with tool naming convention and configured instance for `serena_backend` using rust-analyzer

Project Configuration validation passed. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202 ("Add package search functionality"):

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | Brief, but present |
| Files to Modify | Present | 1 file listed |
| Files to Create | Present | 1 file listed |
| API Changes | **MISSING** | No API Changes section defined |
| Implementation Notes | **MISSING** | No Implementation Notes section at all |
| Acceptance Criteria | Present but **VAGUE** | See details below |
| Test Requirements | Present but **VAGUE** | See details below |

### Missing Sections

**Implementation Notes** -- This section is entirely absent from the task description. The Implementation Notes section is critical because it provides the patterns and code references the implementer must follow. Without it, there is no guidance on:

- Which existing code patterns to follow (e.g., how the existing `list.rs` endpoint in `modules/fundamental/src/package/endpoints/` is structured)
- Which shared utilities to reuse (e.g., the query builder helpers in `common/src/db/query.rs`, the `PaginatedResults<T>` wrapper in `common/src/model/paginated.rs`)
- How to integrate with the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`
- Whether to use the existing `SearchService` in `modules/search/` or build package-specific search logic
- What database query approach to use (e.g., PostgreSQL full-text search with `tsvector`/`tsquery`, SQL `LIKE`/`ILIKE`, or SeaORM filtering)

**API Changes** -- This section is also missing. For a task that adds a search endpoint, the API contract should be explicitly defined: the HTTP method, path, query parameters, request/response shape, and status codes.

### Vague Acceptance Criteria

The Acceptance Criteria section contains three items, but two are insufficiently specific to verify:

1. "Users can search for packages" -- Acceptable as a high-level criterion, but lacks detail on which fields are searchable and what the search input looks like (query string parameter? request body? path parameter?).

2. **"Search results are relevant"** -- This is not a verifiable criterion. "Relevant" is undefined. It does not specify:
   - Which fields should be searched (package name only? version? description? license? pURL?)
   - What ranking or ordering algorithm should be applied to results
   - Whether partial matches, prefix matches, or fuzzy matches are expected
   - Whether results should be scored and sorted by relevance, or simply filtered

3. **"Performance is acceptable"** -- This is not a verifiable criterion. "Acceptable" is undefined. It does not specify:
   - A maximum response time threshold (e.g., < 200ms for 95th percentile)
   - The expected dataset size (how many packages should the search scale to?)
   - Whether pagination is required and what the default/max page size should be
   - Whether database indexing requirements should be addressed

### Vague Test Requirements

The Test Requirements section contains a single item:

- **"Test that search works correctly"** -- This does not define what "correctly" means. It provides no guidance on:
  - What test cases to write (e.g., exact match, partial match, no results, empty query)
  - What assertions to make on the response (status codes, response shape, field values)
  - Whether to test error cases (e.g., invalid query parameters, missing required fields)
  - Whether to test pagination behavior
  - Whether to test performance characteristics
  - What the expected response format is (so assertions can be written against it)

## Execution Halted -- Clarification Required

Per the implement-task skill rules: "If the structured description is incomplete, ask the user for clarification and stop execution. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."

The task description is incomplete. I am stopping execution and will not create a branch, draft an implementation plan, or proceed with any subsequent steps.

### Clarifying Questions

Before I can proceed with implementing TC-9202, I need the following information:

1. **Which fields should be searchable?** The `PackageSummary` struct (in `modules/fundamental/src/package/model/summary.rs`) likely contains fields like name, version, and license. Which of these fields should the search query match against? Should the search cover package name only, or also version strings, license identifiers, pURLs, or other metadata? Should the search support partial/prefix matching, or only exact matches?

2. **What does "relevant" mean for search result ranking?** Should results be returned in a specific order (e.g., exact name matches first, then partial matches)? Is a simple SQL `ILIKE` filter sufficient, or do you need full-text search with relevance scoring (e.g., PostgreSQL `ts_rank`)? Should the existing `SearchService` in `modules/search/` be reused, or should this be a package-specific query?

3. **What is the performance threshold?** What maximum response time is acceptable (e.g., < 200ms p95, < 500ms p99)? How many packages should the search handle (thousands, millions)? Does the search need a database index, and if so, which type (B-tree, GIN for full-text, trigram)?

4. **What is the API contract for the search endpoint?** What HTTP method and path should be used (e.g., `GET /api/v2/package/search?q=...` or a query parameter on the existing `GET /api/v2/package` list endpoint)? Should the response use `PaginatedResults<PackageSummary>` like the existing list endpoint? What query parameters are needed (e.g., `q`, `limit`, `offset`, `sort`)?

5. **What specific test cases should be covered?** For example: search with an exact package name match, search with a partial name, search with no results, search with an empty query string, search with pagination parameters, search returning results ordered by relevance. What edge cases matter?

6. **What Implementation Notes / patterns should be followed?** Should the search handler follow the same structure as the existing `list.rs` in the package endpoints module? Should it use the shared query helpers from `common/src/db/query.rs`? Should it integrate with the `PackageService` or directly query the database?

Please provide the missing Implementation Notes, specific Acceptance Criteria, and detailed Test Requirements so I can proceed with the implementation.
