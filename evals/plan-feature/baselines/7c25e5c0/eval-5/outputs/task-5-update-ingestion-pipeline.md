## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting rows into the `advisory_status` lookup table and storing a foreign key. The pipeline must map incoming status strings from advisory feeds to the corresponding `AdvisoryStatusEnum` variant.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — update the advisory ingestion logic to set `advisory::ActiveModel { status: Set(AdvisoryStatusEnum::from_str(status_string)) }` instead of creating an `advisory_status` row and storing `status_id`; remove any `advisory_status` entity usage
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` entity for status resolution; ensure status mapping uses the enum type

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, find where the pipeline currently inserts into or looks up the `advisory_status` table. Replace with direct enum value assignment
- Use `AdvisoryStatusEnum::try_from(status_str)` or a match statement to map feed status strings to enum variants. Handle unknown status values by defaulting to `AdvisoryStatusEnum::New` or returning an error — follow the existing error handling pattern in `modules/ingestor/src/graph/sbom/mod.rs`
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the ingestion graph pattern: parse → validate → store
- Per CONVENTIONS.md §Error handling: all ingestion methods return `Result<T, AppError>` with `.context()` for error propagation.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Module pattern: ingestion modules follow the graph/ + service/ structure.
  Applies: task modifies `modules/ingestor/src/service/mod.rs` matching the convention's module pattern scope.

## Acceptance Criteria
- [ ] Advisory ingestion writes `advisory_status_enum` values directly to the `status` column
- [ ] No references to `advisory_status` entity or table remain in the ingestor module
- [ ] Status string mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Unknown status values are handled gracefully (error or default)
- [ ] Ingestion pipeline processes advisory feeds end-to-end with the new enum column

## Test Requirements
- [ ] Ingestion of an advisory with status "New" correctly sets the enum column
- [ ] Ingestion of an advisory with status "Fixed" correctly sets the enum column
- [ ] Ingestion of an advisory with an unknown status value is handled without crashing
- [ ] Round-trip test: ingest an advisory, fetch it via the API, verify status matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update entity definitions (ingestion uses updated entity types)
