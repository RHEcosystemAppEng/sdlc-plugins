# Implementation Plan for TC-9201

## Task Summary

**Jira Key:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Status:** To Do
**Dependencies:** None

## Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend mapped to serena_backend instance at `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: serena_backend with rust-analyzer

Configuration is valid. Proceeding.

## Step 1 -- Parse Task Description

Parsed sections from TC-9201:
- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify:** 4 files (1 with no changes needed)
- **Files to Create:** 3 files
- **API Changes:** GET /api/v2/sbom/{id}/advisory-summary (NEW)
- **Acceptance Criteria:** 5 items
- **Test Requirements:** 4 items
- **Target PR:** none
- **Bookend Type:** none
- **Dependencies:** none

## Step 1.5 -- Verify Description Integrity

Check for description digest comment on TC-9201 issue comments:

> No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced.

Proceeding with implementation.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress

- Retrieve current user's Jira account ID via `jira.user_info()`
- Assign TC-9201 to current user via `jira.edit_issue()`
- Transition TC-9201 to "In Progress" via `jira.transition_issue()`

## Step 4 -- Understand the Code

### Files to inspect before modifying

The following files would be read using the serena_backend Serena instance (via `get_symbols_overview` and `find_symbol` with `include_body=true`) to understand current patterns:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Inspect the GET /api/v2/advisory/{id} handler to understand the endpoint pattern: path parameter extraction via `Path<Id>`, service invocation, JSON response return, and `AppError` error handling.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Inspect the AdvisoryService struct and its `fetch`, `list`, and `search` methods to understand the service method signature pattern: `&self`, entity ID parameter, `tx: &Transactional<'_>`, and `Result<T, anyhow::Error>` return type with `.context()` wrapping.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Inspect the AdvisorySummary struct to understand the `severity` field type and how severity values are represented (enum, string, etc.). This is critical for knowing how to count by severity level.

4. **`common/src/error.rs`** -- Inspect the AppError enum to understand available error variants (especially for 404 responses) and how `.context()` is used for error wrapping.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Inspect to understand the route registration pattern for adding the new route.

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- Inspect to understand module registration pattern for adding the new model.

7. **`entity/src/sbom_advisory.rs`** -- Inspect the SBOM-Advisory join table entity to understand how to query advisories linked to a specific SBOM.

8. **`modules/fundamental/src/sbom/endpoints/get.rs`** -- Inspect as a cross-module sibling to confirm the pattern for SBOM-scoped endpoints and 404 handling when SBOM ID does not exist.

### Sibling analysis (convention conformance)

See `outputs/conventions.md` for the full conventions analysis. Key findings:
- Error handling uses `Result<T, AppError>` with `.context()` wrapping
- Module structure follows `model/ + service/ + endpoints/` pattern
- Service methods take `&self`, ID, and `tx: &Transactional<'_>`
- Route registration via `Router::new().route()`

### Documentation files identified

- `CONVENTIONS.md` at repository root
- `docs/api.md` -- REST API reference (may need updating for new endpoint)

### CONVENTIONS.md lookup

Read `CONVENTIONS.md` at repository root. Extract any CI check commands (formatting, linting, compilation) for use in Step 9 verification.

## Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch `TC-9201` created from Target Branch `main`.

## Step 6 & 7 -- Implementation and Tests

### Files to Modify

| # | File | Change |
|---|---|---|
| 1 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` to register the new model module |
| 2 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to AdvisoryService |
| 3 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register the new `/api/v2/sbom/{id}/advisory-summary` route |

### Files to Create

| # | File | Purpose |
|---|---|---|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | SeveritySummary response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for /api/v2/sbom/{id}/advisory-summary |
| 6 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

### No changes needed

- `server/src/main.rs` -- Routes auto-mount via module registration; no changes required.

See `outputs/file-1-description.md` through `outputs/file-6-description.md` for detailed changes per file.

## Step 8 -- Verify Acceptance Criteria

- [ ] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- Verified by endpoint implementation and test_severity_summary_valid_sbom test
- [ ] Returns 404 when SBOM ID does not exist -- Verified by 404 handling in endpoint and test_severity_summary_sbom_not_found test
- [ ] Counts only unique advisories (deduplicates by advisory ID) -- Verified by deduplication logic in service method and test_severity_summary_deduplication test
- [ ] All severity levels default to 0 when no advisories exist -- Verified by Default implementation on SeveritySummary and test_severity_summary_no_advisories test
- [ ] Response time under 200ms for SBOMs with up to 500 advisories -- Verified by efficient single-query approach with GROUP BY

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all changed files are within the Files to Modify and Files to Create lists.

### Untracked file check
Run `git status --short` and check for untracked files in directories where implementation occurred.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches.

### Documentation currency
Check if `docs/api.md` needs updating for the new GET /api/v2/sbom/{id}/advisory-summary endpoint. Update if it documents existing endpoints.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from CONVENTIONS.md (e.g., `cargo fmt --check`, `cargo clippy`, `cargo build`). Hard stop on any failure.

### Data-flow trace
- `GET /api/v2/sbom/{id}/advisory-summary` -> extract SBOM ID from path -> call `AdvisoryService::severity_summary()` -> query sbom_advisory join table -> aggregate by severity -> return `Json<SeveritySummary>` -- **COMPLETE**

### Contract & sibling parity
- SeveritySummary: derives Serialize, matches sibling model patterns
- severity_summary endpoint: follows same pattern as get.rs (Path extraction, service call, Json response, AppError return)
- AdvisoryService::severity_summary: follows same signature pattern as fetch/list methods

### Cross-section reference consistency
- Entity `AdvisoryService` -- Files to Modify: `advisory/service/advisory.rs`, Implementation Notes: `advisory/service/advisory.rs` -- **consistent**
- Entity `AdvisorySummary` -- Implementation Notes: `advisory/model/summary.rs` -- referenced for reading only, not modified -- **consistent**

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
404 handling for non-existent SBOMs.

Implements TC-9201
```

### Commit command

```bash
git add modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes deduplication by advisory ID and
404 handling for non-existent SBOMs.

Implements TC-9201"
```

### Push and create PR

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns advisory severity counts (critical, high, medium, low, total) for a given SBOM.

- New SeveritySummary model struct
- New severity_summary service method on AdvisoryService
- New GET endpoint with 404 handling and deduplication
- Integration tests covering valid SBOM, missing SBOM, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

## Step 11 -- Update Jira

1. Set Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL (ADF inlineCard format).
2. Add comment to TC-9201 with PR link, summary of changes, and confirmation of no deviations from plan.
3. Transition TC-9201 to "In Review".
