# implement-task: TC-9202 — Add package search functionality

## Step 0 – Validate Project Configuration

Checked the project CLAUDE.md (claude-md-mock.md) under `# Project Configuration`:

| Section | Status |
|---|---|
| Repository Registry | Present: `trustify-backend` -> Serena instance `serena_backend`, path `./` |
| Jira Configuration | Present: Project key `TC`, Cloud ID, Feature issue type ID `10142` (plus Git PR field `customfield_10875`, GitHub Issue field `customfield_10747`) |
| Code Intelligence | Present: naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer) |

Configuration is valid. Continuing.

## Step 1 – Fetch and Parse Jira Task

I fetched TC-9202 (simulated `jira.get_issue("TC-9202")`; content taken from task-incomplete.md) and parsed it against the structured template:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` (matches the Repository Registry) |
| Target Branch | Present | `main` |
| Description | Present but too vague | "Add search capabilities to the package module so users can find packages more easily." It doesn't say which fields to search, how to match, what the query parameters are, or what the response looks like. |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| **API Changes** | **Missing** | No endpoint path, HTTP method, query parameters, or response shape |
| **Implementation Notes** | **Missing** | No patterns, code references, or reusable helpers listed |
| Acceptance Criteria | Present but can't be tested | "Users can search", "results are relevant", "performance is acceptable" have no measurable conditions |
| Test Requirements | Present but too vague | "Test that search works correctly" names no scenarios, inputs, or expected outputs |
| Dependencies | Not listed | Fine, no dependency checks needed |
| Target PR / Review Context / Bookend Type | Not present | Fine, they're optional. This would be the default flow. |

**The description doesn't follow the template, so I'm stopping here.** The skill says that when required sections are missing or the description is incomplete, I must list the gaps, ask for clarification, and stop. I won't check integrity, check dependencies, change Jira status or assignee, create a branch, plan the implementation, or change any code until you send the missing information.

## Clarification needed for TC-9202

Please update the Jira task, or reply here, with the following:

### 1. API Changes (missing)
- **Endpoint path and method.** For example, `GET /api/v2/package/search`, or a query parameter on the existing `GET /api/v2/package` list endpoint (such as `?q=`)? The task plans a separate `search.rs` handler. Please confirm it should be a separate route.
- **Request parameters.** What are the parameter names and types (`q`, `name`, `version`, `license`, `purl`, ...)? Which are required? Should pagination (`offset`/`limit`) and sorting be supported?
- **Response shape.** Should it return `PaginatedResults<PackageSummary>` like the other list endpoints, or a different model?

### 2. Implementation Notes (missing)
- **Relation to the existing `search` module.** The repo already has `modules/search/` with `SearchService` (full-text search across entities, `GET /api/v2/search`). `AdvisoryService` also has a `search` method (`modules/fundamental/src/advisory/service/advisory.rs`). Should package search reuse or extend `SearchService` or the advisory search pattern instead of adding new search logic?
- **Query helpers.** Should filtering, pagination, and sorting use the shared helpers in `common/src/db/query.rs`?
- **Service layer.** Does `PackageService` (`modules/fundamental/src/package/service/mod.rs`) need a new `search` method? That file isn't in Files to Modify. If the logic belongs in the service layer, as the `model/ + service/ + endpoints/` convention suggests, please add it to scope.
- **Matching semantics.** Exact match, prefix, `ILIKE` substring, or PostgreSQL full-text search? Should it be case-insensitive?

### 3. Description (too vague)
- Which package fields can be searched (name, namespace, version, PURL, license)?
- Should results be scoped by SBOM, or cover all packages?

### 4. Acceptance Criteria (can't be tested)
Please replace them with checkable criteria. For example:
- "`GET /api/v2/package/search?q=openssl` returns packages whose name contains `openssl`, case-insensitive"
- "Results are paginated and returned as `PaginatedResults<PackageSummary>`"
- "An empty or missing `q` returns 400" (or "returns all packages")
- **What counts as "relevant"?** What ordering or ranking is expected?
- **What counts as "acceptable performance"?** For example, a latency target at a given data volume, or "the query uses an index on `package.name`".

### 5. Test Requirements (too vague)
Please list concrete test scenarios. For example:
- A match on name returns the expected packages (checked by value, not just count)
- No match returns an empty result
- Pagination limits and offsets are respected
- Invalid or missing parameters return the expected error status

Also: which test file should hold them? `tests/api/` has no `package.rs`. Should a new `tests/api/package.rs` go in Files to Create, or should the tests extend `tests/api/search.rs`?

### 6. Scope check
Registering the route may also touch `server/main.rs` if the package routes aren't already mounted. Please confirm that only `endpoints/mod.rs` and `endpoints/search.rs` are in scope, or add any other files needed (for example the `PackageService` file and the test file).

---

**Status: blocked, waiting for clarification.** Once the task description includes API Changes and Implementation Notes, and the Description, Acceptance Criteria and Test Requirements are specific enough to implement and check, re-run `/implement-task TC-9202`. I'll then continue with the description integrity check, dependency verification, assigning the task and moving it to In Progress, code analysis through `serena_backend`, and so on.

No Jira updates, branches, or code changes have been made.
