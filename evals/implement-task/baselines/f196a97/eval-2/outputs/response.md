# implement-task TC-9202 — Clarification Required

## Step 0 — Validate Project Configuration

Project Configuration in CLAUDE.md verified:
- Repository Registry: present, contains `trustify-backend` with Serena instance `serena_backend`
- Jira Configuration: present with Project key (TC), Cloud ID, Feature issue type ID
- Code Intelligence: present with tool naming convention (`mcp__<serena-instance>__<tool>`)

Configuration is complete. Proceeding to task validation.

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description for TC-9202 ("Add package search functionality"):

| Section | Status |
|---|---|
| Repository | Present: `trustify-backend` |
| Target Branch | Present: `main` |
| Description | Present but vague (see below) |
| Files to Modify | Present: 1 file listed |
| Files to Create | Present: 1 file listed |
| API Changes | **Missing entirely** |
| Implementation Notes | **Missing entirely** |
| Acceptance Criteria | Present but vague (see below) |
| Test Requirements | Present but vague (see below) |
| Dependencies | Not listed (acceptable if none) |

## Identified Gaps

The structured description is **incomplete**. The following issues must be resolved before implementation can proceed.

### 1. Missing: Implementation Notes

The task description contains no **Implementation Notes** section. This section is critical because it provides the patterns and code references to follow during implementation. Without it, I cannot determine:

- **Which search mechanism to use.** The repository has a dedicated `modules/search/` module with a `SearchService` that provides full-text search across entities. Should the package search endpoint delegate to `SearchService`, or should it implement search directly within `PackageService` using query builder helpers from `common/src/db/query.rs`?
- **Which query patterns to follow.** The existing `list.rs` endpoint in the package module presumably uses filtering/pagination from `common/src/db/query.rs`. Should the search endpoint extend that pattern with additional filter parameters, or should it use a different approach (e.g., SQL `LIKE`/`ILIKE`, full-text search with `tsvector`, or the `SearchService`)?
- **What fields are searchable.** Should search cover only the package name, or also fields like version, license, or associated SBOM data? The `PackageSummary` struct in `model/summary.rs` includes a `license` field — should that be searchable?
- **How to integrate with existing service layer.** Should a new `search` method be added to `PackageService` in `service/mod.rs`, or should the endpoint handler call existing service methods with filter parameters?

### 2. Missing: API Changes

The task description contains no **API Changes** section. This section is needed to define the search endpoint contract. Specifically:

- **What is the endpoint path?** Is it `GET /api/v2/package/search`, or should it be a query parameter on the existing `GET /api/v2/package` list endpoint (e.g., `GET /api/v2/package?q=openssl`)?
- **What are the request parameters?** What query parameters does the search endpoint accept (e.g., `q` for search term, `field` to limit which fields are searched, pagination parameters)?
- **What is the response format?** Should it return `PaginatedResults<PackageSummary>` (consistent with the list endpoint), or a different response type with search-specific metadata (e.g., relevance scores)?

### 3. Vague: Acceptance Criteria

The acceptance criteria are too vague to verify:

- **"Users can search for packages"** — By what mechanism? What constitutes a valid search query? What fields should match? Does this mean substring matching, prefix matching, or full-text search?
- **"Search results are relevant"** — How is relevance defined? Is there a ranking algorithm expected? Should results be ordered by relevance score, alphabetically, or by some other criterion?
- **"Performance is acceptable"** — What does "acceptable" mean? Is there a target latency (e.g., < 200ms for p95)? Is there a maximum result set size? Should pagination be required?

Each criterion needs to be specific and objectively verifiable.

### 4. Vague: Test Requirements

The test requirements contain only a single item: "Test that search works correctly." This is insufficient to guide test implementation. Specific test cases are needed, such as:

- What search inputs should be tested (exact match, partial match, no match, empty query, special characters)?
- Should tests verify pagination of search results?
- Should tests cover error cases (e.g., invalid query parameters, database errors)?
- Should integration tests be added to `tests/api/` following the existing pattern (e.g., `tests/api/package_search.rs`)?
- What assertions should the tests make on the response shape (status code, body structure, result count, field values)?

## Decision: Stop Execution

Per the skill rules: "If the structured description is incomplete, ask the user for clarification and stop execution. Do not draft an implementation plan."

The task description is missing the **Implementation Notes** and **API Changes** sections entirely, and the **Acceptance Criteria** and **Test Requirements** are too vague to implement against. I am stopping execution and will not proceed with branching, code inspection, or implementation until these gaps are addressed.

**Please provide the following before I can proceed:**

1. **Implementation Notes** — Which search mechanism to use (SearchService, query builder filters, or SQL-level search), which fields should be searchable, and what code patterns to follow (with specific file and symbol references).
2. **API Changes** — The endpoint path, HTTP method, query parameters, and response format for the search functionality.
3. **Refined Acceptance Criteria** — Specific, verifiable criteria replacing the current vague ones (e.g., "Searching for a package name substring returns all packages whose name contains that substring, with results paginated using `PaginatedResults`").
4. **Refined Test Requirements** — Specific test cases to implement, including search scenarios (exact match, partial match, no results), error cases, and response shape assertions.
