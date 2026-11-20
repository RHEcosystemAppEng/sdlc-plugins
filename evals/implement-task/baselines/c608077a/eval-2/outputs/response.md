# implement-task: TC-9202 — Add package search functionality

## Step 0 – Validate Project Configuration: PASSED

I checked the project CLAUDE.md (`claude-md-mock.md`). Every required section is present:

- **Repository Registry**: has one entry (`trustify-backend`, Serena instance `serena_backend`, path `./`)
- **Jira Configuration**: Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142` (plus Git Pull Request field `customfield_10875` and GitHub Issue field `customfield_10747`)
- **Code Intelligence**: has the tool naming convention `mcp__<serena-instance>__<tool>` and one configured instance, `serena_backend` (rust-analyzer)

## Step 0.5 – Jira Access

All Jira calls would go through the Atlassian MCP first, with the REST fallback prompt if MCP fails. In this eval the task description comes from `task-incomplete.md` instead of `jira.get_issue("TC-9202")`.

## Step 1 – Fetch and Parse Jira Task: INCOMPLETE DESCRIPTION, EXECUTION STOPPED

What I parsed:

| Section | Status | Content |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | Present but too vague to implement | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| API Changes | **MISSING** | No endpoint path, HTTP method, query parameters, or response shape |
| Implementation Notes | **MISSING** | No patterns, code references, or reuse guidance |
| Acceptance Criteria | Present but not testable | "Users can search", "results are relevant", "performance is acceptable" |
| Test Requirements | Present but not actionable | "Test that search works correctly" |
| Dependencies | Not specified | (it is unclear whether this means "none") |
| Target PR / Review Context / Bookend Type | Absent | Optional, so this is fine. This is a normal task: new branch, new PR |

The description does not follow the plan-feature template. The skill says that when required sections are missing or the description doesn't follow the template, I must list the gaps, ask the user, and **stop immediately**. So I am **not** going ahead with the digest check, dependency check, Jira transition or assignment, branch creation, an implementation plan, or any code changes.

### Gaps and questions for the user

**1. API Changes (missing)**
- What is the endpoint path and HTTP method? For example, `GET /api/v2/package/search?q=...`, or a `q`/filter query parameter added to the existing `GET /api/v2/package` list endpoint?
- Which query parameters are accepted (search term, filters such as name / version / purl / license, pagination `offset`/`limit`, sort)?
- What is the response shape? `PaginatedResults<PackageSummary>` (the same as `list.rs`) or a different model?

**2. Description: search semantics are not defined**
- Which fields are searched (package name, namespace, version, purl, license)?
- What kind of match: exact, prefix, substring/`ILIKE`, or full-text (PostgreSQL `tsvector`)?
- Should the match be case-sensitive?

**3. Implementation Notes (missing): overlap with existing search code needs a decision**
The repository already has search functionality, so the task needs to say how it relates to it:
- `modules/search/` has a `SearchService` for full-text search across entities, exposed at `GET /api/v2/search`. Should package search reuse or extend `SearchService`, or should it be a separate package-scoped endpoint? A separate endpoint could duplicate existing logic, which the skill's reuse-first rule warns against.
- `modules/fundamental/src/advisory/service/advisory.rs` (`AdvisoryService`) already has a `search` capability. Is that the reference pattern to follow?
- `common/src/db/query.rs` has shared filtering, pagination, and sorting helpers. Should the handler use those?
- `PackageService` (`modules/fundamental/src/package/service/mod.rs`) currently supports only fetch and list. If the search logic belongs in the service layer, as the `model/ + service/ + endpoints/` convention suggests, that file would need changes, but it is **not** listed in Files to Modify. Please confirm whether it is in scope, or whether all the logic should live in `search.rs`.

**4. Acceptance Criteria (not verifiable)**
In Step 8 I have to check each criterion, and I can't with the current wording:
- "Users can search for packages": by which parameters, and through which endpoint?
- "Search results are relevant": what counts as relevant? Is there an expected ranking or ordering?
- "Performance is acceptable": is there a concrete target (e.g. p95 latency under X ms for N packages)? Is a DB index expected? Adding one would need a migration under `migration/`, which is also not in scope.

**5. Test Requirements (not actionable)**
- Where should the tests go? Integration tests live in `tests/api/`, and there is no `tests/api/package.rs` yet. Creating it would be outside Files to Create.
- Which cases are needed: matching results, no results (empty page), pagination, invalid or empty query parameter (400?), case-insensitivity?
- What are the expected values? Tests should assert on returned package fields, not just counts.

**6. Dependencies**
- Does this task depend on any other tasks under TC-9001? If so, which ones? Please confirm whether there are none.

### Suggested next step

Please update TC-9202 in Jira with the missing **API Changes** and **Implementation Notes** sections and with concrete Acceptance Criteria and Test Requirements, or answer the questions above here. Re-running `/plan-feature` for TC-9001 to regenerate the task would also work. When the description is complete I will re-run `/implement-task TC-9202` and continue from Step 1.5: digest check, dependency check, assign and move to In Progress, code analysis with `serena_backend` (including `CONVENTIONS.md`), branch `TC-9202` from `main`, implementation, tests, self-verification, commit and PR, and the Jira update.

## Actions not taken (intentionally)

- No Jira transition or assignment (TC-9202 stays in **To Do**)
- No Jira comment
- No branch created, no code changes, no implementation plan drafted
- No commits, pushes, or PRs
