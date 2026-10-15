# implement-task: TC-9202

## Step 0 -- Validate Project Configuration

Checked CLAUDE.md for required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID, and Feature issue type ID.
3. **Code Intelligence** -- present, includes tool naming convention (`mcp__<serena-instance>__<tool>`), configured instance `serena_backend` with `rust-analyzer`.

All required sections are present. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Would attempt to fetch TC-9202 via MCP (`jira.get_issue(TC-9202)`). (Skipped per eval instructions -- not calling external tools.)

## Step 1 -- Fetch and Parse Jira Task

Parsed the structured description for TC-9202. Here is what was found:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **Missing** | Not provided |
| Implementation Notes | **Missing** | Not provided |
| Acceptance Criteria | Present but **vague** | All three criteria are non-specific and not testable |
| Test Requirements | Present but **vague** | Single item with no concrete test cases |
| Target PR | Not present | (optional -- OK) |
| Bookend Type | Not present | (optional -- OK) |
| Dependencies | Not present | (optional -- OK) |

### Gaps Identified

The task description is **incomplete** and does not follow the structured template expected by this skill. The following gaps prevent implementation:

**1. Missing: Implementation Notes**

This section is required to understand which existing patterns, code references, utilities, and shared modules to follow. Without it, I cannot determine:

- Which query builder patterns to use from `common/src/db/query.rs`
- How to integrate with the existing `PackageService` in `modules/fundamental/src/package/service/mod.rs`
- Whether to use the existing `SearchService` from `modules/search/` or build package-specific search logic
- What response types to use (e.g., `PaginatedResults<PackageSummary>` or a different type)
- How to register the new route in `endpoints/mod.rs` (what path, what method)

**2. Missing: API Changes**

No endpoint specification is provided. I need to know:

- The HTTP method and URL path (e.g., `GET /api/v2/package/search?q=...`)
- Query parameters (search term, filters, pagination parameters)
- Request body format (if POST)
- Response body format and fields
- Whether this should be a new endpoint or a query parameter added to the existing `GET /api/v2/package` list endpoint

**3. Vague: Acceptance Criteria**

The three criteria are not specific or testable:

- "Users can search for packages" -- search by what? Package name? Version? License? PURL? All fields?
- "Search results are relevant" -- what ranking or matching algorithm is expected? Exact match? Substring? Full-text search? What constitutes "relevant"?
- "Performance is acceptable" -- what is the performance target? Response time SLA? Maximum result set size? Index requirements?

**4. Vague: Test Requirements**

"Test that search works correctly" provides no actionable test specification. I need:

- Specific test cases (e.g., search by exact name returns match, search with no results returns empty, partial match behavior)
- Edge cases to cover (empty query, special characters, very long queries)
- Performance test expectations (if any)
- Which test file to create or modify (the repo has `tests/api/` for integration tests)

**5. Ambiguity: Relationship with existing search module**

The repository already has a `modules/search/` module with a `SearchService` providing full-text search across entities and a `GET /api/v2/search` endpoint. The task description does not clarify whether the package search should:

- Extend the existing `SearchService` with package-specific logic
- Add a dedicated search endpoint under the package module (`/api/v2/package/search`)
- Add search/filter query parameters to the existing `GET /api/v2/package` list endpoint

---

## Execution Halted -- Clarification Required

Per the implement-task skill rules (Step 1 and Important Rules), when the structured description is incomplete, I must ask for clarification and **stop execution immediately**. I will not proceed with branching, implementation planning, code changes, or any subsequent steps until the missing information is provided.

**To unblock this task, please provide:**

1. **Implementation Notes** -- Which existing patterns and code references should the search endpoint follow? Specifically:
   - Should this reuse `SearchService` from `modules/search/` or implement search logic directly in `PackageService`?
   - Which query helpers from `common/src/db/query.rs` should be used?
   - What is the route registration pattern to follow in `endpoints/mod.rs`?

2. **API Changes** -- What is the endpoint specification?
   - HTTP method and path
   - Query parameters or request body schema
   - Response format

3. **Specific Acceptance Criteria** -- Testable criteria replacing the vague ones, e.g.:
   - "Users can search packages by name using a `q` query parameter"
   - "Search returns `PaginatedResults<PackageSummary>` matching the existing list endpoint format"
   - "Search responds within 200ms for queries against 10k packages"

4. **Specific Test Requirements** -- Concrete test cases, e.g.:
   - "Search by exact package name returns the matching package"
   - "Search with no matches returns an empty paginated result"
   - "Search with empty query returns all packages (falls back to list behavior)"

Please update the task description in Jira or provide the missing information here so I can proceed.
