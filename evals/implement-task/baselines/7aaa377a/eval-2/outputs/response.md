# implement-task: TC-9202

## Step 0 -- Validate Project Configuration

Checked the project's CLAUDE.md (claude-md-mock.md). All required sections are present:

1. **Repository Registry** -- contains `trustify-backend` with Serena instance `serena_backend`
2. **Jira Configuration** -- contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field
3. **Code Intelligence** -- contains tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` with `rust-analyzer`

Validation passed. Proceeding to Step 1.

## Step 1 -- Fetch and Parse Jira Task

Parsed the task description for TC-9202. Extracted the following sections:

| Section | Status | Content |
|---|---|---|
| Repository | Present | trustify-backend |
| Target Branch | Present | main |
| Description | Present but vague | "Add search capabilities to the package module so users can find packages more easily." |
| Files to Modify | Present but incomplete | Only `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present but incomplete | Only `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **MISSING** | Not provided |
| Implementation Notes | **MISSING** | Not provided |
| Acceptance Criteria | Present but vague | Unmeasurable criteria |
| Test Requirements | Present but vague | Non-specific test description |
| Reuse Candidates | **MISSING** | Not provided (relevant existing code exists) |
| Dependencies | Not present | N/A (optional) |

### Identified Gaps

**STOP -- Execution halted.** The task description is incomplete and does not follow the structured template. The following gaps must be resolved before implementation can proceed:

#### 1. Missing: API Changes

The task is adding a search endpoint but does not specify:
- What is the endpoint path? (e.g., `GET /api/v2/package/search` or `GET /api/v2/package?q=...`)
- What HTTP method is used?
- What query parameters does the search accept? (e.g., `q` for free-text, filters for license, version, ecosystem)
- What is the response format? Does it return `PaginatedResults<PackageSummary>` following the existing list pattern?

#### 2. Missing: Implementation Notes

No implementation guidance is provided. The following must be specified:
- Which existing patterns to follow. The repo has similar search functionality in `modules/search/src/service/mod.rs` (SearchService: full-text search across entities) and `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService includes search). Should the package search reuse or extend the existing `SearchService`, or implement a standalone search within the package module?
- Which shared utilities to use from `common/src/db/query.rs` (filtering, pagination, sorting helpers)
- Whether to use PostgreSQL full-text search (`tsvector`/`tsquery`), simple `ILIKE` pattern matching, or the existing `SearchService` infrastructure
- What fields on the `package` entity are searchable (name, version, license, PURL, etc.)
- How the search endpoint integrates with existing route registration in `modules/fundamental/src/package/endpoints/mod.rs`

#### 3. Missing: Reuse Candidates

The repository has existing search infrastructure that is highly relevant:
- `modules/search/src/service/mod.rs` -- `SearchService` provides full-text search across entities
- `modules/search/src/endpoints/mod.rs` -- existing `GET /api/v2/search` endpoint
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, sorting
- `modules/fundamental/src/advisory/service/advisory.rs` -- `AdvisoryService` already includes search capability

The task should specify whether to reuse these existing modules or explain why new code is needed.

#### 4. Vague: Acceptance Criteria

The current acceptance criteria are not measurable:
- "Users can search for packages" -- By what fields? Name? Version? License? PURL? All of these?
- "Search results are relevant" -- What defines relevance? Exact match? Prefix match? Full-text with ranking? What ranking algorithm?
- "Performance is acceptable" -- What is the latency target? Under 200ms? Under 1s? For what dataset size?

These need to be specific and testable, for example:
- "Users can search packages by name using a `q` query parameter"
- "Search returns packages where the name contains the search term (case-insensitive)"
- "Search results are paginated using `PaginatedResults<PackageSummary>`"
- "Search endpoint responds within 500ms for datasets up to 10,000 packages"

#### 5. Vague: Test Requirements

"Test that search works correctly" is not specific enough to implement. Test requirements should specify concrete test cases, for example:
- "Test that searching by exact package name returns the matching package"
- "Test that searching by partial name returns all matching packages"
- "Test that searching with no results returns an empty paginated response"
- "Test that search respects pagination parameters (offset, limit)"
- "Test that searching with an empty query returns a 400 error (or all packages)"

Additionally, the test file path is not specified -- the repo convention places integration tests in `tests/api/` (e.g., `tests/api/package.rs` or `tests/api/package_search.rs`).

#### 6. Incomplete: Files to Modify

Only the endpoint registration file is listed. A search feature would likely also require:
- `modules/fundamental/src/package/service/mod.rs` -- add a `search` method to `PackageService`
- `modules/fundamental/src/package/mod.rs` -- re-export the new search endpoint module
- Possibly `server/src/main.rs` -- if search requires new route mounting beyond what the package module already registers
- Possibly `common/src/db/query.rs` -- if new query builder helpers are needed for search

#### 7. Incomplete: Files to Create

Only the endpoint handler is listed. A search feature would likely also require:
- A test file (e.g., `tests/api/package_search.rs`) for integration tests

---

## Action Required

Please provide the missing information for sections 1-7 above, or re-run `/plan-feature` to regenerate the task with a complete structured description. Implementation cannot proceed until the task description follows the required template with specific, measurable acceptance criteria and concrete implementation guidance.

No branches have been created. No code changes have been made. No Jira transitions have been performed.
