# implement-task: TC-9202 — Validation Result

## Step 0 — Validate Project Configuration

The project's CLAUDE.md contains the required sections:

1. **Repository Registry** — present, with `trustify-backend` mapped to Serena instance `serena_backend`.
2. **Jira Configuration** — present, with Project key (`TC`), Cloud ID, and Feature issue type ID.
3. **Code Intelligence** — present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and `serena_backend` configured with `rust-analyzer`.

Project Configuration is valid. Proceeding to task validation.

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description of TC-9202 against the required template sections:

| Section | Status | Detail |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No API Changes section. The task adds a search endpoint but does not specify the HTTP method, path, query parameters, or response shape. |
| Implementation Notes | **MISSING** | No Implementation Notes section. There are no references to existing patterns, code samples, or architectural guidance for implementing the search. |
| Acceptance Criteria | Present but **VAGUE** | See details below. |
| Test Requirements | Present but **VAGUE** | See details below. |
| Dependencies | Not present | No dependencies listed (acceptable — field is optional). |
| Target PR | Not present | Not a review feedback fix (acceptable — field is optional). |
| Bookend Type | Not present | Not a bookend task (acceptable — field is optional). |

### Acceptance Criteria gaps

The Acceptance Criteria are too vague to serve as verifiable checkpoints:

- "Users can search for packages" — does not specify which fields are searchable (name? version? license? pURL? namespace?), what search syntax is supported (substring match? prefix? regex? full-text?), or what the API contract looks like (query parameter name, response shape).
- "Search results are relevant" — does not define what "relevant" means. Is there relevance ranking? If so, by what signal (e.g., exact match first, then partial)? Or is this simply a filter that returns all matching rows?
- "Performance is acceptable" — does not define a performance threshold. What response time is acceptable? Under what data volume (e.g., 100 packages vs. 100,000)? Is there an indexing requirement?

### Test Requirements gaps

The Test Requirements section contains a single item:

- "Test that search works correctly" — does not specify what scenarios to test (empty query, no results, partial match, exact match, special characters, pagination of results, case sensitivity), what assertions to make, or what test data to use.

## Execution Halted — Clarification Required

Per the SKILL.md instruction: *"If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately — do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."*

The task description has the following gaps that must be resolved before implementation can proceed:

### Questions for clarification

1. **Which fields should be searchable?** The description says "find packages more easily" but does not specify which `PackageSummary` fields the search should match against. Should the search cover the package name only, or also version, license, pURL, namespace, or other fields? The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` includes a `license` field — should that be searchable too?

2. **What does "relevant" mean for search results, and is relevance ranking required?** "Search results are relevant" is not a verifiable criterion. Does this mean simple substring/prefix filtering (all matches returned in default order), or does it require ranked full-text search with relevance scoring? The repository has a `modules/search/` module with a `SearchService` for full-text search — should the package search integrate with that existing service, or implement its own filtering via the `common/src/db/query.rs` query helpers?

3. **What is the performance threshold?** "Performance is acceptable" is not measurable. What maximum response time is expected (e.g., < 200ms at p95)? Under what data volume (e.g., 10K packages, 100K packages)? Is a database index required? Should the endpoint use the existing `tower-http` caching middleware?

4. **What is the API contract?** The API Changes section is missing entirely. What should the endpoint path be (e.g., `GET /api/v2/package/search?q=...` or a query parameter on the existing `GET /api/v2/package` list endpoint)? What query parameters are accepted? Should the response use `PaginatedResults<PackageSummary>` consistent with other list endpoints?

5. **What specific test scenarios are required?** "Test that search works correctly" does not define coverage. What cases should be tested — empty query, no results, partial match, exact match, case sensitivity, special characters, pagination? Should the tests follow the integration test pattern in `tests/api/` (hitting a real PostgreSQL test database), and if so, what test data should be seeded?

6. **What Implementation Notes should guide the implementation?** The section is missing entirely. Should the search endpoint follow the pattern established by the existing `advisory/service/advisory.rs` (which already has a `search` capability in `AdvisoryService`)? Should it use the shared `query.rs` filtering helpers from `common/src/db/`? Should it integrate with the existing `modules/search/` full-text search service?

**No implementation plan has been drafted, no branch has been created, and no code changes have been made.** Please provide the missing information so the task description can be completed before implementation begins.
