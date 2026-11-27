# implement-task: TC-9202 — Add package search functionality

## Step 0 – Validate Project Configuration

Checked the project CLAUDE.md (`claude-md-mock.md`) under `# Project Configuration`:

| Section | Status |
|---|---|
| Repository Registry | PASS — `trustify-backend` → Serena instance `serena_backend`, path `./` |
| Jira Configuration | PASS — Project key `TC`, Cloud ID, Feature issue type ID `10142` present (plus PR field `customfield_10875`, GitHub Issue field `customfield_10747`) |
| Code Intelligence | PASS — tool naming convention `mcp__<serena-instance>__<tool>` documented; `serena_backend` (rust-analyzer) |

Configuration is valid; proceeding to Step 1.

## Step 0.5 – Jira Access

Would attempt Atlassian MCP first (simulated here — no external calls made).

## Step 1 – Fetch and Parse Jira Task

`jira.get_issue(TC-9202)` (simulated from `task-incomplete.md`). Parsed sections:

| Section | Found? | Content / Assessment |
|---|---|---|
| Repository | Yes | `trustify-backend` |
| Target Branch | Yes | `main` → mode would be **default** (no Target PR, no Bookend Type) |
| Description | Yes, but vague | "Add search capabilities to the package module so users can find packages more easily." — no search fields, query semantics, or endpoint shape |
| Files to Modify | Yes | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Yes | `modules/fundamental/src/package/endpoints/search.rs` |
| **API Changes** | **MISSING** | No endpoint path, HTTP method, query parameters, or response shape |
| **Implementation Notes** | **MISSING** | No patterns or code references to follow |
| Acceptance Criteria | Present, but not verifiable | "Users can search for packages", "Search results are relevant", "Performance is acceptable" — none is testable |
| Test Requirements | Present, but not specific | "Test that search works correctly" — no cases, inputs, or expected results |
| Dependencies | Not present | (optional — nothing to check) |
| Target PR / Review Context / Bookend Type | Not present | (optional) |

The description does not follow the plan-feature template closely enough to implement. Per Step 1:
"If any required section is missing or the description doesn't follow the template, list the
gaps, ask the user for clarification, and **stop execution immediately**."

**Execution stops here.** I would not do any of the following:
- Step 1.5 digest check, Step 2 dependencies, Step 3 Jira transition/assignment
- Step 4 code exploration, Step 5 branch creation (`git checkout -b TC-9202`)
- Steps 6–11 (no code changes, no tests, no commit, no PR, no Jira updates)

---

## Clarification Request to the User

TC-9202 is missing information I need before I can start. Please answer the following (or
update the Jira description and re-run `/implement-task TC-9202`):

### Gap 1 — API Changes section is missing
1. What is the endpoint path and method? For example, `GET /api/v2/package/search`, or a
   query parameter on the existing list endpoint, `GET /api/v2/package?q=...`?
2. What query parameters does it accept (e.g. `q`, `name`, `version`, `license`, `purl`)
   and which are required?
3. What is the response shape? Should it return `PaginatedResults<PackageSummary>` like the
   existing `GET /api/v2/package` list endpoint, or a different type?
4. Should it support pagination and sorting through the shared helpers in
   `common/src/db/query.rs` (`offset`/`limit`/`sort`)?

### Gap 2 — Implementation Notes section is missing
5. Which existing code should this follow? Candidates in the repo:
   - `modules/fundamental/src/advisory/service/advisory.rs`: `AdvisoryService` already has
     a `search` method (closest sibling pattern).
   - `modules/search/` already has a `SearchService` for full-text search across entities,
     exposed at `GET /api/v2/search`. Should package search **reuse/extend** this service
     rather than add a separate endpoint in the package module? If a separate endpoint is
     still wanted, how should it differ from `/api/v2/search`?
6. Should the search logic go in `PackageService` (`modules/fundamental/src/package/service/mod.rs`)?
   That file is not listed in Files to Modify, so adding a service method would be
   out of scope as the task is written.
7. What kind of matching: exact, prefix, case-insensitive substring (`ILIKE`), or PostgreSQL
   full-text search? Do any database indexes or migrations need to be added (`migration/` is
   not in scope)?

### Gap 3 — Acceptance criteria cannot be verified
8. "Search results are relevant": which fields are matched, and how are results ranked or
   ordered (e.g. exact name match first, then alphabetical)?
9. "Performance is acceptable": is there a concrete target (e.g. p95 < 200 ms over N
   packages, a maximum page size)? Should `tower-http` cache configuration apply to this
   route, as with other endpoints?
10. How should empty queries, no matches, and invalid parameters behave (e.g. 200 with empty
    `items`, or 400 via `AppError`)?

### Gap 4 — Test requirements are not specific
11. Which test cases are expected? For example: match by name, match by license, no results,
    pagination, invalid or empty query → error status.
12. Where should tests go? The convention is integration tests in `tests/api/`. There is no
    `tests/api/package.rs` yet, and neither it nor `tests/api/search.rs` is listed in
    Files to Create or Files to Modify.

### Gap 5 — Scope and registration (informational)
13. Wiring a new route may also mean touching `modules/fundamental/src/package/endpoints/mod.rs`
    (listed) and possibly `server/src/main.rs` (not listed, though route mounting is
    normally per module). Please confirm whether OpenAPI or documentation updates
    (`docs/api.md`) are expected.

Once these are answered, I will continue from Step 1.5: verify the description digest,
transition TC-9202 to In Progress, inspect the package and advisory modules via
`serena_backend`, read `CONVENTIONS.md`, branch `TC-9202` from `main`, and implement.
