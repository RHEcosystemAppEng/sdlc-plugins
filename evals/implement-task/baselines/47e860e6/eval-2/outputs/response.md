# implement-task: TC-9202 — Add package search functionality

## Step 0 – Validate Project Configuration

I checked the project CLAUDE.md (claude-md-mock.md) under `# Project Configuration`:

| Required section | Status |
|---|---|
| Repository Registry | Present. `trustify-backend`, Serena instance `serena_backend`, path `./` |
| Jira Configuration | Present. Project key `TC`, Cloud ID, Feature issue type ID `10142` (also has the Git PR field `customfield_10875` and the GitHub Issue field `customfield_10747`) |
| Code Intelligence | Present. Naming convention `mcp__<serena-instance>__<tool>`, instance `serena_backend` (rust-analyzer) |

The configuration is valid, so I continue.

## Step 1 – Fetch and Parse Jira Task

In a real run this would be `jira.get_issue("TC-9202")`. For this eval the description comes from task-incomplete.md.

Sections I parsed from the structured description:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` (it is in the Repository Registry) |
| Target Branch | Present | `main` |
| Description | **Too vague** | "Add search capabilities to the package module so users can find packages more easily." It does not say which fields to search, how to match, the query parameter name or format, or what the response looks like. |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **Missing** | No HTTP method, path, query parameters or response type is given for the new search endpoint. |
| Implementation Notes | **Missing** | No patterns, code references or reusable helpers are given. |
| Acceptance Criteria | **Not verifiable** | "Users can search for packages", "Search results are relevant" and "Performance is acceptable" cannot be tested as written. |
| Test Requirements | **Not verifiable** | "Test that search works correctly" names no test cases, inputs or expected outputs. |
| Target PR / Review Context / Bookend Type | Not present | These are optional. This is a normal task flow. |
| Dependencies | Not listed | Linked issue: "is incorporated by TC-9001" (the parent feature). |
| GitHub Issue (customfield_10747) | Not available in mock | Optional, so I skip it. |

### Result: the task description is incomplete, so execution stops here

The task does not follow the plan-feature template closely enough to implement safely. The skill says: *"If any required section is missing or the description doesn't follow the template, list the gaps, ask the user for clarification, and stop execution immediately."*

So I am **not** proceeding to any of these:
- the description-integrity check, dependency verification, or Jira transition and assignment (Steps 1.5–3)
- code inspection or implementation planning (Steps 4 and 6)
- branch creation (`git checkout -b TC-9202`) (Step 5)
- code changes, tests, commits, PRs or Jira updates (Steps 6–11)

## Clarification needed from the user

Please give the following information (or update TC-9202 / re-run `/plan-feature` for TC-9001) before I implement this task:

1. **API Changes (missing)**
   - What are the HTTP method and path? For example, `GET /api/v2/package/search`, or a `q` query parameter on the existing `GET /api/v2/package` list endpoint?
   - What are the query parameters? Name (`q`? `name`? `purl`?), type, and whether each is required or optional. Should pagination (`offset`/`limit`) and sorting be supported?
   - What is the response shape? Is it `PaginatedResults<PackageSummary>` like the list endpoint, or something else?

2. **Description (too vague)**
   - Which package fields are searchable: name, namespace, version, PURL, license (`PackageSummary` has a license field), or something else?
   - What matching do you want: exact, prefix, case-insensitive substring (`ILIKE`), or PostgreSQL full-text search?
   - Should the endpoint be scoped to packages only, or relate to the existing cross-entity `SearchService` in `modules/search/`?

3. **Implementation Notes (missing)**
   - Which existing code should it follow? Candidates I would expect: `package/endpoints/list.rs` for handler and route structure, `AdvisoryService` search in `advisory/service/advisory.rs`, the shared filter, pagination and sort helpers in `common/src/db/query.rs`, and `modules/search/src/service/mod.rs`.
   - Should search logic go in `PackageService` (`package/service/mod.rs`)? That file is **not** in Files to Modify. Today the scope only allows the endpoint `mod.rs` and a new `search.rs`, so the service layer and the `tests/api/` files are out of scope. Please confirm whether the scope should be widened.
   - Are there caching requirements (tower-http cache config in the route builder)?

4. **Acceptance Criteria (not verifiable)**. Please replace them with concrete, testable criteria. For example:
   - `GET /api/v2/package/search?q=openssl` returns 200 with `PaginatedResults<PackageSummary>` containing only packages whose name matches `openssl` (case-insensitive).
   - An empty or missing `q` returns 400 (or all packages; please specify which).
   - No matches returns 200 with `items: []` and `total: 0`.
   - "Performance is acceptable": give a concrete target, such as p95 latency, a maximum page size, or a required index on the searched column.

5. **Test Requirements (not verifiable)**. Please list the specific test cases and where they live. Should they be integration tests in a new `tests/api/package.rs` (also currently out of scope), unit tests in `search.rs`, or both? Expected cases could include: a match returns the correct packages (value-based assertions), no match returns empty results, case-insensitivity, pagination, and invalid input returns an error.

6. **Dependencies**: are there prerequisite tasks under TC-9001 (for example, a service-layer or DB index task) that must be Done first?

When you provide these details, I will resume at Step 1.5 (description digest check). I will then verify dependencies, assign TC-9202 and move it to In Progress, inspect the package module with `serena_backend`, and implement on branch `TC-9202` off `main`.
