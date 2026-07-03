# implement-task TC-9202

## Step 0 -- Validate Project Configuration

Checking CLAUDE.md for required Project Configuration sections:

1. **Repository Registry** -- Present. Contains `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** -- Present. Project key: TC, Cloud ID: 2b9e35e3-6bd3-4cec-b838-f4249ee02432, Feature issue type ID: 10142.
3. **Code Intelligence** -- Present. Tool naming convention documented: `mcp__<serena-instance>__<tool>`. Configured instance: `serena_backend` with rust-analyzer.

Project Configuration validation passed.

## Step 1 -- Fetch and Parse Jira Task

Parsing the structured description for TC-9202:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **Missing** | No API Changes section -- endpoint path, HTTP method, query parameters, and response shape are unspecified |
| Implementation Notes | **Missing** | No Implementation Notes section -- no patterns, code references, or architectural guidance provided |
| Acceptance Criteria | Present but **vague** | See details below |
| Test Requirements | Present but **vague** | See details below |
| Dependencies | Not present | May be optional, but should be confirmed |

### Gaps Identified

**1. Implementation Notes section is entirely missing.**

This is a required section that provides the patterns and code references needed to implement the task. Without it, there is no guidance on:
- Which existing search infrastructure to use (the repository has a `modules/search/` module with `SearchService` -- should this be reused or is a separate package-specific search needed?)
- Which query helpers from `common/src/db/query.rs` to use for filtering and pagination
- How to integrate with the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`
- What response type to return (e.g., `PaginatedResults<PackageSummary>` from `common/src/model/paginated.rs`)
- How to register the new route in `endpoints/mod.rs`

**2. Acceptance Criteria are vague and unmeasurable.**

- "Search results are relevant" -- There is no definition of what "relevant" means. Does this mean exact match on package name? Substring match? Full-text search across multiple fields? Fuzzy matching? Without a definition of relevance, there is no way to verify this criterion.
- "Performance is acceptable" -- There is no performance threshold defined. What response time is acceptable? Under 200ms? Under 1 second? Under what data volume? Without a concrete threshold, this criterion cannot be verified.
- "Users can search for packages" -- This is somewhat testable but still lacks specificity about what search inputs are supported (name, version, license, purl, etc.).

**3. Test Requirements are vague and non-actionable.**

- "Test that search works correctly" -- This is a single vague statement that provides no guidance on:
  - What test scenarios to cover (empty results, single match, multiple matches, special characters, pagination)
  - What error cases to test (invalid query parameters, empty search term, SQL injection protection)
  - What assertions to make (status codes, response shape, field values)
  - Whether integration tests against PostgreSQL are required (consistent with existing tests in `tests/api/`)

**4. API Changes section is missing.**

There is no specification for the search endpoint: HTTP method, URL path, query parameters (search term, filters, pagination), or response format.

## Execution Halted -- Clarification Required

Per the implement-task skill rules: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."

The task description is incomplete. The following clarifying questions must be answered before implementation can proceed:

### Clarifying Questions

1. **Which fields should the search operate on?** The `PackageSummary` struct likely includes fields such as name, version, purl, and license. Should the search match against the package name only, or should it search across multiple fields (name, version, purl, license, description)? Should this be a simple SQL `ILIKE` / substring match, or should it leverage PostgreSQL full-text search (`tsvector`/`tsquery`), or should it integrate with the existing `SearchService` in `modules/search/`?

2. **What does "relevant" mean for search results, and what relevance ranking is expected?** Should results be ranked by relevance score (e.g., exact match first, then partial match), or is a simple unordered filter sufficient? If ranking is needed, what ranking algorithm should be used? Should results be sorted by relevance, by name, or by some other default order?

3. **What is the concrete performance threshold?** What maximum response time is acceptable for search queries? Is there a target data volume to test against (e.g., 10k packages, 100k packages)? Should the endpoint include database indexing requirements to meet the performance target?

4. **What is the API contract for the search endpoint?** What HTTP method and path should be used (e.g., `GET /api/v2/package/search?q=<term>` or adding a `q` query parameter to the existing `GET /api/v2/package` list endpoint)? What query parameters should be supported (search term, filters, pagination via `offset`/`limit`)? Should the response use the existing `PaginatedResults<PackageSummary>` wrapper?

5. **What specific test scenarios are required?** At minimum, should the tests cover: successful search with results, search with no results, search with pagination, search with special characters, and error cases (e.g., missing search term)? Should these be integration tests hitting a real PostgreSQL database, consistent with the existing test suite in `tests/api/`?

Please provide the missing Implementation Notes, clarify the Acceptance Criteria with measurable thresholds, and specify concrete Test Requirements. Once the task description is complete, I will proceed with implementation.
