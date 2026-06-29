# implement-task: TC-9202 — Processing Response

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md (claude-md-mock.md) contains the required sections:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** — present, contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** — present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` using `rust-analyzer`

All required sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, would prompt the user with the REST API fallback options.

## Step 1 — Fetch and Parse Jira Task

Fetched task TC-9202. Parsing the structured description:

| Section | Status | Content |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Target Branch** | Present | `main` |
| **Description** | Present (vague) | "Add search capabilities to the package module so users can find packages more easily." |
| **Files to Modify** | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| **Files to Create** | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| **API Changes** | **MISSING** | Not specified — no endpoint path, HTTP method, query parameters, or response shape defined |
| **Implementation Notes** | **MISSING** | No patterns, code references, or reusable utilities referenced |
| **Acceptance Criteria** | Present (vague) | Criteria are non-specific: "Users can search for packages", "Search results are relevant", "Performance is acceptable" — no measurable thresholds or concrete definitions |
| **Test Requirements** | Present (vague) | Only "Test that search works correctly" — no specific test scenarios, expected behaviors, or edge cases |
| **Target PR** | Not present (optional) | — |
| **Review Context** | Not present (optional) | — |
| **Bookend Type** | Not present (optional) | — |
| **Dependencies** | Not present | — |

### Gaps Identified

The task description is **incomplete** and does not follow the expected template. The following required sections are missing or insufficiently specified:

1. **API Changes (MISSING):** The task asks to "add search functionality" but does not specify:
   - The endpoint path (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
   - The HTTP method
   - Query parameters (e.g., search term, filters, pagination parameters)
   - The response shape (e.g., `PaginatedResults<PackageSummary>` or a different search-specific response type)

2. **Implementation Notes (MISSING):** No guidance on:
   - Which existing patterns to follow (e.g., how the `advisory` module's search is implemented in `advisory/service/advisory.rs`)
   - Whether to use the existing `SearchService` from `modules/search/` or implement package-specific search logic
   - Which query helpers from `common/src/db/query.rs` to use for filtering and pagination
   - How to integrate with the existing `PackageService` in `package/service/mod.rs`
   - Whether full-text search, substring matching, or field-based filtering is expected

3. **Acceptance Criteria (VAGUE):** The criteria are not measurable or testable:
   - "Users can search for packages" — by what fields? Name, version, license, PURL?
   - "Search results are relevant" — what relevance criteria? Exact match, partial match, ranking?
   - "Performance is acceptable" — what threshold? Response time? Result set size limits?

4. **Test Requirements (VAGUE):** Only one test requirement is listed, and it is too generic:
   - "Test that search works correctly" — what constitutes "correctly"? No specific test scenarios, edge cases, error cases, or expected behaviors are described.
   - No guidance on whether to test pagination, empty results, invalid queries, or performance.

## STOP — Clarification Required

Per the SKILL.md rules: *"If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately** — do not proceed with any subsequent steps (branching, implementation planning, code changes) until the user provides the missing information."*

**I cannot proceed with implementation.** The following information is needed before continuing:

1. **API Changes:** What is the exact endpoint specification?
   - Endpoint path and HTTP method (e.g., `GET /api/v2/package/search?q={term}`)
   - Query parameters and their types
   - Response format (e.g., `PaginatedResults<PackageSummary>`)

2. **Implementation Notes:** What patterns and existing code should be followed?
   - Should this reuse the existing `SearchService` in `modules/search/`, or implement a module-specific search in `PackageService`?
   - Which search approach to use (full-text, LIKE/ILIKE, trigram, etc.)?
   - Which fields on `PackageSummary` are searchable?
   - Reference to an existing search implementation to follow as a pattern (e.g., `AdvisoryService::search` in `modules/fundamental/src/advisory/service/advisory.rs`)

3. **Acceptance Criteria:** What are the measurable success criteria?
   - Which package fields are searchable (name, version, license, namespace, PURL)?
   - What matching behavior is expected (exact, prefix, substring, fuzzy)?
   - What is the performance threshold (e.g., < 200ms for 95th percentile)?
   - Should results be paginated? If so, default page size?

4. **Test Requirements:** What specific test scenarios should be covered?
   - Search by name returns matching packages
   - Search with no results returns empty response
   - Search with pagination parameters
   - Search with special characters or empty query
   - Integration test pattern (which test file, test database setup)

Please provide the missing information or re-run plan-feature to generate a complete task description, then re-invoke `/implement-task TC-9202`.
