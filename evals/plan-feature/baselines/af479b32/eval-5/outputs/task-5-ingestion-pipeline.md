# Task 5: Update advisory ingestion pipeline for direct enum writes

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently maps advisory status strings from the feed to lookup table rows; after this change, it maps them directly to `AdvisoryStatusEnum` variants and writes them inline when inserting or updating advisory rows.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace lookup table insert logic (inserting into `advisory_status` and obtaining an ID) with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants; handle unknown status values with an error rather than silently creating new lookup rows
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it references advisory status insertion or the lookup table

## Implementation Notes
- The current flow likely does: parse status string from feed -> find or insert into `advisory_status` table -> get the `id` -> set `advisory.status_id = id`. The new flow should be: parse status string from feed -> map to `AdvisoryStatusEnum` variant -> set `advisory.status = variant`.
- Use a `match` or `FromStr` implementation to map incoming status strings to enum variants. Handle the case where an unknown status string is received -- this should produce an explicit error rather than silently dropping data, since the enum type has a fixed set of values.
- The advisory ingestion module at `modules/ingestor/src/graph/advisory/mod.rs` handles parsing, storing, and correlating advisories. Focus changes on the store/insert logic.
- Per CONVENTIONS.md: all error handling uses `Result<T, AppError>` with `.context()` wrapping.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's error handling scope.
- Reference the SBOM ingestion pattern (`modules/ingestor/src/graph/sbom/mod.rs`) for how the project handles direct field writes during ingestion.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- existing ingestion module demonstrating the project's pattern for parsing, storing, and linking entities without lookup table intermediaries
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum definition from Task 3 that the ingestion pipeline will use for status mapping

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to the `status` column, not through a lookup table
- [ ] Status string mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Unknown status strings produce a clear error with context, not a silent failure
- [ ] No ingestion code references the `advisory_status` table or `status_id` column
- [ ] Ingestion of a new advisory with each valid status succeeds

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" writes the correct enum value
- [ ] Verify ingestion of an advisory with status "Fixed" writes the correct enum value
- [ ] Verify ingestion of an advisory with an unknown status (e.g., "Unknown") produces an error
- [ ] Verify existing advisory data is not corrupted by re-ingestion after the schema change

## Verification Commands
- `cargo check -p ingestor` -- ingestor module compiles without errors
- `cargo test -p ingestor -- advisory` -- advisory ingestion tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
