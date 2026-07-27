## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly when inserting advisory rows, instead of first writing to the `advisory_status` lookup table and then referencing the row via foreign key. The pipeline currently maps the status string from the advisory feed to a lookup table row; after this change, it maps the status string directly to an `AdvisoryStatusEnum` variant and sets it on the advisory insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert + FK reference with direct enum value assignment on the advisory row; remove any `advisory_status` table interactions
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references the `advisory_status` entity or performs lookup table operations

## Implementation Notes
- The current ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` likely: (1) parses the status string from the feed, (2) finds or creates a row in `advisory_status`, (3) uses the row's ID as `status_id` on the advisory insert. Replace this with: (1) parse the status string, (2) map it to an `AdvisoryStatusEnum` variant (e.g., `"New" -> AdvisoryStatusEnum::New`), (3) set the `status` field directly on the advisory `ActiveModel`.
- Add a mapping function or match expression to convert feed status strings to `AdvisoryStatusEnum` variants. Handle unknown status values with an error rather than silently defaulting.
- Import the `AdvisoryStatusEnum` from `entity::advisory::AdvisoryStatusEnum`.
- Remove any `use entity::advisory_status` imports.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/advisory/mod.rs` for error handling and transaction management.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic; the status mapping replaces the lookup table interaction within the same function
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3; use its variants directly

## Acceptance Criteria
- [ ] Advisory ingestion writes the `advisory_status_enum` value directly on the advisory row
- [ ] No interactions with the `advisory_status` lookup table remain in the ingestion pipeline
- [ ] Status string from the advisory feed is correctly mapped to enum variants
- [ ] Unknown status values produce a clear error rather than a silent default
- [ ] Existing advisory ingestion tests pass (or are updated to reflect the new schema)

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" produces the correct enum value
- [ ] Verify ingestion of an advisory with status "Fixed" produces the correct enum value
- [ ] Verify ingestion of an advisory with an unknown status value produces an error
- [ ] Verify end-to-end ingestion: ingest an advisory feed and verify the advisory row has the correct enum status

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles without errors
- `grep -r "advisory_status\|status_id" modules/ingestor/` — no remaining references to old schema

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
