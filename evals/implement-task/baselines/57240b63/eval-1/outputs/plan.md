# Implementation Plan: TC-9201

## Task Summary

**Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Target Branch**: main
**Branch Name**: TC-9201

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 from Jira and parse the structured description. Extract:

- **Repository**: trustify-backend
- **Target Branch**: main (used as the PR base branch)
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify**: 3 files (advisory service, endpoints mod, model mod)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Acceptance Criteria**: 5 criteria covering response shape, 404 handling, deduplication, defaults, and performance
- **Test Requirements**: 4 tests covering valid counts, 404, empty SBOM, and deduplication
- **Dependencies**: None

## Step 1.5 -- Verify Description Integrity

Retrieve all comments on TC-9201 using `jira.get_issue_comments(TC-9201)`. Search for comments whose body starts with the marker string `[sdlc-workflow] Description digest:`.

- **If no digest comment is found**: Log a warning and proceed normally -- do not block execution: "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."
- **If a digest comment is found**: Extract the stored digest, compute the current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags and hex values. On mismatch, alert the user and ask whether to proceed or stop.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress

- Retrieve current user via `jira.user_info()`
- Assign TC-9201 to current user
- Transition TC-9201 to "In Progress"

## Step 4 -- Understand the Code (Inspection Before Modification)

Before modifying any code, inspect the following files to understand existing patterns. Since no Serena instance is available for trustify-backend, use Read, Grep, and Glob as fallback tools.

### Files to Inspect

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Understand the existing endpoint pattern: how Path<Id> extraction works, how the service is called, how JSON responses are returned, and how errors are handled. This is the primary reference for the new endpoint handler.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Understand the AdvisoryService structure: how `fetch` and `list` methods are implemented, the method signature pattern (particularly `&self, sbom_id: Id, tx: &Transactional<'_>`), and how database queries are constructed.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Understand the AdvisorySummary struct and its `severity` field. This field provides the severity value used for counting by severity level.

4. **`common/src/error.rs`** -- Understand the AppError enum and the Result<T, AppError> pattern with `.context()` wrapping for error handling.

5. **`entity/src/sbom_advisory.rs`** -- Understand the `sbom_advisory` join table structure for finding advisories linked to an SBOM.

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Understand the current route registration pattern (`Router::new().route("/path", get(handler))`).

7. **`modules/fundamental/src/advisory/model/mod.rs`** -- Understand the current module registration pattern for model submodules.

### Convention Conformance Analysis (Sibling Analysis)

Identify sibling files for each file being modified or created:

- **Endpoint siblings**: Other files in `modules/fundamental/src/advisory/endpoints/` (e.g., `get.rs`, `list.rs`) -- examine for route handler patterns, error handling, response types.
- **Service siblings**: Other methods in `advisory/service/advisory.rs` (e.g., `fetch`, `list`) -- examine for method signature patterns, query construction, transaction handling.
- **Model siblings**: Other files in `modules/fundamental/src/advisory/model/` (e.g., `summary.rs`, `details.rs`) -- examine for struct definition patterns, serde derive macros, field naming conventions.
- **Test siblings**: Other files in `tests/api/` -- examine for test setup, assertion patterns, HTTP response validation.

### Test Convention Analysis

Inspect 2-3 sibling test files in `tests/api/` to understand:
- Assertion style (e.g., `assert_eq!` on status codes)
- Response deserialization patterns
- Error case coverage (404 tests)
- Test naming conventions
- Test setup and fixture creation

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at the repository root. If present, read and follow its conventions. If not present, proceed normally with conventions discovered from sibling analysis.

## Step 5 -- Create Branch

Check out the target branch (main), pull latest, and create the task branch:

```bash
git checkout main
git pull
git checkout -b TC-9201
```

The branch is named `TC-9201` after the Jira issue ID. The target branch is `main` as specified in the task description.

## Step 6 -- Implement Changes

Implement changes to the following files, scoped exactly to the task description:

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct with fields: critical, high, medium, low, total (all u32/i64), with Serialize/Deserialize derives.

2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`. Extracts path params via `Path<Id>`, calls AdvisoryService::severity_summary, returns JSON response.

3. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint covering all test requirements.

### Files to Modify

4. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to AdvisoryService following the same pattern as `fetch` and `list` methods.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route for the severity summary endpoint.

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register the new model module.

See individual file description documents (file-1-description.md through file-6-description.md) for detailed changes.

## Step 7 -- Write Tests

Implement the 4 tests described in Test Requirements in `tests/api/advisory_summary.rs`:
- Test valid SBOM with known advisories returns correct severity counts
- Test non-existent SBOM ID returns 404
- Test SBOM with no advisories returns all zeros
- Test duplicate advisory links are deduplicated

Each test function will have a doc comment and given-when-then inline comments for non-trivial tests. Follow test conventions discovered from sibling test files.

Run tests: `cargo test`

## Step 8 -- Verify Acceptance Criteria

Verify each criterion:
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- [ ] Returns 404 when SBOM ID does not exist
- [ ] Counts only unique advisories (deduplicates by advisory ID)
- [ ] All severity levels default to 0 when no advisories exist
- [ ] Response time under 200ms for SBOMs with up to 500 advisories

## Step 9 -- Self-Verification

- **Scope containment**: Run `git diff --name-only` and verify all files are within the Files to Modify and Files to Create lists.
- **Untracked file check**: Run `git status --short` and check for untracked files in implementation directories.
- **Sensitive-pattern check**: Search staged diff for secrets/credentials.
- **Data-flow trace**: Trace HTTP request -> Path extraction -> Service call -> DB query -> Severity counting -> JSON response. Verify all stages are connected.
- **Contract & sibling parity**: Verify the new endpoint follows the same patterns as existing advisory endpoints. Verify the new service method follows the same signature and error handling as `fetch` and `list`.
- **Duplication check**: Search for existing severity aggregation logic to avoid duplication.

## Step 10 -- Commit and Push

Commit message:

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
and integration tests.

Implements TC-9201
```

Commit command:

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
and integration tests.

Implements TC-9201"
```

Push and create PR:

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "## Summary
- Add SeveritySummary model struct for severity count response
- Add severity_summary service method to AdvisoryService
- Add GET /api/v2/sbom/{id}/advisory-summary endpoint
- Add integration tests for the new endpoint

## Jira
Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

## Step 11 -- Update Jira

- Set Git Pull Request custom field (`customfield_10875`) on TC-9201 with the PR URL (in ADF format)
- Add comment to TC-9201 with PR link and summary of changes
- Transition TC-9201 to "In Review"
