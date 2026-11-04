# Task 4 — Add validated filters to GET /api/v2/search

**Summary:** TC-9002: Add validated filters to GET /api/v2/search
**Issue type:** Task | **Labels:** ai-generated-jira | **Priority:** Normal | **Fix Versions:** RHTPA 1.6.0

## Repository
trustify-backend

## Target Branch
main

## Description
This task delivers the "Add filters" requirement of TC-9002. Users get optional filter parameters on the global search endpoint, so they can narrow results.

**Planning assumption (A3, still to be confirmed):** the Feature only says "some kind of filtering capability". This task plans the filter dimensions backed by fields that already exist in the models:
- `type` — entity type: `sbom`, `advisory`, `package` (repeatable)
- `severity` — advisory severity (`AdvisorySummary.severity`, `modules/fundamental/src/advisory/model/summary.rs`)
- `license` — package license (`PackageSummary.license`, `modules/fundamental/src/package/model/summary.rs`; `entity/src/package_license.rs`)

If the Feature owner asks for other dimensions (for example date ranges or SBOM-scoped search), revise this task before implementation.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — parse and validate the new optional query parameters
- `modules/search/src/service/mod.rs` — apply the filters to the per-entity queries
- `tests/api/search.rs` — filter tests

## API Changes
- `GET /api/v2/search` — MODIFY: adds optional query parameters `type` (repeatable: `sbom|advisory|package`), `severity` (advisory severity values) and `license` (SPDX license identifier). With no filters, behavior is identical to before. The response shape (`PaginatedResults<T>`) is unchanged.

## Implementation Notes
- Build the filter conditions with the shared filtering helpers in `common/src/db/query.rs`. Do not hand-write SQL fragments.
- Filter semantics: values within one parameter are combined with OR, and different parameters are combined with AND. Entity-specific filters narrow only their own entity. If `severity` is given without `type`, it applies to advisories only, and SBOM and package results are excluded, because a severity filter implies advisories. Document this rule in the endpoint doc comment.
- **Fail-closed validation:** an unknown filter value (for example `type=foo` or `severity=extreme`) must return 400 Bad Request through `AppError` (`common/src/error.rs`). It must not be dropped silently. Silently ignoring a bad filter returns unfiltered results that look like a success, so users trust results that were never filtered. Put the validation guard in the query-parameter parsing of the search handler in `modules/search/src/endpoints/mod.rs`.
- The license filter joins through `entity/src/package_license.rs`. Check that the join uses existing indexes on the license mapping. If it does not, raise this on TC-9002 rather than adding a migration in this task.
- Constraints (docs/constraints.md): §5.1, §5.2, §5.4 reuse `query.rs`, §5.8 parity with filter handling in sibling list endpoints, §5.14 filter at the data-source level (in SQL), not in memory after the fetch, §2.1–2.3, §3.2–3.3.

## Reuse Candidates
- `common/src/db/query.rs` — shared filter builder used by the list endpoints. This is the main reuse target.
- `modules/fundamental/src/advisory/endpoints/list.rs` — existing list endpoint showing how query parameters are parsed and passed to the service
- `modules/fundamental/src/package/endpoints/list.rs` — same pattern for packages
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — source of the severity field and its allowed values

## Acceptance Criteria
- [ ] `type=advisory` returns only advisories, and repeated `type` values return the union of those types
- [ ] `severity=<value>` returns only advisories with that severity
- [ ] `license=<spdx-id>` returns only packages with that license
- [ ] Filters combine with the free-text query `q` and with each other (AND across parameters)
- [ ] Filtering runs in the database query, so pagination totals reflect the filtered set
- [ ] An unknown value for any filter parameter returns 400 Bad Request with a descriptive error. It never returns unfiltered results.
- [ ] Requests without filter parameters behave exactly as before (backward compatible)

## Test Requirements
- [ ] Integration tests in `tests/api/search.rs` cover each filter on its own (`type`, `severity`, `license`), asserting that only matching entities are returned
- [ ] An integration test combines `q` with two filters and asserts AND semantics and a correct `total`
- [ ] An integration test sends `type=foo` and `severity=invalid` and asserts 400. This is the fail-closed path: unknown values must not produce an unfiltered 200.
- [ ] An integration test without filters asserts results identical to the pre-change behavior

## Verification Commands
- `cargo test --test api search` — all search tests pass
- `curl -s -o /dev/null -w '%{http_code}\n' 'http://localhost:8080/api/v2/search?q=x&type=foo'` — prints `400`

## Documentation Updates
- `README.md` — document the new filter parameters on `GET /api/v2/search`, if the README documents API endpoints

## Dependencies
- Depends on: Task 2 — Use indexed full-text queries and caching in SearchService
