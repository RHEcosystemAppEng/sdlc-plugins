# implement-task TC-9202 — Execution Stopped: Incomplete Task Description

## Step 0 — Validate Project Configuration

Project Configuration validated successfully:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: present with Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field
- **Code Intelligence**: present with tool naming convention and configured instance for `serena_backend`

## Step 1 — Fetch and Parse Jira Task

Parsing the structured description for TC-9202:

| Section | Status |
|---|---|
| Repository | `trustify-backend` |
| Target Branch | `main` |
| Description | Present (but vague — see below) |
| Files to Modify | Present: `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present: `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** |
| Implementation Notes | **MISSING** |
| Acceptance Criteria | Present but **VAGUE** (see below) |
| Test Requirements | Present but **VAGUE** (see below) |
| Dependencies | Not listed |

### Missing: Implementation Notes

The **Implementation Notes** section is entirely absent from the task description. This section is critical — it provides the patterns, code references, and architectural guidance needed to implement changes correctly. Without it, there is no indication of:

- Which existing patterns to follow (e.g., how the advisory search endpoint is structured, which query builder helpers to use from `common/src/db/query.rs`)
- Whether to use the existing `SearchService` in `modules/search/` or build module-local search logic
- What data model or query approach to use (full-text PostgreSQL search, LIKE queries, SeaORM filtering, etc.)
- How to integrate with the shared `PaginatedResults<T>` response wrapper
- Which existing utilities or helpers to reuse

### Vague: Acceptance Criteria

The acceptance criteria lack specificity:

- **"Users can search for packages"** — does not specify which fields are searchable (name? version? license? purl? all of these?), what search syntax is supported (substring, exact match, wildcard, full-text), or what the API contract looks like (query parameter name, request/response shape).
- **"Search results are relevant"** — "relevant" is undefined. There is no specification of what relevance ranking means, whether results should be ordered by relevance score, recency, or alphabetically, and what constitutes a relevant vs. irrelevant result.
- **"Performance is acceptable"** — "acceptable" is undefined. There is no performance threshold (e.g., p95 latency under 200ms, support for 1000 concurrent queries, maximum response time for datasets of N packages).

### Vague: Test Requirements

The test requirements are not actionable:

- **"Test that search works correctly"** — "correctly" is undefined. This does not specify what inputs to test, what outputs to expect, what edge cases to cover (empty query, no results, special characters, very long queries), or what assertions to make. It does not indicate whether integration tests against PostgreSQL are required (consistent with the project's test conventions in `tests/api/`) or if unit tests suffice.

## Execution Stopped

Per the skill's rules (Step 1 and Important Rules): *"If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."* and *"If the structured description is incomplete, ask the user for clarification and stop execution. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."*

The task description is incomplete. I have not created any branches, drafted any implementation plan, or proceeded with any subsequent steps.

## Clarifying Questions

Before I can proceed with implementation, I need the following information:

1. **Which fields should be searchable?** The `PackageSummary` struct includes fields like name, version, and license. Should the search endpoint support searching across all of these fields, or only specific ones (e.g., name only)? Should purl (package URL) also be searchable? And what type of matching is expected — substring/LIKE, exact match, or full-text search with PostgreSQL `tsvector`/`tsquery`?

2. **What does "relevant" mean for search result ranking?** Should results be ranked by a relevance score (e.g., PostgreSQL `ts_rank`), returned in alphabetical order, sorted by most recently ingested, or returned in an unspecified order? If relevance-ranked, which fields should contribute to the ranking and with what weighting?

3. **What is the performance threshold?** What constitutes "acceptable" performance? Is there a target response time (e.g., under 200ms at p95)? What is the expected dataset size (number of packages)? Should the search use a database index (e.g., GIN index on a `tsvector` column), and if so, does a migration need to be included?

4. **What does "search works correctly" mean for testing?** What specific test scenarios should be covered? For example: search by exact name returns the correct package, partial name match returns expected results, search with no matches returns an empty paginated response, special characters in queries are handled safely. Should these be integration tests against PostgreSQL (matching the project's convention in `tests/api/`)?

5. **Should the search reuse the existing `SearchService` in `modules/search/`?** The repository already has a `modules/search/` module with a `SearchService` that provides full-text search across entities. Should the package search be added as a capability within that existing service, or should it be a standalone endpoint within the `package` module? This architectural decision affects the Implementation Notes significantly.

Please provide the missing **Implementation Notes** section and clarify the **Acceptance Criteria** and **Test Requirements** with specific, measurable definitions. Once I have this information, I will proceed with implementation.
