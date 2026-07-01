# Task 4 — Update advisory service and model to use enum column

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service layer and model structs to query the `status` enum column directly instead of joining through the `advisory_status` lookup table. This eliminates the join overhead that added ~40ms p95 latency to advisory list queries. Update `AdvisorySummary` and `AdvisoryDetails` model structs to source the status field from the new enum column.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from fetch, list, and search queries; filter on `advisory.status` enum column directly
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to derive status from the enum column instead of joined table
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to derive status from the enum column instead of joined table
- `modules/fundamental/src/advisory/model/mod.rs` — update any model re-exports or shared types related to status

## Implementation Notes
- The `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs` currently joins `advisory_status` on every query (fetch, list, search). Replace these joins with direct column access on `advisory.status`
- For status filtering, change from `advisory_status.name = ?` join-based filter to `advisory.status = ?::advisory_status_enum` direct enum comparison
- Follow the query builder pattern from `common/src/db/query.rs` for filtering and pagination — the shared helpers already support column-based filtering
- Return `PaginatedResults<AdvisorySummary>` using the pattern from `common/src/model/paginated.rs`
- Error handling: use `Result<T, AppError>` with `.context()` wrapping as established in `common/src/error.rs`
- The status field in response types should remain a string (per the feature requirement "No user-facing API changes — the response shape remains identical")

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering and pagination, already used by advisory queries
- `common/src/model/paginated.rs` — `PaginatedResults<T>` response wrapper
- `common/src/error.rs` — `AppError` enum for error handling pattern
- `modules/fundamental/src/sbom/service/sbom.rs` — reference implementation of service pattern without lookup table joins

## Acceptance Criteria
- [ ] All advisory queries (fetch, list, search) use direct `advisory.status` column instead of joining `advisory_status`
- [ ] Status filtering works with the new enum column
- [ ] `AdvisorySummary` and `AdvisoryDetails` structs correctly represent status from enum column
- [ ] Response shape remains unchanged — status is still returned as a string
- [ ] No references to `advisory_status` table remain in the advisory service or model modules

## Test Requirements
- [ ] Advisory list query returns correct status values from enum column
- [ ] Advisory status filter returns only matching advisories
- [ ] Advisory fetch by ID returns correct status from enum column

## Verification Commands
- `cargo check -p trustify-module-fundamental` — fundamental module compiles
- `cargo test -p trustify-module-fundamental -- advisory` — advisory-related tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

---
Description Digest: sha256-md:5b8c2fae7861385789cd1d6a503b5b99364c442d1e08f3d5e27da5dffb71aa85
Priority: High
Fix Versions: RHTPA 2.0.0
