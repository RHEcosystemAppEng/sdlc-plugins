# Task 5: Update advisory ingestion pipeline for direct enum writes

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing via foreign key. The pipeline currently maps advisory feed status strings to lookup table rows; it must now map them directly to enum values on the advisory insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove `advisory_status` table insert logic; map parsed status string to `AdvisoryStatusEnum` value and set it directly on the advisory `ActiveModel`
- `modules/ingestor/src/service/mod.rs` — remove any `advisory_status` entity imports or status lookup helper functions

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, replace the pattern of inserting into `advisory_status` and getting back an ID with direct enum assignment: parse the status string from the advisory feed, convert to `AdvisoryStatusEnum` variant, and set `advisory_model.status = Set(status_enum)`.
- Add a helper function or `impl From<&str> for AdvisoryStatusEnum` to map feed status strings to enum variants, handling case-insensitive matching and defaulting to `AdvisoryStatusEnum::New` for unrecognized values.
- Remove any imports of `entity::advisory_status` from the ingestor module.
- Reuse `entity/src/advisory.rs::AdvisoryStatusEnum` for the enum type.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for error propagation in ingestion functions. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` scope (Rust syntax signal).

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` value directly to `advisory.status`
- [ ] No references to `advisory_status` entity remain in the ingestor module
- [ ] Status string parsing handles all four enum values: New, Analyzing, Fixed, Rejected
- [ ] Unrecognized status strings default to `New` with a warning log
- [ ] `cargo check -p ingestor` compiles without errors

## Test Requirements
- [ ] Ingestion of an advisory with each status value (New, Analyzing, Fixed, Rejected) stores the correct enum value
- [ ] Ingestion of an advisory with an unrecognized status defaults to New
- [ ] Ingestion pipeline does not attempt to write to the dropped `advisory_status` table

## Verification Commands
- `cargo check -p ingestor` — ingestor crate compiles without errors
- `cargo test -p ingestor` — existing unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
