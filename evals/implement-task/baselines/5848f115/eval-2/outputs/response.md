# implement-task: TC-9202 — Execution Halted (Incomplete Task Description)

## Step 0 — Validate Project Configuration

The project's CLAUDE.md contains all required sections under `# Project Configuration`:

- **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field, and GitHub Issue custom field
- **Code Intelligence** — present, with tool naming convention and configured instances

Project configuration validation passed. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Fetched issue TC-9202. Parsing the structured description against the expected template sections:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | Vague — "find packages more easily" lacks specifics |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | No API endpoint specification (path, method, query params, response shape) |
| Implementation Notes | **MISSING** | No patterns, code references, or architectural guidance provided |
| Acceptance Criteria | Present | **Vague** — contains non-measurable criteria (see below) |
| Test Requirements | Present | **Vague** — contains undefined success criteria (see below) |

### Missing Sections

**Implementation Notes**: This section is entirely absent from the task description. The Implementation Notes section is critical because it specifies which existing code patterns to follow, which utilities to reuse (e.g., the shared query builder in `common/src/db/query.rs`, the `PaginatedResults<T>` wrapper), and how to integrate with the existing architecture. Without it, implementation would require guessing at the intended approach — database-level SQL `LIKE` queries vs. full-text search via the existing `modules/search/` module vs. SeaORM query filters — which violates the skill's constraint against improvising implementation details.

**API Changes**: This section is absent. For a search endpoint, the API contract is essential — the HTTP method, URL path, query parameters (search term, filters, pagination), and response body shape must be specified. The repository already has a `modules/search/` module with `GET /api/v2/search`; it is unclear whether TC-9202 intends to add a separate package-specific search route (e.g., `GET /api/v2/package/search`) or extend the existing cross-entity search endpoint.

### Vague Acceptance Criteria

The following acceptance criteria are not measurable and cannot be objectively verified in Step 8:

1. **"Search results are relevant"** — "Relevant" is undefined. This could mean exact match on package name, substring match, fuzzy match, match across multiple fields (name, version, license, description), or ranked results using a scoring algorithm. Without a definition of relevance, there is no way to verify this criterion or write tests for it.

2. **"Performance is acceptable"** — "Acceptable" is undefined. There is no latency threshold (e.g., "responds within 200ms for datasets up to 10,000 packages"), no specification of whether the search should use database indexes, full-text search indexes, or in-memory filtering, and no load requirements. This criterion cannot be verified without a concrete performance target.

### Vague Test Requirements

**"Test that search works correctly"** — "Correctly" is not defined. This does not specify:
- What inputs to test (single word, multi-word, special characters, empty string, partial matches)
- What fields should be searchable and which should not
- What the expected output shape is (paginated list? ranked results? highlighted matches?)
- What constitutes a correct vs. incorrect result for a given query
- Whether error cases should be tested (e.g., search with no results, invalid query syntax)
- What "correctly" means for edge cases (case sensitivity, Unicode handling, SQL injection prevention)

## Execution Halted — Clarification Required

Per the skill's constraint (Important Rules, item 3): "If the structured description is incomplete, ask the user for clarification and stop execution immediately — do not proceed with any subsequent steps."

The task description is missing required sections and contains vague, non-measurable criteria. I cannot proceed with implementation planning, branch creation, code changes, or any subsequent steps until the following questions are answered:

### Clarifying Questions

1. **Which fields should be searchable, and what search mechanism should be used?**
   The `PackageSummary` struct includes fields like name, version, and license. Which of these fields should the search query match against? Should the search use SQL `ILIKE`/`LIKE` pattern matching on the database, leverage PostgreSQL full-text search (`tsvector`/`tsquery`), or integrate with the existing `modules/search/` module's `SearchService`? Should results match on exact substrings, prefix matches, or fuzzy/typo-tolerant matches?

2. **What does "relevant" mean for search result ranking?**
   Should results be returned in a specific order (e.g., exact name matches first, then partial matches)? Is a relevance score or ranking algorithm required, or is a simple unranked filter sufficient? If ranked, what fields contribute to the score and with what relative weight?

3. **What is the concrete performance threshold for "acceptable" performance?**
   What is the maximum acceptable response time (e.g., under 200ms, under 500ms)? What dataset size should this target apply to (e.g., 1,000 packages, 100,000 packages)? Are database indexes expected to be added as part of this task? Should the endpoint support pagination via the existing `PaginatedResults<T>` pattern and `common/src/db/query.rs` helpers?

4. **What is the API contract for the search endpoint?**
   What HTTP method and path should be used (e.g., `GET /api/v2/package/search?q=...` vs. adding a query parameter to the existing `GET /api/v2/package` list endpoint)? What query parameters should be accepted (search term, filters, pagination, sort order)? What should the response body look like — should it reuse `PaginatedResults<PackageSummary>` or define a new response type with search-specific fields like match highlights or scores?

5. **What specific test scenarios define "works correctly"?**
   What are the concrete test cases? For example: search by exact package name returns that package; search by partial name returns all matching packages; search with no matches returns an empty paginated result; search is case-insensitive. Without defined test cases, I cannot implement tests that meaningfully validate the search behavior.

6. **What Implementation Notes / patterns should be followed?**
   Should this endpoint follow the same pattern as `modules/fundamental/src/sbom/endpoints/list.rs` or `modules/fundamental/src/advisory/endpoints/list.rs`? Should it reuse the query builder helpers from `common/src/db/query.rs`? Are there existing search patterns in `modules/search/src/service/mod.rs` that should be referenced or reused?

Please provide the missing Implementation Notes section, clarify the acceptance criteria with measurable thresholds, and define the test scenarios. Once the task description is complete, I will resume execution from Step 1.5.
