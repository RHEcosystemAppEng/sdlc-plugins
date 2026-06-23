## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory service and model layer to use the new `status` enum column directly instead of joining the `advisory_status` lookup table. This eliminates the join that was adding ~40ms to advisory list endpoint p95 latency. The `AdvisoryService` query methods must be updated to filter and select the enum column, and the model structs must be updated to populate status from the enum field.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove all `advisory_status` table joins from query methods (fetch, list, search); replace with direct `status` enum column access; update status filtering to use `WHERE status = <enum_value>` instead of join-based filtering
- `modules/fundamental/src/advisory/model/summary.rs` — update `AdvisorySummary` struct to populate `status` field from the enum column instead of the joined lookup table value
- `modules/fundamental/src/advisory/model/details.rs` — update `AdvisoryDetails` struct to populate `status` field from the enum column
- `modules/fundamental/src/advisory/model/mod.rs` — update model module exports if any type aliases or re-exports reference the old status type

## Implementation Notes
- In `modules/fundamental/src/advisory/service/advisory.rs`, the existing list/fetch queries likely use something like `.find_also_related(advisory_status::Entity)` or a manual join. Replace these with direct column access: `advisory::Column::Status`.
- For status filtering, the query builder in `common/src/db/query.rs` provides shared filtering helpers. Update any status filter to compare against `AdvisoryStatusEnum` variants instead of joining and filtering by `advisory_status.name`.
- In `modules/fundamental/src/advisory/model/summary.rs`, the `From` impl or constructor that maps database results to `AdvisorySummary` currently extracts status from the joined result. Update it to read `model.status` directly as a string (the enum's string representation).
- Follow the error handling pattern using `Result<T, AppError>` with `.context()` as used throughout the service layer.
- Per CONVENTIONS.md §Key Conventions: use shared query builder helpers from `common/src/db/query.rs` for filtering. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's Rust service file scope.

## Acceptance Criteria
- [ ] All `advisory_status` table joins are removed from `AdvisoryService` methods
- [ ] Status filtering uses the enum column directly (no join)
- [ ] `AdvisorySummary` and `AdvisoryDetails` populate status from the enum column
- [ ] No remaining imports or references to `advisory_status` entity in the advisory service or model modules
- [ ] Service layer compiles with `cargo check -p fundamental`

## Test Requirements
- [ ] Advisory list query returns correct status values from enum column
- [ ] Status filtering returns only advisories matching the requested status
- [ ] Advisory detail query returns correct status from enum column
- [ ] No regression in response shape — status is still returned as a string

## Verification Commands
- `cargo check -p fundamental` — fundamental module compiles

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for enum status

[sdlc-workflow] Description digest: sha256-md:03054e827357a7340b85c165702ed4ea84b3fb0b242b16a36bf4b67c984c4606
