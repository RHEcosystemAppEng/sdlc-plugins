# Implementation Plan for TC-9201

## Task Summary
**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main

## Step 0 -- Validate Project Configuration

Verified CLAUDE.md contains:
- Repository Registry with trustify-backend entry (Serena Instance: serena_backend, Path: ./)
- Jira Configuration with Project key: TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence section with serena_backend instance using rust-analyzer

All required sections present. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

Parsed structured description from TC-9201:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint for advisory severity aggregation per SBOM
- **Files to Modify**: 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs)
- **Files to Create**: 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs tests)
- **API Changes**: GET /api/v2/sbom/{id}/advisory-summary (NEW)
- **Implementation Notes**: Present with code references
- **Acceptance Criteria**: 5 criteria specified
- **Test Requirements**: 4 tests specified
- **Dependencies**: None

### Target Branch Extraction
Target Branch is **main**. This will be used as the base for branch creation (Step 5) and as the --base flag for the PR (Step 10).

## Step 1.5 -- Verify Description Integrity

Retrieve issue comments using `jira.get_issue_comments(TC-9201)` and search for comments whose body starts with the marker string `[sdlc-workflow] Description digest:`.

**If no digest comment is found**: Log a warning and proceed normally -- backward compatibility with tasks created before digest tracking was introduced. The warning message would be:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

This follows the protocol in `shared/description-digest-protocol.md`. Execution is not blocked; we proceed to Step 2 without interruption.

**If a digest comment were found**: We would extract the format tag and hex digest, compute the current description's digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags and hex values, and proceed silently on match or alert the user on mismatch.

## Step 2 -- Verify Dependencies

No dependencies listed for TC-9201. Proceeding.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition TC-9201 to In Progress via `jira.transition_issue`

## Step 4 -- Understand the Code

### Code Inspection Plan

Before making any changes, inspect the following existing files to understand current patterns and confirm the references in Implementation Notes:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Read this file using `mcp__serena_backend__get_symbols_overview` to understand the existing endpoint pattern. This is the primary reference for how to structure the new severity_summary endpoint handler (path parameter extraction via `Path<Id>`, service call pattern, JSON response).

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Read this file using `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand the AdvisoryService method signatures. The new `severity_summary` method must follow the same pattern: `&self, sbom_id: Id, tx: &Transactional<'_>`.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Read using `mcp__serena_backend__get_symbols_overview` to understand the AdvisorySummary struct and its `severity` field, which will be used for counting by severity level.

4. **`common/src/error.rs`** -- Read to understand the AppError enum and how `.context()` wrapping is used for error handling in handlers.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Read to understand the route registration pattern (`Router::new().route("/path", get(handler))`).

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read to understand how model submodules are registered with `pub mod` statements.

7. **`entity/src/sbom_advisory.rs`** -- Read to understand the SBOM-Advisory join table structure for the database query.

### Sibling Analysis

Examine sibling files for convention conformance:
- `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler
- `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler
- `modules/fundamental/src/advisory/model/details.rs` -- sibling model struct
- `tests/api/advisory.rs` -- sibling test file

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read it and extract any CI check commands for Step 9 verification.

### Documentation File Identification

Related documentation files to check:
- `docs/api.md` -- may need updating with the new endpoint
- `README.md` -- check if API overview section exists

## Step 5 -- Create Branch

Check out the target branch (main), pull latest changes, and create a task branch:

```
git checkout main
git pull
git checkout -b TC-9201
```

The branch is named `TC-9201` after the Jira issue ID, based off `main` (the Target Branch extracted in Step 1).

## Step 6 -- Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`
**Change**: Add a `severity_summary` method to AdvisoryService.

The method will:
- Take `&self, sbom_id: Id, tx: &Transactional<'_>` following the pattern of existing `fetch` and `list` methods
- Query the `sbom_advisory` join table to find all advisories linked to the given SBOM
- Join with advisory data to get severity levels from AdvisorySummary
- Deduplicate by advisory ID
- Count advisories per severity level (Critical, High, Medium, Low)
- Return a `SeveritySummary` struct with counts and total
- Use `Result<SeveritySummary, AppError>` return type with `.context()` error wrapping

### 2. `modules/fundamental/src/advisory/endpoints/mod.rs`
**Change**: Register the new severity summary route.

Add a new route registration following the existing pattern:
```rust
.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get))
```

### 3. `modules/fundamental/src/advisory/model/mod.rs`
**Change**: Add `pub mod severity_summary;` to register the new model submodule.

## Step 6 (cont.) -- Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`
**Create**: SeveritySummary response struct.

```rust
/// Summary of advisory severity counts for an SBOM.
#[derive(Debug, Clone, Serialize, Deserialize, PartialEq)]
pub struct SeveritySummary {
    /// Number of critical-severity advisories.
    pub critical: u32,
    /// Number of high-severity advisories.
    pub high: u32,
    /// Number of medium-severity advisories.
    pub medium: u32,
    /// Number of low-severity advisories.
    pub low: u32,
    /// Total number of unique advisories.
    pub total: u32,
}
```

All fields default to 0 when no advisories exist at that level.

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
**Create**: GET handler for /api/v2/sbom/{id}/advisory-summary.

Follow the pattern from `advisory/endpoints/get.rs`:
- Extract path parameter via `Path<Id>`
- Call `AdvisoryService::severity_summary(sbom_id, &tx)`
- Return JSON response using Axum's `Json` extractor
- Return 404 (via AppError) when SBOM ID does not exist
- Use `Result<Json<SeveritySummary>, AppError>` return type with `.context()` wrapping

### 6. `tests/api/advisory_summary.rs`
**Create**: Integration tests for the new endpoint.

Four test cases:
- `test_severity_summary_with_advisories` -- SBOM with known advisories returns correct counts
- `test_severity_summary_nonexistent_sbom` -- Non-existent SBOM ID returns 404
- `test_severity_summary_empty` -- SBOM with no advisories returns all zeros
- `test_severity_summary_deduplication` -- Duplicate advisory links are deduplicated

## Step 7 -- Write Tests

See file-6-description.md for detailed test implementation.

## Step 8 -- Verify Acceptance Criteria

All 5 acceptance criteria addressed:
1. GET endpoint returns the correct JSON structure -- implemented in endpoint handler
2. 404 for non-existent SBOM -- handled by AppError in service method
3. Unique advisory deduplication -- implemented in service query logic
4. Default to 0 for all severity levels -- handled by SeveritySummary struct defaults
5. Performance under 200ms -- database query uses indexed joins, no N+1 queries

## Step 9 -- Self-Verification

- **Scope containment**: All modified/created files are within Files to Modify and Files to Create sections
- **Dead parameter detection**: No parameters removed
- **Sensitive-pattern check**: No secrets or credentials in staged changes
- **Documentation currency**: docs/api.md may need a new endpoint entry -- flag for documentation impact review
- **Duplication check**: No duplication of existing utilities
- **Query-scope verification**: Query scoped to specific SBOM ID -- no broad table scans

## Step 10 -- Commit and Push

### Commit Message

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add SeveritySummary model, AdvisoryService.severity_summary() method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes integration tests for valid SBOM, 404 handling,
empty results, and deduplication.

Implements TC-9201"
```

The commit uses `--trailer='Assisted-by: Claude Code'` to attribute AI assistance per constraint 2.3.

### Push and PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

The PR targets `main` (the Target Branch) with `--base main`.

## Step 11 -- Update Jira

1. Update custom field `customfield_10875` with PR URL (ADF format with inlineCard)
2. Add comment to TC-9201 with PR link and summary of changes
3. Transition TC-9201 to In Review
