## Repository
trustify-backend

## Target Branch
main

## Description
Part of TC-9002 (Improve search experience), requirement "Add filters" (MVP).

This task extends the search filter handling added in Task 2 with two attribute filters that existing models already carry:
- `severity`: filters advisory results by the `severity` field of `AdvisorySummary`
- `license`: filters package results by license, using the package-license mapping

**Assumptions pending confirmation:** both filter dimensions were inferred from repository evidence, not stated in the Feature (see the TC-9002 impact map, clarification question 3).

**Scope check required before implementation:** repository analysis could not tell whether `SearchService` queries the entity tables directly or a derived search index or column filled in at ingestion time (`modules/ingestor/src/graph/advisory/mod.rs`, `modules/ingestor/src/graph/sbom/mod.rs`). If search reads a derived index that lacks severity or license, this task cannot meet its criteria without ingestor and migration changes, which are out of the current scope. In that case, stop and ask for a scope expansion on TC-9002. Do not claim the criteria are met.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — parse and validate the optional `severity` and `license` query parameters
- `modules/search/src/service/mod.rs` — apply the severity filter to advisory results and the license filter to package results (join through the package-license mapping)
- `tests/api/search.rs` — add attribute-filter tests

## API Changes
- `GET /api/v2/search` — MODIFY: new optional query parameters `severity` (repeatable; values matching the existing advisory severity values) and `license` (repeatable; license identifier). Both are optional, and leaving them out keeps the current behavior.

## Implementation Notes
- Severity: use the `severity` field defined on `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`) and the advisory entity (`entity/src/advisory.rs`). Validate input against the same set of severity values the model uses. An unknown severity must return 400 via `AppError`, not an empty or unfiltered result.
- License: join `entity/src/package.rs` to `entity/src/package_license.rs`. The `license` field on `PackageSummary` (`modules/fundamental/src/package/model/summary.rs`) shows how license is exposed today.
- Interaction with `type` (Task 2): an attribute filter applies only to its own entity type. Define and document the semantics explicitly. Recommended: when `severity` is given and `type` is not, results are limited to advisories, because SBOMs and packages have no severity. Record the chosen semantics in the PR.
- Use the shared filtering helpers in `common/src/db/query.rs` and keep Task 1's pagination (`total` reflects the filtered count).
- Per CONVENTIONS.md §Query helpers: filtering goes through `common/src/db/query.rs`. Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service/query scope. Example: `modules/fundamental/src/package/service/mod.rs` (`PackageService` list).
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()`. Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's handler scope. Example: `modules/fundamental/src/package/endpoints/list.rs`.
- Per CONVENTIONS.md §Testing: use real PostgreSQL integration tests with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/search.rs` matching the convention's integration test scope. Example: `tests/api/advisory.rs`.
- Constraints (docs/constraints.md):
  - §2 commits: Conventional Commits, `Implements <task-key>` footer, Assisted-by trailer.
  - §3 PRs: `--base main`, and post the PR link on the Jira task.
  - §5 code changes: change only the listed files, inspect code first, reuse the shared helpers, check parity with the Task 2 filter validation.

## Reuse Candidates
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — the existing `severity` field and its value set
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — the existing `license` field
- `entity/src/package_license.rs` — Package-License mapping entity for the license join
- `common/src/db/query.rs` — shared filtering helpers
- Filter parameter parsing and validation added to `modules/search/src/endpoints/mod.rs` by Task 2

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=<term>&severity=critical` returns only advisories with critical severity
- [ ] `GET /api/v2/search?q=<term>&license=Apache-2.0` returns only packages with that license
- [ ] Multiple values per filter return the union of matches
- [ ] `severity` and `license` combine correctly with the `type` filter from Task 2, with the semantics documented in the PR
- [ ] An unknown `severity` value returns 400. It never returns unfiltered results.
- [ ] Requests without the new parameters behave exactly as before (existing `tests/api/search.rs` passes)
- [ ] It is confirmed and stated in the PR whether search reads entity tables directly or a derived index. If it is a derived index without these fields, work stops and a scope expansion is requested on TC-9002.

## Test Requirements
- [ ] Integration test: seed advisories with different severities. The severity filter returns only matching advisories.
- [ ] Integration test: seed packages with different licenses. The license filter returns only matching packages.
- [ ] Integration test: multiple severity values return their union
- [ ] Integration test: `severity` combined with `type=advisory`, and `license` combined with `type=package`
- [ ] Integration test: an invalid severity returns 400
- [ ] Integration test: no attribute filters returns the unfiltered results (backward compatibility)

## Verification Commands
- `cargo test -p tests search` — all search integration tests pass

## Documentation Updates
- `README.md` — document the `severity` and `license` filter parameters of `GET /api/v2/search`, if the README documents the API

## Dependencies
- Depends on: Task 2 — Add an entity-type filter to GET /api/v2/search
