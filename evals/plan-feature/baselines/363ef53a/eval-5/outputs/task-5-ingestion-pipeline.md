## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory` table instead of inserting into the `advisory_status` lookup table first. The pipeline must map status strings from the advisory feed to `AdvisoryStatusEnum` values and set them directly on the advisory record during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- Update advisory ingestion logic to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of creating `advisory_status` lookup entries and FK references
- `modules/ingestor/src/service/mod.rs` -- Update `IngestorService` if it orchestrates `advisory_status` table writes or coordinates the lookup-then-insert pattern

## Implementation Notes
- Replace the lookup table insert + FK assignment pattern with direct enum value assignment on the advisory `ActiveModel`
- Map incoming status strings to `AdvisoryStatusEnum` variants:
  - "New" -> `AdvisoryStatusEnum::New`
  - "Analyzing" -> `AdvisoryStatusEnum::Analyzing`
  - "Fixed" -> `AdvisoryStatusEnum::Fixed`
  - "Rejected" -> `AdvisoryStatusEnum::Rejected`
- Handle unmapped status strings gracefully -- log a warning and default to `AdvisoryStatusEnum::New`
- Import the `AdvisoryStatusEnum` type from the entity crate (`entity::advisory::AdvisoryStatusEnum`)
- See existing SBOM ingestion `modules/ingestor/src/graph/sbom/mod.rs` for the established ingestion pattern in this project

Per CONVENTIONS.md §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's handler (.rs) file scope.

Per CONVENTIONS.md §Framework: use SeaORM `ActiveModel` for database writes.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust (.rs) file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion pattern as reference for advisory ingestion updates, demonstrates the ActiveModel write pattern
- `entity/src/advisory.rs` -- `AdvisoryStatusEnum` definition for type imports and variant mapping

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` values directly to the `advisory.status` column
- [ ] No writes to the (now-dropped) `advisory_status` table remain in the ingestion pipeline
- [ ] Unmapped status strings are handled gracefully with a default value and warning log
- [ ] Pipeline correctly maps all four status values (New, Analyzing, Fixed, Rejected)

## Test Requirements
- [ ] `cargo check -p ingestor` passes with the updated ingestion code
- [ ] Ingestion of an advisory with status "Fixed" writes `AdvisoryStatusEnum::Fixed` directly
- [ ] Ingestion of an advisory with an unknown status defaults to `New` with a logged warning

## Verification Commands
- `cargo check -p ingestor` -- Verify ingestor module compiles cleanly

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
