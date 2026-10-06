# implement-task: TC-9202 — Add package search functionality

## Step 0 — Validate Project Configuration

Read the project's CLAUDE.md (from `claude-md-mock.md`) and verified the required sections under `# Project Configuration`:

1. **Repository Registry** — Present. Contains one entry: `trustify-backend` with Serena instance `serena_backend` at path `./`.
2. **Jira Configuration** — Present. Contains Project key (`TC`), Cloud ID, Feature issue type ID (`10142`), Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`).
3. **Code Intelligence** — Present. Documents the tool naming convention (`mcp__<serena-instance>__<tool>`) and lists `serena_backend` with `rust-analyzer`.

All required sections are present. Proceeding.

## Step 0.5 — JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, would prompt user with the REST API fallback options as specified in the skill.

*(Eval mode: skipping actual JIRA calls.)*

## Step 1 — Fetch and Parse Jira Task

Fetched TC-9202. Parsed the structured description:

| Section | Status | Value |
|---|---|---|
| **Repository** | Present | `trustify-backend` |
| **Target Branch** | Present | `main` |
| **Description** | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| **Files to Modify** | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| **Files to Create** | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| **API Changes** | **MISSING** | Not present in the task description |
| **Implementation Notes** | **MISSING** | Not present in the task description |
| **Acceptance Criteria** | Present but vague | Three vague items (see below) |
| **Test Requirements** | Present but vague | One vague item (see below) |
| **Target PR** | Not present | Optional — no review feedback fix |
| **Review Context** | Not present | Optional — no review context |
| **Bookend Type** | Not present | Optional — normal implementation task |
| **Dependencies** | Not present | None listed |

### Extracted values

- **Target Branch**: `main`
- **Target PR**: none (new branch and PR flow)
- **Bookend Type**: none (normal implementation flow)
- **GitHub Issue custom field**: `customfield_10747` is configured in CLAUDE.md; would read from fetched issue fields. *(Eval mode: not available.)*
- **Issue webUrl**: would capture from API response for PR description link (e.g., `https://redhat.atlassian.net/browse/TC-9202`).

## Execution Halted — Incomplete Task Description

The task description does not follow the required template. The following gaps prevent implementation:

### Missing required sections

1. **API Changes** — No information about the search endpoint:
   - What is the endpoint path? (e.g., `GET /api/v2/package/search` or query parameter on `GET /api/v2/package`?)
   - What HTTP method?
   - What query parameters does the search accept? (e.g., `q`, `name`, `license`, `purl`?)
   - What is the response format? (e.g., `PaginatedResults<PackageSummary>`?)
   - Does it support pagination, sorting, or filtering?

2. **Implementation Notes** — No guidance on patterns or code references:
   - Should the search use the existing `SearchService` from `modules/search/`? Or implement search directly in `PackageService`?
   - Should it use PostgreSQL full-text search (`tsvector`/`tsquery`), SQL `LIKE`/`ILIKE`, or the existing query helpers from `common/src/db/query.rs`?
   - What existing code patterns should be followed? (The repo has `AdvisoryService` with a `search` method in `modules/fundamental/src/advisory/service/advisory.rs` — should the package search follow that pattern?)
   - Should the search handler integrate with `common/src/db/query.rs` shared filtering and pagination?
   - What fields on the `Package` entity should be searchable?

### Vague acceptance criteria

The acceptance criteria are not actionable:

- "Users can search for packages" — By what fields? Using what interface?
- "Search results are relevant" — What relevance ranking is expected? Exact match? Substring? Full-text with scoring?
- "Performance is acceptable" — What performance threshold? What dataset size? Is indexing required?

### Vague test requirements

- "Test that search works correctly" — What test scenarios? What search inputs and expected outputs? Should it test empty results, partial matches, pagination, edge cases?

### Information needed to proceed

Please provide the following before implementation can begin:

1. **API Changes**: Endpoint path, HTTP method, query parameters, and response type for the package search endpoint.
2. **Implementation Notes**: Which search mechanism to use (full-text search, SQL LIKE, existing `SearchService`, or query helpers), which entity fields are searchable, and which existing code patterns to follow (e.g., the advisory search pattern).
3. **Acceptance Criteria** with specific, testable conditions (e.g., "Search by package name returns matching packages", "Search supports pagination via `offset` and `limit` query parameters").
4. **Test Requirements** with specific test scenarios (e.g., "Test search with matching name returns results", "Test search with no matches returns empty paginated response", "Test search with special characters does not error").

**Execution stopped.** No subsequent steps (branching, code inspection, implementation, or Jira updates) will proceed until the user provides the missing information.
