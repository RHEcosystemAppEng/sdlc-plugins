# implement-task: TC-9202

## Step 0 -- Validate Project Configuration

Verified the project's CLAUDE.md contains the required Project Configuration sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID (`2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** -- present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` for `trustify-backend`.

All required sections are present. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, would prompt the user with the REST API fallback options.

## Step 1 -- Fetch and Parse Jira Task

Fetched issue TC-9202. Parsing the structured description:

| Section | Status | Content |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Target Branch** | Present | `main` |
| **Description** | Present | Add search capabilities to the package module so users can find packages more easily. |
| **Files to Modify** | Present | `modules/fundamental/src/package/endpoints/mod.rs` -- add search route |
| **Files to Create** | Present | `modules/fundamental/src/package/endpoints/search.rs` -- search endpoint handler |
| **API Changes** | **MISSING** | Not provided |
| **Implementation Notes** | **MISSING** | Not provided |
| **Acceptance Criteria** | Present (but vague) | Users can search for packages; Search results are relevant; Performance is acceptable |
| **Test Requirements** | Present (but vague) | Test that search works correctly |
| **Target PR** | Not present (optional) | -- |
| **Review Context** | Not present (optional) | -- |
| **Bookend Type** | Not present (optional) | -- |
| **Dependencies** | Not present | -- |

### Issue URL

Would capture `webUrl` from the Jira API response, e.g., `https://redhat.atlassian.net/browse/TC-9202`.

### GitHub Issue extraction

The Jira Configuration specifies `GitHub Issue custom field: customfield_10747`. Would check the fetched issue's fields for this custom field. Not present in the mock data -- skipped silently.

## Incomplete Description -- STOP

**The task description is incomplete.** The following required sections are missing or insufficient, and I cannot proceed with implementation until clarification is provided:

### Missing Sections

1. **API Changes** -- This section is missing entirely. The task involves adding a search endpoint, but no details are provided about:
   - What is the endpoint path? (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
   - What query parameters does the search accept? (e.g., `q`, `filter`, `limit`, `offset`)
   - What is the response shape? (e.g., `PaginatedResults<PackageSummary>` or a custom search response)
   - What HTTP method is used?

2. **Implementation Notes** -- This section is missing entirely. Without it, I have no guidance on:
   - Which existing patterns to follow (e.g., does the `advisory` module have a search implementation that should be used as a reference?)
   - Whether to reuse the existing `SearchService` from `modules/search/` or build search logic within the `package` module
   - What search strategy to use (database `LIKE`/`ILIKE` queries, full-text search with `tsvector`, or integration with the existing search module)
   - How to integrate with `common/src/db/query.rs` query builder helpers
   - Whether to use any specific crate or utility for search functionality

### Vague Sections

3. **Acceptance Criteria** -- The current criteria are too vague to verify:
   - "Users can search for packages" -- search by what fields? (name, version, license, purl?)
   - "Search results are relevant" -- what defines relevance? Is ranking required? What matching algorithm?
   - "Performance is acceptable" -- what is the performance target? (e.g., < 200ms for 95th percentile)

4. **Test Requirements** -- The current requirement is too vague to implement:
   - "Test that search works correctly" -- what specific test scenarios? (e.g., exact match, partial match, no results, pagination, special characters, case sensitivity)
   - What test fixtures or data setup is needed?
   - Are error case tests required? (e.g., invalid query parameters, empty search string)

### Action Required

Please provide the missing **API Changes** and **Implementation Notes** sections, and clarify the **Acceptance Criteria** and **Test Requirements** with specific, verifiable details. Once the task description is complete, I will proceed with implementation.

**Execution stopped.** No branches have been created, no code has been modified, and no Jira transitions have been made. The task remains in its current status (To Do).
