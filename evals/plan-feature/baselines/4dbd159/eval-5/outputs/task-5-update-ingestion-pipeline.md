# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing via foreign key. The ingestion flow must map incoming status strings from the advisory feed to the `AdvisoryStatusEnum` enum type and set the value on the advisory entity directly during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — remove the lookup table insertion logic (inserting into `advisory_status` table to get a status ID); replace with direct enum value assignment on the advisory `ActiveModel`; map incoming status strings to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` entity for status resolution; remove any `advisory_status` imports

## Implementation Notes
- Import `AdvisoryStatusEnum` from `entity::advisory`
- In the advisory ingestion handler (`graph/advisory/mod.rs`), the current flow likely:
  1. Looks up or inserts a row in `advisory_status` table
  2. Gets the `status_id` from that row
  3. Sets `advisory.status_id = status_id` on the advisory ActiveModel
- Replace this with:
  1. Parse the incoming status string to an `AdvisoryStatusEnum` variant
  2. Set `advisory.status = ActiveValue::Set(AdvisoryStatusEnum::Fixed)` (or whichever variant)
- For string-to-enum mapping, use a match expression:
  ```rust
  let status = match status_str.as_str() {
      "New" => AdvisoryStatusEnum::New,
      "Analyzing" => AdvisoryStatusEnum::Analyzing,
      "Fixed" => AdvisoryStatusEnum::Fixed,
      "Rejected" => AdvisoryStatusEnum::Rejected,
      other => return Err(AppError::BadRequest(format!("Unknown advisory status: {}", other))),
  };
  ```
- Follow error handling patterns from `common/src/error.rs` — use `AppError` with `.context()` wrapping for any parsing failures
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for reference on how ingestion modules interact with entity ActiveModels

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion graph module patterns (how ActiveModels are built and inserted)
- `common/src/error.rs` — AppError enum for error handling in the status parsing path

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to `advisory.status` without touching any lookup table
- [ ] All four status values (New, Analyzing, Fixed, Rejected) are correctly mapped from incoming feed strings
- [ ] Invalid status strings in the feed produce a clear error rather than a silent failure
- [ ] No references to `advisory_status` entity or table remain in the ingestor module
- [ ] The ingestor module compiles without errors

## Test Requirements
- [ ] Test that ingesting an advisory with status "Fixed" results in `status = Fixed` enum value in the database
- [ ] Test that ingesting an advisory with an unknown status string produces an appropriate error
- [ ] Verify end-to-end ingestion flow: ingest an advisory, then query it via the advisory list endpoint and confirm the status is correct

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles without errors
- `cargo test -p ingestor` — ingestor tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
