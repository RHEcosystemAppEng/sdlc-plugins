# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Target PR**: (none -- default flow, create new branch and PR)
**Bookend Type**: (none -- normal implementation task)
**Dependencies**: None

## Step 0 -- Validate Project Configuration

Verify CLAUDE.md contains the required Project Configuration sections:

1. **Repository Registry** -- present, contains `trustify-backend` with Serena instance `serena_backend` and path `./`
2. **Jira Configuration** -- present, contains Project key `TC`, Cloud ID, Feature issue type ID `10142`, Git Pull Request custom field `customfield_10875`, GitHub Issue custom field `customfield_10747`
3. **Code Intelligence** -- present, tool naming convention: `mcp__<serena-instance>__<tool>`, configured instance: `serena_backend` with rust-analyzer

All sections present. Proceed.

## Step 0.5 -- JIRA Access Initialization

Attempt MCP first for all Jira operations. If MCP fails, prompt user with REST API fallback options. (Skipped in this eval -- no external service calls.)

## Step 1 -- Fetch and Parse Jira Task

Parsed sections from TC-9201 description:

- **Repository**: trustify-backend
- **Target Branch**: main
- **Description**: Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and a total.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
  - `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
  - `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module
  - `server/src/main.rs` -- no changes needed (routes auto-mount via module registration)
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
  - `tests/api/advisory_summary.rs` -- integration tests for the new endpoint
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` -- NEW: returns `{ critical: N, high: N, medium: N, low: N, total: N }`
- **Acceptance Criteria**: 5 items (see task description)
- **Test Requirements**: 4 items (see task description)
- **Target PR**: (none)
- **Bookend Type**: (none)
- **Dependencies**: None
- **GitHub Issue custom field**: `customfield_10747` -- would extract GitHub issue URL from this field if present for use in PR description `Closes` line

Also capture the issue's `webUrl` field (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description's clickable "Implements" link.

## Step 1.5 -- Verify Description Integrity

1. Retrieve issue comments via `jira.get_issue_comments(TC-9201)`.
2. Search for comments whose body starts with `[sdlc-workflow] Description digest:`.
3. **If no digest comment found**: log warning and proceed normally (backward compatibility -- tasks created before digest tracking was introduced have no digest comment):
   > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."
4. **If digest comment found**: extract the tagged digest, compute current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags and hex digests. On mismatch, alert user and stop for confirmation.

## Step 2 -- Verify Dependencies

No dependencies listed. Proceed.

## Step 3 -- Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`.
2. Assign TC-9201 to current user via `jira.edit_issue(TC-9201, assignee=<accountId>)`.
3. Transition TC-9201 to In Progress via `jira.transition_issue`.

## Step 4 -- Understand the Code

### Code inspection plan

Use the Serena instance `serena_backend` (tools called as `mcp__serena_backend__<tool>`) to inspect the codebase.

1. **Overview of files to modify**:
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand AdvisoryService struct and existing methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/mod.rs` -- see route registration pattern
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/mod.rs` -- see existing model module registrations

2. **Read specific symbols**:
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- understand the service method pattern (parameters, return type, error handling)
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` -- second reference for the service method pattern
   - `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` -- understand the struct that has the `severity` field we will count by

3. **Check backward compatibility**:
   - `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- ensure adding a new method does not break existing callers

4. **Non-symbolic search**:
   - `mcp__serena_backend__search_for_pattern` for `sbom_advisory` -- confirm the join table entity exists and understand its schema
   - `mcp__serena_backend__search_for_pattern` for `AppError` and `.context()` -- confirm error handling pattern

5. **Convention conformance analysis** (sibling files):
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/get.rs` -- sibling endpoint handler
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/endpoints/list.rs` -- sibling endpoint handler
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/summary.rs` -- sibling model struct (AdvisorySummary)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/model/details.rs` -- sibling model struct (AdvisoryDetails)
   - `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/sbom/endpoints/get.rs` -- sibling module endpoint for cross-reference (SBOM endpoint patterns)
   - Read `tests/api/advisory.rs` and `tests/api/sbom.rs` -- sibling test files for test convention analysis

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at the repository root (`./CONVENTIONS.md`). Per the repo structure, it exists. Read it and extract:
- Naming rules, directory structure for new files, code patterns, test conventions
- **Verification commands**: search for "CI checks", "Linting", "Verification" sections and extract all listed commands
- **Code generation commands**: search for commands that generate code artifacts (e.g., OpenAPI spec generation)

Record extracted commands for use in Step 9's CI verification sub-step.

### Documentation file identification

Identify documentation files related to the changes:
- `README.md` at repository root
- `docs/api.md` -- REST API reference (may need updating for new endpoint)
- `docs/architecture.md` -- system architecture overview
- `CONVENTIONS.md` -- coding conventions

## Step 5 -- Create Branch

Default flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch name `TC-9201` derived from the Jira issue ID, based off target branch `main`.

## Step 6 -- Implement Changes

### Files to modify (3 actual modifications)

1. **`modules/fundamental/src/advisory/model/mod.rs`** -- Add `pub mod severity_summary;` line to register the new model module. Follow the pattern of existing `pub mod summary;` and `pub mod details;` declarations.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- Add a `severity_summary` method to AdvisoryService. Method signature: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`. Follow the pattern of existing `fetch` and `list` methods. The method will:
   - Query the `sbom_advisory` join table for advisories linked to the given SBOM
   - Join with advisory data to get severity levels
   - Deduplicate by advisory ID
   - Count by severity level (Critical, High, Medium, Low)
   - Return a SeveritySummary struct with counts and total
   - Use `.context()` error wrapping matching existing error handling pattern

3. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- Register the new route. Add `mod severity_summary;` and add a `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::get_advisory_summary))` following the pattern of existing route registrations.

4. **`server/src/main.rs`** -- No changes needed (routes auto-mount via module registration). Listed in task but explicitly marked as no changes.

### Files to create (3)

5. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- Define the `SeveritySummary` response struct with fields: `critical: u64`, `high: u64`, `medium: u64`, `low: u64`, `total: u64`. Derive `Serialize`, `Deserialize`, `Debug`, `Clone`, `Default` (matching sibling model patterns). Add `utoipa::ToSchema` if siblings use it for OpenAPI generation. Include doc comments on the struct and each field.

6. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- Define the GET handler function `get_advisory_summary`. Extract path params via `Path<Id>` (matching pattern from `get.rs`). Call `AdvisoryService::severity_summary`, return `Json<SeveritySummary>`. Handle errors with `Result<T, AppError>` and `.context()`. Include doc comments.

7. **`tests/api/advisory_summary.rs`** -- Integration tests covering all 4 test requirements. Each test function gets a doc comment. Non-trivial tests use given-when-then section comments.

### Reuse and deduplication checks

Before implementing:
- **Symbol deduplication**: Search for existing `SeveritySummary` or `severity_summary` symbols in the codebase using `find_symbol` and `search_for_pattern` to avoid redeclaring something that already exists.
- **Reuse check**: The `AdvisorySummary` struct in `model/summary.rs` has a `severity` field -- reuse this for counting rather than re-fetching raw data. Check if any severity counting or aggregation logic already exists elsewhere.
- **Dependency check**: The `entity` crate (`sbom_advisory.rs`) is already a dependency of `modules/fundamental` -- no new cross-package dependency needed.

## Step 7 -- Write Tests

Create `tests/api/advisory_summary.rs` with 4 test functions matching the Test Requirements:

1. `test_valid_sbom_returns_correct_severity_counts` -- Verifies correct counts for a known SBOM with advisories
2. `test_nonexistent_sbom_returns_404` -- Verifies 404 for a non-existent SBOM ID
3. `test_sbom_with_no_advisories_returns_all_zeros` -- Verifies all-zero response
4. `test_duplicate_advisory_links_are_deduplicated` -- Verifies deduplication in count

Each test:
- Has a `///` doc comment explaining what it verifies
- Uses given-when-then section comments (`// Given`, `// When`, `// Then`)
- Uses value-based assertions (`assert_eq!` on specific field values, not just `.len()`)
- Follows sibling test patterns from `tests/api/advisory.rs` and `tests/api/sbom.rs`

Run tests after writing:
```bash
cargo test -p <crate-name>
```

To resolve the correct crate name, run:
```bash
cargo metadata --no-deps --format-version 1
```
from the workspace root and find the package whose manifest or target source contains the modified files. Use that package's `name` field as `<crate-name>`. Do not derive it from the nearest `Cargo.toml`, which may be a virtual workspace manifest.

## Step 8 -- Verify Acceptance Criteria

Verify each criterion:
- [x] GET /api/v2/sbom/{id}/advisory-summary returns correct JSON shape
- [x] Returns 404 for non-existent SBOM ID
- [x] Counts only unique advisories (deduplicated by advisory ID)
- [x] All severity levels default to 0 when no advisories at that level
- [x] Response time under 200ms (verified by query efficiency -- uses indexed join table, single query with GROUP BY)

## Step 9 -- Self-Verification

### Scope containment
Run `git diff --name-only` and compare against Files to Modify and Files to Create. Verify no out-of-scope files were modified.

### Untracked file check
Run `git status --short`, filter `??` entries, check for references in staged diff.

### Dead parameter detection
Scan modified functions for parameters no longer referenced after changes.

### Sensitive-pattern check
Run `git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` -- should find no matches.

### Documentation currency
Check if `docs/api.md` needs updating for the new endpoint. If it documents all REST endpoints, add the new `GET /api/v2/sbom/{id}/advisory-summary` entry.

### CI checks from CONVENTIONS.md
Run all CI check commands extracted from CONVENTIONS.md. Hard stop on any non-zero exit.

### Module-level test requirement (Rust)
Run `cargo metadata --no-deps --format-version 1` from the workspace root. Resolve the package name for each modified file. Run `cargo test -p <crate-name>` for every crate containing modified files. Hard stop on failure.

### Data-flow trace
Trace the complete lifecycle:
- **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
- **Processing**: Endpoint handler extracts `Path<Id>`, calls `AdvisoryService::severity_summary(sbom_id, tx)`, which queries `sbom_advisory` join table, joins advisory data, deduplicates by advisory ID, groups by severity, counts
- **Output**: JSON response `{ critical: N, high: N, medium: N, low: N, total: N }` via `Json<SeveritySummary>`
- All stages connected -- data flow is complete.

### Contract and sibling parity
- **Contract**: `severity_summary` method follows the same `Result<T, AppError>` return pattern as other AdvisoryService methods
- **Sibling parity**: Handler follows same error handling, JSON response, path extraction pattern as `get.rs`
- **Cross-module entity**: Uses `sbom_advisory` join table read-only -- no write conflicts with ingestor module
- **Caller-site**: New endpoint, no existing callers to verify

## Step 10 -- Commit and Push

### Commit message

```
feat(advisory): add severity aggregation service and endpoint

Add SeveritySummary model, AdvisoryService::severity_summary method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes integration tests for valid SBOM, non-existent
SBOM (404), empty advisories, and deduplication.

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

git commit --trailer='Assisted-by: Claude Code' -m "$(cat <<'EOF'
feat(advisory): add severity aggregation service and endpoint

Add SeveritySummary model, AdvisoryService::severity_summary method,
and GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes integration tests for valid SBOM, non-existent
SBOM (404), empty advisories, and deduplication.

Implements TC-9201
EOF
)"
```

### Fork detection

Before creating a PR, detect whether the working directory is a fork:
```bash
git remote get-url upstream 2>/dev/null
```
If upstream exists, parse owner/repo and use `-R` flag with `gh pr create`.

### Push and PR creation

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation service and endpoint" --body "$(cat <<'EOF'
## Summary

- Add `SeveritySummary` response model for advisory severity counts
- Add `AdvisoryService::severity_summary` method querying advisory severities by SBOM ID
- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning `{ critical, high, medium, low, total }`
- Add integration tests for valid SBOM, 404, empty advisories, and deduplication

## Test plan

- [ ] `cargo test -p <crate-name>` passes for all modified crates
- [ ] Manual test: `GET /api/v2/sbom/{id}/advisory-summary` returns correct counts
- [ ] Manual test: Non-existent SBOM ID returns 404
- [ ] CI checks from CONVENTIONS.md pass

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)
EOF
)"
```

If a GitHub issue reference was extracted from `customfield_10747`, append a `Closes <owner>/<repo>#<number>` line to the PR description body.

## Step 11 -- Update Jira

1. Update `customfield_10875` (Git Pull Request custom field) with the PR URL in ADF format.
2. Add a comment to TC-9201 with PR link, summary of changes, and any deviations.
3. Transition TC-9201 to In Review.
