# implement-task TC-9202 — Execution Report

## Step 0 — Validate Project Configuration

Reading the project's CLAUDE.md (`claude-md-mock.md`), I verify the required sections:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** — present with Project key `TC`, Cloud ID, Feature issue type ID, Git Pull Request custom field `customfield_10875`, and GitHub Issue custom field `customfield_10747`.
3. **Code Intelligence** — present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`.

All required sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all Jira operations. If MCP fails, prompt the user with the three options (REST API fallback, skip, or retry).

## Step 1 — Fetch and Parse Jira Task

**STOP — Task description is incomplete. Clarification required before proceeding.**

I would fetch TC-9202 via `jira.get_issue("TC-9202")` and parse its structured description. Comparing against the required task description template, the following sections are present and the following are missing or inadequate:

### Present sections

| Section | Content | Assessment |
|---|---|---|
| Repository | `trustify-backend` | Valid |
| Target Branch | `main` | Valid |
| Description | "Add search capabilities to the package module so users can find packages more easily." | Vague — see below |
| Files to Modify | `modules/fundamental/src/package/endpoints/mod.rs` — add search route | Present but minimal |
| Files to Create | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler | Present but minimal |
| Acceptance Criteria | 3 items | Present but vague — see below |
| Test Requirements | 1 item | Present but vague — see below |

### Missing sections

The following sections expected by the task description template are absent:

- **API Changes** — No endpoint specification provided. What HTTP method and path should the search endpoint use? (e.g., `GET /api/v2/package/search?q=...` or `GET /api/v2/package?search=...`). What query parameters does it accept? What response shape does it return?
- **Implementation Notes** — No guidance on patterns to follow, existing code to reuse, or specific functions/structs to interact with. The repository has existing search infrastructure in `modules/search/` with a `SearchService` for full-text search — should this be reused? Should the endpoint follow the same pattern as `modules/fundamental/src/sbom/endpoints/list.rs` or `modules/fundamental/src/advisory/endpoints/list.rs`? Should it use `common/src/db/query.rs` helpers for filtering/pagination?
- **Reuse Candidates** — Not listed, but the repository contains several reuse candidates that should be referenced:
  - `modules/search/src/service/mod.rs::SearchService` — full-text search across entities
  - `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting
  - `common/src/model/paginated.rs::PaginatedResults<T>` — standard paginated response wrapper
  - `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — has a `search` method that could serve as a pattern

### Vague/underspecified content

1. **Description**: "Add search capabilities" is too vague. What kind of search? Full-text search? Filtering by specific fields (name, license, version)? Fuzzy matching? Should it integrate with the existing `SearchService` in `modules/search/`, or is this a module-local query-based search?

2. **Acceptance Criteria**: All three criteria are vague and not verifiable:
   - "Users can search for packages" — what search parameters? What fields are searchable?
   - "Search results are relevant" — what defines relevance? Is there ranking? What matching algorithm?
   - "Performance is acceptable" — what is the threshold? Is there a latency target or result-set size limit?

3. **Test Requirements**: "Test that search works correctly" is not actionable. What specific scenarios should be tested? Expected behaviors for:
   - Empty search query
   - No results found
   - Partial match
   - Pagination of results
   - Invalid input handling

## Execution Halted — Clarification Needed

Per the implement-task skill rules: "If the structured description is incomplete, ask the user for clarification and **stop execution**. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."

The following information is needed before implementation can proceed:

1. **API Changes**: What is the exact endpoint specification?
   - HTTP method and path (e.g., `GET /api/v2/package/search`)
   - Query parameters (e.g., `q`, `offset`, `limit`)
   - Response format (e.g., `PaginatedResults<PackageSummary>`)

2. **Implementation Notes**: What patterns should be followed?
   - Should the search use the existing `SearchService` from `modules/search/`, or implement query-based filtering using `common/src/db/query.rs`?
   - Which existing endpoint handler should serve as the pattern (e.g., `list.rs` in sbom or advisory)?
   - What search mechanism — SQL `LIKE`/`ILIKE`, PostgreSQL full-text search (`tsvector`/`tsquery`), or integration with the `SearchService`?

3. **Acceptance Criteria**: Need specific, verifiable criteria:
   - Which package fields are searchable (name, version, license, pURL)?
   - Is pagination required? What default page size?
   - What should happen on empty query or no results?

4. **Test Requirements**: Need specific test scenarios:
   - Search by name returns matching packages
   - Search with no matches returns empty paginated result
   - Pagination parameters are respected
   - Invalid/empty search query behavior

Please provide the missing information or re-run `/plan-feature` to generate a complete task description with the required sections, then re-invoke `/implement-task TC-9202`.
