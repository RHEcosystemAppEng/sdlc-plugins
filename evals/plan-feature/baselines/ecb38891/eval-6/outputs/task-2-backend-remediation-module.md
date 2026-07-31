# Task 2: Add remediation aggregation service and API endpoints

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Create a new `remediation` domain module under `modules/fundamental/src/remediation/` that provides two aggregation endpoints for the vulnerability remediation tracking dashboard. The module computes aggregations from existing vulnerability and SBOM relationship data without creating new database tables.

The two endpoints are:
1. `GET /api/v2/remediation/summary` -- returns aggregated counts grouped by severity (Critical/High/Medium/Low) x status (Open/In Progress/Resolved)
2. `GET /api/v2/remediation/by-product` -- returns per-product remediation breakdown with total, open, and resolved counts per product

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root, re-exports model/service/endpoints
- `modules/fundamental/src/remediation/model/mod.rs` -- model module root
- `modules/fundamental/src/remediation/model/summary.rs` -- `RemediationSummary` struct with severity/status matrix counts and `ProductRemediation` struct with per-product breakdown
- `modules/fundamental/src/remediation/service/mod.rs` -- `RemediationService` with aggregation query methods
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- handler for `GET /api/v2/remediation/summary`
- `modules/fundamental/src/remediation/endpoints/by_product.rs` -- handler for `GET /api/v2/remediation/by-product`

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` to expose the new module
- `modules/fundamental/Cargo.toml` -- add any new dependencies if needed
- `server/src/main.rs` -- mount remediation module routes alongside existing SBOM, advisory, and search routes

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns `{ items: [{ severity: string, status: string, count: number }], total: number }` aggregated across all ingested SBOMs
- `GET /api/v2/remediation/by-product` -- NEW: returns `{ items: [{ product: string, total: number, open: number, in_progress: number, resolved: number }], total: number }` with per-product breakdown

## Implementation Notes
- Follow the existing module pattern in `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/` -- each has `model/`, `service/`, and `endpoints/` subdirectories.
- All handlers return `Result<T, AppError>` with `.context()` wrapping, following the error handling pattern in `common/src/error.rs`.
- Use `PaginatedResults<T>` from `common/src/model/paginated.rs` as the response wrapper for both endpoints.
- Use query builder helpers from `common/src/db/query.rs` for filtering, pagination, and sorting.
- Aggregation queries should join existing `advisory`, `sbom_advisory`, `sbom`, and `package` entities from `entity/src/` -- no new SeaORM entities or migrations are needed.
- The summary endpoint groups by `severity` (from `AdvisorySummary` in `entity/src/advisory.rs`) and remediation `status`.
- The by-product endpoint derives product grouping from SBOM metadata linked to advisories via the `sbom_advisory` join table (`entity/src/sbom_advisory.rs`).
- Route registration follows the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs` -- register routes and mount them in `server/src/main.rs`.
- Non-functional: summary endpoint must achieve p95 < 500ms response time; ensure aggregation queries are efficient (use SQL GROUP BY rather than in-memory aggregation).
- Non-functional: must handle up to 10,000 tracked vulnerabilities without performance degradation.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; reuse for remediation queries
- `common/src/model/paginated.rs::PaginatedResults<T>` -- pagination response wrapper; use for both endpoint responses
- `common/src/error.rs::AppError` -- error type with IntoResponse impl; use for all handler error returns
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` -- reference for service pattern and how to query advisory-related data
- `modules/fundamental/src/sbom/endpoints/list.rs` -- reference for list endpoint handler pattern with filtering and pagination

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns aggregated counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved)
- [ ] `GET /api/v2/remediation/by-product` returns per-product remediation breakdown with total, open, in_progress, and resolved counts
- [ ] Both endpoints return `PaginatedResults<T>` response format consistent with other list endpoints
- [ ] Aggregations are computed from existing entity tables (advisory, sbom_advisory, sbom, package) with no new database tables or migrations
- [ ] Both endpoints handle an empty database gracefully (return zero counts, not errors)
- [ ] Summary endpoint achieves p95 < 500ms response time
- [ ] Error responses follow the `AppError` pattern used by existing endpoints
- [ ] Routes are registered in `server/src/main.rs` and accessible at the `/api/v2/remediation/` path prefix

## Test Requirements
- [ ] Integration test for `GET /api/v2/remediation/summary` verifying correct severity x status grouping with seeded test data
- [ ] Integration test for `GET /api/v2/remediation/by-product` verifying per-product breakdown with seeded test data
- [ ] Integration test verifying empty database returns valid empty response (not error)
- [ ] Integration test verifying pagination parameters work correctly on both endpoints
- [ ] Tests follow the pattern in `tests/api/sbom.rs` using `assert_eq!(resp.status(), StatusCode::OK)`

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9006 from main
