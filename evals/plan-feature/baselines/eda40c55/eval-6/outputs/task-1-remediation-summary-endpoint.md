## Repository
trustify-backend

## Target Branch
main

## Description
Add a new remediation module with a summary aggregation endpoint at `GET /api/v2/remediation/summary`. This endpoint computes aggregated vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved) from existing vulnerability and SBOM relationship data. No new database tables are required -- aggregations are computed from existing entity relationships.

This is the first of two backend endpoints supporting the new vulnerability remediation tracking dashboard (TC-9006).

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- Remediation module root, re-exports model, service, and endpoints sub-modules
- `modules/fundamental/src/remediation/model/mod.rs` -- Model sub-module root
- `modules/fundamental/src/remediation/model/summary.rs` -- `RemediationSummary` struct with fields: severity (enum), status (enum), count (i64); and `RemediationSummaryResponse` wrapping a Vec of summaries
- `modules/fundamental/src/remediation/service/mod.rs` -- `RemediationService` with `get_summary()` method that queries advisory-SBOM relationships and aggregates counts
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- Route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- Handler for `GET /api/v2/remediation/summary`

## Files to Modify
- `modules/fundamental/src/lib.rs` -- Register the new `remediation` module
- `server/src/main.rs` -- Mount remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: Returns aggregated remediation counts grouped by severity and status. Response shape: `{ items: [{ severity: string, status: string, count: number }] }`

## Implementation Notes
- Compute aggregations by joining `advisory` and `sbom_advisory` entities from `entity/src/advisory.rs` and `entity/src/sbom_advisory.rs`. The severity field is available on `AdvisorySummary` (see `modules/fundamental/src/advisory/model/summary.rs`).
- The aggregation query should use SeaORM's `select_only()` with `column_as()` and `group_by()` for the severity and status fields, returning counts via `column_as(Expr::count(), "count")`.
- The endpoint must meet p95 < 500ms response time. Consider using the query helpers in `common/src/db/query.rs` for efficient query construction.
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` directory structure for the new remediation module, matching the pattern used by existing modules (sbom, advisory, package).
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping on fallible operations. See `modules/fundamental/src/advisory/endpoints/list.rs` for the established pattern.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust endpoint file scope.
- Per CONVENTIONS.md §Endpoint Registration: register routes in `endpoints/mod.rs` and mount via `server/src/main.rs`. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the route registration pattern.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's Rust endpoint registration scope.
- Per CONVENTIONS.md §Response Types: list/aggregation endpoints should return structured responses using wrappers from `common/src/model/paginated.rs`. For this non-paginated aggregation, define a dedicated response struct but follow the same serialization conventions.
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's Rust model file scope.

## Reuse Candidates
- `common/src/db/query.rs::QueryBuilder` -- Shared query builder helpers for filtering, pagination, and sorting; reuse for constructing the aggregation query
- `common/src/model/paginated.rs::PaginatedResults` -- Response wrapper pattern to reference for the summary response struct design
- `common/src/error.rs::AppError` -- Error enum implementing IntoResponse; use for all error handling in the new module
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` -- Contains severity field definition; reference for severity enum values

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with aggregated counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- [ ] Response includes all severity-status combinations present in the data
- [ ] Aggregation is computed from existing advisory-SBOM relationship data without new database tables
- [ ] Endpoint response time is p95 < 500ms with up to 10,000 tracked vulnerabilities
- [ ] Module follows the `model/ + service/ + endpoints/` structure

## Test Requirements
- [ ] Unit test for `RemediationService::get_summary()` verifying correct aggregation counts
- [ ] Verify response JSON shape matches the defined `RemediationSummaryResponse` struct
- [ ] Verify empty database returns empty items array (not an error)

## Verification Commands
- `cargo test --test api remediation` -- Expected: all remediation endpoint tests pass
- `cargo build` -- Expected: clean build with no warnings in the remediation module

## Dependencies
- None
