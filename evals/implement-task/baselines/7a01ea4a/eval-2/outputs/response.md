# implement-task TC-9202 -- Execution Halted: Incomplete Task Description

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md verified:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: present with Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present with tool naming convention (`mcp__<serena-instance>__<tool>`) and `serena_backend` instance configured for rust-analyzer

Configuration is complete. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202. Expected sections and their status:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily" -- does not specify search algorithm, matching strategy, or scope |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | Task adds a search endpoint but does not specify the route path, HTTP method, query parameters, or response shape |
| Implementation Notes | **MISSING** | No patterns, code references, or architectural guidance provided |
| Acceptance Criteria | Present but vague | See analysis below |
| Test Requirements | Present but vague | See analysis below |

### Missing: Implementation Notes

The **Implementation Notes** section is entirely absent. This section is critical for implementation because it tells the implementer which existing patterns to follow, which shared utilities to reuse, and which code references to consult. Without it, the implementer would have to guess at:

- Whether to use the existing `modules/search/` module's `SearchService` or build a package-specific search
- Which query builder helpers from `common/src/db/query.rs` to use for filtering and pagination
- How to structure the search handler relative to the existing `list.rs` endpoint in the same module
- Whether to use PostgreSQL full-text search, ILIKE queries, or another mechanism

### Vague Acceptance Criteria

The Acceptance Criteria contain two items that are insufficiently specific for implementation:

1. **"Search results are relevant"** -- This is not actionable. "Relevant" is undefined. Does it mean exact match on package name? Substring match? Full-text search with ranking? Does it include searching across package metadata fields (version, license, description) or only the package name? Without a definition of relevance, there is no way to implement or verify this criterion.

2. **"Performance is acceptable"** -- This is not measurable. There is no performance threshold defined (e.g., response time under 200ms for 10,000 packages, or query execution under 50ms). Without a concrete target, this criterion cannot be tested or verified.

### Vague Test Requirements

The single test requirement -- **"Test that search works correctly"** -- does not define what "correctly" means. It does not specify:

- Which search inputs to test (empty query, single term, multiple terms, special characters)
- What constitutes a correct result set (exact matches only? partial matches? ranked by what?)
- Whether to test edge cases (no results, very long queries, SQL injection)
- Whether to test pagination of search results
- What response shape to assert on (status code, body structure, field presence)

This is insufficient to write meaningful tests.

### Missing: API Changes

The task creates a search endpoint but provides no **API Changes** section. The implementer does not know:

- The endpoint path (e.g., `GET /api/v2/package/search?q=...` vs. adding a query parameter to the existing `GET /api/v2/package` list endpoint)
- The HTTP method
- The query parameter names and types
- The response format (reuse `PaginatedResults<PackageSummary>` or a different shape?)

---

## Execution Stopped -- Clarification Required

Per the implement-task skill rules: "If the structured description is incomplete, ask the user for clarification and **stop execution immediately** -- do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

The task description for TC-9202 has significant gaps that prevent implementation. I need the following clarifications before proceeding:

### Questions for the user

1. **Which fields should be searchable?** The package entity (in `entity/src/package.rs`) likely has fields such as name, version, namespace/ecosystem, and related license information (via `package_license.rs`). Which of these fields should the search query match against? Should it search only the package name, or also include version, license, and other metadata?

2. **What does "relevant" mean for search result ranking?** Should results be ranked by exact match first, then prefix match, then substring match? Should the implementation use PostgreSQL full-text search (`tsvector`/`tsquery`) with built-in ranking, or simple `ILIKE` pattern matching? Is there a minimum relevance threshold below which results should be excluded?

3. **What is the performance threshold?** What response time is considered "acceptable"? For example: under 200ms for a dataset of N packages? Is there a maximum result set size? Should there be a default page size for search results?

4. **What should the API contract look like?** Should this be a new `GET /api/v2/package/search` endpoint with a `q` query parameter, or should search be added as a filter on the existing `GET /api/v2/package` list endpoint? Should the response use the existing `PaginatedResults<PackageSummary>` wrapper?

5. **What test scenarios are required?** At minimum, should tests cover: (a) search returning matching results, (b) search returning no results for a non-matching query, (c) search with pagination, (d) search with empty/missing query parameter? Are there specific edge cases that should be validated (special characters, very long queries, case sensitivity)?

6. **Should the implementation reuse the existing search module?** The repository has a `modules/search/` module with a `SearchService` that provides full-text search across entities. Should the package search integrate with this existing service, or should it be a standalone query within the package module?

Please provide the missing Implementation Notes section and clarify the acceptance criteria and test requirements so I can proceed with implementation.
