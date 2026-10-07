# Implementation Plan for TC-9201

## Task Summary

**Jira Issue:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main (extracted from the Target Branch section of the task description)

## Step 1 -- Fetch and Parse Jira Task

Parse the structured description from TC-9201. All required sections are present:

- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM.
- **Files to Modify:** 3 files listed
- **Files to Create:** 3 files listed
- **API Changes:** GET /api/v2/sbom/{id}/advisory-summary (NEW)
- **Implementation Notes:** present with code references
- **Acceptance Criteria:** 5 items
- **Test Requirements:** 4 items
- **Dependencies:** None
- **Target PR:** not present (default flow)
- **Bookend Type:** not present (default flow)
- **Review Context:** not present

Capture the issue webUrl (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

Check the GitHub Issue custom field (`customfield_10747`) on the fetched issue for a linked GitHub issue URL. If present, parse `owner/repo#number` for use in the PR description's `Closes` line.

## Step 1.5 -- Verify Description Integrity

Retrieve all comments on TC-9201 using `jira.get_issue_comments(TC-9201)`. Search for comments whose body starts with the marker string `[sdlc-workflow] Description digest:`.

- If multiple digest comments are found, select the most recent one by `created` timestamp.
- If a digest comment is found, extract the format tag and hex digest, then compute the current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`. Compare format tags first; if they match, compare hex digests. On mismatch, alert the user and stop for confirmation.
- If a digest comment's `created` and `updated` timestamps differ, warn: "Digest comment was edited after initial posting -- integrity cannot be fully guaranteed."
- **If no digest comment is found:** log a warning and proceed normally (backward compatibility -- tasks created before digest tracking was introduced have no digest comment). Do not block execution:
  > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 -- Verify Dependencies

The task lists Dependencies as "None". No dependency verification required.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<accountId>)`
3. Transition TC-9201 to "In Progress" via `jira.transition_issue`

## Step 4 -- Understand the Code (Sibling Analysis)

Before making any changes, inspect existing code to understand patterns and conventions. Use the Serena instance `serena_backend` from the Repository Registry.

### Files to inspect

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Read this sibling endpoint handler to understand the existing GET handler pattern: path parameter extraction via `Path<Id>`, service method invocation, JSON response return, and error handling with `Result<T, AppError>`.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Read the existing `AdvisoryService` to understand the `fetch` and `list` method signatures, particularly the `(&self, id: Id, tx: &Transactional<'_>)` parameter pattern and `Result<T, AppError>` return type with `.context()` error wrapping.

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- Read the existing `AdvisorySummary` struct to understand the `severity` field that will be used for counting by severity level. Also note the struct's derive macros and serialization approach.

4. **`common/src/error.rs`** -- Read the `AppError` enum and its `IntoResponse` implementation to confirm the error handling pattern (`.context()` wrapping for anyhow-style errors).

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Read the route registration pattern: `Router::new().route("/path", get(handler))`.

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read the existing module declarations to see how sub-modules are registered (e.g., `pub mod summary;`, `pub mod details;`).

7. **`entity/src/sbom_advisory.rs`** -- Read the SBOM-Advisory join table entity to understand the relationship between SBOMs and advisories (used by the severity_summary query).

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). If present, read it and extract CI check commands for Step 9 verification. The repo manifest lists `CONVENTIONS.md` at the repository root.

### Convention conformance analysis

Analyze sibling files to discover established patterns. See `outputs/conventions.md` for the full list.

### Documentation file identification

Identify documentation files related to the changes:
- `docs/api.md` -- REST API reference (may need updating for the new endpoint)
- `docs/architecture.md` -- System architecture overview
- `README.md` at repo root

## Step 5 -- Create Branch

Create a task branch from the target branch (main):

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch name `TC-9201` follows the convention of naming branches after the Jira issue ID. The target branch is `main` as specified in the Target Branch section of the task description.

## Step 6 -- Implement Changes

### Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new `/api/v2/sbom/{id}/advisory-summary` route
3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` to register the new model module

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- `SeveritySummary` response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. **`tests/api/advisory_summary.rs`** -- Integration tests for the new endpoint

See individual `file-N-description.md` files for detailed changes per file.

## Step 7 -- Write Tests

Implement the 4 test cases described in Test Requirements in `tests/api/advisory_summary.rs`:

1. Test that a valid SBOM with known advisories returns correct severity counts
2. Test that a non-existent SBOM ID returns 404
3. Test that an SBOM with no advisories returns all zeros
4. Test that duplicate advisory links are deduplicated in the count

Each test function will have a `///` documentation comment and given-when-then section comments. Follow the assertion pattern `assert_eq!(resp.status(), StatusCode::OK)` from sibling test files.

## Step 8 -- Verify Acceptance Criteria

Verify each acceptance criterion against the implementation:

- GET /api/v2/sbom/{id}/advisory-summary returns the expected JSON shape
- Returns 404 when SBOM ID does not exist
- Counts only unique advisories (deduplicated by advisory ID)
- All severity levels default to 0
- Response time validation (design review -- query uses indexed join table)

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and verify all modified/created files match the Files to Modify and Files to Create sections. No out-of-scope files should be modified.

### Module-level test requirement (Rust)
Run `cargo metadata --no-deps --format-version 1` from the workspace root to resolve the package name for each modified file. Use the resolved `name` field from the package whose manifest or target source contains the modified file as `<crate-name>`. Do not derive the crate name from the nearest `Cargo.toml`, which may be a virtual workspace manifest (the root `Cargo.toml` is likely a workspace manifest).

For the files under `modules/fundamental/src/`, resolve the crate name from `modules/fundamental/Cargo.toml` via `cargo metadata`. Then run:

```
cargo test -p <crate-name>
```

For the test file under `tests/`, resolve its crate from `tests/Cargo.toml` via `cargo metadata` and run its tests similarly.

Apply hard-stop rule: if the test command exits non-zero, stop immediately and report.

### Additional checks
- Sensitive-pattern check on staged diff
- Dead parameter detection
- Untracked file check
- Documentation currency (check if `docs/api.md` needs updating for the new endpoint)
- Duplication check (search for existing severity aggregation logic)
- Data-flow trace: API request with SBOM ID -> service queries sbom_advisory join -> counts by severity -> returns JSON response
- Contract & sibling parity checks
- CI checks from CONVENTIONS.md (if extracted)

## Step 10 -- Commit and Push

### Commit message

```
git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201"
```

The commit uses:
- Conventional Commits format: `feat(advisory): add severity aggregation endpoint`
- `--trailer="Assisted-by: Claude Code"` for AI attribution
- Footer references TC-9201

### Fork detection

Run `git remote get-url upstream 2>/dev/null` to detect fork setup. Handle both fork and non-fork flows.

### Push and create PR

```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

The PR description will include:
- Summary of changes
- `Implements [TC-9201](<webUrl>)` with clickable Jira link
- If a GitHub issue was found in Step 1, a `Closes <owner>/<repo>#<number>` line

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
2. Add a comment to TC-9201 with PR link, summary of changes, and any deviations
3. Transition TC-9201 to "In Review"
