# Task 6 — Add optional threshold query parameter to advisory summary endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Add support for the optional `?threshold=<severity>` query parameter on the `GET /api/v2/sbom/{id}/advisory-summary` endpoint. When provided, the endpoint filters severity counts to only include severities at or above the specified threshold level. The severity hierarchy is: critical > high > medium > low. For example, `?threshold=high` returns counts for critical and high only, with medium and low omitted (set to 0 or excluded). This is a non-MVP enhancement supporting alerting integrations that need to check for advisories above a certain severity level.

## Files to Modify
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — add `Query` extractor for the `threshold` parameter and filter logic
- `modules/fundamental/src/sbom/service/sbom.rs` — add optional `threshold` parameter to `advisory_summary` method or add post-query filtering

## Implementation Notes
- Use Axum's `Query` extractor to parse the optional `threshold` parameter from the query string. Define a query params struct (e.g., `AdvisorySummaryParams`) with `threshold: Option<String>` or `threshold: Option<Severity>`.
- The severity hierarchy for threshold filtering: `critical` (highest) > `high` > `medium` > `low` (lowest). When `threshold=high`, include `critical` and `high` counts; set `medium` and `low` to 0.
- Decide whether to filter at the database query level (modify the SQL to exclude lower-severity advisories) or at the application level (compute all counts, then zero out those below the threshold). Application-level filtering is simpler and consistent with the caching strategy (one cached result can serve all threshold values with post-cache filtering).
- If implementing application-level filtering: the `advisory_summary` endpoint handler can apply the threshold filter after receiving the full `AdvisorySeveritySummary` from the service, zeroing out counts below the threshold and recomputing `total`.
- Reference the existing query parameter patterns in other endpoints (e.g., `modules/fundamental/src/sbom/endpoints/list.rs` for pagination parameters) to follow established Axum `Query` extractor conventions.
- Per docs/constraints.md Section 5 (Code Change Rules): changes must be scoped to the listed files; implementation must follow referenced patterns.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — demonstrates Axum `Query` extractor usage for parsing query parameters
- `common/src/db/query.rs` — shared query helpers that may include enum/filter patterns
- `modules/fundamental/src/sbom/endpoints/advisory_summary.rs` — the endpoint handler created in Task 3, which will be extended

## Acceptance Criteria
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=critical` returns only the `critical` count (other severities are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=high` returns `critical` and `high` counts (medium and low are 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=medium` returns `critical`, `high`, and `medium` counts (low is 0)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary?threshold=low` returns all counts (equivalent to no threshold)
- [ ] `GET /api/v2/sbom/{id}/advisory-summary` (no threshold) returns all counts as before
- [ ] `total` is recomputed to reflect only the included severity counts when threshold is applied
- [ ] Invalid threshold values return a 400 Bad Request error

## Test Requirements
- [ ] Integration test: `?threshold=critical` returns only critical count with others zeroed
- [ ] Integration test: `?threshold=high` returns critical and high counts
- [ ] Integration test: `?threshold=medium` returns critical, high, and medium counts
- [ ] Integration test: `?threshold=low` returns all counts (same as no threshold)
- [ ] Integration test: no threshold parameter returns all counts
- [ ] Integration test: invalid threshold value (e.g., `?threshold=invalid`) returns 400

## Verification Commands
- `cargo build` — full project compiles
- `cargo test --test api` — integration tests pass

## Dependencies
- Depends on: Task 3 — Add GET /api/v2/sbom/{id}/advisory-summary endpoint with caching
- Depends on: Task 5 — Add integration tests for advisory summary endpoint
