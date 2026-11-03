# implement-task: TC-9202 — Add package search functionality

## Step 0 – Validate Project Configuration

I read the project CLAUDE.md (`claude-md-mock.md`) and checked the `# Project Configuration` section:

| Required section | Status |
|---|---|
| `## Repository Registry` | Present. One entry: `trustify-backend` → Serena instance `serena_backend`, path `./` |
| `## Jira Configuration` | Present. Project key `TC`, Cloud ID `2b9e35e3-...`, Feature issue type ID `10142`. Also has the Git Pull Request field `customfield_10875` and the GitHub Issue field `customfield_10747` |
| `## Code Intelligence` | Present. Uses the `mcp__<serena-instance>__<tool>` convention. `serena_backend` runs rust-analyzer |

Result: configuration is valid, so I continue.

## Step 1 – Fetch and Parse Jira Task

I fetched TC-9202 (simulated `jira.get_issue("TC-9202")`; content taken from `task-incomplete.md`) and parsed the structured description against the plan-feature template.

### Section-by-section parse

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` (it is in the Repository Registry) |
| Target Branch | Present | `main` |
| Description | Present but **too vague to implement** | "Add search capabilities to the package module so users can find packages more easily." It doesn't say what to search on, how matching works, or what the response shape is |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` — add search route |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` — search endpoint handler |
| **API Changes** | **MISSING** | No endpoint path, HTTP method, query parameters, or response type |
| **Implementation Notes** | **MISSING** | No patterns, code references, or reusable utilities given |
| Acceptance Criteria | Present but **not verifiable** | "Users can search for packages", "Search results are relevant", "Performance is acceptable". None of these can be objectively checked |
| Test Requirements | Present but **not actionable** | "Test that search works correctly". No test cases, inputs, expected outputs, or test file location |
| Dependencies | Not present | Optional. The task is linked to the parent feature TC-9001 ("is incorporated by"), which is not a blocking dependency |
| Target PR / Review Context / Bookend Type | Not present | Optional. This is a normal default-flow task |

### Decision: STOP and ask for clarification

The description does not follow the template. Two required sections are missing, and the sections that are present are too vague to implement or verify. The skill says that in this case I must list the gaps, ask the user, and **stop execution immediately**.

So I am **not** doing any of the following:
- the description-integrity digest check (Step 1.5) or dependency checks (Step 2)
- assigning the issue or moving it to In Progress (Step 3)
- code inspection with Serena (Step 4)
- creating branch `TC-9202` from `main` (Step 5)
- drafting an implementation plan, writing code or tests, committing, opening a PR, or updating Jira (Steps 6–11)

I am also not filling the gaps with guesses (for example, inventing a `GET /api/v2/package/search?q=` endpoint).

---

## Clarification request to the user

> TC-9202 ("Add package search functionality") is missing information I need before I can implement it. Please update the Jira task, or reply with answers, and then re-run `/implement-task TC-9202`.
>
> **Missing required sections**
>
> 1. **API Changes** — please define the endpoint:
>    - HTTP method and path (for example, `GET /api/v2/package/search`, or a query parameter on the existing `GET /api/v2/package` list endpoint?)
>    - Query parameters: names, types, required or optional (for example, `q`, `limit`, `offset`, `sort`)
>    - Response type: should it return `PaginatedResults<PackageSummary>` like the existing list endpoint?
>    - Error responses: for example, 400 for an empty or invalid query
>
> 2. **Implementation Notes** — please name the patterns and code to follow or reuse. Specifically:
>    - Should this reuse the shared filtering, pagination, and sorting helpers in `common/src/db/query.rs`?
>    - Should it delegate to the existing `SearchService` in `modules/search/src/service/mod.rs` (full-text search across entities), or add a search method to `PackageService` in `modules/fundamental/src/package/service/mod.rs`? Note that changing `PackageService` would need that file added to Files to Modify.
>    - Which sibling endpoint should I use as the reference pattern? For example, `package/endpoints/list.rs`, or `AdvisoryService`'s search in `advisory/service/advisory.rs`?
>
> **Sections that are too vague to implement or verify**
>
> 3. **Description** — which package fields are searchable (name, version, purl, namespace, license)? Is matching exact, prefix, substring/`ILIKE`, or full-text (PostgreSQL `tsvector`)? Is it case-sensitive? Can filters be combined?
>
> 4. **Acceptance Criteria** — please replace them with criteria that can be checked. For example:
>    - "`GET /api/v2/package/search?q=openssl` returns 200 with a `PaginatedResults<PackageSummary>` containing only packages whose name contains `openssl` (case-insensitive)"
>    - "Results are ordered by <field>"
>    - "An empty `q` returns 400" (or returns all packages?)
>    - "Performance is acceptable" needs a measurable target, such as a latency budget or a required index. If a DB index or migration is needed, the `migration/` files also need to be in scope.
>
> 5. **Test Requirements** — please list concrete test cases and where they go. For example, a new `tests/api/package.rs`, or extending `tests/api/search.rs`? Note that test files are not in Files to Create or Files to Modify. Example cases: matching query returns the expected packages (by value), no match returns an empty result, pagination works, invalid parameters return 400.
>
> **Possible scope issues to confirm**
>
> - If search logic belongs in the service layer, `modules/fundamental/src/package/service/mod.rs` should be added to Files to Modify.
> - Integration tests need a test file under `tests/api/` in Files to Create or Files to Modify.
> - If the module re-exports or OpenAPI docs need updating, those files need to be listed too.
>
> If you'd rather regenerate the task, re-running `/plan-feature` for TC-9001 should produce a full description for TC-9202.

---

## What happens after clarification (for reference only, not executed)

Once the gaps are filled, I would continue in this order:
1. Step 1.5: verify the description digest.
2. Step 2: check dependencies.
3. Step 3: assign the issue to me and move it to In Progress.
4. Step 4: inspect the code with `mcp__serena_backend__*`, read `CONVENTIONS.md` for CI commands, and study sibling conventions in `package/endpoints/list.rs` and the advisory/sbom endpoints.
5. Step 5: create branch `TC-9202` from `main`.
6. Steps 6–8: implement within the approved scope, add documented value-based tests, and check each acceptance criterion.
7. Step 9: self-verify (scope containment, CI checks, `cargo test -p <crate>`).
8. Step 10: make a conventional commit with `Implements TC-9202` and the `Assisted-by: Claude Code` trailer, then open a PR with `--base main`.
9. Step 11: set the Jira field `customfield_10875` to the PR link, add a comment with the footnote, and move the issue to In Review.

None of these steps has been run, because the task description is incomplete.
