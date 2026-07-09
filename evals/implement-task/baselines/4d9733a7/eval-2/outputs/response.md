# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Project Configuration in CLAUDE.md is valid:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend`
- **Jira Configuration**: present with Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present with tool naming convention and `serena_backend` instance configured

Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Below is the section-by-section assessment against the required template:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **Missing** | No API Changes section — endpoint path, HTTP method, query parameters, and response shape are undefined |
| Implementation Notes | **Missing** | No Implementation Notes section — no patterns, code references, or guidance on how to implement the search |
| Acceptance Criteria | Present but **vague** (see below) | |
| Test Requirements | Present but **vague** (see below) | |
| Dependencies | Not present | May be intentionally absent if there are none, but not confirmed |

### Incomplete: Implementation Notes section is missing

The task description contains no **Implementation Notes** section. This section is critical because it specifies the patterns and code references to follow during implementation. Without it, there is no guidance on:

- Whether to use the existing `modules/search/` module's `SearchService` (full-text search across entities) or build a new search mechanism specific to the package module
- Which query-building utilities from `common/src/db/query.rs` to use
- Whether to use PostgreSQL full-text search, ILIKE queries, or another search strategy
- How to integrate with the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`
- What patterns to follow from sibling endpoints (e.g., the advisory module's search, if one exists)

### Vague: Acceptance Criteria lack specificity

The Acceptance Criteria are too vague to verify:

1. **"Users can search for packages"** — Does not specify which fields are searchable (package name, version, license, PURL, description?), what the search endpoint path is, what query parameters it accepts, or what the response shape looks like.

2. **"Search results are relevant"** — Does not define what "relevant" means. There is no specification of a relevance ranking algorithm, whether results should be sorted by relevance score, whether partial matches are acceptable, or what constitutes a false positive or false negative.

3. **"Performance is acceptable"** — Does not define a performance threshold. There is no target response time (e.g., p95 < 200ms), no maximum dataset size to test against, and no specification of whether pagination is required for large result sets.

### Vague: Test Requirements are insufficient

The single test requirement — **"Test that search works correctly"** — does not define what "correctly" means. It does not specify:

- Which search scenarios to test (exact match, partial match, case sensitivity, no results, special characters)
- Which fields to assert on in the response
- Whether to test error cases (invalid query, empty query)
- Whether to test pagination of search results
- What expected results to validate against (specific test data and expected matches)

## Execution Halted — Clarification Required

Per the implement-task skill rules: *"If the structured description is incomplete, ask the user for clarification and stop execution. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."*

The task description is missing the **Implementation Notes** section and the **API Changes** section entirely, and the Acceptance Criteria and Test Requirements are too vague to implement or verify against. I cannot proceed without clarification.

### Clarifying Questions

1. **Which fields should be searchable?** The `PackageSummary` struct is in `modules/fundamental/src/package/model/summary.rs`, and the `package` entity is in `entity/src/package.rs`. Which fields should the search match against — package name only, or also version, license (via the `package_license` entity), PURL, or other fields? Should the search support multi-field queries or is single-field text matching sufficient?

2. **What does "relevant" mean for search ranking?** Should results be ranked by relevance score (e.g., using PostgreSQL `ts_rank` with full-text search), or is a simple filtered list (ILIKE matching) sufficient? If ranked, what determines relevance — exact matches first, then prefix matches, then substring matches? Should the existing `SearchService` in `modules/search/` be reused or extended, or should this be a separate search mechanism within the package module?

3. **What is the performance threshold?** What response time is "acceptable" — for example, p95 under 200ms, 500ms, or 1 second? What dataset size should this be tested against? Is pagination required (using the existing `PaginatedResults<T>` wrapper from `common/src/model/paginated.rs`), and if so, what is the default page size?

4. **What is the API contract?** What should the endpoint path be (e.g., `GET /api/v2/package/search?q=...` or a query parameter on the existing `GET /api/v2/package` list endpoint)? What query parameters should it accept? What should the response shape be — `PaginatedResults<PackageSummary>` consistent with the list endpoint, or a different shape with relevance scores?

5. **What specific test scenarios define "works correctly"?** Should tests cover exact name match, partial/substring match, case-insensitive match, no-results case, special characters in query, and empty query? Should tests validate the order of results (relevance ranking) or just the presence/absence of expected items?

Please provide the missing Implementation Notes and API Changes sections, clarify the acceptance criteria thresholds, and define the specific test scenarios. I will resume implementation once these gaps are addressed.
