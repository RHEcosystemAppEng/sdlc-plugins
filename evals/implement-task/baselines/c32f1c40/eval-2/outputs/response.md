# implement-task TC-9202 — Execution Response

## Step 0 — Validate Project Configuration

Checked the project's CLAUDE.md (`claude-md-mock.md`) for required sections:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`.

All required sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback. (Skipped per eval instructions — no external service calls.)

## Step 1 — Fetch and Parse Jira Task

Fetched TC-9202 and parsed the structured description. Results:

| Section | Status | Value |
|---------|--------|-------|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **MISSING** | — |
| Implementation Notes | **MISSING** | — |
| Acceptance Criteria | Present but **vague/unmeasurable** | "Users can search for packages", "Search results are relevant", "Performance is acceptable" |
| Test Requirements | Present but **vague/unmeasurable** | "Test that search works correctly" |
| Target PR | Not present (optional) | — |
| Review Context | Not present (optional) | — |
| Bookend Type | Not present (optional) | — |
| Dependencies | Not present | — |

### Gaps Identified — Stopping Execution

The task description does not follow the structured template required by plan-feature. The following gaps prevent implementation:

**1. API Changes section is missing (critical)**

This task adds a search endpoint but does not specify:
- The HTTP method and endpoint path (e.g., `GET /api/v2/package/search`)
- Query parameters (e.g., `q`, `offset`, `limit`, filter fields)
- Response shape (e.g., `PaginatedResults<PackageSummary>` or a different structure)
- Whether this is a new route or modifies an existing one

**2. Implementation Notes section is missing (critical)**

No guidance on:
- Which existing patterns to follow (the `advisory` module has a `search` in `AdvisoryService` — should the package search follow the same pattern?)
- Which shared utilities to reuse (e.g., `common/src/db/query.rs` for query building, `common/src/model/paginated.rs` for response wrapping)
- How to interact with the `SearchService` in `modules/search/` vs. implementing search directly in the package service
- Whether to use full-text PostgreSQL search, ILIKE pattern matching, or the existing `SearchService`
- Which `PackageSummary` fields should be searchable (name, version, license, purl?)

**3. Acceptance Criteria are too vague to verify**

- "Users can search for packages" — what constitutes a search? By name? By purl? By license? What query parameters?
- "Search results are relevant" — what relevance metric? Ordering? Exact match vs. substring vs. full-text?
- "Performance is acceptable" — what is acceptable? No latency target, no dataset size expectation, no indexing strategy

**4. Test Requirements are too vague to implement**

- "Test that search works correctly" — no specific test cases defined. Need at minimum:
  - Search by exact name returns matching packages
  - Search by partial name/substring returns relevant results
  - Search with no results returns empty paginated response
  - Search with pagination parameters works correctly
  - Invalid/empty query parameter handling

**5. Dependencies section is absent**

It is unclear whether this task depends on any prior tasks. The linked issue `TC-9001` ("is incorporated by") is a parent feature, not a dependency, but there may be other tasks that must be completed first (e.g., database migrations for search indexes).

---

**Action required from user:** Please provide the missing information before implementation can proceed. Specifically:

1. What is the exact endpoint path and HTTP method? (e.g., `GET /api/v2/package/search?q=<term>&offset=0&limit=10`)
2. Which fields on `PackageSummary` should be searchable?
3. What search mechanism should be used — the existing `SearchService` in `modules/search/`, PostgreSQL full-text search, or simple ILIKE filtering via `common/src/db/query.rs`?
4. What is the expected response shape? Should it return `PaginatedResults<PackageSummary>`?
5. Are there measurable acceptance criteria (e.g., "search by package name returns matching results within 200ms for 10k packages")?
6. What specific test cases should be covered?
7. Are there any prerequisite tasks that must be completed first?

**Execution is stopped.** No subsequent steps (branching, code inspection, implementation, testing) will be performed until the user provides the missing information. Re-running plan-feature to regenerate this task with a complete structured description is recommended.
