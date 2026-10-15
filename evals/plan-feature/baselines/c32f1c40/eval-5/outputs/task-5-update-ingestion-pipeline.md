## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The ingestion pipeline currently maps incoming advisory status strings to lookup table rows; it must now map them directly to `AdvisoryStatusEnum` values.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- update advisory ingestion logic to map status strings from the feed to `AdvisoryStatusEnum` enum values and insert them directly into the `advisory.status` column; remove any code that inserts into or references the `advisory_status` table
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it references the `advisory_status` entity or table in any initialization, validation, or helper methods

## Implementation Notes
- Per CONVENTIONS.md §Error handling: all ingestion functions must return `Result<T, AppError>` with `.context()` wrapping. Maintain this pattern when updating the status mapping logic.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust handler scope.
- Per CONVENTIONS.md §Module pattern: keep ingestion logic within the `graph/advisory/` module structure. Do not mix ingestion logic with service-layer concerns.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's module directory pattern scope.
- Map incoming status strings to `AdvisoryStatusEnum` variants: "New" -> `AdvisoryStatusEnum::New`, "Analyzing" -> `AdvisoryStatusEnum::Analyzing`, "Fixed" -> `AdvisoryStatusEnum::Fixed`, "Rejected" -> `AdvisoryStatusEnum::Rejected`
- Handle unknown status strings with an error rather than silently ignoring them -- use `.context("Unknown advisory status")` pattern
- Remove any `use` statements referencing the `advisory_status` entity
- The `AdvisoryStatusEnum` type should be imported from the entity crate (`entity::advisory::AdvisoryStatusEnum`)

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion module as a reference for the ingestion pattern (parse, store, link)
- `entity/src/advisory.rs` -- `AdvisoryStatusEnum` definition for the enum type to use during ingestion

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status` column
- [ ] No code in the ingestion pipeline references the `advisory_status` table or entity
- [ ] Ingestion correctly maps all four status strings (New, Analyzing, Fixed, Rejected) to enum values
- [ ] Unknown status strings produce a clear error rather than being silently dropped
- [ ] `cargo check -p ingestor` compiles without errors

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" writes the correct enum value
- [ ] Verify ingestion of an advisory with status "Fixed" writes the correct enum value
- [ ] Verify ingestion with an unknown status string produces an appropriate error
- [ ] Verify end-to-end: ingest an advisory, then fetch it via the API and confirm the status is correct

## Verification Commands
- `cargo check -p ingestor` -- ingestor module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
