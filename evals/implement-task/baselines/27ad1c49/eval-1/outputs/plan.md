# Implementation Plan: TC-9201

## Task Summary

**Jira Key**: TC-9201
**Summary**: Add advisory severity aggregation service and endpoint
**Repository**: trustify-backend
**Target Branch**: main
**Status**: To Do
**Parent Feature**: TC-9001 (is incorporated by)
**Dependencies**: None

---

## Step 0 -- Validate Project Configuration

Verified that the project's CLAUDE.md contains all required sections under `# Project Configuration`:

1. **Repository Registry** -- present, contains entry for `trustify-backend` with Role "Rust backend service", Serena Instance `serena_backend`, Path `./`.
2. **Jira Configuration** -- present, contains Project key (`TC`), Cloud ID (`2b9e35e3-6bd3-4cec-b838-f4249ee02432`), Feature issue type ID (`10142`).
3. **Code Intelligence** -- present, tool naming convention documented (`mcp__<serena-instance>__<tool>`), configured instance `serena_backend` with `rust-analyzer`.

All validations pass. Proceeding.

---

## Step 1 -- Fetch and Parse Jira Task

### Parsed Sections

| Section | Value |
|---|---|
| Repository | trustify-backend |
| Target Branch | main |
| Description | Add a service method and REST endpoint that aggregates vulnerability advisory severity counts for a given SBOM. Returns summary with counts per severity level (Critical, High, Medium, Low) and a total. |
| Files to Modify | 3 files (see below) |
| Files to Create | 3 files (see below) |
| API Changes | `GET /api/v2/sbom/{id}/advisory-summary` -- NEW |
| Implementation Notes | Follow existing endpoint pattern in `get.rs`, add `severity_summary` method following `fetch`/`list` pattern, use `sbom_advisory` join table, use `AdvisorySummary.severity` field, error handling via `AppError` with `.context()` |
| Acceptance Criteria | 5 criteria (severity counts, 404 for missing SBOM, deduplication, zero defaults, performance) |
| Test Requirements | 4 tests (correct counts, 404, zero counts, deduplication) |
| Target PR | Not present (standard flow) |
| Bookend Type | Not present (standard flow) |
| Dependencies | None |

### Files to Modify

1. `modules/fundamental/src/advisory/service/advisory.rs` -- add `severity_summary` method to AdvisoryService
2. `modules/fundamental/src/advisory/endpoints/mod.rs` -- register the new route
3. `modules/fundamental/src/advisory/model/mod.rs` -- add `pub mod severity_summary;` to register the new model module

### Files to Create

1. `modules/fundamental/src/advisory/model/severity_summary.rs` -- SeveritySummary response struct
2. `modules/fundamental/src/advisory/endpoints/severity_summary.rs` -- GET handler for `/api/v2/sbom/{id}/advisory-summary`
3. `tests/api/advisory_summary.rs` -- integration tests for the new endpoint

### Target Branch Extraction

Target Branch: `main`. This will be used as the `--base` argument for `gh pr create` and as the branch to check out from in Step 5.

### GitHub Issue Extraction

GitHub Issue custom field is configured as `customfield_10747` in CLAUDE.md Jira Configuration. Would check the fetched issue's fields for this custom field value. If present, parse the GitHub issue URL and store as `<owner>/<repo>#<number>` for the PR description's `Closes` line.

### webUrl Capture

Would capture the issue's `webUrl` field (e.g., `https://redhat.atlassian.net/browse/TC-9201`) for use in the PR description's `Implements` link.

---

## Step 1.5 -- Verify Description Integrity

1. **Retrieve issue comments**: call `jira.get_issue_comments(TC-9201)` to fetch all comments.
2. **Locate digest comment**: search for comments whose body starts with `[sdlc-workflow] Description digest:`. Select the most recent one by `created` timestamp if multiple exist.
3. **If no digest comment found**: log the following warning and proceed normally (backward compatibility):

   > "No description digest found -- skipping integrity check. This task may have been created before digest tracking was introduced."

4. **If digest comment found**: would perform the following checks:
   - Check if `updated` timestamp is later than `created` -- warn if comment was edited
   - Extract tagged digest (e.g., `sha256-md:a1b2...` or `sha256-adf:a1b2...`)
   - If legacy untagged format (`sha256:<hex>`), log warning and skip
   - Compute current digest: write description to `/tmp/desc-TC-9201.txt`, run `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`
   - Compare format tags -- if mismatch, log warning and skip
   - Compare hex digests -- if match, proceed silently; if mismatch, alert user with expected vs actual and ask whether to proceed or stop

---

## Step 2 -- Verify Dependencies

Task has no dependencies (`Dependencies: None`). Proceeding.

---

## Step 3 -- Transition to In Progress and Assign

1. Call `jira.user_info()` to get current user's account ID.
2. Call `jira.edit_issue(TC-9201, assignee=<current-user-account-id>)` to assign.
3. Call `jira.transition_issue(TC-9201)` to transition to **In Progress**.

---

## Step 4 -- Understand the Code

### 4.1 Code Inspection via Serena

Using `mcp__serena_backend__<tool>` (the configured Serena instance for trustify-backend):

**Files to Modify -- symbols overview:**

1. `modules/fundamental/src/advisory/service/advisory.rs`:
   - `mcp__serena_backend__get_symbols_overview` to see `AdvisoryService` struct and its methods (`fetch`, `list`, `search`)
   - `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` to understand the method signature pattern (takes `&self, id: Id, tx: &Transactional<'_>`) and return type (`Result<..., AppError>`)
   - `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` to see list method pattern

2. `modules/fundamental/src/advisory/endpoints/mod.rs`:
   - `mcp__serena_backend__get_symbols_overview` to see route registration pattern (`Router::new().route(...)`)

3. `modules/fundamental/src/advisory/model/mod.rs`:
   - `mcp__serena_backend__get_symbols_overview` to see existing `pub mod` declarations (`summary`, `details`)

**Files to Create locations -- sibling inspection:**

1. `modules/fundamental/src/advisory/model/summary.rs`:
   - `mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)` to understand the struct pattern (derives, fields including `severity`)

2. `modules/fundamental/src/advisory/endpoints/get.rs`:
   - `mcp__serena_backend__get_symbols_overview` to see handler function pattern
   - `mcp__serena_backend__find_symbol` on the handler to see `Path<Id>` extraction, service call, JSON response pattern

3. `modules/fundamental/src/advisory/endpoints/list.rs`:
   - `mcp__serena_backend__get_symbols_overview` for route handler pattern comparison

**Reference files:**

- `entity/src/sbom_advisory.rs`: `mcp__serena_backend__get_symbols_overview` to understand the join table entity structure
- `common/src/error.rs`: `mcp__serena_backend__find_symbol("AppError", include_body=true)` to see the error enum and `.context()` pattern
- `common/src/model/paginated.rs`: `mcp__serena_backend__get_symbols_overview` to understand `PaginatedResults<T>`

**Backward compatibility check:**

- `mcp__serena_backend__find_referencing_symbols` on any symbols being modified (e.g., if adding an import to `model/mod.rs`, check that adding a new module doesn't break existing re-exports)

### 4.2 CONVENTIONS.md Lookup

The Repository Registry shows trustify-backend has Path `./`. Check for `CONVENTIONS.md` at the repository root. The repo structure confirms `CONVENTIONS.md` exists at `trustify-backend/CONVENTIONS.md`.

Would read it and extract:
- Naming rules, directory structure, code patterns, test conventions
- CI check commands (from headings like "CI checks", "Verification", "Linting")
- Code generation commands (e.g., OpenAPI spec generation)

Record extracted verification commands for use in Step 9.

### 4.3 Convention Conformance Analysis

See `outputs/conventions.md` for the full conventions discovered from sibling analysis.

### 4.4 Documentation File Identification

Identified documentation files related to the changes:
- `docs/api.md` -- REST API reference (may need update for new endpoint)
- `docs/architecture.md` -- System architecture overview (no update expected)
- `README.md` -- Repository readme (unlikely to need update)
- `CONVENTIONS.md` -- Conventions reference (no update needed)

---

## Step 5 -- Create Branch

Standard flow (no Target PR, no Bookend Type):

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch name: `TC-9201` (named after the Jira issue ID).
Based on: `main` (the Target Branch from the task description).

---

## Step 6 -- Implementation Changes

All changes are strictly scoped to the Files to Modify and Files to Create sections.

### Files to Modify

1. **`modules/fundamental/src/advisory/model/mod.rs`** -- add `pub mod severity_summary;` declaration (see `outputs/file-1-description.md`)
2. **`modules/fundamental/src/advisory/service/advisory.rs`** -- add `severity_summary` method to `AdvisoryService` (see `outputs/file-2-description.md`)
3. **`modules/fundamental/src/advisory/endpoints/mod.rs`** -- register the new route (see `outputs/file-3-description.md`)

### Files to Create

4. **`modules/fundamental/src/advisory/model/severity_summary.rs`** -- `SeveritySummary` response struct (see `outputs/file-4-description.md`)
5. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** -- GET handler (see `outputs/file-5-description.md`)
6. **`tests/api/advisory_summary.rs`** -- integration tests (see `outputs/file-6-description.md`)

### Documentation Impact

- The new endpoint `GET /api/v2/sbom/{id}/advisory-summary` should be documented in `docs/api.md` if it contains a REST API reference section. Would check whether `docs/api.md` lists existing endpoints and, if so, add an entry for the new one.
- No Documentation Updates section in the task, so evaluate based on identified documentation files from Step 4.

---

## Step 7 -- Tests

Tests are detailed in `outputs/file-6-description.md`. They follow the patterns discovered in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).

Key test conventions applied:
- Each test function has a `///` doc comment explaining what it verifies
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments
- Value-based assertions (assert on specific field values, not just collection lengths)
- Assertion pattern: `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(body.critical, expected_value)`

After writing tests, run:

```bash
cargo test -p trustify-fundamental
```

(Package name resolved via `cargo metadata --no-deps --format-version 1`, not derived from the nearest `Cargo.toml`.)

Fix any failures before proceeding.

---

## Step 8 -- Verify Acceptance Criteria

| Criterion | Verification |
|---|---|
| GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` | Handler returns `Json<SeveritySummary>` with all five fields |
| Returns 404 when SBOM ID does not exist | Service method checks SBOM existence first, returns `AppError::NotFound` with `.context()` |
| Counts only unique advisories (deduplicates by advisory ID) | Query uses `DISTINCT` on advisory ID or collects into a `HashSet` before counting |
| All severity levels default to 0 when no advisories exist | `SeveritySummary` fields have `#[serde(default)]` or are initialized to 0 |
| Response time under 200ms for SBOMs with up to 500 advisories | Single SQL query with JOIN and GROUP BY; no N+1 queries |

---

## Step 9 -- Self-Verification

### Scope Containment

Run `git diff --name-only` and compare against:

**Expected modified files:**
- `modules/fundamental/src/advisory/service/advisory.rs`
- `modules/fundamental/src/advisory/endpoints/mod.rs`
- `modules/fundamental/src/advisory/model/mod.rs`

**Expected created files:**
- `modules/fundamental/src/advisory/model/severity_summary.rs`
- `modules/fundamental/src/advisory/endpoints/severity_summary.rs`
- `tests/api/advisory_summary.rs`

If `tests/Cargo.toml` or `tests/api/mod.rs` also appear (for test module registration), flag as out-of-scope and ask user for approval.

If `docs/api.md` was updated for documentation impact, flag as out-of-scope and ask user for approval.

### Untracked File Check

Run `git status --short`, filter `??` entries in directories containing modified files. Check staged diff for references to any untracked filenames. Flag and request approval -- do not auto-stage.

### Dead Parameter Detection

Scan modified functions for parameters no longer referenced in the function body. Since we are adding new methods (not removing code from existing ones), this check is unlikely to flag anything, but verify after implementation.

### Sensitive-Pattern Check

```bash
git diff --cached | grep -iE '(password\s*=|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'
```

Flag any matches.

### Documentation Currency

Verify `docs/api.md` still accurately describes the API if we added a new endpoint. Update if needed.

### Duplication Check

Search for existing severity aggregation logic:
- Grep for `severity_summary`, `severity_count`, `SeveritySummary` across the codebase
- Check `AdvisorySummary` struct for any existing aggregation methods
- Verify no existing endpoint already serves this data

### Module-Level Test Requirement (Rust)

Resolve crate names using `cargo metadata --no-deps --format-version 1`:

1. For files in `modules/fundamental/src/...` -- resolve the package name (likely `trustify-fundamental` or similar). Run:
   ```bash
   cargo test -p <resolved-crate-name>
   ```

2. For files in `tests/api/...` -- resolve the test crate package name. Run:
   ```bash
   cargo test -p <resolved-test-crate-name>
   ```

Hard stop if any test fails.

### CI Checks from CONVENTIONS.md

Run every CI check command extracted from `CONVENTIONS.md` in Step 4. Hard stop on any non-zero exit.

### Data-Flow Trace

Trace the complete data flow for the new feature:

1. **Input**: HTTP GET request to `/api/v2/sbom/{id}/advisory-summary` with SBOM ID path parameter
2. **Processing (endpoint)**: `severity_summary` handler extracts `Path<Id>`, passes to `AdvisoryService::severity_summary()`
3. **Processing (service)**: Queries `sbom_advisory` join table for the given SBOM ID, joins with advisory table, groups by severity, counts distinct advisories
4. **Processing (model)**: Populates `SeveritySummary` struct with counts per severity level
5. **Output**: Returns `Json<SeveritySummary>` as HTTP 200 response with `{ critical, high, medium, low, total }`
6. **Error path**: If SBOM not found, returns 404 via `AppError::NotFound` with `.context()`

All stages connected. Flow is complete.

### Contract & Sibling Parity

1. **Contract**: `SeveritySummary` implements `Serialize` (required for `Json<T>`). Handler returns `Result<Json<SeveritySummary>, AppError>` matching Axum's expected pattern.
2. **Sibling parity**: Compare against `get.rs` handler -- same error handling pattern (`AppError` with `.context()`), same path param extraction (`Path<Id>`), same response wrapping (`Json<T>`).
3. **Cross-module entity**: `sbom_advisory` join table is read-only in this feature (no writes), so no transaction/conflict concerns.
4. **Caller-site**: New code follows the same `AdvisoryService` method call pattern as existing callers.

---

## Step 10 -- Commit and Push

### Commit Message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes SeveritySummary model, AdvisoryService method,
and integration tests.

Implements TC-9201
```

Command:

```bash
git add modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "$(cat <<'EOF'
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
advisory severity counts (critical, high, medium, low, total) for a
given SBOM. Includes SeveritySummary model, AdvisoryService method,
and integration tests.

Implements TC-9201
EOF
)"
```

### Fork Detection

```bash
git remote get-url upstream 2>/dev/null
```

- If succeeds: parse upstream owner/repo and fork owner for `gh pr create -R` flags.
- If fails: use default `gh pr create` behavior.

### Push and PR Creation

```bash
git push -u origin TC-9201
```

PR creation (no fork detected):

```bash
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint for SBOM advisories" --body "$(cat <<'EOF'
## Summary

- Add `GET /api/v2/sbom/{id}/advisory-summary` endpoint returning advisory severity counts (critical, high, medium, low, total) for a given SBOM
- Add `SeveritySummary` response model and `AdvisoryService::severity_summary()` service method
- Add integration tests for the new endpoint (valid SBOM, missing SBOM 404, empty advisories, deduplication)

Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)

## Test Plan

- [ ] `cargo test -p <fundamental-crate>` passes all new and existing tests
- [ ] Manual test: `GET /api/v2/sbom/{id}/advisory-summary` returns correct severity counts
- [ ] Manual test: Non-existent SBOM ID returns 404
- [ ] CI checks pass (formatting, linting, compilation)
EOF
)"
```

If a GitHub issue reference was extracted in Step 1, append `Closes <owner>/<repo>#<number>` to the PR body.

---

## Step 11 -- Update Jira

1. **Git Pull Request custom field**: configured as `customfield_10875`. Update with PR URL in ADF format:

   ```
   jira.update_issue(TC-9201, fields={"customfield_10875": {"type": "doc", "version": 1, "content": [{"type": "paragraph", "content": [{"type": "inlineCard", "attrs": {"url": "<PR-URL>"}}]}]}})
   ```

2. **Add comment** to TC-9201 with:
   - PR link
   - Summary: Added severity aggregation endpoint, model, service method, and integration tests
   - Deviations: None (standard implementation)

3. **Transition** TC-9201 to **In Review**.
