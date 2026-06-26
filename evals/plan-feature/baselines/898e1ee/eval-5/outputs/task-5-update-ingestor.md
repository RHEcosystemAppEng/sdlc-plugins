## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it by foreign key. The ingestor currently parses status strings from advisory feeds, looks up or inserts the status in the lookup table, and sets `status_id` on the advisory row. After this change, it maps status strings directly to `AdvisoryStatusEnum` variants and sets the `status` field on the advisory ActiveModel.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- remove lookup table interaction; map parsed status strings to `AdvisoryStatusEnum` variants; set `status` field directly on the advisory ActiveModel instead of `status_id`
- `modules/ingestor/src/service/mod.rs` -- remove any advisory_status entity imports or lookup table references from IngestorService if present

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, the current flow likely: (1) parses the status string from the feed, (2) queries or inserts into `advisory_status` to get the `id`, (3) sets `advisory.status_id = id`. Replace this with: (1) parse the status string, (2) convert to `AdvisoryStatusEnum` variant using a match or `FromStr` implementation, (3) set `advisory.status = ActiveValue::Set(variant)`.
- Import `AdvisoryStatusEnum` from `entity::advisory` (the enum defined in Task 3).
- Handle invalid status strings gracefully: if a feed contains an unrecognized status value, return an error with context using `AppError` and `.context()` from `common/src/error.rs`.
- Remove any `use entity::advisory_status` imports.
- Per CONVENTIONS.md §Error Handling (inferred from Key Conventions): use `.context()` wrapping when mapping status strings to enum variants. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `common/src/error.rs::AppError` -- use for error handling when an unrecognized status string is encountered during ingestion

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to `advisory.status` column
- [ ] No references to `advisory_status` entity or lookup table remain in the ingestor module
- [ ] Unrecognized status strings produce a descriptive error
- [ ] The `ingestor` crate compiles without errors

## Test Requirements
- [ ] Ingesting an advisory with a valid status (New, Analyzing, Fixed, Rejected) succeeds and stores the correct enum value
- [ ] Ingesting an advisory with an unrecognized status string returns an appropriate error
- [ ] Verify no `advisory_status` entity imports exist in the ingestor module

## Verification Commands
- `cargo check -p trustify-ingestor` -- ingestor crate compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:7d2823240ccf6309291a695efe2c5acc8c5ec7e79316e7f043f3f4e640dfe775
