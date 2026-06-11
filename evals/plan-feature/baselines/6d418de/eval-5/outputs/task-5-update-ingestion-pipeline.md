# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The ingestion pipeline currently maps incoming status strings to lookup table rows; it must now map them directly to enum values.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — update advisory ingestion logic to: (1) map incoming status strings to `AdvisoryStatusEnum` variants instead of looking up/inserting into `advisory_status` table; (2) set the `status` field on the `Advisory` active model directly with the enum value; (3) remove any code that reads from or writes to the `advisory_status` table
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` types or passes status IDs to the graph layer

## Implementation Notes
- The ingestion pipeline currently follows a pattern like: parse status string from feed -> find or create row in `advisory_status` table -> use the row's ID as `status_id` on the advisory. Replace this with: parse status string -> map to `AdvisoryStatusEnum` variant -> set directly on advisory model
- Create a mapping function or use `FromStr`/`TryFrom` implementation on `AdvisoryStatusEnum` to convert incoming status strings (e.g., "New", "Analyzing", "Fixed", "Rejected") to enum variants
- Handle invalid status strings gracefully with appropriate error context using the `AppError` pattern from `common/src/error.rs`
- Remove any imports of `advisory_status` entity types from the ingestor module
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for reference on how ingestion modules are structured
- Per docs/constraints.md §5.2: inspect the ingestion code before modifying to understand the current status handling flow
- Per docs/constraints.md §5.8: compare against `sbom/mod.rs` ingestion for parity on error handling and logging

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference implementation for SBOM ingestion pattern (parse, store, link); follow the same structural approach for advisory ingestion
- `modules/ingestor/src/service/mod.rs` — `IngestorService` that orchestrates ingestion; understand how it currently passes status information
- `common/src/error.rs` — `AppError` for error handling in the ingestion pipeline

## Acceptance Criteria
- [ ] Ingestion pipeline maps status strings directly to `AdvisoryStatusEnum` variants
- [ ] Ingestion pipeline sets `advisory.status` enum value directly (no lookup table interaction)
- [ ] All references to `advisory_status` table are removed from the ingestor module
- [ ] Invalid status strings produce clear error messages
- [ ] Ingestion of advisories with all four status values works correctly

## Test Requirements
- [ ] Ingesting an advisory with status "New" sets the correct enum value
- [ ] Ingesting an advisory with status "Fixed" sets the correct enum value
- [ ] Ingesting an advisory with an invalid status string produces an appropriate error
- [ ] Existing advisory ingestion tests pass with the updated pipeline

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles successfully
- `cargo test -p ingestor` — existing ingestor tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
