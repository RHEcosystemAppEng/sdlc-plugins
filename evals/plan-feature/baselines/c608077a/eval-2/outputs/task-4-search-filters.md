## Repository
trustify-backend

## Target Branch
main

## Description
Add filtering to `GET /api/v2/search`, addressing the TC-9002 MVP requirement "Add filters". The Feature says only "some kind of filtering capability", so the filter set below is an assumption based on the attributes that already exist in the backend models. The Product Owner must confirm it before acceptance.

**Assumed filter set (needs confirmation on TC-9002):**
- `type` — restrict results to one or more entity types: `sbom`, `advisory`, `package` (`SearchService` already searches across these entities)
- `severity` — restrict advisory results by severity (backed by the existing `severity` field on `AdvisorySummary`)
- `license` — restrict package results by license (backed by the existing `license` field on `PackageSummary` and the `package_license` mapping)

**Open questions:** Should filters also be added to the per-entity list endpoints (`/api/v2/advisory`, `/api/v2/package`), or only to search? Are date-range filters (for example, published date) wanted? This task covers only `GET /api/v2/search` and the three filters above.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — accept the optional `type`, `severity`, and `license` query parameters, validate them, and pass them to the service
- `modules/search/src/service/mod.rs` — apply the filters in the database query (not in memory after fetching) so pagination `total` stays correct
- `tests/api/search.rs` — add tests for each filter, for combined filters, and for invalid filter values

## API Changes
- `GET /api/v2/search` — MODIFY: new optional query parameters `type` (comma-separated: `sbom|advisory|package`), `severity` (comma-separated advisory severities), and `license` (license identifier). Omitting all of them keeps today's behaviour. Invalid values return 400 through `AppError`.

## Implementation Notes
- Build the filter conditions with the shared filtering helpers in `common/src/db/query.rs`. Do not hand-write SQL fragments for each filter.
- `severity` comes from the advisory model (`modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary`) and the advisory entity (`entity/src/advisory.rs`). Reuse the existing severity type/enum for parsing and validation instead of redefining the allowed values.
- `license` comes from `modules/fundamental/src/package/model/summary.rs::PackageSummary` and the `entity/src/package_license.rs` mapping. Filter with a join or subquery on `package_license`.
- Filter semantics: when `type` excludes `advisory`, a `severity` filter has nothing to apply to, and the same holds for `license` without `package`. Document the chosen behaviour (recommended: return 400 for a contradictory combination such as `type=sbom&severity=high`, so filters are never silently ignored).
- Apply the filters before ordering and pagination so `PaginatedResults.total` reflects the filtered count. This must stay compatible with the relevance ordering from Task 3.
- Per CONVENTIONS.md §Query Helpers: filtering, pagination, and sorting go through `common/src/db/query.rs`. See `modules/fundamental/src/advisory/service/advisory.rs` for usage.
  Applies: task modifies `modules/search/src/service/mod.rs` matching the convention's service query (`service/*.rs`) scope.
- Per CONVENTIONS.md §Error Handling: handlers return `Result<T, AppError>` with `.context()` wrapping; map invalid filter input to a 400 variant of `AppError` in `common/src/error.rs`.
  Applies: task modifies `modules/search/src/endpoints/mod.rs` matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. See `tests/api/advisory.rs`.
  Applies: task modifies `tests/api/search.rs` matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): §2.1–2.3 (commit rules); §3.1–3.3 (PR rules, `--base main`); §5.1–5.4 (scope, inspect first, follow patterns, no duplication).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — the existing `severity` field and type.
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — the existing `license` field.
- `modules/fundamental/src/advisory/endpoints/list.rs`, `modules/fundamental/src/package/endpoints/list.rs` — check whether these list endpoints already parse filter query parameters, and reuse their parameter structs or parsing.

## Acceptance Criteria
- [ ] `type=advisory` returns only advisories; `type=sbom,package` returns only SBOMs and packages
- [ ] `severity=<value>` returns only advisories with that severity
- [ ] `license=<value>` returns only packages with that license
- [ ] Filters combine with AND semantics and work together with the free-text query
- [ ] Filtering happens in the database query, and `PaginatedResults.total` equals the filtered count
- [ ] Invalid filter values and contradictory combinations return 400 with an `AppError` message; they are never silently ignored
- [ ] A request with no filter parameters returns the same results as before this change
- [ ] The filter set is confirmed by the Product Owner on TC-9002 (or revised and the implementation updated) before the task is closed

## Test Requirements
- [ ] One test per filter (`type`, `severity`, `license`) asserting that only matching results are returned
- [ ] Combined-filter test (for example `type=advisory&severity=critical` plus a query term)
- [ ] Pagination-with-filter test asserting `total` equals the filtered count
- [ ] Invalid-value test (unknown `type`, unknown `severity`) asserting 400
- [ ] Contradictory-combination test (`type=sbom&severity=high`) asserting 400
- [ ] No-filter regression test asserting unchanged results

## Verification Commands
- `cargo test --test api search` — all search tests, including the filter tests, pass

## Documentation Updates
- `README.md` — if the README documents the search API, add the `type`, `severity`, and `license` parameters with allowed values

## Dependencies
- Depends on: Task 2 — Optimize search query performance (indexes and pagination)
- Depends on: Task 3 — Improve search result relevance ranking (filters must compose with relevance ordering and touch the same `SearchService` query; sequencing avoids conflicting edits)
