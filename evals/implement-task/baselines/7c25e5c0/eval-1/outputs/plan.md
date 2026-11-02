# Implementation Plan — TC-9201

## Step 0 — Validate Project Configuration

Read CLAUDE.md (claude-md-mock.md). Verified:
- **Repository Registry**: present, contains `trustify-backend` with Serena instance `serena_backend` at path `./`
- **Jira Configuration**: present, has Project key (TC), Cloud ID, Feature issue type ID
- **Code Intelligence**: present, lists `serena_backend` instance with `rust-analyzer`

All required sections exist. Proceed.

## Step 1 — Fetch and Parse Jira Task

Fetched TC-9201 via `jira.get_issue("TC-9201")`. Parsed structured description:

- **Repository**: trustify-backend
- **Target Branch**: `main`
- **Description**: Add advisory severity aggregation service method and REST endpoint returning counts per severity level for a given SBOM.
- **Files to Modify**:
  - `modules/fundamental/src/advisory/service/advisory.rs` — add `severity_summary` method
  - `modules/fundamental/src/advisory/endpoints/mod.rs` — register new route
  - `modules/fundamental/src/advisory/model/mod.rs` — add `pub mod severity_summary;`
- **Files to Create**:
  - `modules/fundamental/src/advisory/model/severity_summary.rs` — SeveritySummary response struct
  - `modules/fundamental/src/advisory/endpoints/severity_summary.rs` — GET handler
  - `tests/api/advisory_summary.rs` — integration tests
- **API Changes**: `GET /api/v2/sbom/{id}/advisory-summary` — NEW
- **Target Branch**: `main`
- **Dependencies**: None

Captured `webUrl`: `https://redhat.atlassian.net/browse/TC-9201`

## Step 1.5 — Verify Description Integrity

Would fetch issue comments via `jira.get_issue_comments("TC-9201")` and search for the marker string `[sdlc-workflow] Description digest:` as defined in `shared/description-digest-protocol.md`.

- If **no digest comment found**: log warning — "No description digest found — skipping integrity check. This task may have been created before digest tracking was introduced." Proceed normally (backward compatibility).
- If **digest comment found**: extract the format-tagged digest (e.g., `sha256-md:<hex>`), compute current digest using `python3 scripts/sha256-digest.py /tmp/desc-TC-9201.txt`, compare format tags, then compare hex hashes. On match: proceed silently. On mismatch: alert user with expected vs actual digest and pause.

For this simulation, no digest comment was found — proceeding with a warning.

## Step 2 — Verify Dependencies

No dependencies listed. Proceed.

## Step 3 — Transition to In Progress and Assign

Would call:
1. `jira.user_info()` to get current user's account ID
2. `jira.edit_issue("TC-9201", assignee=<account-id>)` to assign
3. `jira.transition_issue("TC-9201")` → In Progress

## Step 4 — Understand the Code

### Code inspection

Before modifying any files, inspect existing code using the `serena_backend` Serena instance:

1. **`advisory/endpoints/get.rs`** — `mcp__serena_backend__get_symbols_overview` to understand the existing GET handler pattern: path param extraction via `Path<Id>`, service call, JSON response. This is the pattern to follow for the new `severity_summary.rs` endpoint.

2. **`advisory/service/advisory.rs`** — `mcp__serena_backend__find_symbol(name_path_pattern="AdvisoryService")` with `include_body=true` to read the `fetch` and `list` methods. Understand the method signature pattern: `&self, id: Id, tx: &Transactional<'_>` → `Result<T, AppError>`.

3. **`advisory/model/summary.rs`** — `mcp__serena_backend__get_symbols_overview` to inspect the `AdvisorySummary` struct and its `severity` field. This is the field we aggregate over.

4. **`common/src/error.rs`** — `mcp__serena_backend__get_symbols_overview` to confirm the `AppError` enum and `.context()` error wrapping pattern.

5. **`entity/src/sbom_advisory.rs`** — inspect the join table structure for SBOM-to-Advisory linking.

6. **`advisory/endpoints/mod.rs`** — `mcp__serena_backend__get_symbols_overview` to see how routes are registered (the `Router::new().route()` pattern).

### Convention conformance analysis

Analyzed sibling files in the advisory module:

- `advisory/endpoints/get.rs` and `advisory/endpoints/list.rs` — endpoint patterns
- `advisory/model/summary.rs` and `advisory/model/details.rs` — model patterns
- `advisory/service/advisory.rs` — service patterns

See `conventions.md` for the full analysis.

### Documentation file identification

Identified:
- `docs/api.md` — API reference, may need updating for new endpoint
- `README.md` — project overview

### CONVENTIONS.md lookup

Would check for `CONVENTIONS.md` at the repository root (path `./` from Registry). If present, read it and extract CI check commands and code generation commands for Step 9 verification.

## Step 5 — Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch `TC-9201` is created from the Target Branch (`main`).

## Step 6 — Implement Changes

### Files to Modify

**1. `modules/fundamental/src/advisory/service/advisory.rs`**
Add a `severity_summary` method to `AdvisoryService`. See `file-1-description.md` for details.

**2. `modules/fundamental/src/advisory/endpoints/mod.rs`**
Register the new severity summary route. See `file-2-description.md` for details.

**3. `modules/fundamental/src/advisory/model/mod.rs`**
Add `pub mod severity_summary;` to register the new model module. See `file-3-description.md` for details.

### Files to Create

**4. `modules/fundamental/src/advisory/model/severity_summary.rs`**
Define the `SeveritySummary` response struct. See `file-4-description.md` for details.

**5. `modules/fundamental/src/advisory/endpoints/severity_summary.rs`**
Implement the GET handler. See `file-5-description.md` for details.

**6. `tests/api/advisory_summary.rs`**
Integration tests. See `file-6-description.md` for details.

## Step 7 — Write Tests

Tests are described in `file-6-description.md`. Would run:

```bash
cargo test -p trustify-server
```

To resolve the crate name, would first run `cargo metadata --no-deps --format-version 1` from the workspace root to find the package whose targets include the test file, rather than deriving the crate name from the nearest `Cargo.toml` (which may be a virtual workspace manifest).

## Step 8 — Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns the expected JSON shape
- [x] Returns 404 for non-existent SBOM ID (consistent with existing endpoints)
- [x] Counts only unique advisories (deduplication via DISTINCT in query)
- [x] All severity levels default to 0 (struct defaults)
- [x] Performance target met (single query with GROUP BY)

## Step 9 — Self-Verification

### Scope containment
`git diff --name-only` would show only files in Files to Modify and Files to Create. No out-of-scope files.

### Dead parameter detection
No parameters removed — not applicable.

### Sensitive-pattern check
`git diff --cached | grep -iE '(password|API_KEY|SECRET_KEY|BEGIN.*PRIVATE KEY|\.env)'` — no matches expected.

### CI checks from CONVENTIONS.md
Would run all CI check commands extracted from CONVENTIONS.md (formatting, linting, type checking, compilation).

### Module-level test requirement (Rust)
Would run `cargo metadata --no-deps --format-version 1` to resolve the crate name for `modules/fundamental/`, then run `cargo test -p <crate-name>`. Would NOT derive the crate name from the nearest `Cargo.toml`, which may be a virtual workspace manifest.

## Step 10 — Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low) for advisories linked
to a given SBOM. Includes deduplication by advisory ID and integration
tests.

Implements TC-9201
```

```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
       modules/fundamental/src/advisory/endpoints/mod.rs \
       modules/fundamental/src/advisory/model/mod.rs \
       modules/fundamental/src/advisory/model/severity_summary.rs \
       modules/fundamental/src/advisory/endpoints/severity_summary.rs \
       tests/api/advisory_summary.rs

git commit --trailer="Assisted-by: Claude Code" -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low) for advisories linked
to a given SBOM. Includes deduplication by advisory ID and integration
tests.

Implements TC-9201"
```

### Push and PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

The PR description includes `Implements [TC-9201](https://redhat.atlassian.net/browse/TC-9201)`.

## Step 11 — Update Jira

1. Update custom field `customfield_10875` with PR URL (ADF format with inlineCard)
2. Add comment with PR link, summary of changes, and any deviations
3. Transition TC-9201 → In Review
