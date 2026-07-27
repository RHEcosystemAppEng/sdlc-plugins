# Task 2: Add remediation summary endpoint

**Epic:** TC-9006: trustify-backend

## Repository
trustify-backend

## Target Branch
TC-9006

## Description
Create a new `remediation` module in the fundamental crate following the established module pattern (model/ + service/ + endpoints/). Implement the `GET /api/v2/remediation/summary` endpoint that returns aggregated vulnerability remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). Aggregations must be computed from existing vulnerability and SBOM relationship data without creating new database tables.

## Files to Create
- `modules/fundamental/src/remediation/mod.rs` — remediation module root
- `modules/fundamental/src/remediation/model/mod.rs` — model sub-module root
- `modules/fundamental/src/remediation/model/summary.rs` — RemediationSummary struct with severity-by-status counts
- `modules/fundamental/src/remediation/service/mod.rs` — RemediationService with aggregation query logic
- `modules/fundamental/src/remediation/endpoints/mod.rs` — route registration for /api/v2/remediation
- `modules/fundamental/src/remediation/endpoints/summary.rs` — GET /api/v2/remediation/summary handler

## Files to Modify
- `modules/fundamental/src/lib.rs` — add `pub mod remediation;` to expose the new module
- `server/src/main.rs` — mount remediation routes alongside existing module routes

## API Changes
- `GET /api/v2/remediation/summary` — NEW: returns aggregated remediation counts grouped by severity (Critical/High/Medium/Low) and status (Open/In Progress/Resolved). Response shape: `{ items: [{ severity: string, open: number, in_progress: number, resolved: number }] }`

## Implementation Notes
- Follow the established module pattern from existing modules (e.g., `modules/fundamental/src/sbom/` and `modules/fundamental/src/advisory/`) which use the `model/ + service/ + endpoints/` structure.
- All handler functions must return `Result<T, AppError>` with `.context()` wrapping for error propagation, consistent with the pattern in `common/src/error.rs`.
- Use SeaORM query builders to compute aggregations via `GROUP BY` on severity and status columns from the existing advisory and sbom_advisory entities.
- No new database tables are permitted per the non-functional requirements — all data must be derived from existing entities (`entity/src/advisory.rs`, `entity/src/sbom_advisory.rs`).
- The endpoint must achieve p95 < 500ms response time. Consider using SeaORM's `select_only()` with `column_as()` for efficient aggregation queries rather than loading full entities.
- Register routes in `endpoints/mod.rs` following the pattern in `modules/fundamental/src/sbom/endpoints/mod.rs`.
- Mount the remediation module routes in `server/src/main.rs` following the pattern used for sbom and advisory modules.

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, and sorting; reuse for any query parameter handling
- `common/src/model/paginated.rs` — PaginatedResults<T> response wrapper; use if the summary endpoint supports pagination
- `common/src/error.rs` — AppError enum implementing IntoResponse; use for all error handling
- `modules/fundamental/src/advisory/model/summary.rs` — AdvisorySummary struct includes severity field; reference for severity value patterns
- `modules/fundamental/src/advisory/service/advisory.rs` — AdvisoryService query patterns; reference for building aggregation queries

## Acceptance Criteria
- [ ] `GET /api/v2/remediation/summary` returns aggregated counts grouped by severity and status
- [ ] Response includes all four severity levels (Critical, High, Medium, Low) and three status values (Open, In Progress, Resolved)
- [ ] Aggregations are computed from existing entity data without new database tables
- [ ] Endpoint response time meets p95 < 500ms requirement
- [ ] Error cases return appropriate AppError responses

## Test Requirements
- [ ] Integration test verifying the summary endpoint returns correct aggregated counts for a known dataset
- [ ] Integration test verifying the response shape matches the expected structure
- [ ] Integration test verifying empty database returns zero counts
- [ ] Integration test verifying p95 response time is under 500ms with representative data volume

## Verification Commands
- `cargo test --test api remediation` — run remediation endpoint tests
- `cargo clippy --all-targets` — verify no lint warnings in new code

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9006 from main
