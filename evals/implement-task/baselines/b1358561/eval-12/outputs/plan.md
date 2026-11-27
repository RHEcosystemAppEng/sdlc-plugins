# Implementation Plan — TC-9210: Add severity-sorted remediation list to SBOM risk report

This is a simulated run of `/sdlc-workflow:implement-task TC-9210`. No repository files, Jira, git or Serena calls were made. Each step below describes what would be done.

## Step 0 – Project Configuration validation: PASS
The mock CLAUDE.md has all three required sections:
- Repository Registry: `trustify-backend`, Serena instance `serena_backend`, path `./`.
- Jira Configuration: project key TC, Cloud ID, and Feature issue type ID 10142. It also sets PR field `customfield_10875` and GitHub Issue field `customfield_10747`.
- Code Intelligence: tool naming convention `mcp__<instance>__<tool>`, using rust-analyzer.

## Step 1 – Parse the task
- **Mode: default.** There is no Target PR and no Bookend Type. Target Branch is `main`.
- Repository: `trustify-backend`.
- All required sections are present: Repository, Target Branch, Description, Files to Modify, Files to Create, Implementation Notes, Acceptance Criteria, Test Requirements, Dependencies. There is no API Changes section, but the change to the `GET /api/v2/sbom/{id}` response is covered under Files to Modify and Acceptance Criteria.
- GitHub Issue field `customfield_10747`: would be read from the issue. If it is empty, it is skipped.

## Step 1.5 – Digest check
Would fetch the comments, find `[sdlc-workflow] Description digest:` and compare it using `scripts/sha256-digest.py`. If no digest comment exists, log a warning and continue.

## Step 2 – Dependencies
"Depends on: None". Nothing to verify.

## Step 3 – Jira
Would assign the issue to the current user and transition it to In Progress. Simulated only.

## Step 4 – Understand the code (`serena_backend`)
- `get_symbols_overview` on `sbom/service/sbom.rs` (SbomService), `sbom/endpoints/get.rs`, `sbom/model/details.rs` (SbomDetails), and `advisory/model/summary.rs` (AdvisorySummary, which has the `severity` field).
- `find_symbol(include_body=true)` on the SbomService method that fetches related advisories through the `sbom_advisory` join table. The Implementation Notes say to follow this pattern.
- `find_referencing_symbols` on `SbomDetails` and on the get handler, to check backward compatibility (adding a field is additive).
- **Symbol dedup search for `SEVERITY_ORDER` and its variants.** Full detail is in `symbol-search.md`.
- Read `CONVENTIONS.md` at the repo root and record its CI check commands for Step 9 check 14.
- Sibling conventions, from `advisory/service/advisory.rs`, `sbom/endpoints/list.rs`, `tests/api/sbom.rs` and `tests/api/advisory.rs`:
  - Handlers return `Result<T, AppError>` and wrap errors with `.context()`.
  - Each domain uses the `model/ + service/ + endpoints/` layout.
  - Function names follow a `verb_noun` pattern.
  - Integration tests run against a real PostgreSQL database and check `assert_eq!(resp.status(), StatusCode::OK)`.
- Docs to check later: `README.md`, `CONVENTIONS.md`, and any API docs for `/api/v2/sbom/{id}`.

## Step 5 – Branch
`git checkout main && git pull && git checkout -b TC-9210` (simulated).

## Step 6 – Changes

### SEVERITY_ORDER handling: reuse it, never redeclare it
- The constant already exists in `modules/fundamental/src/advisory/service/advisory.rs` as `["critical", "high", "medium", "low", "none"]`.
- `sbom.rs` imports it with `use crate::advisory::service::advisory::SEVERITY_ORDER;`. It is in the same `fundamental` crate, so no new dependency is needed.
- If the constant is already `pub` or `pub(crate)`: import it and leave `advisory.rs` untouched.
- If it is private: under Reuse rule 2 (same crate, so no new cross-package dependency), change it to `pub(crate)` and import it. Do **not** inline a copy. This one-line visibility change is outside Files to Modify, so it is raised as a Step 9 scope flag for user approval and recorded in the PR description (Reuse rule 4).
- The sort key is the array position: `SEVERITY_ORDER.iter().position(..)`. Comparison is case-insensitive. Unknown or missing severity ranks last (`SEVERITY_ORDER.len()`).
- `Vec::sort_by_key` is a stable sort, so advisories with equal severity keep the order they were fetched in.

### File 1: `modules/fundamental/src/sbom/service/sbom.rs` (modify)
- Add the import of `SEVERITY_ORDER`.
- Add `pub struct RemediationItem { pub advisory_id: String, pub severity: Option<String>, pub title: Option<String>, pub fix_version: Option<String> }`.
  - Derives `Serialize, Deserialize, Debug, Clone, PartialEq, ToSchema` (or whatever sibling model structs derive).
  - Has a `///` doc comment.
  - Field types will match the advisory entity and model. `title` and `fix_version` are likely nullable.
  - Placement: the task lists only `sbom.rs` and `get.rs`, so it goes in `sbom.rs` by default. The convention would put it in `sbom/model/`, and that conflict is raised with the user (see Scope flags).
- Add `pub async fn build_remediation_list(&self, sbom_id: Id, tx/db) -> Result<Vec<RemediationItem>, Error>`:
  - Has a `///` doc comment saying it returns the SBOM's advisories sorted most severe first, using `SEVERITY_ORDER`.
  - Reuses the existing "fetch related advisories" query pattern (`sbom_advisory` join to `advisory`) and adds no new query helper.
  - Maps each row to a `RemediationItem`, guarding optional fields with `Option` / `.unwrap_or_default()` where data crosses the module boundary.
  - Sorts the items with the stable `sort_by_key(severity_rank)`.
  - Returns an empty `Vec` when the SBOM has no advisories.
- Add a private helper `fn severity_rank(severity: Option<&str>) -> usize`, built on `SEVERITY_ORDER`, with a doc comment.
- Optionally add `#[cfg(test)]` unit tests for `severity_rank` and the stable ordering, if sibling service files use inline unit tests.

### File 2: `modules/fundamental/src/sbom/endpoints/get.rs` (modify)
- In the `GET /api/v2/sbom/{id}` handler, call `sbom_service.build_remediation_list(id, ..)` with `.context("...")` error wrapping.
- Include the result in the response as a `remediations: Vec<RemediationItem>` field.
- Preferred approach: add `pub remediations: Vec<RemediationItem>` to `SbomDetails` with `#[serde(default)]`. That file (`sbom/model/details.rs`) is out of scope, so it is raised as a scope flag.
- In-scope alternative if the user declines: a response wrapper struct in `get.rs` that combines `#[serde(flatten)] details: SbomDetails` with `remediations: Vec<RemediationItem>`.
- Keep the existing 404 behavior and caching config unchanged.
- Update the OpenAPI/utoipa annotation if the handler has one.

### File 3: `tests/api/sbom_remediation.rs` (create)
- Follow the style of `tests/api/sbom.rs`: real test database, helpers to ingest fixture SBOMs and advisories, and `assert_eq!(resp.status(), StatusCode::OK)`.
- Every test gets a `///` doc comment and `// Given / // When / // Then` sections.
- `test_remediations_sorted_by_severity`: ingest advisories in mixed order (low, critical, none, high, medium). Assert the full `advisory_id` / `severity` sequence equals `[critical, high, medium, low, none]`. This is a value-based assertion, not just a length check.
- `test_remediations_empty_when_no_advisories`: an SBOM with no advisories returns 200 and `remediations == []`.
- `test_remediations_stable_for_equal_severity`: two or three "high" advisories, linked in a known order. Assert their relative order is kept, and assert each item's `advisory_id`, `title` and `fix_version` values.
- These three tests differ in setup and assertions, so they stay separate. No `rstest` unless siblings already use it.
- The test target may need registering, through a `[[test]]` entry in `tests/Cargo.toml` or a `mod` in the test harness, depending on how existing tests are wired. That is a scope flag if needed.

### Documentation
There is no Documentation Updates section. If the API docs describe the `/api/v2/sbom/{id}` response, the new `remediations` field goes on the Step 9 check 6 flag list rather than being edited.

## Step 7 – Tests
Run the per-crate tests for `fundamental` and the `tests` crate, as resolved in Step 9.

## Step 8 – Acceptance criteria
| Criterion | How it is satisfied |
|---|---|
| `GET /api/v2/sbom/{id}` response includes `remediations` | get.rs handler plus the response field |
| Sorted Critical > High > Medium > Low > None | `sort_by_key` on `SEVERITY_ORDER` position |
| Uses the existing `SEVERITY_ORDER`, no duplicate | Imported from the advisory module; dedup re-check finds a single definition |
| RemediationItem has advisory_id, severity, title, fix_version | Struct definition |

## Step 9 – Self-verification (planned results)
1. **Scope containment: FLAGGED** for user approval. Files that may need touching outside the listed scope:
   - `advisory/service/advisory.rs`: `pub(crate)` on `SEVERITY_ORDER`, only if it is private.
   - `sbom/model/details.rs`: the `remediations` field.
   - Test registration in `tests/Cargo.toml`, if required.
3. Sensitive patterns: PASS.
5. **Duplication**: re-run the `SEVERITY_ORDER` and variant search. Expect one definition and no inline copy. PASS.
6. Documentation currency: check the API docs for the SBOM details response.
10. Cross-section references: PASS. The paths match the repo tree.
11. Data-flow trace: trace from `sbom_advisory` join, to `RemediationItem`, to sort, to the response JSON.
12. Query scope: advisories are fetched with one query scoped to `sbom_id`, with no N+1 queries.
13. Sibling parity: same error and context handling as the other SbomService methods. The sort order matches how the advisory module ranks severity, because both use the same constant.
14. CI checks from CONVENTIONS.md, or fall back to `cargo fmt --check`, `cargo clippy`, `cargo build`.
15. Module tests: resolve crates with `cargo metadata` and run `cargo test -p <fundamental crate>` plus the tests crate.

## Step 10 – Commit and PR (simulated)
- Commit message: `feat(sbom): add severity-sorted remediation list to SBOM details`. Body notes the reuse (or `pub(crate)` export) of `SEVERITY_ORDER`. Footer: `Implements TC-9210`. Trailer: `--trailer="Assisted-by: Claude Code (Claude Opus 5.5)"`.
- Check for an `upstream` remote (fork detection), then `gh pr create --base main`.
- PR body: `Implements [TC-9210](<webUrl>)`, plus `Closes owner/repo#N` if the GitHub Issue field is set.

## Step 11 – Jira (simulated)
- Set `customfield_10875` to the PR URL as an ADF inlineCard.
- Comment with the PR link, a summary, and deviations (the visibility export, the `SbomDetails` field placement). The comment ends with the implement-task footnote.
- Transition to In Review.
