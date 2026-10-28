# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Branch Name**: TC-9201
**Status**: To Do
**Dependencies**: None
**Bookend Type**: None
**Target PR**: None

## Skill Workflow Execution

### Step 0 -- Validate Project Configuration

The project's CLAUDE.md contains all required sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
2. **Jira Configuration** -- present with Project key (TC), Cloud ID, Feature issue type ID
3. **Code Intelligence** -- present with tool naming convention `mcp__<serena-instance>__<tool>` and configured instance `serena_backend` using `rust-analyzer`

Validation: PASSED. Proceed.

### Step 0.5 -- JIRA Access Initialization

Would attempt MCP first for all JIRA operations. If MCP fails, prompt user for REST API fallback.

### Step 1 -- Fetch and Parse Jira Task

Would call: `jira.get_issue("TC-9201")`

Parsed sections from structured description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM
- **Files to Modify**: 3 files (advisory service, endpoints/mod.rs, model/mod.rs)
- **Files to Create**: 3 files (severity_summary model, severity_summary endpoint, integration tests)
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` (NEW)
- **Implementation Notes**: Follow existing endpoint pattern, use sbom_advisory join table, etc.
- **Acceptance Criteria**: 5 items
- **Test Requirements**: 4 items
- **Dependencies**: None
- **webUrl**: captured from API response for PR description linking

**GitHub Issue extraction**: Would check `customfield_10747` on the fetched issue. If populated, parse the GitHub issue URL to extract `owner/repo#number` for use in the PR description `Closes` line.

### Step 1.5 -- Verify Description Integrity

Would execute the description digest protocol:

1. Fetch all comments: `jira.get_issue_comments("TC-9201")`
2. Search for comments starting with `[sdlc-workflow] Description digest:`
3. If multiple matches, select the most recent by `created` timestamp
4. If found: check comment edit timestamps (`created` vs `updated`), extract tagged digest (e.g., `sha256-md:<hex>`), write current description to `/tmp/desc-TC-9201.txt`, compute digest via `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags, then compare hex digests
5. If no digest comment found: log warning ("No description digest found -- skipping integrity check") and proceed
6. If digest mismatch: alert user with expected vs actual, ask whether to proceed or stop

### Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

### Step 3 -- Transition to In Progress and Assign

Would execute:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue("TC-9201", assignee=<account-id>)` to assign
3. `jira.transition_issue("TC-9201")` to "In Progress"

### Step 4 -- Understand the Code

Would use Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`).

#### 4a. Inspect files to modify

1. `mcp__serena_backend__get_symbols_overview` on:
   - `modules/fundamental/src/advisory/service/advisory.rs` -- understand `AdvisoryService` struct and existing methods (`fetch`, `list`, `search`)
   - `modules/fundamental/src/advisory/endpoints/mod.rs` -- understand route registration pattern
   - `modules/fundamental/src/advisory/model/mod.rs` -- understand module re-exports

2. `mcp__serena_backend__find_symbol` with `include_body=true` on:
   - `AdvisoryService::fetch` -- read the method body to understand the service pattern (parameters, return type, error handling, transactional usage)
   - `AdvisoryService::list` -- read for comparison
   - `AdvisorySummary` struct -- read to see the `severity` field type and shape

3. `mcp__serena_backend__find_referencing_symbols` on:
   - `AdvisoryService` -- identify all callers to ensure new method doesn't conflict

4. `mcp__serena_backend__search_for_pattern` for:
   - `sbom_advisory` -- find the join table usage patterns
   - `AppError` -- understand error variant usage in endpoints

#### 4b. Inspect sibling files for convention conformance

Siblings analyzed:
- **Endpoint siblings**: `modules/fundamental/src/advisory/endpoints/get.rs`, `modules/fundamental/src/advisory/endpoints/list.rs` -- handler signature, path extraction, service call, response pattern
- **Model siblings**: `modules/fundamental/src/advisory/model/summary.rs`, `modules/fundamental/src/advisory/model/details.rs` -- struct definition, derives, field types
- **Service siblings**: `modules/fundamental/src/sbom/service/sbom.rs` -- cross-domain service method pattern
- **Test siblings**: `tests/api/advisory.rs`, `tests/api/sbom.rs` -- test setup, assertion patterns, error case coverage

#### 4c. CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at repository root (`./CONVENTIONS.md`). If present, read it and extract:
- CI check commands (formatting, linting, compilation) for Step 9
- Code generation commands
- Any naming or structure conventions

#### 4d. Documentation file identification

Would identify:
- `docs/api.md` -- may need updating with the new endpoint
- `docs/architecture.md` -- likely no changes needed
- `README.md` -- likely no changes needed

#### 4e. Symbol deduplication check

Before declaring `SeveritySummary`, would search for existing definitions:
- `mcp__serena_backend__find_symbol(name_path_pattern="SeveritySummary")` or Grep for `SeveritySummary`
- Search for severity-related constants or enums that could be reused

### Step 5 -- Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

### Step 6 -- Implement Changes

See file-N-description.md files for detailed changes to each file.

#### Files to Modify

| # | File | Change Summary |
|---|------|---------------|
| 1 | `modules/fundamental/src/advisory/service/advisory.rs` | Add `severity_summary` method to `AdvisoryService` |
| 2 | `modules/fundamental/src/advisory/endpoints/mod.rs` | Register new route for severity summary endpoint |
| 3 | `modules/fundamental/src/advisory/model/mod.rs` | Add `pub mod severity_summary;` |

#### Files to Create

| # | File | Description |
|---|------|------------|
| 4 | `modules/fundamental/src/advisory/model/severity_summary.rs` | `SeveritySummary` response struct |
| 5 | `modules/fundamental/src/advisory/endpoints/severity_summary.rs` | GET handler for `/api/v2/sbom/{id}/advisory-summary` |
| 6 | `tests/api/advisory_summary.rs` | Integration tests for the new endpoint |

#### Documentation Impact

After implementing code changes, would check `docs/api.md` for API documentation. Since a new public endpoint (`GET /api/v2/sbom/{id}/advisory-summary`) is being added, would add an entry documenting the endpoint, its parameters, and response shape.

### Step 7 -- Write Tests

See `outputs/file-6-description.md` for detailed test implementation.

Tests cover all 4 requirements:
1. Valid SBOM with known advisories returns correct severity counts
2. Non-existent SBOM ID returns 404
3. SBOM with no advisories returns all zeros
4. Duplicate advisory links are deduplicated in the count

### Step 8 -- Verify Acceptance Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| 1 | GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Endpoint implemented, struct has all 5 fields, handler returns Json<SeveritySummary> |
| 2 | Returns 404 when SBOM ID does not exist | Service method checks SBOM existence first, returns AppError not-found variant |
| 3 | Counts only unique advisories (deduplicates by advisory ID) | Query uses `.distinct()` or collects into HashSet by advisory ID before counting |
| 4 | All severity levels default to 0 when no advisories exist | SeveritySummary fields default to 0 via `Default` derive or explicit initialization |
| 5 | Response time under 200ms for SBOMs with up to 500 advisories | Single query with join and GROUP BY; no N+1; verified by test with timing assertion or manual check |

### Step 9 -- Self-Verification

#### Scope containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create. All 6 files are in scope. If `tests/api/mod.rs` or `tests/Cargo.toml` needed modification to register the new test module, those would be flagged as out-of-scope and presented to the user for approval.

#### Untracked file check
Run `git status --short`, filter `??` entries in directories with modified files. Flag any referenced untracked files for user approval.

#### Dead parameter detection
Scan modified functions for parameters no longer referenced in the body. Not expected for this task since we are adding code, not removing.

#### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- no matches expected.

#### Documentation currency
Verify `docs/api.md` covers the new endpoint if it was identified as relevant in Step 4.

#### Duplication check
Search for existing severity aggregation logic in the repository to ensure we are not duplicating.

#### CI checks from CONVENTIONS.md
Run all CI check commands extracted from `CONVENTIONS.md` in Step 4. Hard stop on any failure.

#### Module-level test requirement (Rust)

Resolve crate names using `cargo metadata`:

```bash
cargo metadata --no-deps --format-version 1
```

Parse the JSON output to find packages. For each modified file, find which package's manifest directory or source targets contain the file path:

- Files in `modules/fundamental/src/...` -- find the package whose `manifest_path` is `modules/fundamental/Cargo.toml`. Extract its `name` field (e.g., `trustify-fundamental` or whatever the crate is named). The crate name comes from the `name` field in the metadata output, NOT from the directory name or nearest `Cargo.toml` (which may be a virtual workspace manifest).
- Files in `tests/api/...` -- find the package whose `manifest_path` is `tests/Cargo.toml`. Extract its `name` field.

Then run tests for each resolved crate:

```bash
cargo test -p <fundamental-crate-name>
cargo test -p <tests-crate-name>
```

Hard stop if any test command exits non-zero.

#### Data-flow trace

Traced flow for the new feature:

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID as path parameter
2. **Processing (endpoint)**: Axum extracts `Path<Id>`, calls `AdvisoryService::severity_summary(sbom_id, &tx)`
3. **Processing (service)**: Queries `sbom_advisory` join table for the given SBOM ID, joins to advisory table, extracts severity from each `AdvisorySummary`, deduplicates by advisory ID, counts per severity level
4. **Output**: Returns `Json<SeveritySummary>` with `{ critical, high, medium, low, total }` fields

All stages connected. No incomplete paths.

#### Contract & sibling parity

| Check | Result |
|-------|--------|
| **Contract** | `SeveritySummary` is a new standalone struct (no trait to implement). Service method follows `AdvisoryService` patterns. |
| **Sibling parity** | Compared with `get.rs` endpoint: same error handling (`Result<T, AppError>`), same `.context()` wrapping, same path extraction pattern. |
| **Cross-module entity** | Uses `sbom_advisory` join table read-only (SELECT). No write conflicts with other modules. |
| **Caller-site** | New endpoint is a leaf; no callers to verify yet. |

### Step 10 -- Commit and Push

#### Commit

```bash
git add modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "$(cat <<'EOF'
feat(api): add advisory severity aggregation endpoint

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to an SBOM.
Includes SeveritySummary response model, AdvisoryService.severity_summary
method, and integration tests covering valid responses, 404 handling,
empty results, and deduplication.

Implements TC-9201
EOF
)"
```

#### Fork detection

```bash
git remote get-url upstream 2>/dev/null
```

If upstream exists, parse owner/repo from upstream URL and fork-owner from origin URL.

#### Push and create PR

```bash
git push -u origin TC-9201
```

If no fork detected:

```bash
gh pr create --base main --title "feat(api): add advisory severity aggregation endpoint" --body "$(cat <<'EOF'
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning severity counts per advisory level
- Add `SeveritySummary` response model and `AdvisoryService::severity_summary` service method
- Add integration tests for valid responses, 404 handling, empty SBOMs, and deduplication

Implements [TC-9201](<webUrl>)

## Test plan

- [ ] Run `cargo test -p <fundamental-crate-name>` to verify service and model compilation
- [ ] Run `cargo test -p <tests-crate-name>` to verify integration tests pass
- [ ] Manual verification: call `GET /api/v2/sbom/{id}/advisory-summary` with a known SBOM
- [ ] Verify 404 response for non-existent SBOM ID
- [ ] Verify all-zero response for SBOM with no advisories
EOF
)"
```

If fork detected:

```bash
gh pr create -R <upstream-owner/repo> --head <fork-owner>:TC-9201 --base main --title "..." --body "..."
```

If GitHub Issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

### Step 11 -- Update Jira

1. **Update Git Pull Request custom field** (`customfield_10875`) with the PR URL using ADF format:

```
jira.update_issue("TC-9201", fields={
  "customfield_10875": {
    "type": "doc",
    "version": 1,
    "content": [{
      "type": "paragraph",
      "content": [{
        "type": "inlineCard",
        "attrs": {"url": "<PR-URL>"}
      }]
    }]
  }
})
```

2. **Add comment** to TC-9201 (with skill footnote from `shared/comment-footnote.md`):

```
jira.add_comment("TC-9201", "Implementation complete.

PR: <PR-URL>

Changes made:
- Added SeveritySummary response model with critical, high, medium, low, total fields
- Added AdvisoryService::severity_summary method querying sbom_advisory join table
- Added GET /api/v2/sbom/{id}/advisory-summary endpoint
- Added integration tests covering all acceptance criteria

No deviations from the plan.

[footnote from shared/comment-footnote.md with skill name implement-task]")
```

3. **Transition** to In Review:

```
jira.transition_issue("TC-9201") -> "In Review"
```
