## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing the row via foreign key. This simplifies the ingestion flow by eliminating the intermediate lookup table write.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- Replace lookup table insertion with direct enum value assignment on the advisory record
- `modules/ingestor/src/service/mod.rs` -- Update `IngestorService` if it references advisory status insertion logic

## Implementation Notes
- The current ingestion flow likely: (1) inserts or finds the status row in `advisory_status`, (2) gets the `id`, (3) sets `advisory.status_id` to that id. Replace this with: (1) map the status string from the feed to an `AdvisoryStatusEnum` variant, (2) set `advisory.status` directly.
- Use a match statement or `AdvisoryStatusEnum::try_from()` to convert incoming status strings to enum variants. Handle unknown status values with an appropriate error using `AppError` and `.context()`.
- Follow the ingestion pattern established in `modules/ingestor/src/graph/sbom/mod.rs` for reference on how the SBOM ingestion pipeline writes entity data
- Remove any code that queries or inserts into the `advisory_status` table

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust handler file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion pattern for reference on entity insertion flow
- `common/src/error.rs` -- AppError for error handling during status string parsing

## Acceptance Criteria
- [ ] Advisory ingestion writes the `advisory_status_enum` value directly to `advisory.status`
- [ ] No code remains that inserts into or queries the `advisory_status` lookup table
- [ ] Unknown status strings in the feed produce a clear error message
- [ ] Ingestion of advisories with all four status values works correctly (New, Analyzing, Fixed, Rejected)

## Test Requirements
- [ ] Verify advisory ingestion succeeds with each valid status value
- [ ] Verify advisory ingestion produces an appropriate error for unknown status values
- [ ] Verify no writes to the (now-dropped) `advisory_status` table occur during ingestion

## Verification Commands
- `cargo check -p ingestor` -- module compiles successfully
- `cargo test -p ingestor` -- unit tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
