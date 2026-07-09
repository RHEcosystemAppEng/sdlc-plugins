# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Parent Feature**: TC-9001 (this task is incorporated by TC-9001)
**Dependencies**: None

## Step 1 -- Fetch and Parse Task Description

Parse the structured description from TC-9201. All required sections are present:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM.
- **Files to Modify**: 3 files
- **Files to Create**: 3 files
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary`
- **Implementation Notes**: Present with pattern references
- **Acceptance Criteria**: 5 criteria
- **Test Requirements**: 4 tests
- **Target PR**: Not present (default flow)
- **Bookend Type**: Not present (default flow)
- **Dependencies**: None

No missing sections -- proceed with implementation.

## Step 1.5 -- Verify Description Integrity

Check for a description digest comment on TC-9201 by fetching all issue comments and searching for those whose body starts with the marker string `[sdlc-workflow] Description digest:`.

- If no digest comment is found: log a warning -- "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced." Proceed normally without blocking execution. This backward compatibility behavior is specified in the description-digest-protocol.
- If a digest comment is found: extract the tagged digest (e.g., `sha256-md:<hex>` or `sha256-adf:<hex>`), compute the current description digest using `python3 scripts/sha256-digest.py`, compare format tags and hex digests, and alert the user only on mismatch.
- If multiple digest comments exist, select the most recent one by `created` timestamp.
- Check comment `created` vs `updated` timestamps for edit detection when available.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to the current user via `jira.edit_issue()`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue()`

## Step 4 -- Understand the Code

### Inspect Existing Files

Before making any changes, read and analyze the following existing files using the Serena instance `serena_backend` (from the Repository Registry in CLAUDE.md):

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Examine the existing GET endpoint pattern: how path params are extracted via `Path<Id>`, how the service is called, how JSON responses are returned. This is the primary pattern reference for the new endpoint.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Examine the existing `AdvisoryService` with its `fetch` and `list` methods. Understand the method signatures (particularly `&self, id: Id, tx: &Transactional<'_>` pattern) and how results are returned. The new `severity_summary` method must follow this same pattern.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Examine the `AdvisorySummary` struct, particularly the `severity` field. This field will be used to count advisories by severity level.

4. **`common/src/error.rs`** -- Examine the `AppError` enum and its `IntoResponse` implementation. Understand how `.context()` wrapping is used for error handling throughout the codebase.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Examine the existing route registration pattern using `Router::new().route("/path", get(handler))`.

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- Examine how existing model sub-modules are registered (e.g., `pub mod summary;`, `pub mod details;`).

7. **`entity/src/sbom_advisory.rs`** -- Examine the SBOM-Advisory join table entity to understand how advisories are linked to SBOMs.

8. **`modules/fundamental/src/sbom/endpoints/get.rs`** -- Examine sibling endpoint in the SBOM module for additional pattern reference.

### Convention Conformance Analysis (Sibling Analysis)

Identify and examine sibling files to discover implicit conventions:

- **Endpoint siblings**: `advisory/endpoints/get.rs`, `advisory/endpoints/list.rs`, `sbom/endpoints/get.rs`, `sbom/endpoints/list.rs`
- **Service siblings**: `advisory/service/advisory.rs`, `sbom/service/sbom.rs`
- **Model siblings**: `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`

### Test Convention Analysis

Examine sibling test files to discover test conventions:

- `tests/api/advisory.rs` -- Advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests
- `tests/api/search.rs` -- Search endpoint integration tests

### Documentation File Identification

- `README.md` at repository root
- `CONVENTIONS.md` at repository root
- `docs/api.md` (API reference)

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (path `./` from the Repository Registry). If present, read it and extract:
- CI check commands (formatting, linting, compilation)
- Code generation commands
- Follow all listed conventions throughout implementation

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type). Check out the Target Branch (`main`) as extracted from the task description:

```bash
git checkout main
git pull
git checkout -b TC-9201
```

The Target Branch is `main` as extracted from the task description's Target Branch section.

## Step 6 -- Implement Changes

### Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`**
   - Add a `severity_summary` method to `AdvisoryService`
   - Method signature follows existing pattern: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
   - Query the `sbom_advisory` join table to find advisories linked to the given SBOM
   - Join with advisory data to get severity levels
   - Deduplicate by advisory ID
   - Count by severity level (Critical, High, Medium, Low)
   - Return `SeveritySummary` struct with counts and total

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`**
   - Add `pub mod severity_summary;` to register the new endpoint module
   - Add route registration: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_severity_summary))`
   - Follow the existing `Router::new().route(...)` pattern

3. **`modules/fundamental/src/advisory/model/mod.rs`**
   - Add `pub mod severity_summary;` to register the new model module

### Files to Create

4. **`modules/fundamental/src/advisory/model/severity_summary.rs`**
   - Define `SeveritySummary` struct with `#[derive(Serialize, Deserialize, Debug, Clone, utoipa::ToSchema)]`
   - Fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`
   - Implement `Default` trait so all counts default to 0

5. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`**
   - Define GET handler function following the pattern in `advisory/endpoints/get.rs`
   - Extract path params via `Path<Id>`
   - Call `AdvisoryService::severity_summary()`
   - Return `Json<SeveritySummary>`
   - Error handling: return `AppError` with `.context()` wrapping
   - Return 404 when SBOM ID does not exist

6. **`tests/api/advisory_summary.rs`**
   - Integration tests hitting a real PostgreSQL test database
   - Test cases per Test Requirements section

### No Changes Needed

- `server/src/main.rs` -- routes auto-mount via module registration (confirmed by task description)

## Step 7 -- Write Tests

Implement tests in `tests/api/advisory_summary.rs`:

1. Test that a valid SBOM with known advisories returns correct severity counts
2. Test that a non-existent SBOM ID returns 404
3. Test that an SBOM with no advisories returns all zeros
4. Test that duplicate advisory links are deduplicated in the count

Follow test conventions discovered from sibling test files (assertion style, naming, setup/teardown patterns).

## Step 8 -- Verify Acceptance Criteria

Verify each criterion:
- GET endpoint returns the correct JSON shape with severity counts
- Returns 404 for non-existent SBOM ID
- Deduplicates by advisory ID
- All severity levels default to 0
- Response time under 200ms for SBOMs with up to 500 advisories

## Step 9 -- Self-Verification

1. **Scope containment**: Run `git diff --name-only` and verify all modified/created files match the task's Files to Modify and Files to Create lists
2. **Untracked file check**: Run `git status --short` and check for `??` entries in directories where implementation work occurred
3. **Sensitive-pattern check**: Search staged diff for secrets/credentials
4. **Documentation currency**: Check if API docs need updating for the new endpoint
5. **CI checks from CONVENTIONS.md**: Run all extracted CI check commands
6. **Data-flow trace**: Verify the complete path: HTTP request -> endpoint handler -> service method -> database query -> response
7. **Contract & sibling parity**: Verify the new code matches patterns in sibling endpoints/services
8. **Duplication check**: Search for existing severity aggregation logic to avoid duplication
9. **Cross-section reference consistency**: Verify file paths are consistent across all sections of the task description

## Step 10 -- Commit and Push

### Commit

```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity
counts (critical, high, medium, low, total) for advisories linked to a
given SBOM. Includes SeveritySummary model, AdvisoryService method, and
integration tests.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "..."
```

The PR description will include:
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- Summary of changes
- Test coverage summary

## Step 11 -- Update Jira

1. Update the Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL using ADF format
2. Add a Jira comment with PR link, summary of changes, and any deviations from the plan
3. Transition TC-9201 to "In Review"
