## Repository
trustify-backend

## Target Branch
main

## Description
Add a new REST endpoint `GET /api/v2/sbom/{id}/advisory-summary` that returns aggregated vulnerability advisory severity counts for a single SBOM, as requested by TC-9001. Today the frontend dashboard fetches every page of an SBOM's advisories and counts severities client-side (~2s for large SBOMs). This task moves that computation to the backend so a single call returns `{ critical, high, medium, low, total }`, counting each advisory only once (deduplicated by advisory ID). A request for an SBOM ID that does not exist must return 404, consistent with the existing SBOM endpoints.

Caching and cache invalidation are delivered separately in Task 2. The optional `?threshold=` filter is delivered separately in Task 3.

## Files to Modify
- `modules/fundamental/src/sbom/model/mod.rs` — declare and re-export the new `advisory_summary` model module
- `modules/fundamental/src/sbom/service/sbom.rs` — add an `SbomService` method (e.g., `advisory_severity_summary`) that verifies the SBOM exists and runs a single aggregate query over the SBOM-advisory relationship
- `modules/fundamental/src/sbom/endpoints/mod.rs` — register the `/api/v2/sbom/{id}/advisory-summary` route alongside the existing `/api/v2/sbom` routes
- `tests/api/sbom.rs` — add integration tests for the new endpoint

## Files to Create
- `modules/fundamental/src/sbom/model/advisory_summary.rs` — `AdvisorySeveritySummary` response struct with `critical`, `high`, `medium`, `low`, `total` integer fields (serde `Serialize`)
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — Axum handler for `GET /api/v2/sbom/{id}/advisory-summary`

## API Changes
- `GET /api/v2/sbom/{id}/advisory-summary` — NEW: returns `{ "critical": N, "high": N, "medium": N, "low": N, "total": N }` for the SBOM; 404 if the SBOM ID does not exist

## Implementation Notes
- **Module layout**: follow the existing `model/ + service/ + endpoints/` structure of the SBOM module. The handler goes in its own file next to `modules/fundamental/src/sbom/endpoints/get.rs` (which serves `GET /api/v2/sbom/{id}`) and is registered in `modules/fundamental/src/sbom/endpoints/mod.rs`. `server/src/main.rs` already mounts the SBOM module's routes, so no change is needed there.
- **404 handling (fail-closed gate)**: in the new `SbomService` method in `modules/fundamental/src/sbom/service/sbom.rs`, first check that the SBOM exists, reusing the lookup `SbomService` already uses for fetch (as called from `modules/fundamental/src/sbom/endpoints/get.rs`). If it is missing, return the same `AppError` not-found variant that `get.rs` returns (`common/src/error.rs`). Do **not** rely on the aggregate query alone: an aggregate over `sbom_advisory` for an unknown ID returns zero rows, which would look like a valid all-zero summary with 200 OK. That would be a silent false success.
- **Aggregation query**: run one database round-trip over `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) joined to `entity/src/advisory.rs`, filtered by SBOM ID and grouped by advisory severity, using `COUNT(DISTINCT advisory.id)` so an advisory linked to the SBOM through more than one row (e.g., through several packages) is counted once. Use SeaORM `select_only()` / `column_as()` / `group_by()`, and reuse the filtering helpers in `common/src/db/query.rs` where they fit. Do not load the advisories and count them in Rust. A single grouped query is needed to meet the p95 < 200ms NFR for SBOMs with up to 500 advisories.
- **No new tables**: the NFR forbids new database tables or migrations. Use only the existing `sbom_advisory` and `advisory` entities.
- **Severity mapping**: check how severity is represented on `AdvisorySummary` in `modules/fundamental/src/advisory/model/summary.rs` and on the `advisory` entity (enum vs. string, casing). Map values into the four buckets in exactly one place. `total` is the number of distinct advisories linked to the SBOM. Advisories whose severity is null or not one of Critical/High/Medium/Low count only toward `total`. This rule is flagged in the impact map for product confirmation.
- **Response type**: this is a single-object endpoint, not a list, so do **not** wrap it in `PaginatedResults<T>` (`common/src/model/paginated.rs`).
- **Existing advisory listing**: the Feature mentions an existing `GET /api/v2/sbom/{id}/advisories` endpoint, but it does not appear in the analyzed repository structure. Before writing the join, search the SBOM and advisory modules for it. If it exists, reuse its SBOM-to-advisory join logic instead of duplicating it.
- Per CONVENTIONS.md §Module pattern: place the response struct in `sbom/model/`, the query in `sbom/service/`, and the handler in `sbom/endpoints/`. Applies: task modifies `modules/fundamental/src/sbom/service/sbom.rs` matching the convention's Rust domain-module (`modules/*/src/**/*.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs` together with `modules/fundamental/src/sbom/model/details.rs`.
- Per CONVENTIONS.md §Error handling: the handler must return `Result<Json<AdvisorySeveritySummary>, AppError>`, and database errors must be wrapped with `.context()`. Applies: task creates `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Endpoint registration: register the route in the module's `endpoints/mod.rs`, not in `server/src/main.rs`. Applies: task modifies `modules/fundamental/src/sbom/endpoints/mod.rs` matching the convention's `endpoints/mod.rs` scope. Example: the existing `/api/v2/sbom` registration in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Per CONVENTIONS.md §Testing: add integration tests in `tests/api/sbom.rs` against the PostgreSQL test database, using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/sbom.rs` matching the convention's `tests/api/*.rs` scope. Example: the existing tests in `tests/api/sbom.rs`.
- **Constraints (docs/constraints.md)**:
  - §1.4/§1.5/§1.6: keep changes to this task's scope, inspect code before changing it, and ask for clarification if this description turns out to be incomplete.
  - §2.1–§2.3: Conventional Commits message, a Jira ID footer (`Implements <task-key>`), and an `Assisted-by:` trailer.
  - §3.1–§3.3: branch named after the task's Jira ID, PR link posted on the Jira task, and `gh pr create --base main`.
  - §5.1–§5.14: change only the listed files, reuse existing helpers instead of duplicating them, trace the full data flow (request → service → query → response), match sibling handlers on error handling, and add doc comments plus given-when-then comments to non-trivial tests.

## Reuse Candidates
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — existing SBOM fetch logic. Reuse it for the existence check that drives the 404.
- `modules/fundamental/src/sbom/endpoints/get.rs` — reference handler for `GET /api/v2/sbom/{id}`: path extraction, not-found mapping, and response shape.
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — already carries the advisory `severity` field. Reuse its severity type and parsing instead of defining a new severity enum.
- `entity/src/sbom_advisory.rs` — existing SBOM-Advisory join entity to aggregate over (no new tables).
- `common/src/db/query.rs` — shared query builder helpers for filtering.
- `common/src/error.rs::AppError` — standard error type, including the not-found response.

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` for an existing SBOM returns 200 with a JSON object containing exactly the integer fields `critical`, `high`, `medium`, `low`, `total`
- [ ] Each advisory is counted once even when it is linked to the SBOM through more than one `sbom_advisory` row (deduplicated by advisory ID)
- [ ] A request with an SBOM ID that does not exist returns 404 (same error shape as `GET /api/v2/sbom/{id}`), **not** 200 with all-zero counts
- [ ] An existing SBOM with no linked advisories returns 200 with all counts equal to 0
- [ ] Counts are computed by a single grouped database query. Advisories are not loaded into memory to be counted.
- [ ] No new database tables or migrations are introduced
- [ ] Existing `/api/v2/sbom` and `/api/v2/advisory` endpoints behave exactly as before

## Test Requirements
- [ ] Integration test: an SBOM linked to advisories of every severity returns the correct count per bucket and the correct `total`
- [ ] Integration test: an advisory linked to the same SBOM through two different link rows is counted once
- [ ] Integration test (fail-closed): a random, non-existent SBOM ID returns 404, and the test asserts the response is not a 200 with zero counts
- [ ] Integration test: an ingested SBOM with no correlated advisories returns 200 with all zeros
- [ ] Integration test: an advisory with null or unrecognized severity counts toward `total` only

## Verification Commands
- `cargo test --test api sbom` — all SBOM integration tests pass, including the new advisory-summary tests
- `curl -s http://localhost:8080/api/v2/sbom/<existing-id>/advisory-summary` — returns a JSON object with `critical`, `high`, `medium`, `low`, `total`
- `curl -s -o /dev/null -w '%{http_code}' http://localhost:8080/api/v2/sbom/does-not-exist/advisory-summary` — prints `404`

## Documentation Updates
- `README.md` — if the README lists the available API endpoints, add `GET /api/v2/sbom/{id}/advisory-summary`. Full API reference documentation is handled in Task 4.
