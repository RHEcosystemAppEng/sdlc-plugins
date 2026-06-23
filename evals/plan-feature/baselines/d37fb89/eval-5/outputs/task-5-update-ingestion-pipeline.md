## Summary
Update advisory ingestion pipeline to write enum status directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline currently parses the status string from the advisory feed, looks up or creates a row in `advisory_status`, and stores the resulting `status_id` on the advisory row. After this change, the pipeline maps the status string directly to the `AdvisoryStatusEnum` variant and inserts it as the `status` column value.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace advisory_status lookup table insert/lookup logic with direct `AdvisoryStatusEnum` mapping; remove any `advisory_status` entity imports; set `status` field on advisory `ActiveModel` to the mapped enum value instead of `status_id`
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it references advisory_status entity or passes status_id to advisory graph operations

## Implementation Notes
The ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` currently handles advisory status by either finding or creating a row in the `advisory_status` table and storing the resulting ID. Replace this with a simple string-to-enum mapping function: map the feed's status string (e.g., "New", "Analyzing", "Fixed", "Rejected") to the corresponding `AdvisoryStatusEnum` variant. If the feed contains an unrecognized status string, return an error using `AppError` with `.context()` rather than silently defaulting. Remove all imports of the `advisory_status` entity module.

Per CONVENTIONS.md: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `common/src/error.rs` -- `AppError` enum for error handling when encountering unrecognized status strings
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum type defined in Task 3 that this task maps feed values to

## Acceptance Criteria
- [ ] Ingestion pipeline maps advisory status strings directly to `AdvisoryStatusEnum` values
- [ ] Ingestion pipeline no longer references or inserts into the `advisory_status` lookup table
- [ ] Ingestion of an advisory with a valid status (New, Analyzing, Fixed, Rejected) succeeds and stores the correct enum value
- [ ] Ingestion of an advisory with an unrecognized status string returns an error
- [ ] No remaining references to `advisory_status` entity in the ingestor module

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" stores `AdvisoryStatusEnum::New` in the `status` column
- [ ] Verify ingestion of an advisory with status "Fixed" stores `AdvisoryStatusEnum::Fixed` in the `status` column
- [ ] Verify ingestion of an advisory with an unrecognized status string (e.g., "Unknown") returns an appropriate error
- [ ] Verify no queries or inserts target the `advisory_status` table

## Verification Commands
- `cargo build -p ingestor` -- ingestor module compiles successfully
- `cargo test -p ingestor` -- all existing ingestion tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:42bce8bca7eb26a3f3d31bf527a005a00a188aa8c226420f4b5706a9d1a01b0b
