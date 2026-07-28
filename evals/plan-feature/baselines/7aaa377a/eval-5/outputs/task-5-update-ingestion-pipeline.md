## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline currently maps incoming status strings to lookup table rows; it must now map them directly to `AdvisoryStatusEnum` enum values and set the enum column on the advisory row during insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert + FK reference with direct enum value assignment; update the advisory insert/update logic to set `status` as an `AdvisoryStatusEnum` value
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it coordinates status handling between ingestion steps

## Implementation Notes
- The ingestion pipeline currently: (1) parses status string from feed, (2) looks up or inserts into `advisory_status` table, (3) uses the resulting ID as `status_id` on the advisory row. After this change: (1) parses status string from feed, (2) maps to `AdvisoryStatusEnum` variant, (3) sets `status` enum column directly on the advisory row.
- The mapping from feed status strings to enum variants must handle case variations (e.g., "new" vs "New"). Use a case-insensitive match or normalize the input.
- Invalid status values from the feed should produce a clear error rather than silently failing — use `.context()` wrapping per the error handling convention.
- Per CONVENTIONS.md §Framework: use SeaORM `ActiveModel` patterns for setting the enum field value during insert.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust/SeaORM file scope.
- Per CONVENTIONS.md §Error Handling: return `Result<T, AppError>` with `.context()` wrapping for status mapping errors.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust handler file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pattern for direct field assignment without lookup tables
- `entity/src/advisory.rs` — updated entity with `AdvisoryStatusEnum` field (from Task 3)

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` values directly to `advisory.status` column
- [ ] No inserts or references to the `advisory_status` lookup table remain in the ingestion code
- [ ] Status string mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Invalid status strings produce a descriptive error

## Test Requirements
- [ ] Ingest an advisory with each valid status value and verify the correct enum value is stored
- [ ] Ingest an advisory with an invalid status value and verify an appropriate error is returned
- [ ] Verify no rows are written to the `advisory_status` table during ingestion (table should not exist after migration)

## Verification Commands
- `cargo build -p ingestor` — compiles without errors
- `cargo test -p ingestor` — all ingestion tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
