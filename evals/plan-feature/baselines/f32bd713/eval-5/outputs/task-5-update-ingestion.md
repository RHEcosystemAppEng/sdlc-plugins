## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The ingestion pipeline currently parses advisory status strings from the feed, looks up or inserts the status in the `advisory_status` table, and then writes the FK reference. After this change, the pipeline maps the status string directly to the `AdvisoryStatusEnum` value and sets it on the advisory row.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert/reference pattern with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references advisory status through the lookup table pattern

## Implementation Notes
- The current ingestion flow likely follows this pattern:
  1. Parse status string from advisory feed
  2. Find or create row in `advisory_status` table matching the status string
  3. Set `advisory.status_id` to the lookup table row's ID
- Replace with:
  1. Parse status string from advisory feed
  2. Map string to `AdvisoryStatusEnum` variant (e.g., `"New"` -> `AdvisoryStatusEnum::New`)
  3. Set `advisory.status` to the enum value directly
- Add a mapping function that converts incoming status strings to `AdvisoryStatusEnum`. Handle case sensitivity and potential variations (e.g., `"new"`, `"NEW"`, `"New"` should all map to `AdvisoryStatusEnum::New`). Return an error for unrecognized status values rather than silently dropping them.
- Per repo Key Conventions §Error handling: all service methods return `Result<T, AppError>` with `.context()` wrapping. Use `.context("Failed to map advisory status")` for the enum mapping.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` service file scope.
- Reference `modules/ingestor/src/graph/sbom/mod.rs` for the established ingestion pattern (parse, validate, store).

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — existing ingestion graph module demonstrating the parse-validate-store pattern
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3 that this task maps incoming strings to

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestor module
- [ ] Status string mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Unrecognized status strings produce a clear error (not silently ignored)
- [ ] `cargo build -p ingestor` compiles without errors

## Test Requirements
- [ ] Ingesting an advisory with status "New" writes `AdvisoryStatusEnum::New` to the advisory row
- [ ] Ingesting an advisory with each of the four status values succeeds
- [ ] Ingesting an advisory with an unrecognized status value produces an error
- [ ] End-to-end ingestion flow works with the new enum column

## Verification Commands
- `cargo build -p ingestor` — ingestor module compiles cleanly
- `cargo test -p ingestor` — ingestor module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
