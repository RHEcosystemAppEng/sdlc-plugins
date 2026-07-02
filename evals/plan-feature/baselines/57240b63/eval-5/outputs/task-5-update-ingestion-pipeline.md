# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of first inserting a row into the `advisory_status` lookup table and then referencing it via foreign key. This simplifies the ingestion flow by eliminating the lookup table insert step and directly mapping advisory status strings from the feed to the PostgreSQL enum type.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace lookup table insert logic with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references advisory status lookup table operations

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, locate the code that inserts into the `advisory_status` table and retrieves the ID for the FK. Replace this with a direct mapping from the incoming status string to an `AdvisoryStatusEnum` variant.
- Implement a mapping function: parse the status string from the advisory feed (e.g., `"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`) and convert it to the corresponding `AdvisoryStatusEnum` variant. Handle unknown status values with an appropriate error using the `AppError` pattern from `common/src/error.rs`.
- When creating the advisory `ActiveModel`, set the `status` field to the mapped enum value instead of setting `status_id` to a looked-up FK value.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for error handling and transaction management.
- Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for status mapping errors.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust source file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — Reference for ingestion graph patterns (parse, store, link) without lookup table indirection
- `common/src/error.rs` — `AppError` enum for error handling when status string mapping fails
- `entity/src/advisory.rs::AdvisoryStatusEnum` — The enum type to use for direct value assignment (created in Task 3)

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `advisory.status` column
- [ ] No code references the `advisory_status` lookup table for ingestion operations
- [ ] Unknown status strings in the feed produce a clear error via `AppError`
- [ ] Ingestion of advisories with all four status values (New, Analyzing, Fixed, Rejected) succeeds
- [ ] The ingestor module compiles without errors

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" writes the correct enum value
- [ ] Verify ingestion of an advisory with status "Fixed" writes the correct enum value
- [ ] Verify ingestion of an advisory with an unknown status string produces an appropriate error
- [ ] Verify the ingestor module compiles: `cargo check -p ingestor`

## Verification Commands
- `cargo check -p ingestor` — expected: compiles without errors
- `cargo test -p ingestor` — expected: existing unit tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

---

[sdlc-workflow] Description digest: sha256-md:a6a9cdc770dbb68930907d19fe614bc0c92da03aca44515f6dd76a5ca636dae0
