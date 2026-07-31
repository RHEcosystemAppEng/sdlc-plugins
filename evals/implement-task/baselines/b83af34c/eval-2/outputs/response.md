## Step 0 -- Validate Project Configuration

Verified the project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`.

Project configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Fetched TC-9202. Parsing the structured description against the required template sections:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No endpoint path, HTTP method, request parameters, or response shape defined |
| Implementation Notes | **MISSING** | No patterns, code references, reusable utilities, or architectural guidance provided |
| Acceptance Criteria | Present but **vague** | All three criteria are unmeasurable (see below) |
| Test Requirements | Present but **vague** | Single item with no specific test cases defined (see below) |
| Dependencies | Not present | Optional; no issue |

### Identified Gaps

**1. Missing: API Changes section**

The task creates a search endpoint but does not specify:
- What is the endpoint path? (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`?)
- What HTTP method is used?
- What request parameters does the search accept? (query string? request body? filtering fields?)
- What is the response shape? (Does it return `PaginatedResults<PackageSummary>`? A different shape?)

**2. Missing: Implementation Notes section**

The task provides no guidance on how to implement the search functionality:
- Should this use the existing `SearchService` from `modules/search/` (full-text search across entities), or implement a module-specific search within the package service?
- What search strategy should be used? (SQL `LIKE`/`ILIKE`? PostgreSQL full-text search with `tsvector`/`tsquery`? The shared query builder helpers in `common/src/db/query.rs`?)
- Should the search endpoint follow the same pattern as `modules/fundamental/src/sbom/endpoints/list.rs` or the `modules/search/src/endpoints/mod.rs`?
- Are there existing query builder utilities in `common/src/db/query.rs` that should be reused for filtering and pagination?
- What fields on `PackageSummary` should be searchable? (name? version? purl? license?)
- How should the new `search.rs` endpoint be registered in the route configuration in `endpoints/mod.rs`?

**3. Vague: Acceptance Criteria**

All three acceptance criteria are unmeasurable and untestable:

- "Users can search for packages" -- Search by what field(s)? What input format? What constitutes a match (exact, prefix, substring, fuzzy)?
- "Search results are relevant" -- What defines relevance? Is there a ranking algorithm expected? How is relevance measured?
- "Performance is acceptable" -- What is the performance target? (e.g., < 200ms for 10k packages? Must use database indexes?) Without a concrete threshold this criterion cannot be verified.

**4. Vague: Test Requirements**

The single test requirement ("Test that search works correctly") does not specify:
- What test cases are needed? (e.g., search by name returns matching packages, search with no results returns empty list, search with special characters is handled)
- What assertions should the tests make? (status codes, response body structure, specific field values)
- Should tests cover edge cases? (empty query, very long query, SQL injection prevention)
- Should tests cover pagination of search results?
- Where should the test file be created? (presumably `tests/api/package.rs` or a new file, following the pattern of `tests/api/sbom.rs` and `tests/api/advisory.rs`)

---

**Execution stopped.** The task description is incomplete. The following information is needed before implementation can proceed:

1. **API Changes**: What is the exact endpoint path, HTTP method, request parameters (with types), and response shape for the package search?
2. **Implementation Notes**: What search strategy should be used (existing `SearchService`, PostgreSQL full-text search, SQL `LIKE`, or query builder filters)? What existing code patterns and utilities should be followed or reused?
3. **Acceptance Criteria**: Please replace the three vague criteria with measurable, testable criteria. For example: "Search by package name using substring match returns matching packages in a `PaginatedResults<PackageSummary>` response" and "Search endpoint responds within 500ms for datasets up to 50k packages."
4. **Test Requirements**: Please specify concrete test cases with expected inputs and outputs. For example: "Test that `GET /api/v2/package/search?q=openssl` returns packages whose name contains 'openssl'" and "Test that an empty query parameter returns a 400 error."

Please provide the missing information so I can proceed with implementation.
