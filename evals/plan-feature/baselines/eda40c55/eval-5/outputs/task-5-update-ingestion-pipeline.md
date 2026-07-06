## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write advisory status as an `advisory_status_enum` value directly on the advisory row, instead of first inserting into the `advisory_status` lookup table and then referencing the inserted row via foreign key. The pipeline must map incoming status strings from advisory feeds to the corresponding `AdvisoryStatusEnum` variant and set the `status` column directly during advisory insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove lookup table insert/query for status; map incoming status string to `AdvisoryStatusEnum` variant; set `status` field directly on the advisory `ActiveModel`
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references the advisory_status table or its entity

## Implementation Notes
- In `advisory/mod.rs`, replace the pattern of `advisory_status::ActiveModel { name: Set(status_string) }.insert(db)` followed by `advisory::ActiveModel { status_id: Set(inserted_status.id) }` with a direct `advisory::ActiveModel { status: Set(AdvisoryStatusEnum::from_str(status_string)) }`.
- Implement a conversion from incoming status strings to `AdvisoryStatusEnum`. Use a `match` expression or `FromStr` impl that maps `"New" | "new"` to `AdvisoryStatusEnum::New`, etc. Handle unknown status values by returning an error with `.context("Unknown advisory status")`.
- Remove any `use entity::advisory_status` imports from the ingestion module.
- Per CONVENTIONS.md §Error handling: all error paths in the ingestion pipeline must return `Result<T, AppError>` with `.context()` wrapping, including the status string-to-enum conversion.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic to modify in place
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion graph patterns that write directly to entity columns without lookup tables

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` value directly to `advisory.status` column
- [ ] No references to `advisory_status` table or entity remain in the ingestion pipeline
- [ ] Ingestion correctly maps all four status strings (New, Analyzing, Fixed, Rejected) to enum variants
- [ ] Unknown status values produce a clear error message, not a panic
- [ ] Ingestion performance is not degraded (one fewer table insert per advisory)

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" results in `status = New` enum value on the advisory row
- [ ] Verify ingestion of each of the four valid status values succeeds
- [ ] Verify ingestion with an unknown status value returns an appropriate error
- [ ] Verify no insert operations target the `advisory_status` table

## Verification Commands
- `cargo build -p ingestor` — compiles without error
- `cargo test -p ingestor` — all ingestor tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
