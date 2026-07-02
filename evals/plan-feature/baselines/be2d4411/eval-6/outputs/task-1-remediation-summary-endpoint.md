## Repository
trustify-backend

## Target Branch
main

## Description
Create a new remediation domain module following the existing model/service/endpoints pattern and implement the `GET /api/v2/remediation/summary` endpoint. This endpoint returns aggregated vulnerability remediation counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved). Aggregations are computed from existing SBOM-advisory relationship data without creating new database tables. The endpoint must meet a p95 response time target of less than 500ms.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root, declares sub-modules
- `modules/fundamental/src/remediation/model/mod.rs` — model sub-module root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary and SeverityStatusCount structs
- `modules/fundamental/src/remediation/service/mod.rs` — service sub-module root
- `modules/fundamental/src/remediation/service/remediation.rs` — RemediationService with summary aggregation query
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for /api/v2/remediation
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation` declaration
- `server/src/main.rs` — mount remediation module routes alongside existing modules

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated remediation counts by severity and status. Response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: number }`

## Implementation Notes
- Follow the existing domain module pattern used by `modules/fundamental/src/advisory/` — each module has `model/`, `service/`, and `endpoints/` sub-directories.
  Per CONVENTIONS.md: follow model/service/endpoints module structure for new domain modules.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's Rust module file scope.
- All endpoint handlers must return `Result<T, AppError>` using `.context()` for error wrapping, matching the pattern in `common/src/error.rs`.
  Per CONVENTIONS.md: use Result<T, AppError> with .context() wrapping for all handlers.
  Applies: task creates `modules/fundamental/src/remediation/endpoints/summary.rs` matching the convention's .rs endpoint file scope.
- Use the shared query builder helpers from `common/src/db/query.rs` for constructing aggregation queries against the existing `sbom_advisory` join table.
- The aggregation query should join `entity/src/advisory.rs` (for severity) with `entity/src/sbom_advisory.rs` (for SBOM-advisory relationships) to compute counts without new tables.
- Register routes in `modules/fundamental/src/remediation/endpoints/mod.rs` following the pattern in `modules/fundamental/src/advisory/endpoints/mod.rs`, then mount in `server/src/main.rs`.
- Response time target: p95 < 500ms. Consider using SQL-level GROUP BY aggregation rather than in-memory collection to meet this target with up to 10,000 tracked vulnerabilities.

## Reuse Candidates
- `common/src/db/query.rs::query` — shared query builder helpers for filtering and pagination
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper for list endpoints
- `common/src/error.rs::AppError` — error type implementing IntoResponse
- `entity/src/advisory.rs` — Advisory entity with severity field for aggregation
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table for relationship traversal
- `modules/fundamental/src/advisory/endpoints/mod.rs` — reference for route registration pattern

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns HTTP 200 with aggregated counts grouped by severity and status
- [ ] Response includes counts for all four severity levels (Critical, High, Medium, Low)
- [ ] Response includes counts for all three status categories (Open, In Progress, Resolved)
- [ ] Endpoint returns valid empty/zero-count response when no vulnerability data exists
- [ ] No new database tables or migrations are created — aggregations use existing entity relationships

## Test Requirements
- [ ] Integration test verifying summary endpoint returns 200 with expected response shape
- [ ] Integration test verifying correct aggregation counts with seeded test data
- [ ] Integration test verifying empty dataset returns zero counts for all severity/status combinations

## Verification Commands
- `cargo test --test api remediation` — run remediation endpoint integration tests
- `cargo clippy --all-targets` — verify no linting warnings in new code

## Dependencies
- None

[sdlc-workflow] Description digest: sha256-md:d5f2eab17ec9d85cec2871ec8aae1b609d4734a2b70b2c0a68145fbc0e3e7643
