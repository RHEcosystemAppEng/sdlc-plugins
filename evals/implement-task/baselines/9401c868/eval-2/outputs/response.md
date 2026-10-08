# implement-task: TC-9202

## Step 0 -- Validate Project Configuration

Reading the project's CLAUDE.md (claude-md-mock.md), I verify that all required sections exist under `# Project Configuration`:

1. **Repository Registry** -- present. Contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** -- present. Contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** -- present. Tool naming convention documented: `mcp__<serena-instance>__<tool>`. Serena instance `serena_backend` configured for `trustify-backend` with `rust-analyzer`.

Project Configuration validation: **PASS**. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all JIRA operations. (Skipped per eval instructions -- no external service calls.)

## Step 1 -- Fetch and Parse Jira Task

Fetched TC-9202. Parsing the structured description for required sections:

| Section | Status | Content |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Target Branch** | Present | `main` |
| **Description** | Present but **vague** | "Add search capabilities to the package module so users can find packages more easily." |
| **Files to Modify** | Present | `modules/fundamental/src/package/endpoints/mod.rs` -- add search route |
| **Files to Create** | Present | `modules/fundamental/src/package/endpoints/search.rs` -- search endpoint handler |
| **API Changes** | **MISSING** | No section present |
| **Implementation Notes** | **MISSING** | No section present |
| **Acceptance Criteria** | Present but **vague** | All criteria are non-specific and unmeasurable |
| **Test Requirements** | Present but **vague** | Single item with no specific test scenarios |
| **Dependencies** | Not mentioned | No section present |

### Identified Gaps

The task description is **incomplete**. The following gaps prevent implementation from proceeding:

**1. Missing: API Changes section**

The task asks to add a search endpoint but does not specify:
- The HTTP method (GET, POST)
- The endpoint path (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`)
- Request parameters (query string parameters, request body schema)
- Response format (should it return `PaginatedResults<PackageSummary>`? a different shape?)

This information is critical for implementing the endpoint handler in `search.rs` and registering the route in `mod.rs`.

**2. Missing: Implementation Notes section**

The task does not reference any existing code patterns to follow. The repository has analogous implementations that could serve as references:
- `modules/fundamental/src/advisory/service/advisory.rs` contains `AdvisoryService` with a search method
- `modules/search/` contains a `SearchService` for full-text search across entities
- `common/src/db/query.rs` provides shared query builder helpers for filtering, pagination, and sorting

Without Implementation Notes, it is unclear:
- Whether to use the existing `SearchService` from `modules/search/` or implement search directly in `PackageService`
- Which query helpers from `common/src/db/query.rs` to use
- Whether to add a method to the existing `PackageService` or create a new service
- What search mechanism to use (SQL `LIKE`/`ILIKE`, full-text search with `tsvector`, or the existing `SearchService` integration)

**3. Vague: Description section**

"Add search capabilities to the package module so users can find packages more easily" does not specify:
- What fields are searchable (package name? version? license? description? all of them?)
- What kind of search (exact match, substring, full-text, fuzzy)
- Whether search should support pagination, sorting, or filtering
- Whether this integrates with the existing `modules/search/` infrastructure or is a standalone endpoint

**4. Vague: Acceptance Criteria**

The three acceptance criteria are not specific or measurable:
- "Users can search for packages" -- does not define the search interface, supported query types, or expected behavior
- "Search results are relevant" -- does not define relevance (ordering, scoring, matching algorithm)
- "Performance is acceptable" -- does not define a performance target (response time threshold, maximum result set size, pagination requirements)

These criteria cannot be objectively verified as written.

**5. Vague: Test Requirements**

"Test that search works correctly" is a single generic item with no specific test scenarios. Missing:
- Specific search queries and expected results
- Edge cases (empty query, no results, special characters)
- Whether integration tests should use the pattern in `tests/api/search.rs` (real PostgreSQL test database)
- Pagination and sorting test cases
- Performance/load test requirements (if any)

**6. Missing: Dependencies section**

No Dependencies section is present. While this may mean there are no dependencies, the linked issue "is incorporated by TC-9001" suggests this is part of a larger feature. It should be clarified whether any prerequisite tasks must be completed first (e.g., database schema changes, service layer additions).

---

## STOP -- Clarification Required

Per the implement-task skill (Step 1) and constraint 1.6, execution stops here. The structured description is incomplete -- it is missing required sections (API Changes, Implementation Notes) and contains vague, non-measurable criteria in multiple sections.

**I need the following information before proceeding:**

1. **API Changes**: What is the endpoint path, HTTP method, request parameters (query params or body), and response type? For example:
   - `GET /api/v2/package/search?q=<query>&offset=0&limit=25`
   - Returns `PaginatedResults<PackageSummary>`

2. **Implementation Notes**: Which existing patterns should be followed? Specifically:
   - Should search use the existing `SearchService` from `modules/search/`, or implement a new query in `PackageService`?
   - Which sibling implementation to follow as a reference (e.g., `advisory/service/advisory.rs` search, or `search/endpoints/mod.rs`)?
   - What search mechanism (SQL LIKE, full-text search, etc.)?

3. **Searchable fields**: Which fields of `PackageSummary` (or the underlying `package` entity) should be searchable?

4. **Acceptance Criteria**: Please provide specific, measurable criteria. For example:
   - "Search by package name returns matching packages using case-insensitive substring match"
   - "Results are paginated using PaginatedResults with default page size of 25"
   - "Search endpoint responds within 200ms for datasets under 100k packages"

5. **Test Requirements**: Please provide specific test scenarios. For example:
   - "Search with a known package name returns that package in results"
   - "Search with no matches returns an empty PaginatedResults"
   - "Search with empty query returns all packages (paginated)"

6. **Dependencies**: Are there any prerequisite tasks from TC-9001 that must be completed before this task?

Please provide the missing information so I can proceed with implementation.
