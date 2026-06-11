# TC-9202 — Task Description Validation

## Step 0 — Validate Project Configuration

The project's CLAUDE.md contains the required sections:

- **Repository Registry** — present, with `trustify-backend` mapped to Serena instance `serena_backend`
- **Jira Configuration** — present, with Project key (`TC`), Cloud ID, and Feature issue type ID
- **Code Intelligence** — present, with tool naming convention and `serena_backend` instance configured for rust-analyzer

Project Configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description for TC-9202 against the required template sections:

| Section | Status | Detail |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No API Changes section — the endpoint path, HTTP method, query parameters, request/response shapes are unspecified |
| Implementation Notes | **MISSING** | No Implementation Notes section — there are no patterns, code references, or architectural guidance for implementation |
| Acceptance Criteria | Present but **VAGUE** | See details below |
| Test Requirements | Present but **VAGUE** | See details below |

### Missing: Implementation Notes

The **Implementation Notes** section is entirely absent. This section is critical because it provides:

- Which existing patterns to follow (e.g., how `advisory/endpoints/` implements search, or how the `modules/search/` module works)
- Code references to reuse (e.g., the shared query builder in `common/src/db/query.rs`, the `PaginatedResults` wrapper in `common/src/model/paginated.rs`)
- Specific guidance on whether to use PostgreSQL full-text search, ILIKE queries, or the existing `SearchService` in `modules/search/`
- How the search endpoint should integrate with the existing `PackageService`

Without Implementation Notes, there is no basis for making architectural decisions about the search implementation.

### Missing: API Changes

The **API Changes** section is absent. There is no specification of:

- The endpoint path (e.g., `GET /api/v2/package/search` vs. a query parameter on `GET /api/v2/package`)
- HTTP method
- Query parameters (search term, filters, pagination)
- Response shape (should it return `PaginatedResults<PackageSummary>` or a different type?)

### Vague: Acceptance Criteria

The Acceptance Criteria are too vague to implement or verify:

1. **"Users can search for packages"** — Which fields should be searchable? Package name only? Name and version? Name, version, and license? pURL? Namespace? This criterion does not define what "search" means in concrete terms.

2. **"Search results are relevant"** — What constitutes "relevant"? Is there a relevance ranking algorithm to implement? Should exact matches rank higher than partial matches? Is fuzzy matching required? Without a definition of relevance, this criterion cannot be implemented or verified.

3. **"Performance is acceptable"** — What is the performance threshold? Is there a target response time (e.g., < 200ms for 95th percentile)? What dataset size should it perform against (100 packages? 100,000?)? Without quantifiable metrics, this criterion is untestable.

### Vague: Test Requirements

The Test Requirements consist of a single item:

- **"Test that search works correctly"** — This does not define what "correctly" means. Effective test requirements should specify:
  - What inputs to test with (exact match, partial match, no match, empty query, special characters)
  - What response properties to assert (status code, result count, result ordering, field values)
  - What edge cases to cover (empty database, very long search terms, SQL injection attempts)
  - Whether integration tests or unit tests are expected (the project uses integration tests against PostgreSQL per its conventions)

## Execution Stopped — Clarification Required

Per the skill's rules: *"If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately — do not proceed with any subsequent steps."*

The task description has significant gaps that prevent implementation. I need clarification on the following before proceeding:

### Clarifying Questions

1. **Which package fields should be searchable?** Should the search operate on package name only, or should it also cover version, license, pURL, namespace, or other fields from the `PackageSummary` struct? Should it support multi-field search (e.g., searching across name and license simultaneously)?

2. **What does "relevant" mean for search result ranking?** Should results be ranked by relevance? If so, what ranking strategy should be used — exact match first, then prefix match, then substring match? Should PostgreSQL full-text search (`tsvector`/`tsquery`) be used, or simple `ILIKE` pattern matching? Should the existing `SearchService` in `modules/search/` be leveraged, or should this be a standalone implementation within the package module?

3. **What is the performance threshold?** What response time is considered "acceptable"? Is there a target latency (e.g., p95 < 500ms)? What is the expected dataset size the search must perform well against? Are there indexing requirements?

4. **What is the API contract?** What should the endpoint path be? What query parameters should it accept (e.g., `q` for search term, `limit`/`offset` for pagination, filter parameters)? Should it return `PaginatedResults<PackageSummary>` consistent with the existing list endpoint?

5. **What specific test scenarios are required?** What constitutes "works correctly" — should tests cover exact match, partial match, case-insensitive match, no-results, pagination of search results, special character handling? Should the tests follow the existing integration test pattern in `tests/api/`?

6. **What patterns and code references should the implementation follow?** The `advisory` module has a `search` method in `AdvisoryService` and the `modules/search/` module provides a cross-entity `SearchService`. Should the package search follow the advisory module's pattern, integrate with the global search service, or take a different approach?

Please provide the missing Implementation Notes, more specific Acceptance Criteria, and detailed Test Requirements so I can proceed with implementation.
