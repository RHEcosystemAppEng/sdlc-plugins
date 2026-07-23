## Repository
trustify-backend

## Target Branch
main

## Description
Create the remediation module with data models, aggregation service, and the summary endpoint. This is the foundational backend task for the vulnerability remediation tracking dashboard (TC-9006). The module follows the existing domain module pattern (model/ + service/ + endpoints/) established by the sbom, advisory, and package modules under modules/fundamental/. The summary endpoint provides aggregated vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved), along with a 30-day trend for progress tracking. All aggregations are computed from existing advisory and SBOM relationship data with no new database tables.

## Files to Create
- `modules/remediation/Cargo.toml` — New crate for the remediation module
- `modules/remediation/src/lib.rs` — Module root, re-exports
- `modules/remediation/src/model/mod.rs` — Model module declarations
- `modules/remediation/src/model/summary.rs` — RemediationSummary struct with severity-by-status breakdown and trend data
- `modules/remediation/src/service/mod.rs` — RemediationService with aggregation queries joining advisory and sbom_advisory entities
- `modules/remediation/src/endpoints/mod.rs` — Route registration for /api/v2/remediation
- `modules/remediation/src/endpoints/summary.rs` — GET /api/v2/remediation/summary handler
- `tests/api/remediation.rs` — Integration tests for the summary endpoint

## Files to Modify
- `Cargo.toml` — Add modules/remediation as a workspace member
- `server/src/main.rs` — Mount remediation module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: Returns aggregated remediation counts by severity x status, total counts (open, in_progress, resolved), and a 30-day daily trend array

## Implementation Notes
- Follow the module pattern established in `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`: each domain module has `model/`, `service/`, and `endpoints/` sub-directories.
- The RemediationSummary model struct should follow the patterns in `modules/fundamental/src/advisory/model/summary.rs` (AdvisorySummary) for struct organization and serialization.
- The RemediationService should follow the query patterns in `modules/fundamental/src/advisory/service/advisory.rs` (AdvisoryService) for database access and aggregation.
- Use `common/src/db/query.rs` for shared query builder helpers (filtering, pagination, sorting).
- All endpoint handlers must return `Result<T, AppError>` with `.context()` wrapping, per the error handling pattern in `common/src/error.rs`.
- The aggregation queries should join `entity/src/advisory.rs` (Advisory entity, which has severity) with `entity/src/sbom_advisory.rs` (SBOM-Advisory join table) to compute remediation statistics across SBOMs.
- NFR: Summary endpoint response time must be p95 < 500ms. Consider using efficient SQL aggregation (GROUP BY) rather than in-memory processing.
- NFR: Must handle up to 10,000 tracked vulnerabilities without performance degradation.
- Register routes in `endpoints/mod.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Mount the remediation routes in `server/src/main.rs` following the existing module mounting pattern.

## Reuse Candidates
- `common/src/db/query.rs::query` — Shared query builder helpers for filtering, pagination, and sorting; reuse for any list/aggregation queries
- `common/src/model/paginated.rs::PaginatedResults` — Standard paginated response wrapper; use if the summary endpoint returns paginated data
- `common/src/error.rs::AppError` — Standard error type; all handlers must use this
- `modules/fundamental/src/advisory/model/summary.rs::AdvisorySummary` — Reference model for struct definition patterns (includes severity field)
- `modules/fundamental/src/advisory/service/advisory.rs::AdvisoryService` — Reference service for aggregation query patterns
- `entity/src/sbom_advisory.rs` — SBOM-Advisory join table entity; critical for computing remediation aggregations across SBOMs

## Acceptance Criteria
- [ ] The remediation module exists at modules/remediation/ with model/, service/, and endpoints/ sub-directories
- [ ] GET /api/v2/remediation/summary returns a JSON response with aggregated counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved)
- [ ] The summary response includes total counts for open, in_progress, and resolved vulnerabilities
- [ ] The summary response includes a trend array with daily resolved counts for the past 30 days
- [ ] The endpoint returns status 200 with valid aggregated data when vulnerabilities exist
- [ ] The endpoint returns status 200 with zero counts when no vulnerabilities exist
- [ ] No new database tables are created — all aggregations use existing entity relationships
- [ ] The remediation routes are mounted in server/src/main.rs

## Test Requirements
- [ ] Integration test: GET /api/v2/remediation/summary returns 200 with correct aggregation structure
- [ ] Integration test: Summary endpoint returns zero counts when no advisory data exists
- [ ] Integration test: Summary endpoint correctly groups by severity and status when test data includes multiple severities and statuses
- [ ] Integration test: Summary endpoint includes 30-day trend data
- [ ] Follow the integration test pattern in `tests/api/advisory.rs` using `assert_eq!(resp.status(), StatusCode::OK)`

## Verification Commands
- `cargo test --test api remediation` — All remediation integration tests pass
- `cargo build` — Project compiles with the new remediation module
