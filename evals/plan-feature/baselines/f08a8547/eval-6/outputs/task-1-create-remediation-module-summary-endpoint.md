## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` module in the backend following the established model/service/endpoints module pattern. Implement the `GET /api/v2/remediation/summary` endpoint that returns aggregated vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). Aggregations are computed from existing vulnerability and SBOM relationship data without creating new database tables. The endpoint must meet the p95 < 500ms performance requirement for up to 10,000 tracked vulnerabilities.

## Files to Modify
- `Cargo.toml` — add remediation module to workspace members
- `server/src/main.rs` — mount remediation module routes

## Files to Create
- `modules/remediation/Cargo.toml` — module crate manifest with dependencies on common and entity crates
- `modules/remediation/src/lib.rs` — module root exposing model, service, and endpoints submodules
- `modules/remediation/src/model/mod.rs` — model module root
- `modules/remediation/src/model/summary.rs` — RemediationSummary struct with severity-by-status breakdown
- `modules/remediation/src/service/mod.rs` — service module root
- `modules/remediation/src/service/remediation.rs` — RemediationService with summary aggregation query
- `modules/remediation/src/endpoints/mod.rs` — route registration for /api/v2/remediation
- `modules/remediation/src/endpoints/summary.rs` — GET /api/v2/remediation/summary handler

## API Changes
- `GET /api/v2/remediation/summary` — NEW: Returns aggregated remediation counts by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)

## Implementation Notes
- Per CONVENTIONS.md §Module pattern: follow the model/ + service/ + endpoints/ directory structure for the new remediation module. See `modules/fundamental/src/sbom/` for the established pattern.
  Applies: task creates `modules/remediation/src/model/summary.rs` matching the convention's Rust module file scope.

- Per CONVENTIONS.md §Error handling: all endpoint handlers must return `Result<T, AppError>` and use `.context()` for error wrapping. See `modules/fundamental/src/sbom/endpoints/get.rs` for the established pattern.
  Applies: task creates `modules/remediation/src/endpoints/summary.rs` matching the convention's .rs endpoint file scope.

- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting from `common/src/db/query.rs`. See existing service implementations for query builder usage patterns.
  Applies: task creates `modules/remediation/src/service/remediation.rs` matching the convention's .rs service file scope.

- Per CONVENTIONS.md §Endpoint registration: register routes in the module's `endpoints/mod.rs` and mount all modules in `server/src/main.rs`. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the route registration pattern.
  Applies: task creates `modules/remediation/src/endpoints/mod.rs` matching the convention's .rs endpoint file scope.

- The aggregation query should join the `advisory` entity (which carries severity data) with `sbom_advisory` (for SBOM correlation) and compute group-by counts using SQL aggregation. No new tables are permitted per NFR.
- Use efficient SQL GROUP BY rather than in-memory processing to meet the p95 < 500ms requirement.

## Reuse Candidates
- `common/src/db/query.rs::*` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper
- `common/src/error.rs::AppError` — error handling enum implementing IntoResponse
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — reference for severity field structure
- `entity/src/advisory.rs` — advisory entity with severity data for aggregation
- `entity/src/sbom_advisory.rs` — SBOM-advisory join table for vulnerability correlation

## Acceptance Criteria
- [ ] New `modules/remediation/` module exists following model/service/endpoints pattern
- [ ] `GET /api/v2/remediation/summary` returns JSON with severity-by-status aggregation matrix
- [ ] Response includes counts for all four severities (Critical, High, Medium, Low) and three statuses (Open, In Progress, Resolved)
- [ ] Aggregations are computed from existing `advisory` and `sbom_advisory` data without new database tables
- [ ] Remediation routes are registered and mounted in `server/src/main.rs`
- [ ] Endpoint returns appropriate error responses for server errors

## Test Requirements
- [ ] Integration test in `tests/api/remediation.rs` verifying summary endpoint returns 200 with correct response structure
- [ ] Test that response includes all severity levels and status values with numeric counts
- [ ] Test with empty dataset returns zero counts for all cells
- [ ] Test response structure matches the RemediationSummary model

## Verification Commands
- `cargo build` — builds successfully with new remediation module
- `cargo test --test remediation` — all remediation integration tests pass

## Dependencies
- None
