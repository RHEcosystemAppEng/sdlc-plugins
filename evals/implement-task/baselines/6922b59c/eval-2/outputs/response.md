# implement-task: TC-9202

## Step 0 -- Validate Project Configuration

Verified the project's CLAUDE.md contains the required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, and Feature issue type ID.
3. **Code Intelligence** -- present, documents `mcp__serena_backend__<tool>` naming convention and the `serena_backend` instance with `rust-analyzer`.

Project Configuration is valid. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Fetched issue TC-9202. Parsing the structured description against the expected template:

| Section | Status | Detail |
|---------|--------|--------|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." -- does not specify what fields are searchable, what search mechanism to use (SQL LIKE, full-text search, integration with the existing `modules/search/` service), or what the expected behavior is. |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **Missing** | No information about the endpoint path, HTTP method, query parameters, request body format, or response shape. |
| Implementation Notes | **Missing** | No patterns, code references, or architectural guidance provided. This section is critical for understanding how to implement the search (e.g., should it follow the existing `advisory/service/advisory.rs` `AdvisoryService::search` pattern? Should it use `common/src/db/query.rs` helpers? Should it integrate with the `modules/search/` full-text search service?). |
| Acceptance Criteria | Present but **vague and non-actionable** | See details below. |
| Test Requirements | Present but **vague and non-actionable** | See details below. |
| Dependencies | **Missing** | No information about prerequisite tasks. |

### Acceptance Criteria gaps

The acceptance criteria are not actionable:

1. **"Users can search for packages"** -- Search by what fields? Name? Version? License? Package URL (purl)? Some combination? What is the search input format (free-text query string, structured filters, both)?
2. **"Search results are relevant"** -- No definition of relevance. Is this full-text ranking, exact match, prefix match, fuzzy match? What ordering is expected (relevance score, alphabetical, most recent)?
3. **"Performance is acceptable"** -- No measurable threshold. What response time is acceptable? Under what data volume? Is there an existing SLA or benchmark to target?

### Test Requirements gaps

The test requirements provide no actionable guidance:

1. **"Test that search works correctly"** -- No specific test cases defined. Missing:
   - What constitutes a successful search result (exact match, partial match, no results)?
   - Edge cases (empty query, special characters, very long queries)
   - Error cases (invalid parameters, database errors)
   - Pagination behavior for search results
   - Whether integration tests should use the existing `tests/api/` pattern with a real PostgreSQL test database

### Files to Modify/Create concerns

The listed files cover only the endpoint layer (`endpoints/`), but the established module pattern in this codebase is `model/ + service/ + endpoints/`. The search functionality likely requires:

- A service-layer method in `modules/fundamental/src/package/service/mod.rs` (or a new service file) to implement the search query logic
- Possibly a new model struct for search-specific request/response types
- Route registration in `server/src/main.rs` if the search is mounted separately
- Integration with either `common/src/db/query.rs` (for SQL-based filtering) or `modules/search/` (for full-text search)

The file list may be incomplete, but without Implementation Notes this cannot be confirmed.

## Execution stopped -- clarification required

The task description is incomplete. The following gaps must be resolved before implementation can proceed:

1. **Implementation Notes (missing)**: What patterns should the search endpoint follow? Specifically:
   - Should it use the existing `modules/search/` full-text search service, or implement SQL-based filtering via `common/src/db/query.rs`?
   - Which sibling endpoint should serve as the reference implementation (e.g., `advisory/endpoints/` which has search, or `sbom/endpoints/list.rs`)?
   - What shared utilities should be reused (e.g., `PaginatedResults<T>`, query builder helpers)?

2. **API Changes (missing)**: What is the endpoint specification?
   - Endpoint path (e.g., `GET /api/v2/package/search?q=...` or query parameters on the existing `GET /api/v2/package` list endpoint?)
   - Query parameters (search term, filters, pagination parameters)
   - Response format (should it return `PaginatedResults<PackageSummary>` like the list endpoint?)

3. **Acceptance Criteria (too vague)**: Need measurable, verifiable criteria:
   - Which package fields are searchable?
   - What matching behavior is expected (exact, prefix, contains, full-text)?
   - What is the expected result ordering?
   - What is the performance target (e.g., response time under N ms for datasets of size M)?

4. **Test Requirements (too vague)**: Need specific test cases:
   - What are the happy-path scenarios to test?
   - What edge cases should be covered (empty query, no results, special characters)?
   - What error cases should be tested?
   - Should tests follow the existing `tests/api/` integration test pattern?

5. **Files to Modify/Create (potentially incomplete)**: Does this task require changes to the service layer (`package/service/mod.rs`) or model layer? The current file list only covers endpoints.

**I will not proceed with branching, implementation planning, or code changes until these gaps are addressed.** Please provide the missing information or re-run plan-feature to regenerate the task with a complete description.
