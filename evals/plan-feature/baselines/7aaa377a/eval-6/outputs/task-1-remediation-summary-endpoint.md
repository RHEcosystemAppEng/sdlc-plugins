## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation module under modules/fundamental/ and implement the `GET /api/v2/remediation/summary` endpoint. This endpoint returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). The aggregation is computed from existing vulnerability and SBOM relationship data without creating new database tables, satisfying the feature's non-functional requirement. The endpoint must meet p95 < 500ms response time.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root, re-exports model, service, and endpoints
- `modules/fundamental/src/remediation/model/mod.rs` -- model module root
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary struct with severity-by-status aggregation fields
- `modules/fundamental/src/remediation/service/mod.rs` -- RemediationService with summary aggregation query
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for /api/v2/remediation
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler

## Files to Modify
- `server/src/main.rs` -- mount the remediation module routes alongside existing module routes
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` to expose the new module
- `modules/fundamental/Cargo.toml` -- add any new dependencies if needed

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns aggregated remediation counts grouped by severity (Critical, High, Medium, Low) x status (Open, In Progress, Resolved). Response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }`

## Implementation Notes
- Follow the existing module pattern (model/ + service/ + endpoints/) as established by the sbom, advisory, and package modules under modules/fundamental/src/.
  Per CONVENTIONS.md (Key Conventions -- Module pattern): structure the remediation module with model/, service/, and endpoints/ subdirectories.
  Applies: task creates `modules/fundamental/src/remediation/mod.rs` matching the convention's Rust module scope.
- Per CONVENTIONS.md (Key Conventions -- Error handling): all handlers must return `Result<T, AppError>` with `.context()` wrapping for error propagation.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md (Key Conventions -- Endpoint registration): register routes in the module's `endpoints/mod.rs` and mount in `server/main.rs`, following the pattern in `modules/fundamental/src/advisory/endpoints/mod.rs`.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` file scope.
- Per CONVENTIONS.md (Key Conventions -- Caching): consider applying `tower-http` caching middleware to the summary endpoint for performance, following existing cache configuration patterns in other endpoint route builders.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` file scope.
- Aggregation queries should join across the `advisory`, `sbom_advisory`, and related entities to compute severity-by-status counts. Use SeaORM's query builder with the existing entity definitions in `entity/src/`.
- Use `common/src/db/query.rs` for any shared query building helpers needed for filtering and pagination.

## Reuse Candidates
- `common/src/db/query.rs::query helpers` -- shared filtering, pagination, and sorting utilities; reuse for any query parameter handling in the remediation service
- `common/src/model/paginated.rs::PaginatedResults<T>` -- standard response wrapper for list endpoints; use for the summary response structure
- `common/src/error.rs::AppError` -- standard error type implementing IntoResponse; use in all endpoint handlers
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- reference implementation for service pattern with SeaORM queries; follow the same structure for RemediationService
- `modules/fundamental/src/advisory/endpoints/mod.rs` -- reference for route registration pattern
- `entity/src/advisory.rs` -- Advisory entity with severity field; used as data source for severity-based aggregation
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table; used to correlate vulnerabilities with SBOMs for aggregation

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with aggregated counts grouped by severity and status
- [ ] Response includes all four severity levels (Critical, High, Medium, Low) with Open, In Progress, and Resolved counts for each
- [ ] Aggregation is computed from existing entity data without new database tables
- [ ] Endpoint follows existing module conventions (model/ + service/ + endpoints/)
- [ ] Error cases return appropriate AppError responses

## Test Requirements
- [ ] Summary endpoint returns correct aggregation when vulnerabilities exist across multiple severities and statuses
- [ ] Summary endpoint returns zero counts when no vulnerability data exists
- [ ] Summary endpoint returns appropriate error response on database failure

## Verification Commands
- `cargo build` -- project compiles without errors
- `cargo test --test api` -- integration tests pass

## Dependencies
- None (first task in the chain)
