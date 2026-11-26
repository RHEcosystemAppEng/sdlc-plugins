# implement-task: TC-9202 — Execution Halted, Clarification Required

## Step 0 – Validate Project Configuration: PASSED

The project CLAUDE.md (claude-md-mock.md) contains every required section under `# Project Configuration`:

- **Repository Registry**: `trustify-backend` (Rust backend service, Serena instance `serena_backend`, path `./`)
- **Jira Configuration**: Project key `TC`, Cloud ID `2b9e35e3-6bd3-4cec-b838-f4249ee02432`, Feature issue type ID `10142`. Also present: Git Pull Request field `customfield_10875`, GitHub Issue field `customfield_10747`
- **Code Intelligence**: tool naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer)

## Step 0.5 – Jira Access

In a real run, every Jira operation would try the Atlassian MCP first and offer the REST API fallback if MCP failed. For this eval, the task was read from `task-incomplete.md` and no Jira calls were made.

## Step 1 – Fetch and Parse Jira Task: INCOMPLETE DESCRIPTION, STOPPING

Parsed TC-9202 ("Add package search functionality"):

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` (matches Registry) |
| Target Branch | Present | `main` |
| Description | **Too vague** | "Add search capabilities to the package module so users can find packages more easily." It does not say what to search on, how matching works, or what the response looks like. |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **Missing** | No endpoint path, HTTP method, query parameters, or response type given |
| Implementation Notes | **Missing** | No patterns or code to follow, no reusable code listed |
| Acceptance Criteria | **Present but can't be checked** | "Users can search for packages", "Search results are relevant", "Performance is acceptable" are all subjective. None can be verified in Step 8. |
| Test Requirements | **Present but can't be checked** | "Test that search works correctly" names no scenarios, inputs or expected outputs |
| Dependencies | Not specified | None listed |
| Target PR / Review Context / Bookend Type | Not present | Optional. This would be a default-flow task. |
| GitHub Issue (customfield_10747) | Not available in mock | Optional, skipped |

The description does not meet the plan-feature template. The skill says that when required sections are missing or incomplete it must **list the gaps, ask the user for clarification, and stop immediately**. So I am **not** doing any of the following:

- Step 1.5 digest check / Step 2 dependency check / Step 3 transition to In Progress and assign
- Step 4 code inspection via `serena_backend`
- Step 5 branch creation (`git checkout -b TC-9202`)
- Drafting an implementation plan or writing any code or tests

## Questions for the User

Please fill in the following, ideally by updating the Jira description or re-running `/plan-feature` for TC-9001:

1. **API Changes**: What exactly is the endpoint contract?
   - Path and method, e.g. `GET /api/v2/package/search`? Or should search be a query parameter (`?q=`) on the existing `GET /api/v2/package` list endpoint?
   - Query parameters: a free-text `q`, or specific field filters (name, namespace, version, purl, license)? Should pagination and sorting params be supported?
   - Response type: `PaginatedResults<PackageSummary>` (matching the list endpoint), or something else?

2. **Search semantics (Description)**:
   - Which fields are searched (name, purl, version, license, ...)?
   - Matching type: exact, prefix, case-insensitive substring (`ILIKE`), or PostgreSQL full-text search?
   - How are results ordered, and what counts as "relevant"?

3. **Implementation Notes / reuse**: The repository already has code that may overlap. Which of these should this task use?
   - `modules/search/` — `SearchService` (full-text search across entities) and `GET /api/v2/search`. Should package search delegate to or extend it, rather than adding a separate implementation in the `fundamental` module?
   - `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` already has a `search` operation. Is that the pattern to copy?
   - `common/src/db/query.rs` — shared filtering, pagination and sorting helpers
   - `modules/fundamental/src/package/endpoints/list.rs` and `package/service/mod.rs` (`PackageService`). Should a `search` method be added to `PackageService`? If so, `package/service/mod.rs` must be added to **Files to Modify**, because the current scope only lists the endpoints files.

4. **Acceptance Criteria**: Please make them measurable, for example:
   - "`GET /api/v2/package/search?q=openssl` returns 200 with a `PaginatedResults<PackageSummary>` containing only packages whose name contains `openssl` (case-insensitive)"
   - "An empty result set returns 200 with `items: []` and `total: 0`"
   - "A missing or empty `q` returns 400 (or acts like the list endpoint, which?)"
   - "Performance is acceptable": give a concrete target (e.g. p95 latency under X ms at N packages), or say whether a DB index or migration is needed (that would add files to scope)

5. **Test Requirements**: Which scenarios are needed, and where should the tests live? Siblings are in `tests/api/` (e.g. `tests/api/search.rs`, `tests/api/sbom.rs`), and no `tests/api/package.rs` exists yet. Should it be added to **Files to Create**? Suggested scenarios: match found, no match, pagination, case-insensitivity, invalid or empty query.

6. **Dependencies**: Does this task depend on any other TC-9001 tasks, for example a migration or index, being Done first?

## Next Steps

Once the description is updated, re-run `/implement-task TC-9202`. The skill will then:

1. Re-fetch the task and verify the description digest
2. Check dependencies
3. Assign the task and move it to In Progress
4. Inspect the code via `serena_backend`, including `CONVENTIONS.md` and sibling conventions
5. Create branch `TC-9202` from `main`
6. Implement and test
7. Self-verify
8. Commit with an `Implements TC-9202` footer and open a PR against `main`
9. Update Jira: set PR field `customfield_10875`, add a comment, move to In Review
