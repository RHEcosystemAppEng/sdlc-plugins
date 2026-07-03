## Repository
trustify-backend

## Target Branch
main

## Description
Add a new `remediation` module under `modules/fundamental/src/` following the established domain module pattern (model/ + service/ + endpoints/). This task creates the foundational module structure and implements the `GET /api/v2/remediation/summary` endpoint, which returns aggregated vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved).

The aggregation must compute results from existing vulnerability and SBOM relationship data (entity tables: `advisory`, `sbom_advisory`) without creating new database tables, per the Feature's non-functional requirement. The endpoint must meet the p95 < 500ms performance requirement.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root
- `modules/fundamental/src/remediation/model/mod.rs` -- model module root
- `modules/fundamental/src/remediation/model/summary.rs` -- RemediationSummary and SeverityStatusCount structs
- `modules/fundamental/src/remediation/service/mod.rs` -- service module root
- `modules/fundamental/src/remediation/service/remediation.rs` -- RemediationService with summary aggregation query
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for /api/v2/remediation
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- GET /api/v2/remediation/summary handler

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` declaration
- `server/src/main.rs` -- mount remediation routes alongside existing sbom and advisory routes
- `modules/fundamental/Cargo.toml` -- add dependencies if needed

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns aggregated remediation counts by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved) with totals for open, in-progress, and resolved vulnerabilities

## Implementation Notes
- Follow the existing domain module pattern established by `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`: each module has `model/`, `service/`, and `endpoints/` subdirectories.
  Per CONVENTIONS.md section "Module pattern": structure the remediation module as model/ + service/ + endpoints/.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` module file scope.

- The summary endpoint handler should return `Result<Json<RemediationSummary>, AppError>` following the error handling pattern in `common/src/error.rs`. All internal errors should use `.context()` wrapping for actionable error messages.
  Per CONVENTIONS.md section "Error handling": all handlers return `Result<T, AppError>` with `.context()` wrapping.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` scope.

- Use SeaORM query builders to aggregate from `advisory` and `sbom_advisory` entities. Reference `entity/src/advisory.rs` for the Advisory entity structure (which includes the severity field) and `entity/src/sbom_advisory.rs` for the SBOM-Advisory join table that correlates vulnerabilities to SBOMs.

- Use database-level `GROUP BY` for the severity x status aggregation rather than loading all rows into memory, to meet the p95 < 500ms performance requirement.

- Register routes in `endpoints/mod.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` (route registration with Axum router).

- Mount the remediation module routes in `server/src/main.rs` following the same mount pattern used for sbom and advisory modules.

- Consider adding tower-http caching middleware configuration for the summary response, following the caching pattern documented in the project conventions.
  Per CONVENTIONS.md section "Caching": uses tower-http caching middleware; cache configuration in endpoint route builders.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs::PaginatedResults<T>` -- standard response wrapper for list endpoints (may be used for consistency)
- `common/src/error.rs::AppError` -- error type implementing IntoResponse for all endpoint handlers
- `entity/src/advisory.rs` -- Advisory entity with severity field, key entity for aggregation queries
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table for vulnerability correlation
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- reference implementation showing established service-layer query patterns

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with aggregated counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
- [ ] Response includes totals for total open, total in-progress, and total resolved
- [ ] Aggregation computes from existing entity tables (`advisory`, `sbom_advisory`) without creating new database tables
- [ ] Endpoint returns valid JSON with correct content type
- [ ] Remediation module follows the model/ + service/ + endpoints/ directory structure
- [ ] Routes are mounted and accessible at /api/v2/remediation/summary

## Test Requirements
- [ ] Integration test verifying `GET /api/v2/remediation/summary` returns 200 with correct response shape
- [ ] Integration test verifying aggregation counts match expected values for seeded test data
- [ ] Integration test verifying empty database returns zero counts (not an error)

## Verification Commands
- `cargo build` -- verify compilation with new module
- `cargo test --test remediation` -- run remediation integration tests

## Documentation Updates
- Backend API documentation -- add reference for `GET /api/v2/remediation/summary` endpoint with request/response examples

## Dependencies
- None (first task in the backend epic)
