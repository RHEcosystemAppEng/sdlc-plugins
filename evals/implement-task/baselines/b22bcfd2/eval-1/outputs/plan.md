# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Status**: To Do
**Parent Feature**: TC-9001 (is incorporated by)
**Dependencies**: None

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required Project Configuration sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present, contains Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present, with tool naming convention `mcp__<serena-instance>__<tool>` and `serena_backend` configured with `rust-analyzer`

All sections are present and complete. Proceed.

## Step 1 -- Fetch and Parse Jira Task

Fetch the issue via `jira.get_issue(TC-9201)` and parse the structured description.

### Extracted Sections

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed (auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Implementation Notes**: Follow existing patterns in `get.rs`, use `sbom_advisory` join table, use `AdvisorySummary.severity` field for counting, return `AppError` with `.context()` wrapping
- **Acceptance Criteria**: 5 criteria (correct response shape, 404 for missing SBOM, deduplication, zero defaults, performance)
- **Test Requirements**: 4 tests (correct counts, 404, zeros, deduplication)
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None

### Target Branch Extraction

Target Branch is `main`. This will be used as `--base main` when creating the PR in Step 10.

### GitHub Issue Extraction

GitHub Issue custom field (`customfield_10747`) would be checked on the fetched issue. If present, parse the GitHub issue URL for use in the PR description's `Closes` line.

## Step 1.5 -- Verify Description Integrity

1. Retrieve issue comments via `jira.get_issue_comments(TC-9201)`.
2. Search for comments whose body starts with `[sdlc-workflow] Description digest:`.
3. If multiple digest comments exist, select the most recent one by `created` timestamp.
4. If a digest comment is found:
   - Check if `updated` > `created` (warn if edited after posting).
   - Extract the tagged digest value (e.g., `sha256-md:a1b2...` or `sha256-adf:a1b2...`).
   - If legacy untagged format (`sha256:<hex>`), log warning and skip integrity check.
   - Compute the current digest by writing the description to a temp file and running:
     ```bash
     python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt
     ```
   - Compare format tags; if mismatched, log warning and proceed.
   - Compare hex digests when tags match; if mismatch, alert user and stop for confirmation.
5. If no digest comment is found: log warning "No description digest found -- skipping integrity check" and proceed.

## Step 2 -- Verify Dependencies

The task lists "Depends on: None". No dependency verification needed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user: `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition: `jira.transition_issue(TC-9201)` to "In Progress"

## Step 4 -- Understand the Code

Use Serena instance `serena_backend` (from Repository Registry) with tools called as `mcp__serena_backend__<tool>`.

### Files to Inspect

1. **Existing files to modify**:
   - `modules/fundamental/src/advisory/service/advisory.rs` -- use `mcp__serena_backend__get_symbols_overview` to see AdvisoryService structure, then `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` and `list` methods to understand existing patterns
   - `modules/fundamental/src/advisory/endpoints/mod.rs` -- overview to see route registration pattern
   - `modules/fundamental/src/advisory/model/mod.rs` -- overview to see module registration pattern

2. **Sibling files for convention analysis**:
   - `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler (referenced in Implementation Notes)
   - `modules/fundamental/src/advisory/endpoints/list.rs` -- another sibling endpoint handler
   - `modules/fundamental/src/advisory/model/summary.rs` -- sibling model (AdvisorySummary with `severity` field)
   - `modules/fundamental/src/advisory/model/details.rs` -- sibling model
   - `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module sibling for SBOM endpoint pattern
   - `modules/fundamental/src/sbom/endpoints/list.rs` -- cross-module sibling for SBOM list pattern

3. **Referenced code**:
   - `entity/src/sbom_advisory.rs` -- join table for SBOM-Advisory relationship
   - `common/src/error.rs` -- AppError enum and `.context()` pattern

4. **Backward compatibility check**:
   - Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify callers
   - Use `mcp__serena_backend__find_referencing_symbols` on `advisory/model/mod.rs` to check existing module consumers

5. **Test sibling files**:
   - `tests/api/advisory.rs` -- sibling test file for advisory endpoints
   - `tests/api/sbom.rs` -- sibling test file for SBOM endpoints

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at repository root (`./CONVENTIONS.md`). The repo structure shows this file exists. Read it and extract:
- Naming rules, directory structure, code patterns, test conventions
- CI check commands (from "CI checks" or "Verification" section)
- Code generation commands

### Documentation File Identification

- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating with new endpoint)
- `docs/architecture.md` -- system architecture overview

### Convention Conformance Analysis

(See outputs/conventions.md for full analysis)

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201`

## Step 6 -- Implement Changes

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- SeveritySummary response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler for `/api/v2/sbom/{id}/advisory-summary`

### Files to Modify

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;`
4. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register new route

### Files to Create (Tests)

6. **`tests/api/advisory_summary.rs`** -- integration tests

(See outputs/file-1-description.md through outputs/file-6-description.md for detailed changes)

### Documentation Impact

- `docs/api.md` may need updating with the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint documentation. Evaluate after implementation.
- No architectural changes, so `docs/architecture.md` does not need updating.

## Step 7 -- Write Tests

Implement tests described in Test Requirements (see outputs/file-6-description.md for details):
1. Test valid SBOM with known advisories returns correct severity counts
2. Test non-existent SBOM ID returns 404
3. Test SBOM with no advisories returns all zeros
4. Test duplicate advisory links are deduplicated

Run `cargo test` to verify all tests pass. Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }` -- verified by test 1
2. Returns 404 when SBOM ID does not exist -- verified by test 2
3. Counts only unique advisories (deduplicates by advisory ID) -- verified by test 4
4. All severity levels default to 0 when no advisories exist -- verified by test 3
5. Response time under 200ms for SBOMs with up to 500 advisories -- verified by query design (single aggregation query)

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and verify all modified/created files are within the task's scope:
- `modules/fundamental/src/advisory/model/severity_summary.rs` (Files to Create)
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs` (Files to Create)
- `tests/api/advisory_summary.rs` (Files to Create)
- `modules/fundamental/src/advisory/model/mod.rs` (Files to Modify)
- `modules/fundamental/src/advisory/service/advisory.rs` (Files to Modify)
- `modules/fundamental/src/advisory/endpoints/mod.rs` (Files to Modify)
- `server/src/main.rs` -- task says "no changes needed", confirm no changes made

If `docs/api.md` was updated (documentation impact), flag as out-of-scope and ask user to approve.

### Untracked File Check

Run `git status --short` and check for `??` entries in directories where implementation work occurred. Flag any referenced untracked files for user review.

### Sensitive-Pattern Check

Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` and verify no secrets are present.

### Documentation Currency

If `docs/api.md` describes existing advisory endpoints, it should be updated with the new endpoint. Check and update if needed.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract `id` from path (input) -> call `AdvisoryService::severity_summary(id, tx)` (processing) -> query `sbom_advisory` join table, count by severity (processing) -> return `SeveritySummary` as JSON (output) -- **COMPLETE**

### Contract & Sibling Parity

- `SeveritySummary` is a new standalone struct, no trait/interface contract to implement beyond `Serialize` and `Deserialize`
- Sibling parity with `get.rs` handler: both extract path params via `Path<Id>`, call service, return JSON -- verified
- Sibling parity with `fetch`/`list` service methods: `severity_summary` follows same signature pattern (`&self, id, tx`) -- verified

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` (if any). Hard stop on any failure.

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

### Commit Command

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

- Add \`GET /api/v2/sbom/{id}/advisory-summary\` endpoint returning severity counts per advisory level
- Add \`SeveritySummary\` response model with critical, high, medium, low, and total fields
- Add \`severity_summary\` method to \`AdvisoryService\` using \`sbom_advisory\` join table
- Add integration tests covering correct counts, 404, zero defaults, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
"
```

## Step 11 -- Update Jira

1. **Set Git Pull Request custom field** (`customfield_10875`) with the PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with PR link, summary of changes, and any deviations from plan.

3. **Transition** to "In Review": `jira.transition_issue(TC-9201)` to "In Review"
