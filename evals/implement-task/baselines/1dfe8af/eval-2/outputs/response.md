# implement-task TC-9202 — Execution Halted: Incomplete Task Description

## Step 0 — Validate Project Configuration

The project's CLAUDE.md (claude-md-mock.md) contains:

1. **Repository Registry** — present, with `trustify-backend` mapped to Serena instance `serena_backend`.
2. **Jira Configuration** — present, with Project key (`TC`), Cloud ID, and Feature issue type ID.
3. **Code Intelligence** — present, with tool naming convention (`mcp__<serena-instance>__<tool>`) and the `serena_backend` instance configured for `rust-analyzer`.

Project Configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description of TC-9202 against the required template sections:

| Section | Status | Detail |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present (but vague) | "Add search capabilities to the package module so users can find packages more easily." — lacks specifics on search behavior, supported fields, query syntax, or matching strategy |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No endpoint path, HTTP method, request parameters, or response shape defined. The repository already has a `modules/search/` module with a `SearchService` — unclear whether this task should use the existing search infrastructure or create a new package-specific endpoint |
| Implementation Notes | **MISSING** | No patterns, code references, or architectural guidance provided. Critical gap: no indication of whether to use the existing `SearchService` in `modules/search/`, extend `PackageService`, or build standalone search logic. No reference to query builder helpers in `common/src/db/query.rs` or pagination via `PaginatedResults<T>` |
| Acceptance Criteria | Present (but vague) | All three criteria are unmeasurable — see analysis below |
| Test Requirements | Present (but vague) | Single criterion "Test that search works correctly" is not actionable — see analysis below |
| Target PR | Absent (optional) | N/A — not required |
| Review Context | Absent (optional) | N/A — not required |
| Bookend Type | Absent (optional) | N/A — not required |
| Dependencies | Absent (optional) | N/A — not required |

### Missing Required Sections

**1. API Changes — MISSING**

This task adds a search endpoint but provides no API contract:
- What is the endpoint path? (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
- What HTTP method does it use?
- What query parameters or request body does it accept?
- What is the response shape? Does it return `PaginatedResults<PackageSummary>` consistent with other list endpoints?

**2. Implementation Notes — MISSING**

This is a critical gap. Without Implementation Notes, there is no guidance on:
- Whether to reuse the existing `SearchService` in `modules/search/src/service/mod.rs` (which already provides full-text search across entities) or build package-specific search logic
- Which fields on `PackageSummary` (or the underlying `package` entity) are searchable
- Whether to use PostgreSQL full-text search, `ILIKE` pattern matching, or another strategy
- How to integrate with the shared query builder helpers in `common/src/db/query.rs`
- Whether to extend `PackageService` with a search method or create a new service
- How the new `search.rs` endpoint handler should be registered in `endpoints/mod.rs`
- What existing patterns to follow (e.g., the `advisory` module has a `search` capability in its `AdvisoryService` — should the package module follow the same pattern?)

### Vague Acceptance Criteria

The three acceptance criteria are not measurable or verifiable:

1. **"Users can search for packages"** — By what mechanism? What fields? What query format? What constitutes a valid search input?
2. **"Search results are relevant"** — How is relevance defined? Is there a ranking algorithm? Should results be sorted by relevance score, alphabetically, or by creation date? What counts as a "relevant" result vs. an irrelevant one?
3. **"Performance is acceptable"** — What is the performance target? What is the expected dataset size? Is there a maximum response time (e.g., < 200ms for 95th percentile)? Should the query use an index?

### Vague Test Requirements

The single test requirement ("Test that search works correctly") is not actionable:
- What specific scenarios should be tested? (e.g., exact match, partial match, no results, special characters, pagination)
- Should there be error case tests? (e.g., empty query, invalid parameters)
- What assertions define "works correctly"? (e.g., status code, response shape, specific field values)
- Where should the test file live? (Likely `tests/api/package.rs` or a new `tests/api/package_search.rs` based on repository conventions, but this should be specified)

## Execution Halted — Clarification Required

Per the skill's rules: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."

**I am stopping execution and will not proceed with branching, implementation planning, code changes, or any subsequent steps.**

### Questions for Clarification

Before proceeding, please provide the following:

1. **API Changes**: What is the endpoint specification?
   - Endpoint path and HTTP method (e.g., `GET /api/v2/package/search?q={query}`)
   - Request parameters (query string, filters, pagination params)
   - Response shape (e.g., `PaginatedResults<PackageSummary>`)

2. **Implementation Notes**: What is the intended search architecture?
   - Should this use the existing `SearchService` in `modules/search/`, or build package-specific search logic?
   - Which package fields should be searchable (e.g., name, version, license, purl)?
   - What search strategy should be used (PostgreSQL full-text search, `ILIKE`, trigram similarity)?
   - Should the implementation follow the `AdvisoryService` search pattern as a reference?
   - Should `PackageService` in `modules/fundamental/src/package/service/mod.rs` be extended with a search method?

3. **Acceptance Criteria**: Can you provide measurable criteria?
   - What fields must be searchable?
   - How should results be ranked/sorted?
   - Is there a performance target (e.g., response time under N milliseconds)?
   - Should partial matching be supported (e.g., searching "log" matches "log4j")?

4. **Test Requirements**: What test scenarios are required?
   - Should tests cover: exact match, partial match, no results, empty query, pagination of results, filtering?
   - What is the target test file path?
   - Should error cases (400, 404) be covered?

Please update the task description with the missing sections or provide the answers here, and I will resume implementation.
