# Implementation Plan: TC-9201 -- Add Advisory Severity Aggregation Service and Endpoint

## Step 0 -- Validate Project Configuration

Verified that the project's CLAUDE.md contains the required sections:
- **Repository Registry**: present, lists `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present, includes Project key (TC), Cloud ID, Feature issue type ID, Git Pull Request custom field (`customfield_10875`), and GitHub Issue custom field (`customfield_10747`)
- **Code Intelligence**: present, lists `serena_backend` with `rust-analyzer`

All required sections are present. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

**Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Status**: To Do

### Parsed Sections

- **Repository**: trustify-backend
- **Target Branch**: `main`
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. The endpoint returns a summary with counts per severity level (Critical, High, Medium, Low) and a total, enabling dashboard widgets to render severity breakdowns without client-side counting.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
  - `tests/api/advisory_summary.rs` -- integration tests for the new endpoint
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW) -- returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Implementation Notes**: Follow existing endpoint pattern in `get.rs`, add `severity_summary` method to `AdvisoryService`, use `sbom_advisory` join table, count by severity from `AdvisorySummary.severity`, register route in `endpoints/mod.rs`, error handling with `AppError` and `.context()`, return struct directly via Axum's `Json` extractor.
- **Acceptance Criteria**: 5 criteria covering correct response shape, 404 handling, deduplication, zero defaults, and performance.
- **Test Requirements**: 4 tests covering valid counts, 404 for non-existent SBOM, all-zeros for no advisories, and deduplication.
- **Dependencies**: None.

### Target Branch Extraction

The Target Branch section specifies `main`. This value will be used in Step 5 (branch creation with `git checkout main`) and Step 10 (PR creation with `--base main`).

### GitHub Issue Extraction

The Jira Configuration lists `GitHub Issue custom field: customfield_10747`. Would read this custom field value from the fetched issue's fields. If present, parse the GitHub issue URL and store the reference for use in Step 10's PR description (`Closes <owner>/<repo>#<number>`).

## Step 1.5 -- Verify Description Integrity (Digest Check)

Per the description digest protocol defined in `shared/description-digest-protocol.md`:

1. **Retrieve issue comments**: Would call `jira.get_issue_comments(TC-9201)` to fetch all comments.
2. **Locate the digest comment**: Search for comments whose body starts with the marker string `[sdlc-workflow] Description digest:`. If multiple comments match, select the most recent one by `created` timestamp.
3. **If no digest comment found**: Log a warning and proceed normally without blocking execution (backward compatibility -- tasks created before digest tracking was introduced have no digest comment):
   > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."
4. **If digest comment found**: Would extract the format tag and hex digest, compute the current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags (if they differ, log a warning about format mismatch and proceed), then compare hex digests. On match, proceed silently. On mismatch, alert the user and pause execution.

Since this is a simulated run, no actual comments are available. In a real execution, if no digest comment were found, we would proceed with the warning per backward compatibility.

## Step 2 -- Verify Dependencies

No dependencies listed for TC-9201. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<current-user-account-id>)` to assign
3. `jira.transition_issue(TC-9201)` to "In Progress"

## Step 4 -- Understand the Code (Pre-Implementation Inspection)

### Code Inspection Plan

Before making any changes, inspect the following existing files to understand current patterns and confirm Implementation Notes references:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Read/analyze this file to understand the existing endpoint pattern: how path parameters are extracted via `Path<Id>`, how the service is called, and how JSON responses are returned. This is the primary pattern reference for the new severity_summary endpoint handler.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Read/analyze this file to understand `AdvisoryService`'s existing methods (`fetch`, `list`, `search`), their signatures (particularly the `&self, id: Id, tx: &Transactional<'_>` pattern), return types, and error handling. The new `severity_summary` method must follow this same pattern.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Read/analyze to understand the `AdvisorySummary` struct, specifically its `severity` field which will be used for counting by severity level.

4. **`common/src/error.rs`** -- Read/analyze to understand the `AppError` enum and how `.context()` wrapping is used for error propagation. All new code must follow this error handling pattern.

5. **`entity/src/sbom_advisory.rs`** -- Read to understand the SBOM-Advisory join table structure, which will be used to find advisories linked to a given SBOM.

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Read to understand how routes are registered using `Router::new().route("/path", get(handler))` so the new route follows the same pattern.

7. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read to see how existing model submodules are registered (e.g., `pub mod summary;`, `pub mod details;`) to follow the same pattern for `pub mod severity_summary;`.

### Sibling Analysis for Convention Conformance

Sibling files examined:
- `modules/fundamental/src/advisory/endpoints/get.rs` and `list.rs` -- endpoint handler siblings
- `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` -- model struct siblings
- `modules/fundamental/src/sbom/service/sbom.rs` -- service sibling in another domain module
- `tests/api/advisory.rs` and `tests/api/sbom.rs` -- test siblings

Conventions discovered are documented in `outputs/conventions.md`.

### CONVENTIONS.md Lookup

The Repository Registry lists `trustify-backend` at path `./`. Would check for `CONVENTIONS.md` at the repository root. Per the repo-backend.md manifest, `CONVENTIONS.md` exists in the repository root. Would read it and extract any CI check commands for use in Step 9.

### Documentation File Identification

Relevant documentation files identified:
- `docs/api.md` -- REST API reference, may need updating with new endpoint
- `docs/architecture.md` -- System architecture overview
- `README.md` -- Project readme

## Step 5 -- Create Branch

**Target Branch**: `main` (extracted from the task's Target Branch section)

Branch operations:
```
git checkout main
git pull
git checkout -b TC-9201
```

This creates a task branch named `TC-9201` based on `main`, following the convention that task branches are named after the Jira issue ID (constraint 3.1).

## Step 6 -- Implement Changes

### Files to Modify

#### 1. `modules/fundamental/src/advisory/service/advisory.rs`
Add a `severity_summary` method to `AdvisoryService`. See `outputs/file-1-description.md` for detailed changes.

#### 2. `modules/fundamental/src/advisory/endpoints/mod.rs`
Register the new severity summary route. See `outputs/file-2-description.md` for detailed changes.

#### 3. `modules/fundamental/src/advisory/model/mod.rs`
Add `pub mod severity_summary;` to register the new model module. See `outputs/file-3-description.md` for detailed changes.

### Files to Create

#### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`
SeveritySummary response struct. See `outputs/file-4-description.md` for detailed changes.

#### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
GET handler for /api/v2/sbom/{id}/advisory-summary. See `outputs/file-5-description.md` for detailed changes.

#### 6. `tests/api/advisory_summary.rs`
Integration tests for the new endpoint. See `outputs/file-6-description.md` for detailed changes.

### Scope Verification

All files listed above are strictly within the Files to Modify and Files to Create sections of the task description. No out-of-scope files are modified.

## Step 7 -- Write Tests

Tests are defined in `outputs/file-6-description.md`. The tests follow the project's existing integration test patterns found in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

## Step 8 -- Verify Acceptance Criteria

Each acceptance criterion would be verified:
- GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape -- verified by test
- Returns 404 for non-existent SBOM ID -- verified by test
- Counts only unique advisories (deduplicates) -- verified by implementation using DISTINCT and by test
- All severity levels default to 0 -- verified by empty SBOM test
- Response time under 200ms for 500 advisories -- verified by using indexed query on sbom_advisory join table

## Step 9 -- Self-Verification

### Scope Containment
Run `git diff --name-only` and verify all modified/created files match the Files to Modify and Files to Create sections. No out-of-scope files.

### Dead Parameter Detection
No parameters removed in this implementation -- only new code added.

### Sensitive-Pattern Check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` to verify no secrets in the diff.

### CI Checks
Run any CI check commands extracted from CONVENTIONS.md. Fix failures before proceeding.

### Query-Scope Verification
The implementation queries advisories linked to a specific SBOM by ID, which is a properly scoped query. No batch/broad queries needed.

### Data-Flow Trace
- Input: HTTP GET request with SBOM ID path parameter
- Processing: Extract ID, query sbom_advisory join, aggregate severity counts, deduplicate by advisory ID
- Output: JSON response with severity counts
- All stages connected.

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add a new GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes AdvisoryService.severity_summary method,
SeveritySummary response model, and integration tests.

Implements TC-9201
```

The commit would be executed with `--trailer='Assisted-by: Claude Code'`:

```
git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add a new GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes AdvisoryService.severity_summary method,
SeveritySummary response model, and integration tests.

Implements TC-9201"
```

### Fork Detection

Before creating a PR, check for an `upstream` remote:
```
git remote get-url upstream 2>/dev/null
```

### Push and PR Creation

```
git push -u origin TC-9201
```

Then create a PR targeting `main` (the Target Branch):
```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

The PR description would include:
- Summary of changes
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`
- `Closes <owner>/<repo>#<number>` if GitHub Issue was found in the custom field

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
2. Add a comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 to "In Review"
