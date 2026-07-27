# implement-task: TC-9202 — Add package search functionality

## Step 0 -- Validate Project Configuration

Reading the project's CLAUDE.md (claude-md-mock.md):

1. **Repository Registry** -- Present. Contains one entry: `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- Present. Contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** -- Present. Tool naming convention documented (`mcp__<serena-instance>__<tool>`). One instance configured: `serena_backend` for `trustify-backend` with `rust-analyzer`.

All required sections are present and complete. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all Jira operations. If MCP fails, would prompt the user with the three options (REST API fallback, skip, retry) as specified.

## Step 1 -- Fetch and Parse Jira Task

Fetching TC-9202. Parsing the structured description against the required template sections:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` -- add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` -- search endpoint handler |
| API Changes | **MISSING** | No endpoint specification |
| Implementation Notes | **MISSING** | No patterns, code references, or reuse guidance |
| Acceptance Criteria | Present but vague | Non-specific, non-testable criteria |
| Test Requirements | Present but vague | Single line with no specifics |
| Target PR | Absent (optional) | N/A |
| Review Context | Absent (optional) | N/A |
| Bookend Type | Absent (optional) | N/A |
| Dependencies | Absent (optional) | N/A |

### Critical gaps identified

**STOP EXECUTION.** The task description is incomplete. The following gaps must be resolved before implementation can proceed:

### 1. API Changes section is missing (required for an endpoint task)

The task creates a new search endpoint but does not specify:
- The HTTP method and route path (e.g., `GET /api/v2/package/search?q=...` or `GET /api/v2/package?q=...` as a query parameter on the existing list endpoint)
- Query parameters (search term, filters, pagination)
- Response shape (does it return `PaginatedResults<PackageSummary>` like the existing list endpoint?)
- Status codes for success and error cases

### 2. Implementation Notes section is missing (required)

The repository has significant existing infrastructure that the task description should reference:

- **`modules/search/`** -- A dedicated search module already exists with `SearchService` providing full-text search across entities. Should the package search use this service, or implement its own query-based search?
- **`common/src/db/query.rs`** -- Shared query builder helpers for filtering, pagination, and sorting. Should the search endpoint use these?
- **`common/src/model/paginated.rs`** -- `PaginatedResults<T>` response wrapper used by all list endpoints. Should search results use this?
- **`modules/fundamental/src/package/service/mod.rs`** -- `PackageService` currently has `fetch` and `list` methods. Should a `search` method be added here?
- **`modules/fundamental/src/advisory/service/advisory.rs`** -- `AdvisoryService` already has a `search` method that could serve as a pattern reference.
- **`entity/src/package.rs`** -- Package entity (SeaORM). Which fields should be searchable (name? version? license via `package_license.rs`)?

Without these references, the implementer cannot determine the intended approach.

### 3. Acceptance Criteria are too vague to verify

The current criteria are not testable:
- "Users can search for packages" -- Search by what? Name? License? Version? PURL?
- "Search results are relevant" -- What defines relevance? Exact match? Substring? Full-text ranking?
- "Performance is acceptable" -- What is the threshold? Response time target? Result set size limit?

These need to be rewritten as specific, verifiable conditions, for example:
- "Search by package name substring returns matching packages"
- "Search results are paginated using PaginatedResults"
- "Empty search term returns a 400 Bad Request"

### 4. Test Requirements are too vague

"Test that search works correctly" does not specify:
- Which test file to create or modify (the repo has `tests/api/` for integration tests -- should a `tests/api/package.rs` be created?)
- What test scenarios to cover (successful search, empty results, invalid input, pagination)
- What assertion patterns to follow (the repo uses `assert_eq!(resp.status(), StatusCode::OK)` pattern per conventions)

---

**Action required from user:** Please provide the missing information for the sections listed above. Specifically:

1. What is the API endpoint specification? (method, path, query parameters, response shape)
2. Should the search use the existing `SearchService` from `modules/search/`, or add a search/filter method to `PackageService`?
3. Which package fields should be searchable?
4. What are the specific, testable acceptance criteria?
5. What specific test scenarios should be covered, and in which test file?

I will not proceed with branching, code analysis, implementation planning, or any code changes until these gaps are resolved.
