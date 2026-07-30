## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory` table instead of first inserting into the `advisory_status` lookup table and referencing via foreign key. The ingestion flow must map status strings from the advisory feed to `AdvisoryStatusEnum` values and insert them directly into the `status` column on the `advisory` row.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert logic with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants; remove any `advisory_status` entity imports and insert operations

## Implementation Notes
- The current ingestion flow likely inserts a row into `advisory_status` (or looks up an existing row) and then uses the resulting ID as `status_id` when inserting the advisory. Replace this with direct enum value assignment: parse the status string from the feed, convert to `AdvisoryStatusEnum` variant, and set it on the advisory `ActiveModel`
- Handle status string mapping defensively: if the feed contains an unrecognized status string, log a warning and use a default (e.g., `AdvisoryStatusEnum::New`) or return an error, following the existing error handling pattern in the ingestion module
- Remove any imports of `advisory_status` entity from the ingestion module

Per CONVENTIONS.md §Error handling: all handlers must return `Result<T, AppError>` with `.context()` wrapping — maintain this pattern for status parsing errors in the ingestion pipeline.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust handler/service scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic to adapt (replace lookup table flow with direct enum assignment)
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion patterns that write directly without intermediate lookup tables

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` value directly to the `status` column
- [ ] No remaining references to `advisory_status` entity in ingestion code
- [ ] No remaining insert operations targeting the `advisory_status` table
- [ ] Ingestion correctly maps all four status strings (New, Analyzing, Fixed, Rejected) to enum variants
- [ ] Unrecognized status strings are handled gracefully (error or default)

## Test Requirements
- [ ] Verify advisory ingestion creates advisories with correct enum status values
- [ ] Verify ingestion handles each of the four valid status strings
- [ ] Verify ingestion handles invalid/unknown status strings without panicking

## Verification Commands
- `cargo check -p ingestor` — verify ingestor module compiles
- `cargo test -p ingestor` — run module-level tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
