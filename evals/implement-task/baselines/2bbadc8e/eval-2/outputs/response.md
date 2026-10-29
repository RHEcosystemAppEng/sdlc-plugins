# implement-task: TC-9202 — Processing Result

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** — present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** — present. Contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — present. Tool naming convention documented; `serena_backend` instance configured with `rust-analyzer`.

Result: **PASS** — all required configuration sections are present and complete.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all JIRA operations. (Simulated — no actual JIRA calls made.)

## Step 1 — Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Below is the result of parsing each expected section:

| Section | Status | Content |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Target Branch** | Present | `main` |
| **Description** | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| **Files to Modify** | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| **Files to Create** | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| **API Changes** | **MISSING** | Not present in the task description |
| **Implementation Notes** | **MISSING** | Not present in the task description |
| **Acceptance Criteria** | Present but **insufficiently specified** | See details below |
| **Test Requirements** | Present but **insufficiently specified** | See details below |
| **Target PR** | Absent (optional) | N/A |
| **Bookend Type** | Absent (optional) | N/A |
| **Dependencies** | Absent (optional) | N/A |

### Gaps Identified

#### 1. MISSING: API Changes

The task creates a new search endpoint but does not specify:
- The HTTP method and route path (e.g., `GET /api/v2/package/search?q=...` vs. query parameters on the existing list endpoint)
- Request parameters (query string? request body? what fields are searchable?)
- Response schema (does it return `PaginatedResults<PackageSummary>`? a different shape?)
- Any OpenAPI spec updates required

#### 2. MISSING: Implementation Notes

This is a critical gap. The Implementation Notes section should provide:
- Which existing patterns to follow (e.g., reference the advisory search implementation in `modules/fundamental/src/advisory/service/advisory.rs` which already has search functionality)
- Whether to use the existing `SearchService` from `modules/search/` or implement search directly in the package service
- Which query helpers from `common/src/db/query.rs` to use for filtering/pagination
- How to integrate with the route registration pattern in `endpoints/mod.rs`
- Whether full-text search (PostgreSQL `tsvector`/`tsquery`) or simple `LIKE`/`ILIKE` filtering is expected
- What fields on `PackageSummary` should be searchable (name? version? license? purl?)

#### 3. VAGUE: Acceptance Criteria

The current acceptance criteria are not actionable:

- **"Users can search for packages"** — Does not specify: search by what fields? What query syntax (simple text, wildcards, exact match)? What search parameters are supported? Is pagination required?
- **"Search results are relevant"** — Does not define relevance. Is there ranking? Is it ordered by match score, name, or recency? What constitutes a "relevant" vs. "irrelevant" result?
- **"Performance is acceptable"** — Does not define acceptable performance. No latency thresholds, no dataset size expectations, no indexing requirements.

#### 4. VAGUE: Test Requirements

The current test requirement is a single item:

- **"Test that search works correctly"** — Does not specify any concrete test scenarios. Expected test cases would include:
  - Search with a matching query returns expected results
  - Search with no matches returns an empty result set
  - Search with pagination parameters
  - Search with special characters or empty query
  - Search response format matches the expected schema
  - Performance/timeout behavior under load (if applicable)

## Execution Decision: STOP

Per the skill's Step 1 rules:

> "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately** -- do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

**Execution is halted.** The following information is needed before implementation can proceed:

### Clarification Requests

1. **API Changes**: What is the exact endpoint specification?
   - HTTP method and path (e.g., `GET /api/v2/package/search`)
   - Query parameters (e.g., `q`, `offset`, `limit`, `sort`)
   - Response schema — does it return `PaginatedResults<PackageSummary>` like other list endpoints?

2. **Implementation Notes**: What patterns and references should be followed?
   - Should this use the existing `SearchService` from `modules/search/`, or implement search within `PackageService`?
   - What search mechanism — PostgreSQL full-text search (`tsvector`/`tsquery`), `ILIKE` filtering, or something else?
   - Which `PackageSummary` fields should be searchable (name, version, purl, license)?
   - Should the implementation follow the advisory search pattern in `modules/fundamental/src/advisory/service/advisory.rs`?
   - Are there shared query builder helpers in `common/src/db/query.rs` that should be reused?

3. **Acceptance Criteria**: Please provide measurable, verifiable criteria:
   - What specific fields are searchable?
   - What is the expected search behavior (substring match, prefix match, full-text)?
   - Are there pagination requirements (default page size, max page size)?
   - What is the acceptable response time threshold (e.g., < 200ms for 95th percentile)?
   - Should results be ranked by relevance score, or returned in a fixed sort order?

4. **Test Requirements**: Please provide specific test scenarios:
   - What fixture data should tests use?
   - What specific search queries and expected results should be verified?
   - Should tests cover pagination, empty results, and error cases?
   - Are integration tests against a real PostgreSQL test database expected (consistent with existing test patterns in `tests/api/`)?

**No steps beyond Step 1 have been executed.** No branches have been created, no code has been read or modified, and no implementation planning has been performed. Once the above gaps are resolved, the task can be re-processed from Step 1.5 onward.
