# implement-task TC-9202 -- Execution Halted: Incomplete Task Description

## Step 0 -- Validate Project Configuration

Project Configuration in CLAUDE.md has been validated:

1. **Repository Registry** -- present with `trustify-backend` mapped to Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID, and custom fields
3. **Code Intelligence** -- present with tool naming convention (`mcp__<serena-instance>__<tool>`) and `serena_backend` instance configured with `rust-analyzer`

Configuration is complete. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202 ("Add package search functionality") against the required template sections:

| Section | Status | Details |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." -- lacks specifics on search behavior (full-text? field-based filtering? which fields? what query parameters?) |
| Files to Modify | Present but minimal | Only lists `modules/fundamental/src/package/endpoints/mod.rs` -- likely incomplete (no service layer changes listed) |
| Files to Create | Present but minimal | Only lists `modules/fundamental/src/package/endpoints/search.rs` -- no service or model files |
| API Changes | **MISSING** | No endpoint specification: HTTP method, path, query parameters, request/response shapes are all unspecified |
| Implementation Notes | **MISSING** | No patterns, code references, or guidance on how to implement the search (e.g., should it use the existing `SearchService` in `modules/search/`, or add search directly to `PackageService`? Should it use the shared `query.rs` helpers for filtering?) |
| Acceptance Criteria | Present but vague/non-measurable | All three criteria are subjective: "Users can search for packages" (by what mechanism?), "Search results are relevant" (how is relevance defined?), "Performance is acceptable" (what threshold?) |
| Test Requirements | Present but vague/non-measurable | Single item: "Test that search works correctly" -- no specific test scenarios, edge cases, or expected behaviors described |
| Dependencies | Not listed | Task is linked to TC-9001 ("is incorporated by TC-9001") but no Dependencies section is present to indicate prerequisite tasks |

## Identified Gaps

The task description is **incomplete** and does not follow the structured template expected by plan-feature. The following critical information is missing or insufficiently specified:

### Missing Sections

1. **API Changes**: The task creates a search endpoint but does not specify:
   - The HTTP method and URL path (e.g., `GET /api/v2/package/search?q=...` or query parameters on the existing `GET /api/v2/package` list endpoint)
   - Query parameters and their types (e.g., `q: string`, `field: enum`, `limit: integer`)
   - Response shape (e.g., does it return `PaginatedResults<PackageSummary>` like the existing list endpoint?)

2. **Implementation Notes**: The task provides no guidance on:
   - Whether to use the existing `SearchService` (`modules/search/`) for full-text search, or add filtering directly to `PackageService`
   - Whether to follow the pattern used by the `advisory` module (which already has search in `AdvisoryService`)
   - How to integrate with the shared query builder helpers in `common/src/db/query.rs`
   - Whether database migrations or index changes are needed
   - How to register the new route in `server/main.rs`

### Vague/Non-Measurable Sections

3. **Acceptance Criteria** are not actionable:
   - "Users can search for packages" -- by what fields? Name, version, license, PURL, all of these?
   - "Search results are relevant" -- what defines relevance? Exact match? Substring? Full-text ranking?
   - "Performance is acceptable" -- what latency or result-set-size thresholds apply?

4. **Test Requirements** lack specificity:
   - "Test that search works correctly" -- no test scenarios are defined (e.g., search with results, search with no results, search with special characters, search by different fields, pagination of search results, error cases)

### Potentially Incomplete Scope

5. **Files to Modify / Files to Create** appear incomplete given the repository structure:
   - No service layer file listed -- a search endpoint would likely require changes to or creation of a service method in `modules/fundamental/src/package/service/mod.rs`
   - No model changes listed -- search may require a search query model or search-specific response type
   - No test file listed -- `tests/api/` has tests for other modules but no package search test file is specified
   - No mention of `server/main.rs` for route mounting, if the search module needs separate registration

## Decision: Stop Execution

Per the implement-task skill rules:

> "If the structured description is incomplete, ask the user for clarification and **stop execution**. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."

**Execution is halted.** The following clarifications are needed before implementation can proceed:

1. **API Changes**: What is the exact endpoint specification? (HTTP method, path, query parameters, response shape)
2. **Implementation Notes**: Should this use the existing `SearchService` in `modules/search/`, extend `PackageService` with filtering, or follow the `AdvisoryService` search pattern? What shared utilities should be reused?
3. **Acceptance Criteria**: What specific fields are searchable? What matching strategy should be used (exact, substring, full-text)? What performance thresholds apply?
4. **Test Requirements**: What specific test scenarios should be covered? (e.g., successful search, empty results, invalid queries, pagination, field-specific filtering)
5. **Files scope**: Should service layer files, model files, test files, and route registration in `server/main.rs` be included in the scope?

Please provide the missing information or re-run plan-feature to generate a complete task description, then re-invoke `/implement-task TC-9202`.
