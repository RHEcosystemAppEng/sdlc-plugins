# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Checked the project's CLAUDE.md (`claude-md-mock.md`) for required sections:

1. **Repository Registry** — present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** — present. Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID: 10142, Git Pull Request custom field: customfield_10875, GitHub Issue custom field: customfield_10747.
3. **Code Intelligence** — present. Tool naming convention: `mcp__<serena-instance>__<tool>`. Configured instance: `serena_backend` (rust-analyzer).

All required Project Configuration sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, would prompt the user to choose between REST API fallback, skipping the operation, or retrying MCP. (Skipped for this eval — no external service calls.)

## Step 1 — Fetch and Parse Jira Task

Fetched TC-9202. Parsed the structured description:

| Section | Status | Content |
|---|---|---|
| Repository | Present | trustify-backend |
| Target Branch | Present | main |
| Description | **Incomplete** | "Add search capabilities to the package module so users can find packages more easily." — too vague to implement |
| Files to Modify | Present (minimal) | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present (minimal) | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **Missing** | No endpoint path, HTTP method, query parameters, request/response shapes defined |
| Implementation Notes | **Missing** | No patterns, code references, or reusable code identified |
| Acceptance Criteria | **Incomplete** | Criteria are vague and unmeasurable (see details below) |
| Test Requirements | **Incomplete** | Single vague line with no specific test cases (see details below) |
| Dependencies | Not present | (Optional — no blockers identified) |
| Target PR | Not present | (Optional — this is a new implementation, not a review fix) |
| Bookend Type | Not present | (Optional — this is a normal implementation task) |
| Review Context | Not present | (Optional) |

### Identified Gaps

**STOP — the task description is incomplete. The following gaps must be resolved before implementation can proceed:**

1. **API Changes section is missing entirely.** To implement a search endpoint, the following must be specified:
   - HTTP method and endpoint path (e.g., `GET /api/v2/package/search` or query parameter on `GET /api/v2/package`)
   - Query parameters (e.g., `q`, `name`, `license`, `page`, `per_page`)
   - Response shape (does it return `PaginatedResults<PackageSummary>` like the existing list endpoint?)
   - Whether this is a new endpoint or an extension of the existing list endpoint with filtering

2. **Implementation Notes section is missing entirely.** The following details are needed:
   - Which existing patterns to follow (e.g., follow `advisory/endpoints/` search pattern, or `modules/search/` global search pattern?)
   - Which query helpers from `common/src/db/query.rs` to use for filtering/pagination
   - Whether to use the existing `SearchService` from `modules/search/` or implement package-specific search logic in `PackageService`
   - Which database fields to search on (package name? version? license? pURL?)
   - Whether full-text search or simple LIKE/ILIKE filtering is expected

3. **Acceptance Criteria are vague and unmeasurable:**
   - "Users can search for packages" — search by what? Name? License? Version? pURL? All fields?
   - "Search results are relevant" — what defines relevance? Exact match? Substring? Full-text ranking?
   - "Performance is acceptable" — what is acceptable? Under 200ms? Under 1s? No specific SLA defined

4. **Test Requirements are insufficient:**
   - "Test that search works correctly" — no specific test cases defined. Need at minimum:
     - Test search with a matching query returns results
     - Test search with no matches returns empty results
     - Test search with pagination
     - Test search with invalid/empty query parameters
     - Test search response shape matches expected schema

5. **Description is too vague to derive implementation specifics.** "Add search capabilities" does not specify:
   - Search mechanism (database query filtering vs. full-text search index)
   - Which fields are searchable
   - Whether search supports boolean operators, wildcards, or exact match only
   - Whether results should be ranked by relevance or sorted by a default field

### Questions for the User

Before proceeding with implementation, please provide:

1. What is the endpoint path and HTTP method for the search? (e.g., `GET /api/v2/package/search?q=...` or adding a `q` parameter to the existing `GET /api/v2/package` list endpoint?)
2. Which package fields should be searchable? (name, version, license, pURL, description?)
3. What search mechanism should be used? (SQL ILIKE filtering via `common/src/db/query.rs` helpers, or integration with the `modules/search/` full-text search service?)
4. Should the response use `PaginatedResults<PackageSummary>` to match the existing list endpoint pattern?
5. What existing code patterns should be followed? (e.g., does `advisory/service/advisory.rs` have a `search` method that serves as a reference implementation?)
6. What specific test scenarios should be covered?
7. What are the measurable acceptance criteria? (e.g., "search by name returns matching packages within 500ms for datasets up to 100k packages")

**Execution stopped.** Will not proceed with branching, implementation planning, code changes, or any subsequent steps until the user provides the missing information.
