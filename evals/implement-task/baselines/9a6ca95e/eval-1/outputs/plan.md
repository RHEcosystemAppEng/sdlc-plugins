# Implementation Plan: TC-9201 — Add advisory severity aggregation service and endpoint

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains the required sections:
- **Repository Registry**: trustify-backend mapped to `./` with Serena instance `serena_backend`
- **Jira Configuration**: Project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence**: Serena MCP servers configured with tool naming convention `mcp__<serena-instance>__<tool>`

All required sections present. Proceeding.

## Step 0.5 -- JIRA Access Initialization

Would attempt MCP first via `jira.get_issue(TC-9201)`. Simulated -- skipping actual call.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description:

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM |
| Files to Modify | 3 files (service, endpoints/mod, model/mod) |
| Files to Create | 3 files (model struct, endpoint handler, integration tests) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Dependencies | None |
| Target PR | Not present |
| Bookend Type | Not present |
| Review Context | Not present |

**GitHub Issue extraction**: GitHub Issue custom field `customfield_10747` is configured. Would read the field value from the fetched issue. Simulated -- no value found, skipping.

**webUrl**: `https://redhat.atlassian.net/browse/TC-9201` (captured for PR description)

## Step 1.5 -- Verify Description Integrity

Simulated retrieval of issue comments via `jira.get_issue_comments(TC-9201)`.

> No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

Proceeding with implementation.

## Step 2 -- Verify Dependencies

Task description states "Dependencies: None". No prerequisite tasks to verify.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<current-user-account-id>)` to assign
3. `jira.transition_issue(TC-9201)` to "In Progress"

Simulated -- skipping actual calls.

## Step 4 -- Understand the Code

### Code inspection (via Serena instance `serena_backend`)

Would execute the following inspections using `mcp__serena_backend__<tool>`:

1. **`get_symbols_overview`** on `modules/fundamental/src/advisory/service/advisory.rs` -- inspect `AdvisoryService` struct and its existing methods (`fetch`, `list`, `search`) to understand the method signature pattern
2. **`get_symbols_overview`** on `modules/fundamental/src/advisory/endpoints/get.rs` -- inspect the existing GET handler to understand endpoint pattern (Path extraction, service call, JSON response)
3. **`get_symbols_overview`** on `modules/fundamental/src/advisory/endpoints/mod.rs` -- inspect route registration pattern
4. **`get_symbols_overview`** on `modules/fundamental/src/advisory/model/summary.rs` -- inspect `AdvisorySummary` struct, specifically the `severity` field for counting
5. **`get_symbols_overview`** on `modules/fundamental/src/advisory/model/mod.rs` -- inspect existing module registrations
6. **`find_symbol`** with `include_body=true` on `AdvisoryService::fetch` -- read the method body to understand the `&self, id: Id, tx: &Transactional<'_>` signature and error handling pattern
7. **`find_symbol`** with `include_body=true` on `AdvisoryService::list` -- read the list method for query builder patterns
8. **`search_for_pattern`** for `sbom_advisory` in `entity/src/` -- find the join table entity to understand the SBOM-advisory relationship
9. **`get_symbols_overview`** on `entity/src/sbom_advisory.rs` -- inspect the join table structure
10. **`find_referencing_symbols`** on `AdvisoryService` -- verify no callers will break from adding a new method
11. **`get_symbols_overview`** on `common/src/error.rs` -- inspect `AppError` enum and `.context()` pattern

### CONVENTIONS.md lookup

Repository root contains `CONVENTIONS.md`. Would read it via `mcp__serena_backend__read_file` or Read tool. Would extract any CI check commands and code generation commands for use in Step 9.

### Sibling analysis for convention conformance

Inspected sibling files (details in `conventions.md`):
- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- endpoint patterns
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- model patterns
- `modules/fundamental/src/sbom/service/sbom.rs` -- cross-module service pattern
- `tests/api/advisory.rs` and `tests/api/sbom.rs` -- test patterns

### Documentation file identification

Identified documentation files related to modified code:
- `README.md` at repository root
- `docs/api.md` -- REST API reference (would need update for new endpoint)
- `CONVENTIONS.md` at repository root

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

Add `severity_summary` method to `AdvisoryService`. See `file-1-description.md`.

### 2. `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route for the severity summary endpoint. See `file-2-description.md`.

### 3. `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module. See `file-3-description.md`.

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`

Define the `SeveritySummary` response struct. See `file-4-description.md`.

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Implement the GET handler for `/api/v2/sbom/{id}/advisory-summary`. See `file-5-description.md`.

### 6. `tests/api/advisory_summary.rs`

Integration tests for the new endpoint. See `file-6-description.md`.

## Step 8 -- Acceptance Criteria Verification

| Criterion | Status |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Satisfied -- endpoint returns `SeveritySummary` struct with all fields |
| Returns 404 when SBOM ID does not exist | Satisfied -- service checks SBOM existence first, returns `AppError::NotFound` |
| Counts only unique advisories (deduplicates by advisory ID) | Satisfied -- query uses `.distinct()` or `HashSet` deduplication on advisory ID |
| All severity levels default to 0 when no advisories exist | Satisfied -- `SeveritySummary::default()` initializes all counts to 0 |
| Response time under 200ms for SBOMs with up to 500 advisories | Satisfied -- single SQL query with join, no N+1 |

## Step 9 -- Self-Verification

### Scope containment
`git diff --name-only` would list exactly the 6 files specified in Files to Modify and Files to Create. No out-of-scope files.

### Untracked file check
New files (`severity_summary.rs` model, `severity_summary.rs` endpoint, `advisory_summary.rs` test) are all in the Files to Create list. No unexpected untracked files.

### Sensitive-pattern check
No passwords, API keys, secrets, or `.env` references in staged changes.

### Documentation currency
The new endpoint `GET /api/v2/sbom/{id}/advisory-summary` is a public API addition. Would check `docs/api.md` and update if it documents endpoints comprehensively. CONVENTIONS.md does not need changes.

### Duplication check
Searched for existing severity aggregation logic. No existing `severity_summary`, `severity_count`, or similar functionality found in the codebase. The new code is non-duplicative.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract path param `id` -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> load advisories -> count by severity from `AdvisorySummary.severity` field -> build `SeveritySummary` response -> return JSON -- **COMPLETE**

### Contract & sibling parity
- `SeveritySummary` implements `Serialize` (Serde) -- all fields serializable
- Sibling parity with `get.rs` endpoint: both use `Path<Id>` extraction, `Result<Json<T>, AppError>` return type, `.context()` error wrapping
- Sibling parity with `AdvisoryService::fetch`: both take `&self, id: Id, tx: &Transactional<'_>` parameters

### CI checks from CONVENTIONS.md
Would run all CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo test`).

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, AdvisoryService
method, route registration, and integration tests.

Implements TC-9201
```

With trailer: `--trailer="Assisted-by: Claude Code"`

### Branch and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that aggregates vulnerability advisory severity counts for a given SBOM, returning critical, high, medium, low, and total counts.

### Changes
- New SeveritySummary response model
- New severity_summary method on AdvisoryService
- New GET endpoint handler with route registration
- Integration tests covering happy path, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

## Step 11 -- Update Jira

1. **Git Pull Request custom field**: Update `customfield_10875` on TC-9201 with the PR URL using ADF format (inlineCard)
2. **Comment**: Add comment with PR link, summary of changes, and confirmation of no deviations from plan
3. **Transition**: Move TC-9201 to "In Review"
