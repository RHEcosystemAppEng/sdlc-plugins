## Repository
trustify-backend

## Target Branch
main

## Parent Epic
TC-9006: trustify-backend

## Description
Add a new remediation module under `modules/fundamental/` that provides a summary aggregation endpoint for vulnerability remediation tracking. The `GET /api/v2/remediation/summary` endpoint returns aggregated vulnerability counts grouped by severity (Critical, High, Medium, Low) and remediation status (Open, In Progress, Resolved). The aggregation computes over existing vulnerability and SBOM relationship data without requiring new database tables, fulfilling the feature requirement for portfolio-wide remediation visibility.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, re-exports sub-modules
- `modules/fundamental/src/remediation/model/mod.rs` — model sub-module root
- `modules/fundamental/src/remediation/model/summary.rs` — `RemediationSummary` struct with severity x status counts
- `modules/fundamental/src/remediation/service/mod.rs` — `RemediationService` with `get_summary()` method performing aggregation query
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` — handler for `GET /api/v2/remediation/summary`

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to register the new module
- `server/src/main.rs` — mount remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated vulnerability counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved). Response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }] }`

## Implementation Notes
- Follow the established module pattern: `model/ + service/ + endpoints/` as used by `sbom/`, `advisory/`, and `package/` modules.
  Per CONVENTIONS.md §Module Pattern: structure the remediation module with model/, service/, and endpoints/ sub-directories.
  Applies: task creates `modules/fundamental/src/remediation/mod.rs` matching the convention's module structure scope.
- The handler must return `Result<Json<RemediationSummary>, AppError>` following the error handling convention.
  Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for all error paths.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's `.rs` handler file scope.
- Register routes in `endpoints/mod.rs` and mount in `server/src/main.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`.
  Per CONVENTIONS.md §Endpoint Registration: register routes in the module's `endpoints/mod.rs` and mount in `server/main.rs`.
  Applies: task modifies `server/src/main.rs` matching the convention's route mounting scope.
- Aggregate data using SeaORM queries over existing `advisory`, `sbom_advisory`, and related entities. No new database tables — use `GROUP BY` on severity and status fields.
- Use `common/src/db/query.rs` query builder helpers for constructing the aggregation query.
  Per CONVENTIONS.md §Query Helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`.
  Applies: task creates `modules/fundamental/src/remediation/service/mod.rs` matching the convention's `.rs` service file scope.
- Non-functional: p95 response time must be under 500ms. Consider query optimization for datasets with up to 10,000 tracked vulnerabilities.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering, pagination, and sorting; reuse for aggregation query construction
- `common/src/model/paginated.rs::PaginatedResults` — standard response wrapper for list endpoints; evaluate whether the summary endpoint needs pagination or returns a fixed-size result
- `common/src/error.rs::AppError` — standard error type; reuse for handler error responses
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — reference implementation of the service pattern with SeaORM queries
- `modules/fundamental/src/sbom/endpoints/mod.rs` — reference for route registration pattern

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns a 200 response with aggregated counts grouped by severity and status
- [ ] Response includes counts for all four severity levels: Critical, High, Medium, Low
- [ ] Response includes counts for all three statuses: Open, In Progress, Resolved
- [ ] Aggregation computes from existing vulnerability and SBOM relationship data (no new database tables created)
- [ ] Route is registered and mounted in the server alongside existing modules
- [ ] Error responses use `AppError` with appropriate status codes

## Test Requirements
- [ ] Integration test verifying `GET /api/v2/remediation/summary` returns 200 with correct JSON structure
- [ ] Integration test verifying counts are accurate against known test data
- [ ] Integration test verifying empty database returns zero counts (not an error)

## Verification Commands
- `cargo test --test api remediation` — verify integration tests pass
- `cargo clippy --all-targets` — verify no lint warnings in new code

## Dependencies
- None (first task in the implementation sequence)
