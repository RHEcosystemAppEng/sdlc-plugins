# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting rows into the `advisory_status` lookup table and referencing them via foreign key. The ingestion pipeline currently parses advisory feeds, looks up or creates a status row in the lookup table, and sets `status_id` on the advisory. After this change, the pipeline maps the status string from the feed directly to an `AdvisoryStatusEnum` value and sets it on the advisory entity.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace lookup table insert/query logic with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants; remove any imports of the `advisory_status` entity
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references `advisory_status` for status resolution during ingestion

## Implementation Notes
- Replace the pattern of `advisory_status::Entity::find().filter(advisory_status::Column::Name.eq(status_str))` followed by `advisory_model.status_id = status.id` with a direct enum assignment: `advisory_model.status = AdvisoryStatusEnum::from_str(status_str)` or a match expression
- Handle the case where the incoming status string does not match any enum variant — return an error with context rather than silently ignoring
- Remove any `advisory_status::ActiveModel::insert()` calls that were used to create lookup table rows during ingestion
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for enum conversion errors during ingestion.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.
- Per CONVENTIONS.md §Module pattern: maintain the existing module structure in the ingestor crate.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's module structure scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — Reference for ingestion patterns that write entity fields directly without lookup tables
- `entity/src/advisory.rs::AdvisoryStatusEnum` — The enum type defined in Task 3 that must be used for status assignment

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to the `status` column
- [ ] No references to `advisory_status` entity remain in the ingestor crate
- [ ] Ingestion correctly maps all four status values (New, Analyzing, Fixed, Rejected) to enum variants
- [ ] Invalid status strings during ingestion produce a clear error with context

## Test Requirements
- [ ] Verify ingestion of an advisory with each valid status value produces the correct enum value in the database
- [ ] Verify ingestion with an invalid status string returns an appropriate error
- [ ] Verify bulk ingestion of advisories with mixed statuses succeeds

## Verification Commands
- `cargo check -p ingestor` — ingestor crate compiles without errors
- `cargo test -p ingestor` — unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
