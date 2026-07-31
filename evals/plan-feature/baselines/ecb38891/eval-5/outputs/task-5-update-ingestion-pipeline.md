## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory` table instead of inserting into the `advisory_status` lookup table first and then referencing the FK. The pipeline currently parses advisory status from the feed, looks up or creates a row in `advisory_status`, and stores the FK ID. After this change, the pipeline maps the status string from the feed directly to an `AdvisoryStatusEnum` variant and inserts it into the `status` enum column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace the lookup-table insert pattern with direct enum value mapping; remove any references to the `advisory_status` entity or table; map feed status strings to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it references advisory status through the lookup table

## Implementation Notes
- The feed status string must be mapped to an `AdvisoryStatusEnum` variant. Implement a conversion function or use `FromStr`/`TryFrom` on the enum. Handle unrecognized status values by logging a warning and defaulting to `AdvisoryStatusEnum::New` (or returning an error, depending on the existing error handling pattern in the ingestion pipeline)
- Remove any `advisory_status::ActiveModel` usage or `advisory_status::Entity::find()` lookups
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for the insert/update structure
- The `advisory::ActiveModel` should now set `status: Set(AdvisoryStatusEnum::from_str(status_str))` instead of `status_id: Set(lookup_id)`
- Error handling: use the existing `IngestorService` error pattern for mapping parse failures

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- reference for ingestion graph pattern (parse, store, link)
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum type defined in Task 3

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `status` column
- [ ] No references to `advisory_status` entity or table remain in the ingestor module
- [ ] Ingestion handles all four valid status values: New, Analyzing, Fixed, Rejected
- [ ] Ingestion handles unrecognized status values gracefully (log warning or error)
- [ ] `cargo check -p ingestor` compiles without errors

## Test Requirements
- [ ] Verify ingestion of an advisory with status "Fixed" stores `AdvisoryStatusEnum::Fixed` in the `status` column
- [ ] Verify ingestion of an advisory with status "New" stores `AdvisoryStatusEnum::New`
- [ ] Verify ingestion of an advisory with an unrecognized status handles the error gracefully

## Verification Commands
- `cargo check -p ingestor` -- compiles without errors
- `cargo test -p ingestor` -- all existing tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions (ingestion uses the updated entity types)
