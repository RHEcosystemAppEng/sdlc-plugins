## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently inserts a row into `advisory_status` first, then uses the generated ID as the `status_id` when creating advisory records. After this change, the pipeline maps the status string from the advisory feed directly to an `AdvisoryStatusEnum` value and writes it to the `status` column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert with direct enum value assignment; remove any code that inserts into or queries the `advisory_status` table
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it coordinates status table operations

## Implementation Notes
- In `advisory/mod.rs`, locate the code that inserts into the `advisory_status` table or looks up an existing status row by name. Replace this with a direct mapping: parse the status string from the feed to `AdvisoryStatusEnum` (e.g., `"New"` -> `AdvisoryStatusEnum::New`)
- When constructing the `advisory` `ActiveModel` for insertion, set the `status` field to the mapped enum value instead of setting `status_id` to a foreign key
- Remove any imports of the `advisory_status` entity from this module
- Handle invalid status strings gracefully — if the feed contains a status not in the enum, return an error with context rather than silently failing
- Follow the error handling pattern: use `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's error handling scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion module patterns (parse, store, link) without lookup table indirection

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `advisory.status` column
- [ ] No code in the ingestion pipeline references the `advisory_status` table
- [ ] Invalid status strings from the feed produce clear error messages
- [ ] Ingestion of new advisories succeeds end-to-end with the enum column

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" writes the correct enum value
- [ ] Verify ingestion of advisories with all four status values (New, Analyzing, Fixed, Rejected) succeeds
- [ ] Verify ingestion with an invalid status string returns an appropriate error
- [ ] Verify no references to `advisory_status` entity remain in the ingestor module

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status
