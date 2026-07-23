# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Checked the project's CLAUDE.md for required `# Project Configuration` sections:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — present, documents tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` with `rust-analyzer`.

All required sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all JIRA operations. In this eval, JIRA operations are skipped (no external service calls).

## Step 1 — Fetch and Parse Jira Task

Parsed the task description for TC-9202. Here is what was found:

| Section | Status | Content |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Target Branch** | Present | `main` |
| **Description** | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| **Files to Modify** | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| **Files to Create** | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| **API Changes** | **MISSING** | No endpoint path, HTTP method, query parameters, request/response shapes defined |
| **Implementation Notes** | **MISSING** | No patterns, code references, reusable modules, or architectural guidance provided |
| **Acceptance Criteria** | Present but **insufficiently specific** | Criteria are vague and unmeasurable (e.g., "Search results are relevant", "Performance is acceptable") |
| **Test Requirements** | Present but **insufficiently specific** | Single vague requirement ("Test that search works correctly") with no specific scenarios |
| **Target PR** | Not present | (Optional — acceptable) |
| **Bookend Type** | Not present | (Optional — acceptable) |
| **Dependencies** | Not listed | Cannot verify prerequisite completion |

### Gaps Identified

The task description does **not** follow the structured template expected by this skill. The following information is missing or insufficient:

#### Missing Sections

1. **API Changes**: No endpoint specification is provided. To implement a search endpoint, I need:
   - The HTTP method (e.g., `GET`)
   - The endpoint path (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
   - Query parameters (e.g., `q` for search term, pagination parameters)
   - Response shape (e.g., `PaginatedResults<PackageSummary>`)

2. **Implementation Notes**: No guidance on patterns or code references. To implement correctly, I need:
   - Which search mechanism to use (e.g., PostgreSQL full-text search via `tsvector`/`tsquery`, SQL `LIKE`/`ILIKE`, or integration with the existing `modules/search/` module's `SearchService`)
   - Which fields on the `package` entity should be searchable (e.g., name, version, license, purl)
   - Whether to reuse the existing `common/src/db/query.rs` query builder helpers for filtering and pagination
   - Whether to follow the pattern in `advisory/service/advisory.rs` which already has a `search` method, or use a different approach
   - How the new search endpoint integrates with the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`

#### Insufficiently Specific Sections

3. **Acceptance Criteria**: The current criteria are not measurable:
   - "Users can search for packages" — search by what? Name? Version? License? PURL? All of these?
   - "Search results are relevant" — what defines relevance? Exact match? Substring? Ranked results?
   - "Performance is acceptable" — what is the performance target? Response time threshold? Result set size limit?

4. **Test Requirements**: The single requirement "Test that search works correctly" does not specify:
   - What search scenarios to test (e.g., exact match, partial match, no results, special characters)
   - Whether to test pagination of search results
   - Whether to test error cases (e.g., empty query, invalid parameters)
   - Whether integration tests should be added to `tests/api/` (following the existing pattern for `sbom.rs`, `advisory.rs`, `search.rs`)
   - What assertions to make on the response (status codes, result structure, specific field values)

## STOP — Clarification Required

Per the implement-task skill rules: the structured description is incomplete. I am stopping execution immediately and will not proceed with any subsequent steps (branching, code understanding, implementation planning, or code changes) until the missing information is provided.

**To proceed, please provide the following:**

1. **API Changes**: What is the endpoint specification? (method, path, query parameters, response shape)
2. **Implementation Notes**: What search mechanism should be used? Which package fields are searchable? What existing code patterns should be followed? Should this integrate with the existing `SearchService` in `modules/search/`, or be a standalone search within the package module?
3. **Acceptance Criteria**: Please provide specific, measurable criteria (e.g., "Search by package name returns matching results within 200ms", "Partial name matches are supported", "Results are paginated using `PaginatedResults`").
4. **Test Requirements**: Please provide specific test scenarios (e.g., "Test search with exact package name match returns the package", "Test search with no results returns empty paginated response", "Test search with pagination parameters").
5. **Dependencies**: Are there any prerequisite tasks that must be completed first?

Please update the task description in Jira with this information, or provide it here, and then re-run `/implement-task TC-9202`.
