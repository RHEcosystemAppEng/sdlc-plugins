# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Project Configuration verified in CLAUDE.md:
- Repository Registry: present (trustify-backend, Serena instance: serena_backend)
- Jira Configuration: present (Project key: TC, Cloud ID, Feature issue type ID)
- Code Intelligence: present (tool naming convention documented, serena_backend configured with rust-analyzer)

Configuration is valid. Proceeding to Step 1.

## Step 1 — Fetch and Parse Jira Task

Parsed the structured description for TC-9202. The following sections were found:

| Section | Status |
|---|---|
| Repository | Present: `trustify-backend` |
| Target Branch | Present: `main` |
| Description | Present (but vague — see below) |
| Files to Modify | Present: `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present: `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** |
| Implementation Notes | **MISSING** |
| Acceptance Criteria | Present but **insufficiently specific** (see below) |
| Test Requirements | Present but **insufficiently specific** (see below) |
| Target PR | Not present (optional) |
| Bookend Type | Not present (optional) |
| Dependencies | Not present (optional) |

## Gaps Identified — Execution Stopped

The task description for TC-9202 is incomplete and cannot be implemented as written. The following gaps require clarification before any implementation work (branching, planning, or code changes) can begin.

### 1. Missing: Implementation Notes

The **Implementation Notes** section is entirely absent from the task description. This section is expected to contain patterns and code references to follow during implementation — for example, which existing service methods to call or extend, which query builder patterns from `common/src/db/query.rs` to use, how to integrate with the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`, and whether to leverage the existing `modules/search/` module or build a standalone search within the package module. Without Implementation Notes, there is no guidance on how to implement the search — only what to implement at a high level. This is a required section per the task template.

### 2. Vague Acceptance Criteria

The Acceptance Criteria contain two items that are not specific enough to verify or implement against:

- **"Search results are relevant"** — This criterion does not define what "relevant" means. Relevance depends on which fields are searched (package name only? version? license? description?), whether partial/substring matches count, whether there is any ranking or scoring of results, and whether fuzzy matching is expected. Without a concrete definition, there is no way to verify this criterion is satisfied.

- **"Performance is acceptable"** — This criterion does not define what "acceptable" means. There is no latency threshold (e.g., "responds within 200ms for 10,000 packages"), no throughput requirement, and no indication of expected dataset size. Without a measurable target, this criterion cannot be verified.

### 3. Vague Test Requirements

The sole test requirement — **"Test that search works correctly"** — does not define what "correctly" means. It does not specify:

- Which search inputs to test (exact match, partial match, case sensitivity, empty query, special characters)
- Which response fields to validate (result count, ordering, field presence, pagination)
- Which error cases to cover (no results found, invalid query parameters, unauthorized access)
- Whether integration tests against a real database are expected (following the pattern in `tests/api/`) or unit tests at the service layer

This is insufficient to write meaningful tests. The existing test suite in `tests/api/` (e.g., `sbom.rs`, `advisory.rs`, `search.rs`) follows specific patterns for endpoint testing — but without knowing what "correctly" means for package search, those patterns cannot be applied.

---

## Clarifying Questions

The following questions must be answered before implementation can proceed:

1. **Which fields should be searchable?** The `PackageSummary` struct in `modules/fundamental/src/package/model/summary.rs` likely contains fields such as package name, version, and license. Should the search query match against the package name only, or also against version strings, license identifiers, or other metadata? Should the search support filtering by specific fields (e.g., `?name=foo&license=MIT`) in addition to or instead of a free-text query?

2. **What does "relevant" mean for search results, and is ranking required?** Should results be ranked by relevance (e.g., exact matches first, then prefix matches, then substring matches)? Or is a simple SQL `LIKE`/`ILIKE` filter sufficient, returning all matches in default order? Does the search need to integrate with the existing full-text search infrastructure in `modules/search/` (which provides `SearchService` for cross-entity search), or should it be a standalone query within the package module using the shared query helpers in `common/src/db/query.rs`?

3. **What is the required performance threshold?** What response time is considered "acceptable" — for example, under 200ms at p95? What is the expected dataset size (hundreds, thousands, or millions of packages)? Does the search need database indexing (e.g., a GIN/trigram index for text search), or is a basic query sufficient for the expected scale?

4. **What specific test scenarios are required?** What inputs and expected outputs should the tests cover? For example: exact name match returns the correct package, partial name match returns matching packages, search with no results returns an empty paginated response, search with invalid parameters returns a 400 error. Should the tests follow the integration test pattern in `tests/api/search.rs` (hitting a real PostgreSQL test database), or are unit tests at the service layer sufficient?

5. **What API shape should the search endpoint use?** The task lists `search.rs` as a new file but the **API Changes** section is missing. Should this be `GET /api/v2/package/search?q=<query>` with a dedicated search route, or should search be added as query parameters on the existing `GET /api/v2/package` list endpoint (following the filtering pattern used by `common/src/db/query.rs`)? Should the response use `PaginatedResults<PackageSummary>` consistent with the existing list endpoint?

---

**Execution stopped.** Please provide the missing Implementation Notes, clarify the Acceptance Criteria and Test Requirements, and answer the questions above. Once the gaps are resolved, I will proceed with Step 2 (Verify Dependencies) and subsequent implementation steps.
