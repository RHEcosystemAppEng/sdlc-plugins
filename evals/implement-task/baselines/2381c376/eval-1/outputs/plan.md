# Implementation Plan for TC-9201

## Task Summary

**Jira Issue**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Bookend Type**: None (standard implementation flow)
**Target PR**: None (create new branch and PR)
**Dependencies**: None

## Step 0 -- Validate Project Configuration

Verified the following sections exist in CLAUDE.md under `# Project Configuration`:

1. **Repository Registry** -- present with trustify-backend entry (Serena instance: `serena_backend`, Path: `./`)
2. **Jira Configuration** -- present with Project key `TC`, Cloud ID, Feature issue type ID `10142`
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend`

All required sections are present. Proceeding.

## Step 1 -- Fetch and Parse Jira Task

### Parsed Sections

| Section | Value |
|---------|-------|
| Repository | trustify-backend |
| Target Branch | main |
| Bookend Type | (none) |
| Target PR | (none) |
| Dependencies | None |
| GitHub Issue custom field | customfield_10747 (no value present on issue) |
| Git Pull Request custom field | customfield_10875 |
| Jira web URL | https://redhat.atlassian.net/browse/TC-9201 |

### Files to Modify

1. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
3. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
4. `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)

### Files to Create

1. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for /api/v2/sbom/{id}/advisory-summary
3. `tests/api/advisory_summary.rs` -- integration tests for the new endpoint

### API Changes

- `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`

### Acceptance Criteria

1. GET /api/v2/sbom/{id}/advisory-summary returns `{ critical: N, high: N, medium: N, low: N, total: N }`
2. Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints
3. Counts only unique advisories (deduplicates by advisory ID)
4. All severity levels default to 0 when no advisories exist at that level
5. Response time under 200ms for SBOMs with up to 500 advisories

### Test Requirements

1. Test that a valid SBOM with known advisories returns correct severity counts
2. Test that a non-existent SBOM ID returns 404
3. Test that an SBOM with no advisories returns all zeros
4. Test that duplicate advisory links are deduplicated in the count

## Step 1.5 -- Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments(TC-9201)` and locate any digest comment starting with `[sdlc-workflow] Description digest:`. Compare stored digest against computed digest of current description. (Skipped in eval -- no Jira access.)

## Step 2 -- Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 -- Transition to In Progress and Assign

Would perform:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue(TC-9201, assignee=<account-id>)` to assign
3. `jira.transition_issue(TC-9201)` to In Progress

(Skipped in eval -- no Jira access.)

## Step 4 -- Understand the Code

### Code Inspection Plan

Using Serena instance `serena_backend` (from Repository Registry):

1. **get_symbols_overview** on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService struct and existing methods (`fetch`, `list`, `search`)
2. **find_symbol** with `include_body=true` on `AdvisoryService::fetch` -- read the fetch method body to understand the pattern for the new `severity_summary` method
3. **get_symbols_overview** on `modules/fundamental/src/advisory/endpoints/get.rs` -- understand the endpoint handler pattern (Path extraction, service call, JSON response)
4. **find_symbol** with `include_body=true` on the get handler function -- read the full handler
5. **get_symbols_overview** on `modules/fundamental/src/advisory/model/summary.rs` -- understand AdvisorySummary struct and its `severity` field
6. **get_symbols_overview** on `modules/fundamental/src/advisory/endpoints/mod.rs` -- see route registration pattern
7. **find_referencing_symbols** on `AdvisoryService` -- identify all callers to ensure changes do not break them
8. **search_for_pattern** on `sbom_advisory` in `entity/src/` -- understand the join table structure
9. **get_symbols_overview** on `common/src/error.rs` -- understand AppError enum
10. **get_symbols_overview** on sibling files for convention analysis:
    - `modules/fundamental/src/sbom/endpoints/get.rs`
    - `modules/fundamental/src/sbom/model/summary.rs`
    - `tests/api/advisory.rs`

### CONVENTIONS.md Lookup

Repository path from Registry: `./`
Would check for `CONVENTIONS.md` at repository root. Per repo-backend.md, `CONVENTIONS.md` exists at the repo root. Would read it and extract:
- CI check commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo check`)
- Code generation commands (if any)
- Naming rules, directory structure, test conventions

### Convention Conformance Analysis

See `outputs/conventions.md` for the full conventions list derived from sibling analysis.

### Documentation File Identification

Identified documentation files:
- `README.md` at repository root
- `docs/api.md` -- REST API reference (relevant since we add a new endpoint)
- `docs/architecture.md` -- system architecture overview
- `CONVENTIONS.md` at repository root

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201`

## Step 6-9 -- Implementation, Tests, Verification

### Files to Create (3 files)

See `outputs/file-1-description.md` through `outputs/file-3-description.md` for detailed changes.

1. **file-1**: `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
2. **file-2**: `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler
3. **file-3**: `tests/api/advisory_summary.rs` -- integration tests

### Files to Modify (3 files with actual changes)

See `outputs/file-4-description.md` through `outputs/file-6-description.md` for detailed changes.

4. **file-4**: `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;`
5. **file-5**: `modules/fundamental/src/advisory/endpoints/mod.rs` -- register new route
6. **file-6**: `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method

### Files NOT Modified

- `server/src/main.rs` -- task description confirms no changes needed (routes auto-mount via module registration)

### Documentation Impact

- `docs/api.md` -- would need updating to document the new `GET /api/v2/sbom/{id}/advisory-summary` endpoint. This would be flagged in Step 9's documentation currency check but is technically out of scope per Files to Modify. Would flag for user approval.

## Step 9 -- Self-Verification Checks

### Scope Containment
- `git diff --name-only` would show exactly the 6 files listed above
- `server/src/main.rs` is listed in Files to Modify but has no changes -- skip it
- If `docs/api.md` or `tests/api/mod.rs` were modified, flag as out-of-scope for user approval

### Untracked File Check
- `tests/api/advisory_summary.rs` is a new file (untracked) -- referenced in test plan, would be staged

### Dead Parameter Detection
- No parameters removed from existing functions -- skip

### Sensitive-Pattern Check
- `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- expect no matches

### Duplication Check
- Search for existing severity counting logic across the repo
- Search for `severity_summary`, `SeveritySummary` to ensure no collision

### CI Checks from CONVENTIONS.md
- Run extracted CI commands (e.g., `cargo fmt --check`, `cargo clippy`, `cargo check`)
- Hard stop on any failure

### Module-level Test Requirement (Rust)
- Run `cargo metadata --no-deps --format-version 1` from workspace root
- Resolve crate names for modified files:
  - Files in `modules/fundamental/src/` belong to the `trustify-fundamental` crate (or similar name resolved from Cargo.toml)
  - Files in `tests/api/` belong to the integration test crate
- Run `cargo test -p <crate-name>` for each resolved crate
- Hard stop on test failure

### Data-Flow Trace
- **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with path parameter `id`
- **Processing**: Path parameter extracted via `Path<Id>` -> `AdvisoryService::severity_summary(id, tx)` called -> query `sbom_advisory` join table to find advisories linked to SBOM -> load each advisory's severity from `AdvisorySummary` -> deduplicate by advisory ID -> count by severity level (Critical, High, Medium, Low) -> compute total
- **Output**: JSON response `{ critical: N, high: N, medium: N, low: N, total: N }` via `Json<SeveritySummary>`
- All stages connected. Complete data flow verified.

### Query-Scope Verification
- The query scopes to a specific SBOM ID via the `sbom_advisory` join table -- correctly restricted to the target SBOM
- Deduplication by advisory ID ensures unique counts
- No broad/unscoped queries present

### Contract & Sibling Parity
- **Contract**: `severity_summary` method follows the same `Result<T, AppError>` return pattern as `fetch` and `list`
- **Sibling parity**: handler uses `Path<Id>`, calls service, returns `Json<T>` -- matches `get.rs` pattern; error handling uses `.context()` wrapping -- matches existing handlers
- **Cross-module entity**: reads from `sbom_advisory` join table (read-only) -- no write conflicts with other modules
- **Caller-site**: endpoint is a new consumer of `AdvisoryService` -- follows established calling pattern

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Enables dashboard widgets to render severity breakdowns without
client-side counting.

Implements TC-9201
```

Commit command:
```
git commit --trailer="Assisted-by: Claude Code" -m "$(cat <<'EOF'
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Enables dashboard widgets to render severity breakdowns without
client-side counting.

Implements TC-9201
EOF
)"
```

### Fork Detection

```
git remote get-url upstream 2>/dev/null
```

If upstream exists, use fork-aware PR creation. Otherwise, use default flow.

### Push and PR Creation

```
git push -u origin TC-9201
```

PR creation (no fork detected):
```
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint that returns severity counts (critical, high, medium, low, total) for advisories linked to a given SBOM
- Add `SeveritySummary` response model with derive macros for serialization and OpenAPI schema
- Add `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, deduplicates by advisory ID, and counts by severity level
- Integration tests covering valid SBOM, non-existent SBOM (404), empty advisory list, and deduplication

## Test plan

- [x] Test valid SBOM with known advisories returns correct severity counts
- [x] Test non-existent SBOM ID returns 404
- [x] Test SBOM with no advisories returns all zeros
- [x] Test duplicate advisory links are deduplicated in the count

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
EOF
)"
```

## Step 11 -- Update Jira

1. Update Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment to TC-9201 with PR link and summary of changes
3. Transition TC-9201 to In Review
