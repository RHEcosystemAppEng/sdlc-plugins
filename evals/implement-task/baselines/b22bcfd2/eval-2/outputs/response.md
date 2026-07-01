# implement-task TC-9202 — Clarification Required

## Step 0 — Validate Project Configuration

Project Configuration in CLAUDE.md verified:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: present, contains Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` instance configured

Configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Evaluating required sections:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." — lacks specifics on search behavior, query parameters, or matching strategy |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **Missing** | No endpoint path, HTTP method, query parameters, or response shape specified |
| Implementation Notes | **Missing** | No patterns, code references, or guidance on how to implement the search (e.g., whether to use the existing `SearchService` in `modules/search/`, the `query.rs` helpers in `common/src/db/`, or PostgreSQL full-text search directly) |
| Acceptance Criteria | Present but vague | All three criteria are unmeasurable (see below) |
| Test Requirements | Present but vague | Single item "Test that search works correctly" provides no specifics (see below) |
| Dependencies | Not present | Acceptable if none exist |

### Missing sections

1. **API Changes** — completely absent. There is no specification for the search endpoint: no URL path (e.g., `GET /api/v2/package/search?q=...`), no HTTP method, no query parameters, and no response shape.

2. **Implementation Notes** — completely absent. There is no guidance on which existing patterns to follow. The repository already has a `modules/search/` module with a `SearchService` for full-text search across entities, as well as shared query builder helpers in `common/src/db/query.rs` for filtering, pagination, and sorting. Without Implementation Notes, it is unclear whether this task should reuse those existing abstractions or implement something new within the package module.

### Vague Acceptance Criteria

The three acceptance criteria are unmeasurable:

- **"Users can search for packages"** — which fields should be searchable? Package name only, or also version, license, description, purl, namespace, or other fields from the `PackageSummary` struct? What query syntax is supported (substring match, prefix match, full-text search, regex)?
- **"Search results are relevant"** — what does "relevant" mean? Is there a relevance ranking algorithm expected (e.g., exact match first, then prefix, then substring)? Should results be sorted by relevance score, or by name alphabetically? Is fuzzy matching required?
- **"Performance is acceptable"** — what is the performance threshold? Is there a maximum response time (e.g., < 200ms for 95th percentile)? What dataset size should this perform against? Should the endpoint use database indexes, and if so, which ones?

### Vague Test Requirements

- **"Test that search works correctly"** — this provides no specifics about what test cases to write. Should there be tests for: empty query, exact match, partial match, no results, pagination of results, special characters in query, case sensitivity, multiple matching packages? Should tests verify response shape, field presence, or sort order?

## Decision: Stop Execution (SKILL.md §1.6)

The structured description is incomplete. Per SKILL.md constraint: "If the structured description is incomplete, ask the user for clarification and stop execution immediately — do not proceed with any subsequent steps."

Stopping execution. No branch has been created, no code has been written, and no Jira transitions have been made.

## Clarifying Questions

Before proceeding with implementation, the following information is needed:

### 1. Search scope — which fields should be searchable?

The `PackageSummary` struct (in `modules/fundamental/src/package/model/summary.rs`) likely contains fields such as name, version, namespace/purl, and license. Which of these fields should the search query match against? Should the search support:
- Single-field search (e.g., name only)?
- Multi-field search (e.g., name + namespace + license)?
- Different match types per field (e.g., substring on name, exact on license)?

### 2. What does "relevant" mean for search result ranking?

The acceptance criterion "Search results are relevant" needs a concrete definition:
- Should results be ranked by relevance score, or returned in a fixed order (e.g., alphabetical by name)?
- If ranked, what is the ranking strategy? For example: exact match > prefix match > substring match > fuzzy match?
- Should the existing `SearchService` in `modules/search/` be reused (it already provides full-text search across entities), or should this be a simpler query-parameter-based filter on the existing package list endpoint?
- Is there a minimum relevance threshold below which results should be excluded?

### 3. What is the performance threshold, and what query parameters / response shape should the endpoint use?

- What is the maximum acceptable response time (e.g., p95 < 200ms, p99 < 500ms)? Against what dataset size (e.g., 10K packages, 100K packages)?
- Should the endpoint return `PaginatedResults<PackageSummary>` (consistent with sibling endpoints like `GET /api/v2/package`)?
- What query parameters should the endpoint accept? For example: `q` (search term), `limit`, `offset`, `sort_by`? Should it support the shared filtering/pagination/sorting from `common/src/db/query.rs`?
- Does this require a new database index (e.g., GIN index for full-text search, or a B-tree index on the name column)?

### 4. What test scenarios are required?

The test requirement "Test that search works correctly" needs elaboration:
- What are the expected test cases? At minimum: empty query behavior, exact match, partial/substring match, no results found, pagination, and special character handling?
- Should tests follow the integration test pattern in `tests/api/` (hitting a real PostgreSQL test database), consistent with `tests/api/sbom.rs` and `tests/api/search.rs`?
- Are there specific edge cases to cover (e.g., case-insensitive search, Unicode handling, SQL injection prevention)?

### 5. Should this reuse or extend the existing search module?

The repository already has `modules/search/` with a `SearchService` that provides full-text search across entities, and an endpoint at `GET /api/v2/search`. Should this task:
- Add package search to the existing `SearchService` and `/api/v2/search` endpoint?
- Create a separate search endpoint specific to packages at `/api/v2/package/search`?
- Simply add query-parameter filtering to the existing `GET /api/v2/package` list endpoint (similar to how advisory might handle filtered listing)?

Please provide the missing information so the task description can be completed and implementation can proceed.
