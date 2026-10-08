# Implementation Plan -- TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**webUrl**: https://redhat.atlassian.net/browse/TC-9201

## Pre-Implementation Steps

### Step 0 -- Validate Project Configuration

CLAUDE.md validated:
- Repository Registry: trustify-backend with Serena instance `serena_backend`, path `./`
- Jira Configuration: Project key TC, Cloud ID present, Feature issue type ID 10142
- Code Intelligence: `mcp__serena_backend__<tool>` convention documented

### Step 1 -- Fetch and Parse Jira Task

All required sections present in task description:
- Repository: trustify-backend
- Target Branch: main
- Description: present
- Files to Modify: 3 files listed
- Files to Create: 3 files listed
- API Changes: GET /api/v2/sbom/{id}/advisory-summary
- Implementation Notes: present with pattern references
- Acceptance Criteria: 5 items
- Test Requirements: 4 items
- Dependencies: None
- No Target PR (default flow)
- No Bookend Type (default flow)
- GitHub Issue custom field: `customfield_10747` -- would read from API response

### Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9201)` and search for
digest comments starting with `[sdlc-workflow] Description digest:`. Select the most
recent if multiple exist. If found, compute current digest via
`python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags and hex
values. On mismatch, prompt the user. If no digest comment found, log backward-compat
warning and proceed.

### Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

### Step 3 -- Transition to In Progress and Assign

1. `jira.user_info()` -- retrieve current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<current-user-account-id>)` -- assign task
3. `jira.transition_issue(TC-9201)` -> In Progress

### Step 4 -- Understand the Code

Would use Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`):

1. `get_symbols_overview` on:
   - `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService methods (fetch, list, search)
   - `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `modules/fundamental/src/advisory/model/mod.rs` -- understand model module re-exports

2. `find_symbol` with `include_body=true` on:
   - `AdvisoryService::fetch` -- understand service method pattern for the new `severity_summary` method
   - `AdvisoryService::list` -- secondary reference for service patterns
   - Route registration in `advisory/endpoints/mod.rs` -- understand how routes are added

3. `find_referencing_symbols` on:
   - `AdvisoryService` -- verify no breaking changes
   - `AdvisorySummary` -- understand usage of the severity field

4. Convention conformance analysis on siblings:
   - `modules/fundamental/src/advisory/endpoints/get.rs` -- endpoint handler pattern
   - `modules/fundamental/src/advisory/endpoints/list.rs` -- endpoint handler pattern
   - `modules/fundamental/src/advisory/model/summary.rs` -- model struct pattern
   - `modules/fundamental/src/sbom/endpoints/get.rs` -- cross-module endpoint comparison
   - `tests/api/advisory.rs` -- test pattern reference
   - `tests/api/sbom.rs` -- test pattern reference

5. `search_for_pattern` for:
   - `sbom_advisory` join table usage in `entity/src/sbom_advisory.rs`
   - `severity` field usage in `AdvisorySummary`
   - Existing deduplication patterns

6. CONVENTIONS.md check:
   - Would read `./CONVENTIONS.md` for CI check commands and coding standards
   - Extract verification commands for Step 9

7. Documentation files identified:
   - `README.md`, `CONVENTIONS.md`, `docs/api.md`, `docs/architecture.md`

## Step 5 -- Create Branch

```
git checkout main
git pull
git checkout -b TC-9201
```

## Files to Modify

### 1. `modules/fundamental/src/advisory/service/advisory.rs`

Add a `severity_summary` method to `AdvisoryService`. See `outputs/file-1-description.md`.

### 2. `modules/fundamental/src/advisory/endpoints/mod.rs`

Register the new `/api/v2/sbom/{id}/advisory-summary` route. See `outputs/file-2-description.md`.

### 3. `modules/fundamental/src/advisory/model/mod.rs`

Add `pub mod severity_summary;` to register the new model module. See `outputs/file-3-description.md`.

## Files to Create

### 4. `modules/fundamental/src/advisory/model/severity_summary.rs`

New `SeveritySummary` response struct. See `outputs/file-4-description.md`.

### 5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`

New GET handler for `/api/v2/sbom/{id}/advisory-summary`. See `outputs/file-5-description.md`.

### 6. `tests/api/advisory_summary.rs`

Integration tests for the new endpoint. See `outputs/file-6-description.md`.

## Step 9 -- Self-Verification Plan

### Scope containment
- Run `git diff --name-only` and verify only the 6 files listed above are modified/created.
- Flag any out-of-scope files for user approval.

### Untracked file check
- Run `git status --short`, filter `??` entries in modified directories.
- Search staged diff for references to untracked filenames.

### Dead parameter detection
- Scan modified functions for parameters no longer referenced in function bodies.

### Sensitive-pattern check
- Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`

### Documentation currency
- Check if `docs/api.md` needs updating with the new endpoint.
- If so, update with new GET /api/v2/sbom/{id}/advisory-summary documentation.

### CI checks from CONVENTIONS.md
- Run all CI check commands extracted from CONVENTIONS.md.
- Hard stop on any non-zero exit.

### Module-level test requirement (Rust)
- Run `cargo metadata --no-deps --format-version 1` from workspace root.
- Resolve crate names for modified files (do NOT derive from nearest Cargo.toml).
- For files under `modules/fundamental/src/`, use the package name from `modules/fundamental/Cargo.toml` as resolved by cargo metadata.
- For files under `tests/`, use the package name from `tests/Cargo.toml` as resolved by cargo metadata.
- Run `cargo test -p <crate-name>` for each resolved crate.
- Hard stop on test failure.

### Data-flow trace
- Input: GET request with SBOM ID path parameter
- Processing: Handler extracts `Path<Id>`, calls `AdvisoryService::severity_summary(sbom_id, tx)`, which queries `sbom_advisory` join table, fetches linked advisories, groups by severity from `AdvisorySummary`, deduplicates by advisory ID, counts per level
- Output: JSON response `{ critical: N, high: N, medium: N, low: N, total: N }`
- All stages connected. Complete path verified.

### Query-scope verification
- Query targets advisories linked to a specific SBOM (filtered by `sbom_id`).
- Uses `sbom_advisory` join table with SBOM ID filter -- correctly scoped, not loading all advisories.

### Contract and sibling parity
- **Contract**: `SeveritySummary` implements `Serialize` for JSON response; handler returns `Result<Json<SeveritySummary>, AppError>` matching Axum contract.
- **Sibling parity**: Error handling uses `.context()` like `get.rs`/`list.rs`; 404 on missing SBOM matches existing SBOM endpoint behavior.
- **Cross-module entity**: `sbom_advisory` join table read-only access, no write contention.
- **Caller-site**: N/A (new endpoint, no existing callers).

### Duplication check
- Search for existing severity counting/aggregation logic in the codebase.
- Verify no existing utility duplicates the new `severity_summary` function.

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add a service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM. The endpoint GET
/api/v2/sbom/{id}/advisory-summary returns counts per severity level
(Critical, High, Medium, Low) and a total.

Implements TC-9201
```

### Commit Command

```
git add modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "$(cat <<'EOF'
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add a service method and REST endpoint that aggregates vulnerability
advisory severity counts for a given SBOM. The endpoint GET
/api/v2/sbom/{id}/advisory-summary returns counts per severity level
(Critical, High, Medium, Low) and a total.

Implements TC-9201
EOF
)"
```

### Fork Detection

Before creating a PR, would run:
```
git remote get-url upstream 2>/dev/null
```
- If succeeds: parse `<upstream-owner/repo>` and `<fork-owner>`, use `-R` and `--head` flags.
- If fails: use default `gh pr create` behavior.

### Push and PR Creation

```
git push -u origin TC-9201
```

No fork detected (default flow):
```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "$(cat <<'EOF'
## Summary
- Add `SeveritySummary` response struct for advisory severity counts
- Add `severity_summary` method to `AdvisoryService` that aggregates severity counts from advisories linked to an SBOM via the `sbom_advisory` join table
- Add GET `/api/v2/sbom/{id}/advisory-summary` endpoint returning `{ critical, high, medium, low, total }`
- Add integration tests for the new endpoint covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

## Test plan
- [ ] Verify GET /api/v2/sbom/{id}/advisory-summary returns correct severity counts for a known SBOM
- [ ] Verify 404 response for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
- [ ] Verify deduplication of advisory links in severity counts

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
EOF
)"
```

If GitHub Issue was extracted from `customfield_10747`, would append `Closes <owner>/<repo>#<number>` to PR body.

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format:
   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. Add comment to TC-9201 with PR link, summary of changes, and any deviations.

3. Transition: `jira.transition_issue(TC-9201)` -> In Review
