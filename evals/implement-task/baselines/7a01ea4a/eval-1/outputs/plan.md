# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main (extracted from the Target Branch section of the task description)
**Parent Feature**: TC-9001 (this task is incorporated by TC-9001)

## Step 0 -- Validate Project Configuration

Verified that CLAUDE.md contains the required sections:
- Repository Registry: contains trustify-backend with Serena instance `serena_backend` at path `./`
- Jira Configuration: contains Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (customfield_10875), GitHub Issue custom field (customfield_10747)
- Code Intelligence: configured with serena_backend instance using rust-analyzer

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description sections:
- **Repository**: trustify-backend
- **Target Branch**: main -- this is the branch to use as PR base
- **Description**: Add a service method and REST endpoint that aggregates advisory severity counts for a given SBOM
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, advisory_summary tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow patterns from get.rs endpoint, AdvisoryService methods, sbom_advisory join table, AdvisorySummary severity field, AppError with .context()
- **Acceptance Criteria**: 5 criteria covering response shape, 404 handling, deduplication, defaults, performance
- **Test Requirements**: 4 test cases
- **Dependencies**: None
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **GitHub Issue custom field**: customfield_10747 -- would check the fetched issue fields for a GitHub issue reference

## Step 1.5 -- Verify Description Integrity

Would retrieve issue comments via `jira.get_issue_comments(TC-9201)` and search for comments whose body starts with `[sdlc-workflow] Description digest:`. If no digest comment is found, proceed with a warning:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

This follows the backward compatibility behavior specified in shared/description-digest-protocol.md: when no digest is found, proceed normally rather than blocking execution.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would:
1. Retrieve current user's account ID via `jira.user_info()`
2. Assign task via `jira.edit_issue(TC-9201, assignee=<accountId>)`
3. Transition to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code (Inspect Before Modify)

### Files to inspect before making any changes

The following existing files would be read and analyzed using Serena (`mcp__serena_backend__*` tools) before any modifications:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Inspect using `get_symbols_overview` and `find_symbol` to understand the existing GET handler pattern: how path parameters are extracted via `Path<Id>`, how the service is called, and how JSON responses are returned. This is the primary template for the new severity_summary endpoint handler.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Inspect using `get_symbols_overview` to see the AdvisoryService struct and its existing methods (`fetch`, `list`, `search`). Use `find_symbol` with `include_body=true` on the `fetch` method to understand the method signature pattern (parameters, return type, transaction handling with `Transactional`). This tells us how to structure the new `severity_summary` method.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Inspect to understand the `AdvisorySummary` struct, specifically the `severity` field that will be used to count by severity level. This confirms the data source for aggregation.

4. **`common/src/error.rs`** -- Inspect to understand the `AppError` enum and its `IntoResponse` implementation. Verify the `.context()` wrapping pattern used for error handling across the codebase.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Inspect to see how routes are registered using `Router::new().route("/path", get(handler))` pattern.

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- Inspect to see how model sub-modules are declared (e.g., `pub mod summary;`, `pub mod details;`).

7. **`entity/src/sbom_advisory.rs`** -- Inspect the SBOM-Advisory join table entity to understand the relationship used for linking advisories to SBOMs.

### Sibling analysis for convention discovery

Would use `get_symbols_overview` on:
- `modules/fundamental/src/sbom/endpoints/get.rs` (sibling GET endpoint handler)
- `modules/fundamental/src/sbom/service/sbom.rs` (sibling service)
- `modules/fundamental/src/sbom/model/summary.rs` (sibling model struct)
- `tests/api/advisory.rs` and `tests/api/sbom.rs` (sibling test files)

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root (path `./` from Repository Registry). If present, read it for naming rules, directory structure, code patterns, test conventions, and CI check commands.

### Documentation file identification

Would look for:
- `docs/api.md` (API documentation referenced in CLAUDE.md)
- `docs/architecture.md` (architecture overview)
- README files in advisory module directory

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

This creates a branch named `TC-9201` from the target branch `main`.

## Step 6 -- Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService` that:
- Takes `&self, sbom_id: Id, tx: &Transactional<'_>` as parameters
- Queries the `sbom_advisory` join table to find advisories linked to the given SBOM
- Loads each advisory's severity from `AdvisorySummary`
- Deduplicates by advisory ID
- Counts advisories per severity level (Critical, High, Medium, Low)
- Returns `Result<SeveritySummary, AppError>` with `.context()` wrapping on errors
- Returns 404 (via AppError) when the SBOM ID does not exist

### 2. `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route:
- Add `mod severity_summary;` to import the new handler module
- Add `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))` to the router

### 3. `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module alongside existing `pub mod summary;` and `pub mod details;`.

## Step 6 (continued) -- Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct with Serialize/Deserialize derives and fields: `critical: u32`, `high: u32`, `medium: u32`, `low: u32`, `total: u32`. Include documentation comment explaining the struct's purpose.

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler following the pattern from `advisory/endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Call `AdvisoryService::severity_summary()`
- Return `Result<Json<SeveritySummary>, AppError>`
- Use `.context()` for error wrapping

### 6. `tests/api/advisory_summary.rs`

Create integration tests covering all 4 test requirements:
- Test valid SBOM with known advisories returns correct severity counts
- Test non-existent SBOM ID returns 404
- Test SBOM with no advisories returns all zeros
- Test duplicate advisory links are deduplicated

## Step 7 -- Write Tests

Tests are described in file-6-description.md. Would run `cargo test` to verify.

## Step 8 -- Verify Acceptance Criteria

All 5 acceptance criteria are covered by the implementation and tests:
- GET endpoint returns correct shape
- 404 for non-existent SBOM
- Deduplication by advisory ID
- Defaults to 0 for severity levels with no advisories
- Performance target (200ms for 500 advisories) addressed via efficient SQL query

## Step 9 -- Self-Verification

- Scope containment: `git diff --name-only` should list exactly the 6 files above
- Untracked file check: verify no untracked files in modified directories
- Sensitive-pattern check: search staged diff for secrets/credentials
- Documentation currency: check if docs/api.md needs update for new endpoint
- Data-flow trace: GET request -> path param extraction -> service call -> DB query -> aggregation -> JSON response (COMPLETE)

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

### Commit command

```
git add modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes SeveritySummary model, AdvisoryService method,
endpoint handler, and integration tests.

Implements TC-9201"
```

### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

The PR targets `main` (the Target Branch extracted from the task description) and references TC-9201 with a clickable Jira link.

## Step 11 -- Update Jira

- Update Git Pull Request custom field (customfield_10875) with PR URL in ADF format
- Add comment summarizing changes made and PR link
- Transition TC-9201 to In Review
