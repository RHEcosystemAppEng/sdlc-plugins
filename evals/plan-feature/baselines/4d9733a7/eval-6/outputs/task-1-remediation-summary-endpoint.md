## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` module under `modules/fundamental/src/` and implement the `GET /api/v2/remediation/summary` endpoint. This endpoint aggregates vulnerability remediation counts across all ingested SBOMs, grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved). The aggregation is computed from existing vulnerability and SBOM relationship data without requiring new database tables, as specified by the non-functional requirements.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, declares sub-modules
- `modules/fundamental/src/remediation/model/mod.rs` — model sub-module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` struct with severity-by-status counts
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `get_summary()` method
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — handler for `GET /api/v2/remediation/summary`

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` declaration
- `modules/fundamental/Cargo.toml` — add any additional dependencies if needed
- `server/src/main.rs` — mount remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated remediation counts grouped by severity and status. Response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }`

## Implementation Notes
- Follow the established module pattern used by `sbom`, `advisory`, and `package` modules: each has `model/`, `service/`, and `endpoints/` sub-directories. See `modules/fundamental/src/sbom/` for the canonical example.
- Per repo conventions (Module pattern): each domain module follows `model/ + service/ + endpoints/` structure.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's module structure scope.
- Per repo conventions (Error handling): all handlers return `Result<T, AppError>` with `.context()` wrapping. See `common/src/error.rs` for the `AppError` enum.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust endpoint file scope.
- Per repo conventions (Endpoint registration): register routes in `endpoints/mod.rs` and mount in `server/src/main.rs`. See `modules/fundamental/src/sbom/endpoints/mod.rs` for the route registration pattern.
  Applies: task modifies `server/src/main.rs` matching the convention's endpoint registration scope.
- Per repo conventions (Response types): use `PaginatedResults<T>` from `common/src/model/paginated.rs` if the summary response uses pagination, or a custom response struct if not.
  Applies: task creates `modules/fundamental/src/remediation/model/summary.rs` matching the convention's Rust model file scope.
- Aggregation must be computed via SQL queries joining existing entity tables (`entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`) rather than creating new tables, per the non-functional requirement.
- Target p95 response time < 500ms. Consider using indexed queries and avoiding N+1 patterns in the aggregation.
- Per repo conventions (Caching): use `tower-http` caching middleware for the summary endpoint to reduce database load. See existing endpoint route builders for cache configuration patterns.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust endpoint file scope.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering, pagination, and sorting; reuse for any filtering on the summary endpoint
- `common/src/model/paginated.rs::PaginatedResults` — standard paginated response wrapper; use if the summary supports pagination
- `common/src/error.rs::AppError` — standard error type; use for all handler error returns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — reference for service pattern including database query construction against advisory data
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; key for building aggregation queries across vulnerabilities and SBOMs

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns a 200 response with aggregated counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved)
- [ ] The response is computed from existing vulnerability and SBOM relationship data without new database tables
- [ ] The endpoint follows the established module pattern (model/service/endpoints)
- [ ] Error responses use the standard `AppError` format
- [ ] The endpoint is registered and accessible in the running server

## Test Requirements
- [ ] Verify `GET /api/v2/remediation/summary` returns 200 with correct response shape
- [ ] Verify aggregation correctly groups counts by severity and status
- [ ] Verify the endpoint returns empty counts when no vulnerability data exists
- [ ] Verify error handling returns appropriate error responses

## Verification Commands
- `cargo build` — confirm the project compiles with the new module
- `cargo test` — confirm existing tests still pass

## Dependencies
- None (first task)
