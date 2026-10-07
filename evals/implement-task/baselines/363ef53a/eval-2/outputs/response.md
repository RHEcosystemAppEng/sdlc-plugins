# implement-task: TC-9202

## Step 0 -- Validate Project Configuration

Checked the project CLAUDE.md (`claude-md-mock.md`). All required sections are present:

1. **Repository Registry** -- contains `trustify-backend` with Serena instance `serena_backend`
2. **Jira Configuration** -- contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present with tool naming convention and configured `serena_backend` instance

Project Configuration is valid. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Here is what was found:

| Section | Status |
|---|---|
| Repository | Present: `trustify-backend` |
| Target Branch | Present: `main` |
| Description | Present but vague |
| Files to Modify | Present |
| Files to Create | Present |
| API Changes | **MISSING** |
| Implementation Notes | **MISSING** |
| Acceptance Criteria | Present but **insufficiently specific** (see below) |
| Test Requirements | Present but **insufficiently specific** (see below) |
| Target PR | Not present (optional) |
| Bookend Type | Not present (optional) |
| Dependencies | Not present (optional) |

### Gaps identified

Per the skill's Step 1 rule: "If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and **stop execution immediately**."

The following gaps prevent implementation from proceeding:

---

### Gap 1: Implementation Notes section is missing

The task description contains no **Implementation Notes** section. This section is critical because it tells the implementer which existing code patterns, utilities, helpers, and references to follow. Without it, there is no guidance on:

- Which existing search patterns in the codebase to follow (e.g., the `modules/search/` module already has a `SearchService` with full-text search -- should the package search reuse or extend it?)
- Which query builder helpers from `common/src/db/query.rs` to use for filtering, pagination, and sorting
- What request/response types to use (e.g., should results use `PaginatedResults<PackageSummary>` from `common/src/model/paginated.rs`?)
- Whether to use SeaORM query methods, raw SQL, or the existing `SearchService`

Implementation cannot proceed without this guidance -- improvising these decisions risks building something that contradicts the intended architecture.

### Gap 2: Acceptance Criteria are vague

The Acceptance Criteria lack the specificity needed for implementation:

- **"Search results are relevant"** -- This is not actionable. What does "relevant" mean in this context? Is there a relevance ranking algorithm expected (e.g., exact match first, then prefix match, then substring)? Which fields determine relevance? Is ordering by relevance score required, or is any match sufficient?
- **"Performance is acceptable"** -- This is not measurable. What is the performance threshold? Is there a maximum response time requirement (e.g., < 200ms for 95th percentile)? Is there a maximum dataset size to test against? Without a concrete threshold, there is no way to verify this criterion in Step 8.

The first criterion ("Users can search for packages") is reasonable but still underspecified -- search by what? Name? Version? License? PURL? All fields?

### Gap 3: Test Requirements are vague

The single test requirement -- **"Test that search works correctly"** -- does not define what "correctly" means. This makes it impossible to write meaningful tests. Correct behavior could mean:

- Exact match on package name returns results
- Partial/substring match returns results
- Case-insensitive matching works
- No results returned for non-matching queries
- Pagination works with search results
- Empty search query behavior is defined
- Special characters are handled

Without specifying what "correctly" entails, any test written would be an improvisation rather than a verification of intended behavior.

---

## Execution stopped -- clarification required

Per constraint 1.6 and the skill's Important Rules ("If the structured description is incomplete, ask the user for clarification and **stop execution**. Do not draft an implementation plan, create branches, or proceed with any subsequent steps until the user provides the missing information."), I am stopping here.

I have not created any branches, drafted any implementation plan, or made any code changes.

### Clarifying questions

Please provide answers to the following before implementation can proceed:

1. **Which fields should the search operate on?** Should users be able to search by package name only, or also by version, license, PURL, or other fields in `PackageSummary`? Should there be a single search query parameter that searches across multiple fields, or separate filter parameters per field?

2. **What does "relevant" mean for search result ranking?** Should results be ranked by relevance (e.g., exact match > prefix match > substring match > fuzzy match), or is any unordered set of matches acceptable? Is there a specific relevance algorithm to use, or should this integrate with the existing `SearchService` in `modules/search/`?

3. **What is the concrete performance threshold?** What maximum response time is "acceptable" (e.g., < 200ms at P95)? Against what dataset size should this be measured? Are there indexing requirements (e.g., adding a database index on the search fields)?

4. **What specific test scenarios define "works correctly"?** For example: exact match returns results, no match returns empty, partial match behavior, case sensitivity, pagination with search, special character handling -- which of these are required?

5. **Should the Implementation Notes reference the existing `modules/search/` module?** The repository already has a `SearchService` with full-text search endpoints. Should the package search extend or reuse that service, or is this an independent search endpoint within the package module?

6. **What API contract is expected?** The API Changes section is missing. What should the endpoint path, HTTP method, query parameters, and response shape look like? Should it follow the existing pattern of returning `PaginatedResults<PackageSummary>`?

Please update the task description with the missing Implementation Notes, specific Acceptance Criteria, and detailed Test Requirements, then I will proceed with implementation.
