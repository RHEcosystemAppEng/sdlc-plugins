## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory` table instead of first inserting into the `advisory_status` lookup table and then referencing via foreign key. The pipeline should map incoming status strings to `AdvisoryStatusEnum` values and set them directly on the advisory row during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace the pattern of inserting into `advisory_status` lookup table and setting `status_id` FK with direct `AdvisoryStatusEnum` value mapping and assignment on the advisory row
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it contains any references to the `advisory_status` lookup table or `status_id` column in advisory-related operations

## Implementation Notes
- In the advisory ingestion handler, replace the existing pattern:
  1. Insert status string into `advisory_status` table
  2. Get the inserted row's ID
  3. Set `status_id` on the advisory row
  With the new pattern:
  1. Map the incoming status string to an `AdvisoryStatusEnum` variant using a `match` or `FromStr` implementation
  2. Set `status` directly on the advisory `ActiveModel` before insertion
- Map incoming status strings to enum variants: `"New"` -> `AdvisoryStatusEnum::New`, `"Analyzing"` -> `AdvisoryStatusEnum::Analyzing`, `"Fixed"` -> `AdvisoryStatusEnum::Fixed`, `"Rejected"` -> `AdvisoryStatusEnum::Rejected`
- Handle unknown status values by returning an `AppError` with a descriptive message rather than silently ignoring them or panicking
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for status mapping errors and ingestion failures.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust source file scope.
- Per CONVENTIONS.md §Module pattern: maintain the established `graph/ + service/` module structure within the ingestor module.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module directory scope.
- Constraint §5.1: changes scoped to files listed in this task
- Constraint §5.4: reuse the `AdvisoryStatusEnum` type from the entity crate rather than defining a new enum

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum type defined in Task 3; use for mapping incoming status strings to typed values
- `modules/ingestor/src/graph/sbom/mod.rs` -- reference for SBOM ingestion patterns (parse, store, link) in the ingestor module
- `modules/ingestor/src/graph/advisory/mod.rs` -- existing advisory ingestion implementation to modify in-place

## Acceptance Criteria
- [ ] Advisory ingestion writes enum status values directly to the `advisory.status` column
- [ ] Status string-to-enum mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Unknown or invalid status values produce a clear error via `AppError`
- [ ] No references to `advisory_status` lookup table remain in the ingestor module
- [ ] No references to `status_id` column remain in the ingestor module
- [ ] `cargo build -p ingestor` compiles successfully

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" succeeds and writes the correct enum value
- [ ] Verify ingestion of an advisory with status "Analyzing" succeeds
- [ ] Verify ingestion of an advisory with status "Fixed" succeeds
- [ ] Verify ingestion of an advisory with status "Rejected" succeeds
- [ ] Verify ingestion with an unknown status value (e.g., "Invalid") returns an appropriate error
- [ ] Verify no insert operations target the `advisory_status` table

## Verification Commands
- `cargo build -p ingestor` -- compilation succeeds
- `cargo test -p ingestor` -- ingestor tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
