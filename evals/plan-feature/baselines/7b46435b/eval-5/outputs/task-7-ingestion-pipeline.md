# Task 7 — Update advisory ingestion pipeline for direct enum writes

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and then referencing via foreign key. The pipeline should map status strings from the advisory feed to `AdvisoryStatusEnum` variants and set them directly on the advisory entity during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert + FK assignment with direct enum value assignment on the advisory `ActiveModel`; remove any `advisory_status` table interaction
- `modules/ingestor/Cargo.toml` — add dependency on entity crate's `AdvisoryStatusEnum` if not already present

## Implementation Notes
- The current ingestion flow likely: (1) checks if the status exists in `advisory_status` table, (2) inserts it if not found, (3) uses the returned `status_id` FK when creating the advisory row. Replace this entire flow with: (1) parse the status string from the feed, (2) convert to `AdvisoryStatusEnum` variant, (3) set `status` field directly on the advisory `ActiveModel`
- Handle invalid status strings gracefully — if the feed provides a status value not matching any of the four enum variants (New, Analyzing, Fixed, Rejected), return an error via `AppError` with a descriptive message rather than silently dropping the advisory
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for error handling, entity creation, and transaction management
- Verify that `IngestorService` in `modules/ingestor/src/service/mod.rs` does not maintain its own reference to the `advisory_status` table — update if needed

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference ingestion pattern for entity creation, error handling, and `ActiveModel` usage
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type to map feed status strings to

## Acceptance Criteria
- [ ] Ingestion pipeline writes enum values directly to `advisory.status` column
- [ ] No interaction with `advisory_status` lookup table during ingestion
- [ ] Invalid status strings from the feed produce clear error messages via `AppError`
- [ ] All four valid status values (New, Analyzing, Fixed, Rejected) are correctly mapped from feed input

## Test Requirements
- [ ] Verify ingestion with a feed containing each valid status value produces correct enum values in the database
- [ ] Verify ingestion with an invalid status value returns an appropriate error
- [ ] Verify the ingestor crate compiles: `cargo check -p ingestor`

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles
- `cargo test -p ingestor` — ingestor module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
