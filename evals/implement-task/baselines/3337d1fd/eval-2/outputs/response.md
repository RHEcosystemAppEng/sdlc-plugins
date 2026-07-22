# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Checked the project's CLAUDE.md (`claude-md-mock.md`) for required sections under `# Project Configuration`:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

All required sections are present and complete. Proceeding.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, would prompt the user with the three options (REST API fallback, skip, or retry) as specified in the skill.

## Step 1 — Fetch and Parse Jira Task

Fetched task TC-9202. Parsed the structured description:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present (vague) | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **MISSING** | No endpoint path, HTTP method, query parameters, or response shape specified |
| Implementation Notes | **MISSING** | No patterns, code references, or reusable utilities referenced |
| Acceptance Criteria | Present (non-verifiable) | Criteria are vague and not concretely testable |
| Test Requirements | Present (non-verifiable) | Single line "Test that search works correctly" — no specific scenarios |
| Target PR | Not present (optional) | N/A |
| Review Context | Not present (optional) | N/A |
| Bookend Type | Not present (optional) | N/A |
| Dependencies | Not present | No dependencies listed |

### Gaps Identified

The task description does not follow the structured template expected by the implement-task skill. The following gaps prevent implementation:

**1. API Changes section is missing.**
This section is needed to define:
- The endpoint path (e.g., `GET /api/v2/package/search` or a query parameter on `GET /api/v2/package?q=...`)
- The HTTP method
- Query parameters (search term, pagination, filters)
- The response shape (what struct wraps the results, pagination format)

**2. Implementation Notes section is missing.**
This section is needed to specify:
- Which existing patterns to follow (the repo has similar search in `modules/search/` and list endpoints in `modules/fundamental/src/package/endpoints/list.rs` and `modules/fundamental/src/advisory/service/advisory.rs` which has a `search` method)
- Which shared utilities to reuse (`common/src/db/query.rs` for filtering/pagination, `common/src/model/paginated.rs` for `PaginatedResults<T>`)
- Whether to use the existing `SearchService` from `modules/search/` or build package-specific search in `PackageService`
- Whether to use SQL `LIKE`/`ILIKE`, full-text search (`tsvector`/`tsquery`), or the existing search module's infrastructure
- How search integrates with the existing `PackageService` (extend `fetch`/`list`, or add a new `search` method)

**3. Acceptance Criteria are vague and non-verifiable.**
The current criteria cannot be objectively verified during implementation:
- "Users can search for packages" — by what fields? Name? Version? License? PURL?
- "Search results are relevant" — what defines relevance? Exact match? Substring? Fuzzy?
- "Performance is acceptable" — what is the threshold? Response time? Result set size?

These need to be concrete, e.g.:
- "Search by package name returns packages whose name contains the search term (case-insensitive)"
- "Search results are paginated using `PaginatedResults<PackageSummary>`"
- "Empty search term returns a 400 Bad Request"

**4. Test Requirements are vague.**
"Test that search works correctly" does not specify:
- Which test file to create or modify (e.g., `tests/api/package.rs` or a new `tests/api/package_search.rs`)
- What scenarios to test (successful search, empty results, invalid input, pagination)
- Expected response status codes and body shapes

## Decision: Stop Execution

Per the skill's instructions: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately — do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."

**The task description is incomplete. I am stopping execution and requesting clarification.**

---

## Clarification Needed

Before I can proceed with implementing TC-9202, please provide the following information (or re-run plan-feature to regenerate the task with a complete structured description):

1. **API Changes**: What is the exact endpoint specification?
   - Endpoint path and HTTP method (e.g., `GET /api/v2/package/search?q={term}`)
   - Query parameters (search term, pagination params, filter fields)
   - Response type (e.g., `PaginatedResults<PackageSummary>`)
   - Error responses (e.g., 400 for empty query, 404 behavior)

2. **Implementation Notes**: What patterns and existing code should be followed?
   - Should the search use the existing `SearchService` from `modules/search/`, or should a new search method be added to `PackageService`?
   - What search mechanism should be used (SQL LIKE/ILIKE, PostgreSQL full-text search, or the search module's infrastructure)?
   - Which fields on `PackageSummary` should be searchable (name, version, license, PURL)?
   - Should the search endpoint reuse `common/src/db/query.rs` helpers for filtering and pagination?
   - Reference to sibling search implementations (e.g., `AdvisoryService::search` in `modules/fundamental/src/advisory/service/advisory.rs`)

3. **Acceptance Criteria**: Please provide concrete, verifiable criteria, for example:
   - "Search by package name using case-insensitive substring match"
   - "Results paginated with `offset` and `limit` query parameters"
   - "Returns 400 Bad Request when search query is empty"
   - "Returns empty `PaginatedResults` when no packages match"

4. **Test Requirements**: Please specify test scenarios, for example:
   - "Test successful search returns matching packages"
   - "Test search with no results returns empty paginated response"
   - "Test search with pagination parameters"
   - "Test search with empty query returns 400"
   - Specify whether tests go in `tests/api/package.rs` (existing) or a new file

Once these gaps are addressed, I will resume implementation from Step 1.5 (Verify Description Integrity) onward.
