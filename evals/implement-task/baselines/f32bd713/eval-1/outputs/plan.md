# Implementation Plan for TC-9201

## Task Summary

**Jira ID**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Serena Instance**: serena_backend
**Dependencies**: None
**Bookend Type**: None
**Target PR**: None
**webUrl**: https://redhat.atlassian.net/browse/TC-9201

## Step-by-Step Execution

### Step 0 -- Validate Project Configuration

CLAUDE.md contains all required sections:
- Repository Registry: trustify-backend mapped to serena_backend at path `./`
- Jira Configuration: Project key TC, Cloud ID, Feature issue type ID, custom fields
- Code Intelligence: serena_backend with rust-analyzer

Validation passes. Proceed.

### Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all Jira operations, with REST API fallback if MCP fails.

### Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201:
- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify**: 3 files (advisory.rs service, endpoints/mod.rs, model/mod.rs); server/src/main.rs confirmed no changes needed
- **Files to Create**: 3 files (severity_summary.rs model, severity_summary.rs endpoint, advisory_summary.rs test)
- **API Changes**: GET /api/v2/sbom/{id}/advisory-summary (NEW)
- **Implementation Notes**: Present with specific patterns
- **Acceptance Criteria**: 5 items
- **Test Requirements**: 4 items
- **Dependencies**: None
- **GitHub Issue custom field**: customfield_10747 -- would check for linked GitHub issue

### Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9201)` and search for comments starting with `[sdlc-workflow] Description digest:`. If a digest comment is found, would:
1. Check for comment editing (compare `created` vs `updated` timestamps)
2. Extract the tagged digest value (e.g., `sha256-md:<hex>`)
3. Write description to `/tmp/desc-TC-9201.txt` and compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
4. Compare format tags; if matching, compare hex digests
5. On mismatch, alert user and wait for decision

If no digest comment found, log warning and proceed (backward compatibility).

### Step 2 -- Verify Dependencies

No dependencies listed. Skip.

### Step 3 -- Transition to In Progress and Assign

1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9201)` to In Progress

### Step 4 -- Understand the Code

**Serena inspection** (using `mcp__serena_backend__<tool>`):

1. `get_symbols_overview` on:
   - `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService methods (fetch, list, search)
   - `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `modules/fundamental/src/advisory/model/mod.rs` -- understand module registration pattern
   - `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct and its severity field

2. `find_symbol` with `include_body=true` on:
   - `AdvisoryService::fetch` -- understand the method signature and pattern
   - `AdvisoryService::list` -- understand query patterns
   - Route registration in endpoints/mod.rs -- understand how routes are added

3. `find_referencing_symbols` on:
   - Any symbols being modified to ensure backward compatibility

4. `search_for_pattern` on:
   - `sbom_advisory` entity to understand the join table structure
   - `AppError` usage patterns for error handling

5. **Sibling analysis** (convention conformance):
   - `get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` -- sibling endpoint pattern
   - `get_symbols_overview` on `modules/fundamental/src/sbom/model/summary.rs` -- sibling model pattern
   - `get_symbols_overview` on `modules/fundamental/src/sbom/service/sbom.rs` -- sibling service pattern
   - `get_symbols_overview` on `tests/api/sbom.rs` -- sibling test pattern
   - `get_symbols_overview` on `tests/api/advisory.rs` -- sibling test pattern

6. **CONVENTIONS.md lookup**: Read `./CONVENTIONS.md` at repository root. Extract CI check commands (formatting, linting, compilation) and any code generation commands for use in Step 9.

7. **Documentation files identified**:
   - `docs/api.md` -- REST API reference, may need updating for new endpoint
   - `README.md` -- general project documentation
   - `docs/architecture.md` -- system architecture

### Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6-9 -- Implementation, Tests, Verification

See file-level descriptions below (file-1 through file-6).

### Step 9 -- Self-Verification

1. **Scope containment**: `git diff --name-only` must show only the 6 files (3 modified, 3 created). Flag any out-of-scope files.
2. **Untracked file check**: `git status --short` to find untracked files in modified directories.
3. **Dead parameter detection**: Scan modified functions for unused parameters after changes.
4. **Sensitive-pattern check**: `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'`
5. **Documentation currency**: Check if `docs/api.md` needs updating for the new endpoint.
6. **Duplication check**: Search for existing severity aggregation logic in the repository.
7. **CI checks from CONVENTIONS.md**: Run all CI check commands extracted in Step 4.
8. **Module-level test requirement (Rust)**: Run `cargo metadata --no-deps --format-version 1` from workspace root, resolve the package name for each modified crate (do NOT derive from nearest Cargo.toml -- use the `name` field from `cargo metadata`), then run `cargo test -p <crate-name>` for each affected crate.
9. **Data-flow trace**: Trace the advisory summary data flow:
   - Input: GET /api/v2/sbom/{id}/advisory-summary request with SBOM ID path parameter
   - Processing: Endpoint handler extracts Path<Id>, calls AdvisoryService::severity_summary, which queries sbom_advisory join table, joins to advisory table, aggregates by severity level, deduplicates by advisory ID
   - Output: JSON response with `{ critical, high, medium, low, total }` counts
   - All stages connected. Complete path.
10. **Query-scope verification**: The query scopes to a specific SBOM ID via the path parameter, matching the task's target scope.
11. **Contract & sibling parity**:
    - Contract: SeveritySummary struct implements Serialize (required for Json response)
    - Sibling parity: Handler follows same Result<T, AppError> pattern as get.rs, list.rs
    - Cross-module entity: Uses sbom_advisory join table read-only, no write conflicts
    - Caller-site: Route registered same way as existing routes in endpoints/mod.rs

### Step 10 -- Commit and Push

**Fork detection**: Run `git remote get-url upstream 2>/dev/null` to check for fork.

**Commit command**:
```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary response model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201"
```

**Push and create PR**:
```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning aggregated advisory severity counts per SBOM
- Add `SeveritySummary` response model with critical, high, medium, low, and total fields
- Add `AdvisoryService::severity_summary` method querying the sbom_advisory join table with deduplication
- Add integration tests covering valid SBOM, non-existent SBOM (404), empty advisories, and deduplication

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
EOF
)"
```

### Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL using ADF format
2. Add comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 to In Review

## Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns aggregated
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary response model,
AdvisoryService::severity_summary method, and integration tests.

Implements TC-9201
Assisted-by: Claude Code
```

## Files Summary

| # | File | Action | Description |
|---|------|--------|-------------|
| 1 | `modules/fundamental/src/advisory/model/severity_summary.rs` | Create | SeveritySummary response struct |
| 2 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | Create | GET handler for advisory severity summary |
| 3 | `tests/api/advisory_summary.rs` | Create | Integration tests for the new endpoint |
| 4 | `modules/fundamental/src/advisory/service/advisory.rs` | Modify | Add severity_summary method to AdvisoryService |
| 5 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Modify | Register the new severity_summary route |
| 6 | `modules/fundamental/src/advisory/model/mod.rs` | Modify | Add pub mod severity_summary; declaration |

## Branch

`TC-9201` (branched from `main`)
