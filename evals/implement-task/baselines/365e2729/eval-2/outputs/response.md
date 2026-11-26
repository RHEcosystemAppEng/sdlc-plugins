# implement-task: TC-9202 — Add package search functionality

## Step 0 – Validate Project Configuration: PASSED

The project CLAUDE.md (`claude-md-mock.md`) contains every required section under `# Project Configuration`:

- **Repository Registry**: present. `trustify-backend` uses Serena instance `serena_backend` at path `./`.
- **Jira Configuration**: present. Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`. The Git Pull Request field (`customfield_10875`) and GitHub Issue field (`customfield_10747`) are also configured.
- **Code Intelligence**: present, with the `mcp__<serena-instance>__<tool>` naming convention. Known limitation: rust-analyzer can take 30–60 seconds to index on first use.

## Step 0.5 – Jira Access

The MCP method would be tried first, with the REST fallback prompt if MCP failed. This eval does not call Jira. The task content comes from `task-incomplete.md`.

## Step 1 – Fetch and Parse Jira Task: STOPPED (description is incomplete)

I parsed TC-9202's description against the structured template that plan-feature produces.

### Sections found

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but too vague | "Add search capabilities to the package module so users can find packages more easily." It doesn't say which fields are searched, what the query parameters are, or how results are matched or ranked. |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| **API Changes** | **MISSING** | No endpoint path, HTTP method, query parameters or response shape. |
| **Implementation Notes** | **MISSING** | No patterns, code references or reusable utilities named. |
| Acceptance Criteria | Present but can't be verified | "Users can search for packages", "Search results are relevant" and "Performance is acceptable" have no measurable conditions. |
| Test Requirements | Present but too vague | "Test that search works correctly" names no cases, inputs or expected outputs. |
| Dependencies | Not present | Optional. The issue is linked to parent feature TC-9001 ("is incorporated by"). |
| Target PR / Review Context / Bookend Type | Not present | Optional. This is the default flow. |

### Why I'm stopping

The skill says: *"If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."* Two required sections are missing (**API Changes** and **Implementation Notes**). Several other sections are too vague to implement or verify.

I have **not** done any of the following, and won't until you clarify:
- Step 1.5: check the description digest
- Step 2: verify dependencies
- Step 3: assign TC-9202 or move it to In Progress
- Step 4: inspect code with Serena
- Step 5: create branch `TC-9202` from `main`
- Steps 6–11: plan, write code or tests, commit, open a PR or update Jira

I have not drafted an implementation plan or guessed at a design.

## Questions for you

Please answer these, or update TC-9202 in Jira (ideally by re-running plan-feature for TC-9001), and then re-run `/implement-task TC-9202`.

1. **API Changes (missing)**
   - What is the endpoint path and method? For example, `GET /api/v2/package/search`, or a `q` query parameter on the existing `GET /api/v2/package`?
   - What query parameters does it take (e.g. `q`, `name`, `version`, `purl`, `license`), and which are required?
   - What does the response look like? Should it be `PaginatedResults<PackageSummary>` like the other list endpoints, and does it need `offset`/`limit` and sorting?

2. **Implementation Notes (missing)**
   - Should the handler use the shared filtering, pagination and sorting helpers in `common/src/db/query.rs`?
   - Should it reuse `modules/search/` (`SearchService`, which does full-text search across entities), or should package search be separate inside `modules/fundamental/src/package/`?
   - Which sibling should it follow? The advisory module looks like the closest example, since `AdvisoryService` already has a `search` operation.
   - Where does the query logic go? `modules/fundamental/src/package/service/mod.rs` (`PackageService`) is not listed in Files to Modify. If the logic belongs there, please add that file to the scope. Otherwise, should all the logic sit in `search.rs`?

3. **Description / matching rules**
   - Which fields are searched (name, namespace, version, PURL, license)?
   - How does matching work: exact, prefix, case-insensitive substring (`ILIKE`), or PostgreSQL full-text search?
   - How are results ordered or ranked?

4. **Acceptance Criteria (can't be verified as written)**
   - What does "relevant" mean? For example: "a query for `openssl` returns every package whose name contains `openssl`, case-insensitively".
   - What does "acceptable performance" mean? Is there a latency target or dataset size? Is a new DB index (and so a `migration/` change, currently out of scope) expected?
   - How should an empty query, no matches, or invalid parameters behave? For example, should an invalid request return 400 via `AppError`?

5. **Test Requirements**
   - Which cases do you want? For example: match by name, no results, pagination, case-insensitivity, invalid parameters.
   - Where do the tests go? `tests/api/` has `sbom.rs`, `advisory.rs` and `search.rs`, but no package test file. Should I create `tests/api/package.rs` (and add it to Files to Create)?

6. **Dependencies**
   - Does TC-9202 depend on any other TC-9001 tasks that must be Done first?

Once these sections are filled in, I'll continue from Step 1.5 (digest check) through Step 11.
