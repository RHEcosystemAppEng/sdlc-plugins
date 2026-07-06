# implement-task: TC-9202

## Step 0 -- Validate Project Configuration

Verified the project's CLAUDE.md (claude-md-mock.md) contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`

Project Configuration validation: **PASSED**

## Step 1 -- Fetch and Parse Jira Task

Fetched issue TC-9202. Parsing the structured description against the task description template.

### Sections present

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present but incomplete | Only `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present but incomplete | Only `modules/fundamental/src/package/endpoints/search.rs` |
| Acceptance Criteria | Present but vague | 3 items, all unmeasurable |
| Test Requirements | Present but vague | 1 item, no specifics |

### Sections missing

| Section | Required? | Impact |
|---|---|---|
| **API Changes** | Expected for an endpoint task | No HTTP method, path, query parameters, or response format specified |
| **Implementation Notes** | Expected | No patterns to follow, no existing code references, no guidance on reuse |

### Gaps identified

**EXECUTION STOPPED.** The task description does not follow the structured template and has critical gaps that prevent implementation. The following information is missing or insufficient:

#### 1. API Changes section is missing

This task adds a search endpoint but does not specify:
- The HTTP method and URL path (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
- Query parameters (search term, filters by license, pagination, sorting)
- Request format (query string parameters vs. request body)
- Response format (should it return `PaginatedResults<PackageSummary>` consistent with the existing list endpoint?)

#### 2. Implementation Notes section is missing

Without Implementation Notes, there is no guidance on:
- Which existing patterns to follow. The repository has an existing `modules/search/` module with `SearchService` for full-text search -- should this task integrate with that, or implement search independently within the package module?
- Whether to use the shared `common/src/db/query.rs` query builder helpers for filtering and pagination
- How to structure the search query (SQL LIKE, ILIKE, full-text search with `tsvector`, or delegating to the existing `SearchService`)
- Whether the `PackageSummary` model needs new fields or a separate search result model
- How to integrate with the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`

#### 3. Files to Modify is incomplete

Only `modules/fundamental/src/package/endpoints/mod.rs` is listed for route registration. A search feature would likely also require modifications to:
- `modules/fundamental/src/package/service/mod.rs` -- to add a search method to `PackageService`
- Potentially `server/src/main.rs` if new route mounting is needed
- Potentially `entity/src/package.rs` if the entity needs search-related changes (e.g., indexes)

#### 4. Files to Create is incomplete

Only the endpoint handler is listed. Depending on the search approach, additional files may be needed:
- A search request/query model (for deserializing search parameters)
- Migration files if database indexes are needed for search performance

#### 5. Acceptance Criteria are vague and unmeasurable

The current criteria cannot be objectively verified:
- "Users can search for packages" -- search by what? Name? Version? License? PURL? All fields?
- "Search results are relevant" -- what defines relevance? Exact match? Substring? Fuzzy? Ranking?
- "Performance is acceptable" -- what is the threshold? Response time under N ms? Tested with how many records?

#### 6. Test Requirements are vague

"Test that search works correctly" provides no guidance on:
- Which test file to create or modify (the repo has `tests/api/` for integration tests but no package test file is listed)
- Specific test cases (search with results, search with no results, search with special characters, pagination of search results, search by specific fields)
- Whether to follow the existing integration test pattern in `tests/api/search.rs` or `tests/api/advisory.rs`

## Action Required

Please provide the missing information before implementation can proceed. Specifically:

1. **API Changes**: What is the endpoint path, HTTP method, query parameters, and response shape?
2. **Implementation Notes**: Should this integrate with the existing `SearchService` in `modules/search/`, or implement search independently? Which existing patterns and code should be reused?
3. **Files to Modify**: Complete list of files that need changes (service layer, entity layer, etc.)
4. **Acceptance Criteria**: Measurable criteria with specific search fields, behavior expectations, and performance thresholds
5. **Test Requirements**: Specific test cases to implement, including the test file location

No branches have been created, no code has been modified, and no further steps will be taken until these gaps are resolved. The recommended path is to re-run `/plan-feature` for the parent feature (TC-9001) to regenerate this task with a complete structured description.
