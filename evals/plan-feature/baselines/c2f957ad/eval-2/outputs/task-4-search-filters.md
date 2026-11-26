# Task 4 — Add filter parameters to search endpoint

**Jira:** Task, parent EPIC-3 ("TC-9002: Search filtering"), labels `ai-generated-jira`, priority `Normal`, fixVersions `RHTPA 1.6.0`

## Repository
trustify-backend

## Target Branch
main

## Description
TC-9002 asks for "some kind of filtering capability" without naming the dimensions. This task adds optional filter query parameters to `GET /api/v2/search`. It uses only fields that already exist in the domain models, so no schema changes are needed.

**Assumptions (pending clarification on TC-9002, open question 3). The product owner must confirm these before implementation:**
- `type`: limit results to one or more entity types (`sbom`, `advisory`, `package`)
- `severity`: limit advisory results by `AdvisorySummary.severity` (`modules/fundamental/src/advisory/model/summary.rs`)
- `license`: limit package results by `PackageSummary.license` (`modules/fundamental/src/package/model/summary.rs`, backed by `entity/src/package_license.rs`)
- All filters are optional and combine with AND. If no filter is given, the endpoint behaves exactly as it does today.

## Files to Modify
- `modules/search/src/endpoints/mod.rs` — accept and validate the optional `type`, `severity` and `license` query parameters, and pass them to the service
- `modules/search/src/service/mod.rs` — apply the filters to the per-entity queries, skipping entity types excluded by `type`
- `tests/api/search.rs` — add filter tests
- `README.md` — document the new search filter parameters

## API Changes
- `GET /api/v2/search` — MODIFY: adds the optional query parameters `type` (comma-separated: `sbom`, `advisory`, `package`), `severity` (advisory severity values) and `license` (package license identifier). The response shape (`PaginatedResults<T>`) is unchanged

## Implementation Notes
- Use the shared filtering helpers in `common/src/db/query.rs`. Do not build WHERE clauses by hand.
- Reject invalid filter values (unknown `type`, unknown `severity`) with a 400 `AppError` (`common/src/error.rs`). Do not ignore them silently: an ignored filter returns unfiltered results that look like a success.
- Apply `severity` only to advisory results and `license` only to package results. When `severity` is given without `type`, return only advisories that match the severity. Do not return unfiltered SBOMs and packages next to them. Write this behavior down in the README and the PR so the product owner can confirm it.
- `total` in `PaginatedResults<T>` (`common/src/model/paginated.rs`) must reflect the filtered count.
- This task and Task 3 both edit `modules/search/src/service/mod.rs`. Rebase on whichever merges first, and keep the filters compatible with relevance ordering.
- Per CONVENTIONS.md §Query helpers: shared filtering, pagination and sorting go through `common/src/db/query.rs`. Express the new filters with these helpers. Applies: task modifies modules/search/src/service/mod.rs matching the convention's Rust query construction (`.rs`) scope. Example usage: `modules/fundamental/src/advisory/endpoints/list.rs`.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` with `.context()` wrapping, and validation failures map to an `AppError` variant. Applies: task modifies modules/search/src/endpoints/mod.rs matching the convention's Rust handler (`.rs`) scope.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`, and filtering must not change this wrapper. Applies: task modifies modules/search/src/endpoints/mod.rs matching the convention's Rust endpoint (`.rs`) scope.
- Per CONVENTIONS.md §Testing: integration tests go in `tests/api/` against the real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/search.rs matching the convention's integration test (`tests/api/*.rs`) scope.
- Constraints (docs/constraints.md): §1.4 and §5.1 scope limits. §5.2 inspect before modifying. §5.4 reuse `common/src/db/query.rs`. §5.8 parity with the filtering on `GET /api/v2/advisory` and `GET /api/v2/package`. §2.1–2.3 commit rules. §3.1–3.3 PR rules. §5.9–5.12 test conventions.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering helpers. Use them for every new filter
- `modules/fundamental/src/advisory/endpoints/list.rs` — existing list endpoint whose filter parameter handling can be copied
- `modules/fundamental/src/package/endpoints/list.rs` — existing package list endpoint, a possible example for license filtering
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — source of the `severity` field and its values

## Acceptance Criteria
- [ ] `GET /api/v2/search?q=<term>&type=advisory` returns only advisories
- [ ] `GET /api/v2/search?q=<term>&type=sbom,package` returns only SBOMs and packages
- [ ] `GET /api/v2/search?q=<term>&severity=<value>` returns only advisories with that severity
- [ ] `GET /api/v2/search?q=<term>&license=<id>` returns only packages with that license
- [ ] Combined filters apply with AND semantics
- [ ] An invalid `type` or `severity` value returns HTTP 400 with an `AppError` body and does not return unfiltered results
- [ ] `total` reflects the filtered result count
- [ ] Requests without filter parameters return exactly the same results as before this change
- [ ] README documents the new parameters and their semantics

## Test Requirements
- [ ] Test each filter on its own (`type`, `severity`, `license`), asserting `StatusCode::OK` and that only matching entities come back
- [ ] Test combined filters (for example `type=advisory&severity=<value>`)
- [ ] Test that an invalid filter value returns 400 and not an unfiltered 200 (fail-closed)
- [ ] Test that `total` matches the filtered count across pages
- [ ] Regression: existing `tests/api/search.rs` tests without filters pass unchanged

## Verification Commands
- `cargo test --test api search` — all search tests pass
- `curl -s 'http://localhost:8080/api/v2/search?q=openssl&type=advisory'` — only advisory items come back

## Documentation Updates
- `README.md` — add the `type`, `severity` and `license` query parameters of `GET /api/v2/search`, with examples and the AND/entity-scoping semantics

## Dependencies
- None
