# Implementation Plan for TC-9201

## Task Summary

**Jira Key:** TC-9201
**Summary:** Add advisory severity aggregation service and endpoint
**Target Branch:** main
**Branch to Create:** TC-9201

## Step 1.5 — Description Digest Verification

Check for a description digest comment on the Jira issue by fetching all comments via `jira.get_issue_comments(TC-9201)` and searching for any comment whose body starts with the marker string `[sdlc-workflow] Description digest:`.

**Result:** No description digest comment found. Per the backward compatibility clause in `shared/description-digest-protocol.md`: "No description digest found — skipping integrity check. This task may have been created before digest tracking was introduced." Proceed with implementation normally without blocking execution.

## Pre-Implementation Inspection (Step 4)

Before making any changes, inspect the following existing files to understand current patterns and conventions:

1. **`modules/fundamental/src/advisory/endpoints/get.rs`** — Understand the existing endpoint handler pattern: `Path<Id>` extraction, service invocation, JSON response wrapping, `Result<T, AppError>` return type.
2. **`modules/fundamental/src/advisory/service/advisory.rs`** — Understand the `AdvisoryService` struct and its existing methods (`fetch`, `list`) to match the pattern for the new `severity_summary` method, including the `(&self, id: Id, tx: &Transactional<'_>)` signature pattern.
3. **`modules/fundamental/src/advisory/model/summary.rs`** — Understand the `AdvisorySummary` struct and its `severity` field, which will be used to count by severity level.
4. **`modules/fundamental/src/advisory/model/mod.rs`** — Understand the module registration pattern (`pub mod summary;`, `pub mod details;`) to add `pub mod severity_summary;`.
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Understand the route registration pattern (`Router::new().route("/path", get(handler))`) to register the new endpoint.
6. **`common/src/error.rs`** — Understand the `AppError` enum and `.context()` wrapping pattern for error handling.
7. **`entity/src/sbom_advisory.rs`** — Understand the SBOM-Advisory join table for querying advisories linked to an SBOM.
8. **`tests/api/advisory.rs`** — Understand the integration test patterns: test naming, assertion style, status code checks, body deserialization.

Also inspect sibling files for convention conformance:
- **`modules/fundamental/src/sbom/endpoints/get.rs`** — Sibling endpoint handler for comparison.
- **`modules/fundamental/src/sbom/model/summary.rs`** — Sibling model struct for comparison.
- **`tests/api/sbom.rs`** — Sibling test file for test convention analysis.

## Files to Create (3 new files)

1. **`modules/fundamental/src/advisory/model/severity_summary.rs`** — `SeveritySummary` response struct with fields: `critical`, `high`, `medium`, `low`, `total` (all `u64`), deriving `Serialize`, `Deserialize`, `Debug`, `Default`.
2. **`modules/fundamental/src/advisory/endpoints/severity_summary.rs`** — GET handler for `/api/v2/sbom/{id}/advisory-summary` that extracts `Path<Id>`, calls `AdvisoryService::severity_summary`, and returns `Json<SeveritySummary>`.
3. **`tests/api/advisory_summary.rs`** — Integration tests covering: valid SBOM with known severity counts, non-existent SBOM returns 404, SBOM with no advisories returns all zeros, duplicate advisory deduplication.

## Files to Modify (3 existing files)

4. **`modules/fundamental/src/advisory/service/advisory.rs`** — Add `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table for the given SBOM ID, fetches linked advisories, counts unique advisories by severity level, and returns `Result<SeveritySummary, AppError>`.
5. **`modules/fundamental/src/advisory/endpoints/mod.rs`** — Register the new route: `.route("/api/v2/sbom/:id/advisory-summary", get(severity_summary::handler))`.
6. **`modules/fundamental/src/advisory/model/mod.rs`** — Add `pub mod severity_summary;` to register the new model module.

## Scope

All changes are strictly scoped to the files listed in the task's "Files to Modify" and "Files to Create" sections. No other files will be touched. The task explicitly states that `server/src/main.rs` requires no changes (routes auto-mount via module registration).

## Branching Strategy

1. Check out target branch and pull latest:
   ```
   git checkout main
   git pull
   ```
2. Create the task branch:
   ```
   git checkout -b TC-9201
   ```

## Commit Strategy

Use Conventional Commits format with `--trailer='Assisted-by: Claude Code'`:

```
feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201
```

Command:
```
git commit --trailer='Assisted-by: Claude Code' -m "feat(advisory): add severity aggregation endpoint for SBOM advisories

Add GET /api/v2/sbom/{id}/advisory-summary endpoint that returns
severity counts (critical, high, medium, low, total) for advisories
linked to a given SBOM. Includes SeveritySummary model, service method,
endpoint handler, and integration tests.

Implements TC-9201"
```

## PR Creation

After pushing the branch, create a PR targeting the `main` branch:
```
git push -u origin TC-9201
gh pr create --base main --title "feat(advisory): add severity aggregation endpoint" --body "..."
```

The PR description will include an `Implements [TC-9201](<webUrl>)` link to the Jira issue.
