# Task 1: Create remediation module with summary aggregation endpoint

## Repository
trustify-backend

## Target Branch
main

## Description
Create a new `remediation` module under `modules/fundamental/src/` that provides aggregated vulnerability remediation data. This task establishes the module structure (model, service, endpoints) and implements the summary aggregation endpoint that returns remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). Aggregations are computed from existing vulnerability and SBOM relationship data -- no new database tables are required. This is the foundational backend task for the remediation tracking dashboard (TC-9006).

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` -- remediation module root, re-exports model, service, and endpoints
- `modules/fundamental/src/remediation/model/mod.rs` -- model module root
- `modules/fundamental/src/remediation/model/summary.rs` -- `RemediationSummary` struct with severity x status counts
- `modules/fundamental/src/remediation/service/mod.rs` -- service module root
- `modules/fundamental/src/remediation/service/remediation.rs` -- `RemediationService` with `get_summary()` method that queries existing entity tables
- `modules/fundamental/src/remediation/endpoints/mod.rs` -- route registration for `/api/v2/remediation`
- `modules/fundamental/src/remediation/endpoints/summary.rs` -- `GET /api/v2/remediation/summary` handler
- `tests/api/remediation.rs` -- integration tests for the summary endpoint

## Files to Modify
- `modules/fundamental/src/lib.rs` -- add `pub mod remediation;` declaration
- `modules/fundamental/Cargo.toml` -- add any new dependencies if needed
- `server/src/main.rs` -- mount remediation routes alongside existing module routes
- `tests/Cargo.toml` -- add remediation test module if needed

## API Changes
- `GET /api/v2/remediation/summary` -- NEW: returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). Response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }], total: { open: number, in_progress: number, resolved: number } }`

## Implementation Notes
- Follow the existing module pattern used by `sbom`, `advisory`, and `package` modules: each has `model/`, `service/`, and `endpoints/` subdirectories. See `modules/fundamental/src/sbom/` for the canonical example.
  - Applies: task creates `modules/fundamental/src/remediation/mod.rs` matching the module directory pattern.
- Use `Result<T, AppError>` with `.context()` wrapping for all error handling, consistent with the pattern in `modules/fundamental/src/sbom/service/sbom.rs`.
  - Applies: task creates `modules/fundamental/src/remediation/service/remediation.rs` matching the Rust service file scope.
- The summary endpoint does not return a paginated list, so do not use `PaginatedResults<T>` -- use a custom response struct. However, reuse the query builder helpers from `common/src/db/query.rs` for any filtering or query construction.
- Compute aggregations from existing entity tables (`advisory`, `sbom_advisory`, and related joins). Reference `entity/src/advisory.rs` and `entity/src/sbom_advisory.rs` for the entity definitions.
- The `AdvisorySummary` struct in `modules/fundamental/src/advisory/model/summary.rs` includes a severity field -- use this as the severity source for aggregation.
- NFR: summary endpoint response time must be p95 < 500ms. Consider query optimization (indexed joins, avoiding N+1 queries).
- Register routes in `endpoints/mod.rs` using the same Axum router pattern as `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Integration tests should follow the pattern in `tests/api/sbom.rs` and `tests/api/advisory.rs` -- use `assert_eq!(resp.status(), StatusCode::OK)` pattern against a real PostgreSQL test database.

## Reuse Candidates
- `common/src/db/query.rs` -- shared query builder helpers for filtering, pagination, and sorting; reuse for constructing aggregation queries
- `common/src/error.rs` -- `AppError` enum implementing `IntoResponse`; use for all error returns
- `common/src/model/paginated.rs` -- `PaginatedResults<T>` wrapper (reference for response structure patterns, though this endpoint uses a custom response)
- `modules/fundamental/src/advisory/model/summary.rs` -- `AdvisorySummary` struct with severity field; reference for how severity is represented
- `entity/src/advisory.rs` -- Advisory entity definition; needed for aggregation queries
- `entity/src/sbom_advisory.rs` -- SBOM-Advisory join table entity; needed for correlating vulnerabilities with SBOMs

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns HTTP 200 with aggregated counts grouped by severity (Critical, High, Medium, Low) and status (Open, In Progress, Resolved)
- [ ] Response includes a `total` field with overall open, in_progress, and resolved counts
- [ ] Aggregations are computed from existing entity tables without creating new database tables
- [ ] The remediation module follows the `model/ + service/ + endpoints/` structure consistent with sibling modules
- [ ] Routes are registered in `server/src/main.rs`
- [ ] Integration tests pass against a PostgreSQL test database

## Test Requirements
- [ ] Integration test: `GET /api/v2/remediation/summary` returns 200 with expected response shape
- [ ] Integration test: summary counts correctly aggregate across multiple advisories with different severities and statuses
- [ ] Integration test: summary returns zero counts when no advisory data exists
- [ ] Integration test: response time is within acceptable bounds (verify no N+1 query patterns)

## Verification Commands
- `cargo test --test api remediation` -- expected: all remediation integration tests pass

## Documentation Updates
- `README.md` -- add mention of the remediation module in the backend module listing
