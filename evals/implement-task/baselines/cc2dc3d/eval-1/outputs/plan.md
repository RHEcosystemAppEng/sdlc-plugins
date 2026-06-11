# Implementation Plan for TC-9201

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), GitHub Issue custom field (`customfield_10747`)
3. **Code Intelligence** -- present, lists tool naming convention (`mcp__<serena-instance>__<tool>`) and configured instance `serena_backend` with `rust-analyzer`

Validation passes. Proceeding.

## Step 1 -- Parse Task Description

Parsed fields from TC-9201:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
  - `tests/api/advisory_summary.rs` -- integration tests for the new endpoint
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Implementation Notes**: Follow existing patterns in `get.rs`, `advisory.rs` service, use `sbom_advisory` join table, count by severity from `AdvisorySummary`, register route in `endpoints/mod.rs`, return `AppError` with `.context()`, return struct directly via Axum `Json`
- **Acceptance Criteria**: 5 criteria covering correct response shape, 404 on missing SBOM, deduplication, zero defaults, and performance
- **Test Requirements**: 4 tests covering valid SBOM counts, 404, empty SBOM, and deduplication
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Review Context**: not present
- **Dependencies**: None

No GitHub Issue custom field value to extract (would check `customfield_10747` on the fetched issue).

The issue `webUrl` would be captured as `https://redhat.atlassian.net/browse/TC-9201`.

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9201)` and search for comments starting with `[sdlc-workflow] Description digest:`.

No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

## Step 2 -- Verify Dependencies

The task lists "Dependencies: None". No prerequisite tasks to verify. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to retrieve current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<current-user-account-id>)` to assign the task
3. `jira.transition_issue(TC-9201)` to transition to In Progress

## Step 4 -- Understand the Code

### Files inspected

Would use the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`) to inspect:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- understand existing endpoint pattern: how path params are extracted via `Path<Id>`, how the service is called, how JSON responses are returned, and how errors are handled with `Result<T, AppError>`.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- understand existing service methods (`fetch`, `list`, `search`): their signatures (taking `&self, id: Id, tx: &Transactional<'_>`), how they query the database using SeaORM, and how they return `Result<T, AppError>` with `.context()` error wrapping.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- understand the `AdvisorySummary` struct, specifically the `severity` field that will be used to count by severity level.

4. **`common/src/error.rs`** -- understand the `AppError` enum and its `IntoResponse` implementation for consistent error handling.

5. **`entity/src/sbom_advisory.rs`** -- understand the SBOM-Advisory join table entity for querying advisories linked to a specific SBOM.

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- understand the route registration pattern (`Router::new().route("/path", get(handler))`).

7. **`modules/fundamental/src/advisory/model/mod.rs`** -- understand how model sub-modules are registered with `pub mod` statements.

### Documentation file identification

Would check for:
- `docs/api.md` -- referenced in CLAUDE.md, would need updating with the new endpoint
- `docs/architecture.md` -- referenced in CLAUDE.md, likely no changes needed
- `CONVENTIONS.md` -- would check at repository root for project conventions and CI check commands

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). The repo structure shows it exists. Would read it and extract any CI check commands and code generation commands for use in Step 9.

### Convention conformance analysis

See outputs/conventions.md for the full discovered conventions.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

## Step 6 -- Implementation Plan

All changes are scoped to the Files to Modify and Files to Create from the task description.

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- New file containing the `SeveritySummary` response struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Derives `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default`, `utoipa::ToSchema`. Includes a doc comment explaining the struct's purpose. See file-1-description.md.

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- New file containing the GET handler for `/api/v2/sbom/{id}/advisory-summary`. Extracts `Path<Id>` for the SBOM ID, calls `AdvisoryService::severity_summary()`, returns `Json<SeveritySummary>`. Error handling with `Result<Json<SeveritySummary>, AppError>`. See file-2-description.md.

3. **`tests/api/advisory_summary.rs`** -- New file containing integration tests: test valid SBOM returns correct severity counts, test non-existent SBOM returns 404, test SBOM with no advisories returns all zeros, test deduplication of advisory links. See file-3-description.md.

### Files to Modify

4. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to `AdvisoryService`. Takes `&self, sbom_id: Id, tx: &Transactional<'_>`, queries `sbom_advisory` join table for advisories linked to the SBOM, fetches their severity via `AdvisorySummary`, deduplicates by advisory ID, counts by severity level, returns `Result<SeveritySummary, AppError>`. See file-4-description.md.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Add `mod severity_summary;` declaration and register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))`. See file-5-description.md.

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` line to register the new model module. See file-6-description.md.

Note: `server/src/main.rs` is listed in Files to Modify but explicitly states "no changes needed" since routes auto-mount via module registration. No modifications will be made to this file.

### Documentation impact

Would check `docs/api.md` for API documentation that needs updating with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. If the API documentation lists endpoints, would add an entry for the new one.

## Step 7 -- Write Tests

Tests are detailed in file-3-description.md. Would run `cargo test` after writing tests and fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

Each acceptance criterion would be verified:
1. GET /api/v2/sbom/{id}/advisory-summary returns correct shape -- verified by test and endpoint implementation
2. Returns 404 for non-existent SBOM -- verified by test and error handling in service
3. Counts only unique advisories -- verified by deduplication logic using HashSet on advisory ID
4. Severity levels default to 0 -- verified by using `SeveritySummary::default()` and test for empty SBOM
5. Response time under 200ms -- verified by efficient single query with join (no N+1)

## Step 9 -- Self-Verification

Would perform:
- **Scope containment**: `git diff --name-only` to verify only in-scope files are modified
- **Untracked file check**: `git status --short` to find untracked files and verify they are in scope
- **Sensitive-pattern check**: scan staged diff for secrets/credentials
- **Documentation currency**: verify docs are updated if needed
- **CI checks from CONVENTIONS.md**: run any CI commands extracted from CONVENTIONS.md
- **Duplication check**: search for existing severity counting or aggregation logic
- **Data-flow trace**: trace from HTTP request -> path param extraction -> service call -> DB query -> count aggregation -> JSON response (all stages connected)
- **Contract & sibling parity**: verify SeveritySummary struct and handler follow the same patterns as sibling implementations (AdvisorySummary, AdvisoryDetails, get.rs, list.rs)
- **Cross-section reference consistency**: verify all file paths referenced in task description are consistent across sections (Files to Modify, Files to Create, and Implementation Notes all reference consistent paths)

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201
```

Command:
```
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

### Push and PR

```
git push -u origin TC-9201
```

```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that aggregates
vulnerability advisory severity counts for a given SBOM, returning counts per
severity level (Critical, High, Medium, Low) and a total.

### Changes
- New `SeveritySummary` model struct
- New `severity_summary` method on `AdvisoryService`
- New endpoint handler with route registration
- Integration tests covering happy path, 404, empty SBOM, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

The PR explicitly targets `--base main` (the Target Branch from the task description).

## Step 11 -- Update Jira

Would execute:
1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
2. Add a Jira comment with PR link, summary of changes, and confirmation of no deviations from the plan
3. Transition TC-9201 to In Review via `jira.transition_issue`
