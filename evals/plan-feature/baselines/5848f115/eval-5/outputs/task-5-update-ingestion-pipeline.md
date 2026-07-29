## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline should map the status string from the advisory feed to an `AdvisoryStatusEnum` value and set it directly on the advisory row during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace the lookup-table-based status assignment (currently inserts into `advisory_status` table and sets `status_id` on the advisory) with direct enum value assignment; map the incoming status string to `AdvisoryStatusEnum` and set the `status` field on the `ActiveModel`
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it contains status-related logic that references the lookup table

## Implementation Notes
- The ingestion flow currently: (1) receives a status string from the feed, (2) looks up or inserts the status in the `advisory_status` table to get an ID, (3) sets `status_id` on the advisory `ActiveModel`. The new flow should: (1) receive the status string, (2) parse it into an `AdvisoryStatusEnum` variant, (3) set `status` on the advisory `ActiveModel`.
- Use a `FromStr` or `TryFrom<String>` implementation on `AdvisoryStatusEnum` for the string-to-enum conversion. Handle unknown status values with an appropriate error (return `AppError` with context).
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for the `ActiveModel` field-setting approach.
- Per the project's Key Conventions: all error handling uses `Result<T, AppError>` with `.context()`. Apply this to the status string parsing step.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — existing ingestion pattern showing how to set fields on an `ActiveModel` during ingestion
- `entity/src/advisory.rs` — the `AdvisoryStatusEnum` definition (from Task 3) for import and variant matching

## Acceptance Criteria
- [ ] The ingestion pipeline writes the `status` enum value directly to the advisory row
- [ ] No references to the `advisory_status` lookup table remain in the ingestor module
- [ ] Unknown or invalid status strings produce a clear error rather than a silent failure
- [ ] All four valid status values (New, Analyzing, Fixed, Rejected) are correctly mapped during ingestion

## Test Requirements
- [ ] Verify ingestion of an advisory with each valid status value produces the correct enum value in the database
- [ ] Verify ingestion of an advisory with an invalid status value returns an appropriate error

## Verification Commands
- `cargo check -p ingestor` — compiles without errors
- `grep -r "advisory_status" modules/ingestor/` — returns no results

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions
