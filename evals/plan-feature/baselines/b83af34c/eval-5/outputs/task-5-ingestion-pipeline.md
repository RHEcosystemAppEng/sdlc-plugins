## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing via foreign key. The pipeline should map incoming status strings to `AdvisoryStatus` enum values and set them directly on the advisory row during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace lookup table insert + FK reference with direct enum value assignment on the advisory entity
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references advisory status through the lookup table

## Implementation Notes
The advisory ingestion logic in `modules/ingestor/src/graph/advisory/mod.rs` currently writes status by:
1. Looking up or inserting the status string in the `advisory_status` table
2. Setting `status_id` on the advisory row to reference the lookup table row

Replace this with:
1. Parse the incoming status string to an `AdvisoryStatus` enum value
2. Set `status` directly on the advisory `ActiveModel`

Use the `AdvisoryStatus` enum from the entity crate (`entity::advisory::AdvisoryStatus`). Handle unrecognized status strings with an error using `.context()` from the `AppError` pattern in `common/src/error.rs`.

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` for status parsing failures during ingestion. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Acceptance Criteria
- [ ] Ingestion pipeline maps status strings to `AdvisoryStatus` enum values
- [ ] Ingestion writes enum status directly to `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestion module
- [ ] Unrecognized status strings produce a clear error via `AppError`
- [ ] All four valid status values (New, Analyzing, Fixed, Rejected) are handled correctly

## Test Requirements
- [ ] Test ingestion of an advisory with each valid status value
- [ ] Test ingestion with an unrecognized status string produces an appropriate error
- [ ] Verify ingested advisories have the correct enum status in the database

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
