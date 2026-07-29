# Implementation Plan for TC-9201

## Task Summary

**Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Dependencies**: None

## Step 1 -- Fetch and Parse Jira Task

Fetch TC-9201 via `jira.get_issue("TC-9201")`. Parse the structured description and extract:
- Repository: trustify-backend
- Target Branch: main
- No Target PR (this is a standard implementation, not a review fix)
- No Bookend Type (standard flow)
- No Dependencies

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

Look up the GitHub Issue custom field (`customfield_10747`) from the Jira Configuration section in CLAUDE.md. If the field contains a value, parse the GitHub issue URL and store the reference for the PR description's `Closes` line.

## Step 1.5 -- Verify Description Integrity

Retrieve all comments on TC-9201 via `jira.get_issue_comments("TC-9201")`. Search for comments whose body starts with the marker string `[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`.

**Expected outcome for this task**: No digest comment is found. Log the warning and proceed normally without blocking execution:

> "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

This is the backward-compatible behavior per `shared/description-digest-protocol.md` -- older tasks created before digest tracking was introduced should not be blocked.

If a digest comment were found, we would:
1. Check if `created` and `updated` timestamps differ (indicating the comment was edited)
2. Extract the tagged digest value (e.g., `sha256-md:a1b2...` or `sha256-adf:a1b2...`)
3. Compute the current digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
4. Compare format tags and hex digests, halting only on a confirmed mismatch

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign TC-9201 to current user via `jira.edit_issue("TC-9201", assignee=<accountId>)`
3. Transition to In Progress via `jira.transition_issue("TC-9201", "In Progress")`

## Step 4 -- Understand the Code

### 4.1 Inspect existing files before modification

Using the Serena instance `serena_backend` (from the Repository Registry in CLAUDE.md), inspect each file in the scope:

**Files to Modify -- read and analyze before changing:**

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the structure of `AdvisoryService`. Then use `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` and `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` to understand the method patterns (parameter types, return types, error handling, transaction usage).

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the route registration pattern. Read how existing routes are registered (e.g., `Router::new().route("/path", get(handler))`).

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Read this file to see how existing model submodules are registered (e.g., `pub mod summary;`, `pub mod details;`).

**Files referenced in Implementation Notes -- read for patterns:**

4. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- Use `mcp__serena_backend__find_symbol` with `include_body=true` to read the GET handler. Understand the `Path<Id>` extraction, service call, and JSON response pattern.

5. **`modules/fundamental/src/advisory/model/summary.rs`** -- Use `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to inspect the struct and its `severity` field.

6. **`entity/src/sbom_advisory.rs`** -- Read/inspect the join table entity to understand the relationship between SBOMs and advisories.

7. **`common/src/error.rs`** -- Use `mcp__serena_backend__find_symbol("AppError", include_body=true)` to understand the error enum and `.context()` wrapping pattern.

### 4.2 CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (Path `./` from the Repository Registry). The repo structure confirms it exists. Read it and extract:
- CI check commands (for Step 9)
- Code generation commands (if any)
- Naming rules, directory structure, code patterns

### 4.3 Convention conformance analysis (sibling analysis)

Identify sibling files for each file being modified or created:

**Production code siblings:**
- For `advisory/endpoints/severity_summary.rs` (new) -- siblings are `advisory/endpoints/get.rs` and `advisory/endpoints/list.rs`. Also cross-module siblings: `sbom/endpoints/get.rs`, `sbom/endpoints/list.rs`.
- For `advisory/service/advisory.rs` (modify) -- siblings are `sbom/service/sbom.rs`, `package/service/mod.rs`.
- For `advisory/model/severity_summary.rs` (new) -- siblings are `advisory/model/summary.rs`, `advisory/model/details.rs`, `sbom/model/summary.rs`.

Use `mcp__serena_backend__get_symbols_overview` on 2-3 siblings in each category to discover patterns for naming, error handling, option/parameter propagation, import organization, and module structure.

**Test code siblings:**
- For `tests/api/advisory_summary.rs` (new) -- siblings are `tests/api/advisory.rs`, `tests/api/sbom.rs`, `tests/api/search.rs`.

Use `mcp__serena_backend__get_symbols_overview` on 2-3 sibling test files to discover assertion patterns, response validation, error case coverage, test naming, and parameterized test usage.

### 4.4 Documentation file identification

Identify documentation files related to the changes:
- `docs/api.md` -- REST API reference, may need updating for the new endpoint
- `docs/architecture.md` -- system architecture, check if advisory module is documented
- `README.md` at repository root

### 4.5 Check backward compatibility

Use `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., `AdvisoryService`, `advisory/endpoints/mod.rs` route registration) to ensure changes do not break existing callers.

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

The branch is named `TC-9201` after the Jira issue. The base is `main` (from the Target Branch section).

## Step 6 -- Implement Changes

### Files to Create (3 files)

#### File 1: `modules/fundamental/src/advisory/model/severity_summary.rs`

Create the `SeveritySummary` response struct with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64` or `i64` depending on sibling convention). Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `utoipa::ToSchema`. Add a documentation comment explaining the struct's purpose. Implement `Default` so all counts start at zero.

#### File 2: `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

Create the GET handler for `/api/v2/sbom/{id}/advisory-summary`. Follow the pattern from `advisory/endpoints/get.rs`:
- Extract path params via `Path<Id>`
- Get `AdvisoryService` from app state
- Call `service.severity_summary(sbom_id, &tx)` 
- Return `Json(result)` on success
- Return `AppError` with `.context()` on failure
- Return 404 when the SBOM ID does not exist

#### File 3: `tests/api/advisory_summary.rs`

Create integration tests following the patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- Test valid SBOM with known advisories returns correct severity counts
- Test non-existent SBOM ID returns 404
- Test SBOM with no advisories returns all zeros
- Test duplicate advisory links are deduplicated

Each test function gets a `///` doc comment and given-when-then section comments.

### Files to Modify (3 files)

#### File 4: `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`. The method:
- Takes `&self, sbom_id: Id, tx: &Transactional<'_>` (matching `fetch` and `list` patterns)
- Queries the `sbom_advisory` join table to find advisories linked to the SBOM
- Joins with advisory data to get severity levels
- Deduplicates by advisory ID
- Counts by severity level (Critical, High, Medium, Low)
- Returns `Result<SeveritySummary, AppError>` with `.context()` error wrapping
- Returns 404 if the SBOM does not exist

#### File 5: `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new route by adding:
- `mod severity_summary;` at the top
- A new `.route("/api/v2/sbom/{id}/advisory-summary", get(severity_summary::handler))` to the Router chain

Follow the existing registration pattern visible in the file.

#### File 6: `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model submodule, following the pattern of existing `pub mod summary;` and `pub mod details;` declarations.

### Files explicitly excluded

`server/src/main.rs` -- the task description notes "no changes needed" because routes auto-mount via module registration. No modifications will be made to this file.

## Step 7 -- Write Tests

Implement the 4 tests specified in Test Requirements in `tests/api/advisory_summary.rs`. Follow sibling test conventions discovered in Step 4 (assertion style, response validation, test naming). Each test gets:
- A `///` documentation comment explaining what it verifies
- Given-when-then section comments inside the test body
- Value-based assertions (assert on actual severity counts, not just collection lengths)

Run `cargo test` to verify all tests pass. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

Verify each criterion:
1. GET endpoint returns correct JSON shape with severity counts
2. Returns 404 for non-existent SBOM ID
3. Deduplication logic confirmed in service method
4. Default zeros confirmed via `Default` impl on `SeveritySummary`
5. Performance -- the query uses indexed join table; verified acceptable for 500 advisories

## Step 9 -- Self-Verification

1. **Scope containment**: Run `git diff --name-only` and confirm only the 6 in-scope files are changed
2. **Untracked file check**: Run `git status --short` to find `??` entries; check for references in staged code
3. **Dead parameter detection**: Scan modified functions for unused parameters
4. **Sensitive-pattern check**: Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
5. **Documentation currency**: Check if `docs/api.md` needs updating for the new endpoint
6. **CI checks from CONVENTIONS.md**: Run all CI check commands extracted in Step 4
7. **Data-flow trace**: Trace the full path: HTTP request -> Path extraction -> AdvisoryService.severity_summary() -> DB query -> SeveritySummary response -> JSON serialization -> HTTP response. Verify all stages connected.
8. **Contract & sibling parity**: Verify SeveritySummary implements required derives; verify endpoint handler follows same patterns as sibling handlers
9. **Duplication check**: Search for existing severity aggregation logic to avoid duplication

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated vulnerability advisory severity counts (critical, high,
medium, low, total) for a given SBOM. Includes SeveritySummary model,
AdvisoryService.severity_summary() method, and integration tests.

Implements TC-9201
```

### Commit command

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
aggregated vulnerability advisory severity counts (critical, high,
medium, low, total) for a given SBOM. Includes SeveritySummary model,
AdvisoryService.severity_summary() method, and integration tests.

Implements TC-9201"
```

### Fork detection and PR creation

Run `git remote get-url upstream 2>/dev/null` to detect fork.

If no fork:
```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "..."
```

The PR description includes:
- `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)` (clickable Jira link)
- `Closes <owner>/<repo>#<number>` if GitHub Issue custom field was populated
- Summary of changes

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format
2. Add a comment to TC-9201 with PR link, summary of changes, and any deviations
3. Transition TC-9201 to "In Review" via `jira.transition_issue`
