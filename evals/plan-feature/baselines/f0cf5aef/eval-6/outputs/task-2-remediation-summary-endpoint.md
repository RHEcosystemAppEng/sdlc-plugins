## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Add a new `remediation` module under `modules/fundamental/src/` and implement the `GET /api/v2/remediation/summary` endpoint. This endpoint returns aggregated vulnerability counts grouped by severity (Critical, High, Medium, Low) and remediation status (Open, In Progress, Resolved). The aggregation is computed from existing vulnerability and SBOM relationship data without creating new database tables.

This is the primary backend endpoint for the remediation tracking dashboard (TC-9006), providing portfolio-wide remediation visibility.

## Files to Modify
- `modules/fundamental/src/lib.rs` — register the new `remediation` submodule
- `modules/fundamental/Cargo.toml` — add any needed dependencies for the remediation module
- `server/src/main.rs` — mount the remediation module routes

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root
- `modules/fundamental/src/remediation/model/mod.rs` — model module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` struct with severity x status counts
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with aggregation query logic
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — `GET /api/v2/remediation/summary` handler
- `tests/api/remediation.rs` — integration tests for the summary endpoint

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated vulnerability counts by severity x status. Response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }`

## Implementation Notes
- Follow the existing module pattern used by `sbom/`, `advisory/`, and `package/` modules: `model/ + service/ + endpoints/` structure.
- The handler must return `Result<Json<RemediationSummary>, AppError>` following the error handling pattern in `common/src/error.rs` with `.context()` wrapping.
- Build the aggregation query using the shared query helpers in `common/src/db/query.rs` for filtering and pagination.
- Use SeaORM to query from existing entities: `advisory` (for severity), `sbom_advisory` (for SBOM-advisory relationships), and derive status from advisory state fields.
- No new database tables are permitted per non-functional requirements. All aggregations must be computed from existing `entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`, and related entities.
- Register routes in `endpoints/mod.rs` following the same pattern as `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Performance requirement: p95 response time < 500ms. Consider using database-level GROUP BY for aggregation rather than loading all records into memory.
- Per repo conventions: use `tower-http` caching middleware for the summary endpoint route builder to enable response caching.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper for list endpoints
- `common/src/error.rs` — `AppError` enum for error handling
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct as a reference for severity field handling
- `modules/fundamental/src/sbom/endpoints/mod.rs` — route registration pattern to follow
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService` as a reference for service layer pattern

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns 200 with aggregated counts grouped by severity and status
- [ ] Response includes counts for all four severity levels: Critical, High, Medium, Low
- [ ] Response includes counts for all three status values: Open, In Progress, Resolved
- [ ] Endpoint returns correct totals that match the sum of individual severity/status combinations
- [ ] No new database tables are created — aggregation uses existing entity relationships
- [ ] p95 response time is under 500ms with 10,000 tracked vulnerabilities

## Test Requirements
- [ ] Integration test: `GET /api/v2/remediation/summary` returns 200 with correct structure
- [ ] Integration test: verify aggregated counts match expected values for test data
- [ ] Integration test: verify response with no vulnerabilities returns zero counts
- [ ] Integration test: verify response handles large datasets (10,000+ vulnerabilities) without timeout

## Verification Commands
- `cargo test --test api remediation` — runs remediation endpoint integration tests, expects all tests to pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
