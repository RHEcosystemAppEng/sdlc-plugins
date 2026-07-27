# implement-task TC-9202 — Execution Halted: Incomplete Task Description

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md contains the required sections:

- **Repository Registry** — present, maps `trustify-backend` to Serena instance `serena_backend`
- **Jira Configuration** — present with Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence** — present with tool naming convention (`mcp__<serena-instance>__<tool>`) and `serena_backend` instance configured with rust-analyzer

Project Configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Below is the section-by-section assessment:

| Section | Status | Detail |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily" — does not specify search algorithm, fields, or behavior |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No endpoint path, HTTP method, query parameters, or response shape defined |
| Implementation Notes | **MISSING** | No patterns, code references, or architectural guidance provided |
| Acceptance Criteria | Present but **vague** | All three criteria are unmeasurable (see details below) |
| Test Requirements | Present but **vague** | Single item with no specificity (see details below) |
| Target PR | Absent (optional) | — |
| Bookend Type | Absent (optional) | — |
| Dependencies | Absent (optional) | — |

### Identified Gaps

**1. Missing: Implementation Notes**

This section is entirely absent. Without it, there is no guidance on:
- Which existing patterns to follow (e.g., does the existing `modules/search/` module provide a `SearchService` that should be reused, or should this be a standalone SQL query within the package module?)
- Whether to use PostgreSQL full-text search (`tsvector`/`tsquery`), SQL `LIKE`/`ILIKE`, or the existing `SearchService` in `modules/search/`
- How to integrate with the existing `common/src/db/query.rs` query builder helpers
- What the search endpoint's request/response shape should look like

**2. Missing: API Changes**

No API contract is defined. The task needs to specify:
- The endpoint path (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package` list endpoint?)
- The HTTP method
- Query parameters (e.g., `q`, `limit`, `offset`, filters)
- Response format (e.g., `PaginatedResults<PackageSummary>` or a different shape with relevance scores?)

**3. Vague: Acceptance Criteria**

Each criterion is unmeasurable as written:

- "Users can search for packages" — which fields should be searchable? Package name only? Name + version? Name + namespace + description + license? Does it support partial matching, wildcard, or exact match?
- "Search results are relevant" — what does "relevant" mean operationally? Is there a relevance ranking algorithm required (e.g., TF-IDF, exact-match-first, prefix-match weighting)? Or is simple substring matching sufficient?
- "Performance is acceptable" — what is the performance threshold? A p95 latency target (e.g., < 200ms)? A maximum dataset size the search must handle (e.g., 100K packages)? Does it need an index?

**4. Vague: Test Requirements**

- "Test that search works correctly" — this is a single untestable statement. What scenarios should be covered? At minimum, tests typically need: search with results, search with no results, search with special characters, pagination of search results, empty query handling, and response shape validation.

## Execution Halted

Per the implement-task skill rules, the structured description is incomplete. I am stopping execution immediately and will not proceed with branching, implementation planning, code changes, or any subsequent steps until these gaps are resolved.

## Clarifying Questions

Please provide answers to the following before I can proceed:

1. **Which package fields should be searchable, and what matching strategy should be used?**
   The `PackageSummary` struct exists in `modules/fundamental/src/package/model/summary.rs`. Should search cover just the package name, or also version, namespace, description, and/or the license field? Should matching be exact, prefix-based, substring (`ILIKE`), or full-text search (`tsvector`/`tsquery`)? Should the existing `SearchService` in `modules/search/` be reused, or is this a module-local implementation?

2. **What does "relevant" mean for search result ranking, and what is the expected API contract?**
   Should results be ranked by relevance score (e.g., exact matches first, then prefix matches, then substring matches), or is unranked filtering acceptable? What endpoint path and query parameters should be used (e.g., `GET /api/v2/package/search?q=...&limit=...`)? Should the response use `PaginatedResults<PackageSummary>` consistent with the existing list endpoint, or a different shape that includes relevance scores?

3. **What is the concrete performance threshold, and what test scenarios are required?**
   "Performance is acceptable" needs a measurable target — for example, p95 latency under 200ms for a dataset of N packages, or a requirement for a database index. For test requirements, what scenarios should be covered? At minimum: successful search with results, search returning empty results, partial/substring matching behavior, pagination, and special character handling. Should tests follow the existing integration test pattern in `tests/api/` against a real PostgreSQL test database?

4. **Should there be Implementation Notes referencing the patterns in sibling modules?**
   The advisory module has an existing search capability (`AdvisoryService` includes a `search` method in `modules/fundamental/src/advisory/service/advisory.rs`). Should the package search follow the same pattern? The `common/src/db/query.rs` provides shared query builder helpers for filtering and pagination — should those be used for the search query construction?
