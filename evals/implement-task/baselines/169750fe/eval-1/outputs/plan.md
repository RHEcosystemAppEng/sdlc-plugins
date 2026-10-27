# Implementation Plan: TC-9201

## Task Summary

**Issue:** TC-9201 — Add advisory severity aggregation service and endpoint
**Repository:** trustify-backend
**Target Branch:** main
**Branch Name:** TC-9201

## Step 0 — Validate Project Configuration

Verified CLAUDE.md contains all required sections:
- Repository Registry: present, lists trustify-backend with Serena instance `serena_backend`
- Jira Configuration: present, project key TC, Cloud ID, Feature issue type ID, Git Pull Request custom field, GitHub Issue custom field
- Code Intelligence: present, with `serena_backend` instance using rust-analyzer

## Step 1 — Fetch and Parse Jira Task

Parsed structured description for TC-9201:
- **Repository:** trustify-backend
- **Target Branch:** main
- **Description:** Add service method and REST endpoint for advisory severity aggregation per SBOM
- **Dependencies:** None

### Target Branch extraction

Extracted Target Branch: **main**. This is the branch the PR will target (via `--base main`).

## Step 1.5 — Verify Description Integrity

Retrieve issue comments via `jira.get_issue_comments(TC-9201)`. Search for comments whose body starts with `[sdlc-workflow] Description digest:`.

**No digest comment found.** Log warning and proceed normally (backward compatibility — tasks created before digest tracking was introduced have no digest comment):

> "No description digest found — skipping integrity check. This task may have been created before digest tracking was introduced."

## Step 2 — Verify Dependencies

No dependencies listed. Proceeding.

## Step 3 — Transition to In Progress and Assign

1. Retrieve current user's Jira account ID via `jira.user_info()`
2. Assign task: `jira.edit_issue(TC-9201, assignee=<account-id>)`
3. Transition: `jira.transition_issue(TC-9201) → In Progress`

## Step 4 — Understand the Code

### Code inspection (before any modifications)

Using `serena_backend` Serena instance to inspect existing code:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — inspect via `mcp__serena_backend__get_symbols_overview` to understand the existing endpoint pattern: `Path<Id>` extraction, service call, JSON response. Read specific handler function with `mcp__serena_backend__find_symbol` to see the full pattern.

2. **`modules/fundamental/src/advisory/service/advisory.rs`** — inspect via `mcp__serena_backend__get_symbols_overview` to see existing `AdvisoryService` methods (`fetch`, `list`, `search`). Read `fetch` method body with `find_symbol(include_body=true)` to understand signature pattern: `&self, sbom_id: Id, tx: &Transactional<'_>` → `Result<T, AppError>`.

3. **`modules/fundamental/src/advisory/model/summary.rs`** — inspect `AdvisorySummary` struct to see the `severity` field type and derive macros used.

4. **`common/src/error.rs`** — inspect `AppError` enum and `.context()` error wrapping pattern.

5. **`entity/src/sbom_advisory.rs`** — inspect the SBOM-Advisory join table entity to understand the relationship schema.

6. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — inspect current route registration pattern (`Router::new().route(...)` chains).

7. **`modules/fundamental/src/advisory/model/mod.rs`** — inspect existing module declarations (`pub mod summary; pub mod details;`).

### Convention conformance analysis

Analyzed sibling files for patterns (see outputs/conventions.md for full details).

### CONVENTIONS.md lookup

Check for `CONVENTIONS.md` at repository root — found at `trustify-backend/CONVENTIONS.md`. Read for CI check commands and code generation commands.

### Documentation file identification

Identified documentation files:
- `docs/api.md` — REST API reference (may need updating for new endpoint)
- `README.md` — project overview

## Step 5 — Create Branch

```bash
git checkout main
git pull
git checkout -b TC-9201
```

Branch named `TC-9201` based on Target Branch `main`.

## Step 6 — Implement Changes

### Files to Modify

1. **`modules/fundamental/src/advisory/service/advisory.rs`** — Add `severity_summary` method to `AdvisoryService`
2. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Register the new `/api/v2/sbom/{id}/advisory-summary` route
3. **`modules/fundamental/src/advisory/model/mod.rs`** — Add `pub mod severity_summary;` module declaration

### Files to Create

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** — `SeveritySummary` response struct
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** — GET handler for the new endpoint
3. **`tests/api/advisory_summary.rs`** — Integration tests

See `file-1-description.md` through `file-6-description.md` for detailed changes per file.

## Step 7 — Write Tests

Tests described in `file-6-description.md` (advisory_summary.rs). Following test conventions from sibling `tests/api/advisory.rs`:
- Integration tests hitting real PostgreSQL test database
- `assert_eq!(resp.status(), StatusCode::OK)` pattern for status checks
- Value-based assertions on response body (specific counts, not just existence checks)
- Each test function has a `///` doc comment

## Step 8 — Verify Acceptance Criteria

- [x] GET /api/v2/sbom/{id}/advisory-summary returns `{ critical, high, medium, low, total }` — implemented in endpoint handler
- [x] Returns 404 when SBOM ID does not exist — service returns `AppError::NotFound` with `.context()`
- [x] Counts only unique advisories — uses DISTINCT in query via `sbom_advisory` join
- [x] All severity levels default to 0 — `SeveritySummary::default()` initializes all to 0
- [x] Response time under 200ms for 500 advisories — single aggregation query, no N+1

## Step 9 — Self-Verification

### Scope containment
All modified/created files are within the Files to Modify and Files to Create sections:
- Modified: `advisory/service/advisory.rs`, `advisory/endpoints/mod.rs`, `advisory/model/mod.rs`
- Created: `advisory/model/severity_summary.rs`, `advisory/endpoints/severity_summary.rs`, `tests/api/advisory_summary.rs`

No out-of-scope files modified.

### Module-level test requirement (Rust)

Resolve the crate name using `cargo metadata --no-deps --format-version 1` from the workspace root. The modified files are in `modules/fundamental/`, so we look up the package whose manifest or target source contains these files. The resolved crate name is used for test execution:

```bash
cargo test -p <resolved-crate-name>
```

Do not derive the crate name from the nearest `Cargo.toml`, which may be a virtual workspace manifest.

### Dead parameter detection
No parameters removed — no dead parameter cleanup needed.

### Sensitive-pattern check
No secrets or credentials in staged changes.

### Duplication check
Searched for existing severity aggregation logic — none found. New code is unique.

### Query-scope verification
Query targets advisories linked to a specific SBOM ID via `sbom_advisory` join — correctly scoped, not loading all advisories.

## Step 10 — Commit and Push

### Commit message

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Includes SeveritySummary model, AdvisoryService method, endpoint
handler, and integration tests.

Implements TC-9201
```

### Commit command

```bash
git add modules/fundamental/src/advisory/service/advisory.rs \
      modules/fundamental/src/advisory/endpoints/mod.rs \
      modules/fundamental/src/advisory/model/mod.rs \
      modules/fundamental/src/advisory/model/severity_summary.rs \
      modules/fundamental/src/advisory/endpoints/severity_summary.rs \
      tests/api/advisory_summary.rs

git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary that returns severity counts
(critical, high, medium, low, total) for advisories linked to a given
SBOM. Includes SeveritySummary model, AdvisoryService method, endpoint
handler, and integration tests.

Implements TC-9201"
```

### Push and PR

```bash
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

PR targets `--base main` as extracted from the Target Branch section.

## Step 11 — Update Jira

1. Set Git Pull Request custom field (`customfield_10875`) with PR URL in ADF format
2. Add comment summarizing changes and PR link
3. Transition TC-9201 → In Review
