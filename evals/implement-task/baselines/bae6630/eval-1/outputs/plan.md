# Implementation Plan for TC-9201

## Task Summary

**Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains all required sections:
- **Repository Registry** -- present, contains `trustify-backend` with Serena Instance `serena_backend` and Path `./`
- **Jira Configuration** -- present, contains Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
- **Code Intelligence** -- present, lists `serena_backend` with `rust-analyzer`

All required sections are present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all JIRA operations. If MCP fails, prompt the user for REST API fallback.

## Step 1 -- Fetch and Parse Jira Task

Fetch task via `jira.get_issue(TC-9201)`. Parse the structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
  - `server/src/main.rs` -- no changes needed (routes auto-mount)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
  - `tests/api/advisory_summary.rs` -- integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW
- **Target PR**: not present (default flow)
- **Bookend Type**: not present (default flow)
- **Dependencies**: None
- **GitHub Issue custom field**: check `customfield_10747` on the fetched issue; extract owner/repo#number if present for PR description

Capture the issue's `webUrl` (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description.

## Step 1.5 -- Verify Description Integrity

1. Retrieve issue comments: `jira.get_issue_comments(TC-9201)`
2. Search for comments starting with `[sdlc-workflow] Description digest:`
3. **If no digest comment found**: Log warning and proceed:
   > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."
4. **If digest comment found**:
   - Check for comment editing (compare `created` vs `updated` timestamps)
   - Extract the stored digest (tagged format like `sha256-md:<hex>` or `sha256-adf:<hex>`)
   - Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
   - Compare format tags; if mismatched, warn and proceed
   - Compare hex digests; if mismatched, alert user and ask whether to proceed or stop

## Step 2 -- Verify Dependencies

No dependencies listed. Skip.

## Step 3 -- Transition to In Progress and Assign

1. `jira.user_info()` to get current user account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. `jira.transition_issue(TC-9201)` to In Progress

## Step 4 -- Understand the Code

### Code Inspection

Inspect the following files before modifying using the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** -- use `mcp__serena_backend__get_symbols_overview` to understand the existing endpoint pattern (path params via `Path<Id>`, calling service, returning JSON). This is the primary pattern reference for the new endpoint handler.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- use `mcp__serena_backend__get_symbols_overview` to see AdvisoryService structure, then `mcp__serena_backend__find_symbol` with `include_body=true` on `fetch` and `list` methods to understand the method signature pattern (`&self, id: Id, tx: &Transactional<'_>`).

3. **`modules/fundamental/src/advisory/model/summary.rs`** -- use `mcp__serena_backend__find_symbol` on `AdvisorySummary` to see the `severity` field type and derive macros used.

4. **`common/src/error.rs`** -- use `mcp__serena_backend__get_symbols_overview` to understand `AppError` enum and how `.context()` wrapping works.

5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- inspect route registration pattern (`Router::new().route(...)` calls).

6. **`modules/fundamental/src/advisory/model/mod.rs`** -- inspect existing module declarations to follow the `pub mod` pattern.

7. **`entity/src/sbom_advisory.rs`** -- inspect the SBOM-Advisory join table entity for SeaORM column definitions and relations needed by the aggregation query.

### CONVENTIONS.md Lookup

Check for `CONVENTIONS.md` at repository root (`./CONVENTIONS.md`). Per the repo structure, `CONVENTIONS.md` exists. Read it for:
- Naming rules, directory structure, code patterns, test conventions
- CI check commands (extract for Step 9)
- Code generation commands (extract for Step 9)

### Documentation File Identification

Identify documentation files for review:
- `README.md` at repository root
- `docs/architecture.md` -- system architecture overview
- `docs/api.md` -- REST API reference (likely needs updating for the new endpoint)

### Convention Conformance Analysis

See `outputs/conventions.md` for the full conventions analysis.

### Test Convention Analysis

Inspect sibling test files to understand test patterns:
- `tests/api/advisory.rs` -- advisory endpoint integration tests
- `tests/api/sbom.rs` -- SBOM endpoint integration tests

Analysis of test patterns documented in `outputs/conventions.md`.

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

This creates branch `TC-9201` from the Target Branch `main`.

## Step 6 -- Implement Changes

### Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add `severity_summary` method to AdvisoryService following the same pattern as `fetch` and `list`:
   - See `outputs/file-1-description.md` for detailed changes

2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route:
   - See `outputs/file-2-description.md` for detailed changes

3. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add module declaration:
   - See `outputs/file-3-description.md` for detailed changes

4. **`server/src/main.rs`** -- No changes needed (routes auto-mount via module registration)

### Files to Create

5. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- New SeveritySummary struct:
   - See `outputs/file-4-description.md` for detailed changes

6. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- New GET handler:
   - See `outputs/file-5-description.md` for detailed changes

7. **`tests/api/advisory_summary.rs`** -- Integration tests:
   - See `outputs/file-6-description.md` for detailed changes

### Code Quality Practices

- Every new struct, enum, and public function will have a `///` doc comment
- Follow existing patterns from sibling files exactly

### Documentation Impact

- Update `docs/api.md` to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint

## Step 7 -- Write Tests

Implement tests in `tests/api/advisory_summary.rs` following sibling test conventions from `tests/api/advisory.rs` and `tests/api/sbom.rs`:
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern
- Test names follow `test_<endpoint>_<scenario>` pattern
- Include `/// ` doc comments on every test function
- Include given-when-then section comments for non-trivial tests
- Assert on actual values, not just collection lengths

Run tests:
```bash
cargo test --test advisory_summary
```

Fix any failures before proceeding.

## Step 8 -- Verify Acceptance Criteria

Verify each criterion:
- [ ] GET /api/v2/sbom/{id}/advisory-summary returns correct shape
- [ ] Returns 404 for non-existent SBOM ID
- [ ] Counts only unique advisories (deduplicates by advisory ID)
- [ ] All severity levels default to 0
- [ ] Response time under 200ms for up to 500 advisories

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against Files to Modify and Files to Create. Flag any out-of-scope files.

### Untracked File Check

Run `git status --short`, filter `??` entries by proximity to modified directories, search for code references.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

### Documentation Currency

Check that `docs/api.md` is updated for the new endpoint.

### CI Checks from CONVENTIONS.md

Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any failure.

### Data-Flow Trace

- `GET /api/v2/sbom/{id}/advisory-summary` -> extract SBOM ID from path -> call `AdvisoryService::severity_summary(sbom_id, tx)` -> query `sbom_advisory` join table -> aggregate severity counts from `AdvisorySummary.severity` -> return `SeveritySummary` as JSON -- **COMPLETE**

### Contract & Sibling Parity

- Verify `SeveritySummary` serialization matches expected JSON shape
- Compare new endpoint handler against sibling `get.rs` for parity (error handling, response wrapping)
- Compare new service method against sibling `fetch`/`list` methods for parity (transaction handling, error wrapping)

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
and integration tests.

Implements TC-9201
```

### Commit Command

```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
and integration tests.

Implements TC-9201"
```

### Push and Create PR

```bash
git push -u origin TC-9201

gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "## Summary

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns severity counts (critical, high, medium, low, total) for advisories linked to a given SBOM.

- SeveritySummary response model
- AdvisoryService::severity_summary method
- GET handler with 404 handling for missing SBOMs
- Integration tests for happy path, 404, empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)"
```

If GitHub Issue reference was found in `customfield_10747`, append `Closes <owner>/<repo>#<number>` to the PR body.

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with the PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. Add a Jira comment with:
   - PR link
   - Summary of changes made
   - Any deviations from the plan
   - Comment footer with sdlc-workflow version from `plugins/sdlc-workflow/.claude-plugin/plugin.json`

3. Transition the task:
   ```
   jira.transition_issue(TC-9201) -> In Review
   ```
