## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation module following the established model/service/endpoints pattern and implement the `GET /api/v2/remediation/summary` endpoint. This endpoint returns aggregated vulnerability remediation counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved). Aggregations are computed from existing vulnerability and SBOM relationship data without creating new database tables. The endpoint must meet the p95 < 500ms response time requirement and handle up to 10,000 tracked vulnerabilities.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, declares model, service, and endpoints submodules
- `modules/fundamental/src/remediation/model/mod.rs` — model submodule registration
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` response struct with severity-by-status counts
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with summary aggregation query logic
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the new `remediation` module
- `server/src/main.rs` — mount remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). Response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }`

## Implementation Notes
- Per CONVENTIONS.md §Module Pattern: follow the `model/ + service/ + endpoints/` structure used by existing domain modules. See `modules/fundamental/src/sbom/` for the established pattern.
  Applies: task creates `modules/fundamental/src/remediation/mod.rs` matching the convention's module directory scope.
- Per CONVENTIONS.md §Error Handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation. See `common/src/error.rs` for the `AppError` enum.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Response Types: list endpoints return `PaginatedResults<T>` from `common/src/model/paginated.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` endpoint file scope.
- Per CONVENTIONS.md §Endpoint Registration: register routes in the module's `endpoints/mod.rs` and mount in `server/src/main.rs`. See `modules/fundamental/src/sbom/endpoints/mod.rs` for route registration pattern.
  Applies: task modifies `server/src/main.rs` matching the convention's server setup scope.
- Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting utilities from `common/src/db/query.rs`.
  Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` service file scope.
- No new database tables — aggregate from existing `advisory`, `sbom_advisory`, and related entities using SeaORM queries
- Use `GROUP BY` on severity and status columns to compute counts efficiently
- Consider adding database indexes or query optimization to meet the p95 < 500ms SLA under 10,000 vulnerabilities

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for list endpoints
- `common/src/error.rs::AppError` — error enum implementing IntoResponse
- `entity/src/advisory.rs` — Advisory entity with severity field, source for aggregation queries
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for correlating vulnerabilities with SBOMs
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — existing service pattern to follow for query structure

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with aggregated counts grouped by severity and status
- [ ] Response includes counts for all four severity levels: Critical, High, Medium, Low
- [ ] Response includes counts for all three status values: Open, In Progress, Resolved
- [ ] Aggregation computed from existing advisory and SBOM data without new database tables
- [ ] Endpoint responds within p95 < 500ms with up to 10,000 tracked vulnerabilities
- [ ] Remediation module registered in `modules/fundamental/src/lib.rs`
- [ ] Remediation routes mounted in `server/src/main.rs`

## Test Requirements
- [ ] Integration test in `tests/api/remediation.rs` verifying `GET /api/v2/remediation/summary` returns 200 with correct response shape
- [ ] Test with seeded advisory data covering multiple severity levels and statuses to verify correct aggregation counts
- [ ] Test with empty dataset returns zero counts for all severity-status combinations
- [ ] Test response time is within acceptable bounds under load (10,000 vulnerabilities)

## Verification Commands
- `cargo test --test api remediation` — runs remediation endpoint integration tests
- `cargo clippy --all-targets` — verifies no lint warnings in new code

## Dependencies
- None (first task in the implementation sequence)
