# implement-task: TC-9202 — Add package search functionality

## Step 0 – Validate Project Configuration

The project CLAUDE.md has every required section under `# Project Configuration`:

- **Repository Registry**: present, with one entry (`trustify-backend`, Serena instance `serena_backend`, path `./`)
- **Jira Configuration**: present (Project key `TC`, Cloud ID, Feature issue type ID `10142`, plus Git Pull Request field `customfield_10875` and GitHub Issue field `customfield_10747`)
- **Code Intelligence**: present, with the `mcp__<serena-instance>__<tool>` naming convention and the `serena_backend` instance (rust-analyzer)

Configuration is valid, so execution continues.

## Step 1 – Fetch and Parse Jira Task

I fetched TC-9202 (simulated via `jira.get_issue(TC-9202)`) and parsed its structured description:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` (add search route) |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` (search endpoint handler) |
| API Changes | **Missing** | No endpoint path, HTTP method, query parameters, or response shape |
| Implementation Notes | **Missing** | No patterns or code references to follow, and no reusable code listed |
| Acceptance Criteria | Present but not verifiable | "Users can search for packages", "Search results are relevant", "Performance is acceptable" |
| Test Requirements | Present but not actionable | "Test that search works correctly" (no test file, scenarios, or expected results) |
| Target PR / Bookend Type / Review Context | Not present | Optional. This is the default flow. |
| Dependencies | Not listed | — |

### Result: the task description is incomplete. Execution stops here.

The skill says: *"If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."* So I have **not**:

- run the description digest check, or verified dependencies
- assigned TC-9202 or moved it to In Progress in Jira
- created branch `TC-9202` from `main`
- inspected code with Serena, drafted an implementation plan, or written any code or tests
- committed, pushed, opened a PR, or commented on Jira

## Gaps and clarification questions

### 1. API Changes (missing)
The task says to "add search route" but gives no contract for it. Please specify:
- **Endpoint path and method.** For example, is it `GET /api/v2/package/search`, or a query parameter on the existing list endpoint, `GET /api/v2/package?q=...`?
- **Query parameters.** Is it a free-text `q`? Structured filters such as name, version, purl, license or ecosystem? Do pagination (`offset`/`limit`) and sorting apply?
- **Response shape.** Should it return `PaginatedResults<PackageSummary>` like the existing list endpoint (`common/src/model/paginated.rs`), or a different model?

### 2. Implementation Notes (missing)
No patterns or code references are given. The repository has several possible approaches, and the task needs to say which one to use:
- **`modules/search/` (`SearchService`)** already provides full-text search across entities at `GET /api/v2/search`. Should package search reuse or extend `SearchService`, or should it be a separate package-specific search?
- **`AdvisoryService` (`modules/fundamental/src/advisory/service/advisory.rs`)** already has a `search` operation. Should the package version follow that pattern?
- **`common/src/db/query.rs`** has shared filtering, pagination and sorting helpers. Should the search use them?
- **`PackageService` (`modules/fundamental/src/package/service/mod.rs`)** currently only offers fetch and list. A search handler will almost certainly need a new service method there, but that file is **not** in Files to Modify. Should it be added to scope? If yes, are any other files in scope, such as `package/model/` or `entity/package.rs` / `entity/package_license.rs` for license-based matching?

### 3. Description (too vague to implement)
"Find packages more easily" does not say what search means. Please clarify:
- Which fields are searchable (name, namespace, version, purl, license)?
- What kind of matching is wanted: exact, prefix, substring (`ILIKE`), or PostgreSQL full-text search?
- Is matching case-sensitive? What happens with an empty query?

### 4. Acceptance Criteria (not verifiable)
I cannot check any of the three criteria objectively in Step 8:
- **"Users can search for packages"**: by which fields, at which endpoint?
- **"Search results are relevant"**: what counts as relevant? Is there a ranking or ordering requirement, such as exact matches first or sorting by name?
- **"Performance is acceptable"**: what is the measurable target (for example p95 latency under N ms at M packages)? Is a database index needed? Index work would need a migration under `migration/`, which is also outside the current scope. Should the endpoint use the `tower-http` caching middleware like the other route builders?

Please restate these as concrete, testable criteria.

### 5. Test Requirements (not actionable)
"Test that search works correctly" names no test file or scenarios. Please specify:
- **Test file location.** For example, a new `tests/api/package.rs`. There is no package test file today; `tests/api/search.rs` covers the cross-entity search module. The test file is also missing from Files to Create.
- **Scenarios.** Examples: a matching query returns the expected packages (assert on values, not just counts), no match returns an empty result, pagination works, invalid parameters return 400, and an empty query behaves as defined.

## Next steps

Please update the Jira description for TC-9202 (or reply here) with the missing **API Changes** and **Implementation Notes**, a more specific **Description**, measurable **Acceptance Criteria**, concrete **Test Requirements**, and the expanded **Files to Modify / Files to Create** lists if extra files are needed. Another option is to re-run `/plan-feature` for TC-9001 to regenerate this task with full detail.

Once I have that information, I will re-run `/implement-task TC-9202` from Step 1: digest check, dependency check, assign and move to In Progress, then branch `TC-9202` from `main`, Serena code analysis via `serena_backend`, implementation, tests, self-verification, PR, and the Jira update.
