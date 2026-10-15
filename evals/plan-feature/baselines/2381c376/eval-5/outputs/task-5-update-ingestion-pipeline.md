## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The ingestion pipeline currently maps status strings from advisory feeds to rows in the lookup table; after this change, it maps them directly to enum values and writes them to the `status` column on the `advisory` row. This eliminates the ingestion dependency on the lookup table, which is a prerequisite for dropping it in Task 6.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- Update advisory ingestion to map feed status strings to `AdvisoryStatusEnum` values and write directly to the `status` column instead of the lookup table
- `modules/ingestor/src/service/mod.rs` -- Update `IngestorService` if it references the advisory_status entity for status resolution

## Implementation Notes
- Replace the lookup pattern: currently the pipeline does `advisory_status::Entity::find().filter(advisory_status::Column::Name.eq(status_str))` to get the status ID, then sets `status_id` on the advisory. Replace this with a direct `AdvisoryStatusEnum::from_str(status_str)` (or match statement) that maps the feed string to the enum variant
- Handle unknown status values gracefully: if the feed contains a status string not matching any enum variant, log a warning and either skip the advisory or use a default value (document the decision)
- Remove any `use entity::advisory_status` imports from the ingestion module
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` for error handling in the updated ingestion logic.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust file scope.
- See `modules/ingestor/src/graph/sbom/mod.rs` for a reference ingestion implementation pattern

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- reference ingestion implementation showing the parse-store-link pattern used in this project
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum type defined in Task 3 that the ingestion pipeline must use

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `advisory.status` column
- [ ] Advisory ingestion no longer references or writes to the `advisory_status` lookup table
- [ ] All four status values (New, Analyzing, Fixed, Rejected) from advisory feeds are correctly mapped to enum variants
- [ ] Unknown status values in feeds are handled gracefully (logged, not silently dropped)
- [ ] No references to `advisory_status` entity remain in the ingestor module

## Test Requirements
- [ ] Test ingestion of an advisory with each of the four status values and verify the `status` column is set correctly
- [ ] Test ingestion with an unknown/invalid status value and verify graceful error handling
- [ ] Verify that no rows are written to the `advisory_status` table during ingestion

## Verification Commands
- `cargo test -p ingestor -- advisory` -- ingestor advisory tests pass
- `cargo check -p ingestor` -- ingestor module compiles without advisory_status references

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for new schema
