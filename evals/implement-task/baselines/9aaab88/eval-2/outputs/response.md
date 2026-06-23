# implement-task TC-9202 — Execution Halted: Incomplete Task Description

## Step 0 — Validate Project Configuration

Verified the project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** — present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** — present, contains Project key (`TC`), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** — present, with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Project configuration is valid. Proceeding to task fetch.

## Step 1 — Fetch and Parse Jira Task

Fetched TC-9202. Parsing the structured description against the expected template:

| Section | Status | Notes |
|---|---|---|
| Repository | Present | `trustify-backend` |
| Target Branch | Present | `main` |
| Description | **Incomplete** | Too vague — "Add search capabilities to the package module so users can find packages more easily" does not specify what search mechanism to use (full-text search, SQL LIKE, integration with the existing `search` module, etc.), what fields are searchable, or what the query parameters should be. |
| Files to Modify | Present | `modules/fundamental/src/package/endpoints/mod.rs` |
| Files to Create | Present | `modules/fundamental/src/package/endpoints/search.rs` |
| API Changes | **Missing** | No endpoint specification — what HTTP method, path, query parameters, request/response shape should the search endpoint use? |
| Implementation Notes | **Missing** | No patterns or code references provided. For a Rust/Axum backend with SeaORM, this section should reference existing patterns (e.g., how `advisory` search works in `modules/fundamental/src/advisory/service/advisory.rs`, how `common/src/db/query.rs` query helpers are used, how the `modules/search/` module relates to this task). |
| Acceptance Criteria | **Incomplete** | All three criteria are vague and unmeasurable: "Users can search for packages" (by what fields? what query format?), "Search results are relevant" (what defines relevance? ranking?), "Performance is acceptable" (what latency threshold? what dataset size?). |
| Test Requirements | **Incomplete** | Single generic line "Test that search works correctly" — no specific test scenarios, no error cases, no edge cases, no performance benchmarks specified. |
| Dependencies | Not present | No dependencies listed (acceptable if none exist). |
| Target PR | Not present | Not applicable (optional). |
| Bookend Type | Not present | Not applicable (optional). |

## Execution Stopped — Clarification Required

The structured description for TC-9202 is incomplete. The following gaps must be resolved before implementation can proceed:

### Missing Sections

1. **API Changes**: The task creates a search endpoint but does not specify:
   - What is the endpoint path? (e.g., `GET /api/v2/package/search` or a query parameter on the existing `GET /api/v2/package`?)
   - What query parameters does it accept? (e.g., `q`, `name`, `namespace`, `type`, `version`?)
   - What is the response shape? (e.g., `PaginatedResults<PackageSummary>` like other list endpoints?)
   - Are there any filters or sorting options?

2. **Implementation Notes**: The task does not reference any code patterns to follow. Key questions:
   - Should this integrate with the existing `modules/search/` full-text search module, or implement a separate query-based search within the package module?
   - What query mechanism should be used? (SQL `LIKE`/`ILIKE`, PostgreSQL full-text search `tsvector`/`tsquery`, or delegation to the `SearchService`?)
   - Which existing patterns should be followed? (e.g., the advisory module's search implementation in `modules/fundamental/src/advisory/service/advisory.rs`)
   - Should the `common/src/db/query.rs` shared query builder be extended, or should search logic be self-contained?

### Incomplete Sections

3. **Description**: Too vague to implement. Needs to specify:
   - What fields are searchable (package name, namespace, type, version, license, associated SBOMs)?
   - What kind of search (exact match, prefix, substring, full-text)?
   - Whether search supports combining multiple criteria

4. **Acceptance Criteria**: All three criteria are unmeasurable. They should specify:
   - Concrete searchable fields and expected behavior for each
   - What "relevant" means (e.g., exact matches ranked above partial matches)
   - Quantitative performance thresholds (e.g., "responds within 200ms for datasets up to 100k packages")

5. **Test Requirements**: The single generic test requirement should be expanded to cover:
   - Specific search scenarios (search by name, by namespace, by multiple fields)
   - Edge cases (empty query, no results, special characters)
   - Error cases (invalid parameters, malformed queries)
   - Response shape validation (correct fields, pagination)
   - Performance or load test requirements (if any)

**Please provide the missing information for these sections, then re-run `/implement-task TC-9202`.** No branches have been created, no code has been modified, and no Jira transitions have been made.
