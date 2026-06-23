## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory` table instead of inserting into the `advisory_status` lookup table first. The pipeline currently parses advisory feeds, maps the status string to a lookup table row, and inserts the FK. After this change, the pipeline maps the status string to an `AdvisoryStatusEnum` variant and writes it directly to the `status` column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — update advisory ingestion logic to map status strings to `AdvisoryStatusEnum` variants and write them directly to the `status` column; remove any code that inserts into or queries the `advisory_status` lookup table
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` entity or lookup table operations

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, the current ingestion flow likely:
  1. Parses status string from advisory feed
  2. Looks up or inserts into `advisory_status` table to get the ID
  3. Sets `status_id` on the advisory record
- Replace this with:
  1. Parse status string from advisory feed
  2. Map to `AdvisoryStatusEnum` variant (e.g., `"Fixed"` -> `AdvisoryStatusEnum::Fixed`)
  3. Set `status` field directly on the advisory `ActiveModel`
- Add error handling for unrecognized status values — return an `AppError` with context rather than silently defaulting.
- Import `AdvisoryStatusEnum` from `entity::advisory`.
- Per CONVENTIONS.md §Key Conventions: error handling uses `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module file scope.

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `status` column
- [ ] No remaining references to `advisory_status` lookup table in the ingestor module
- [ ] Unrecognized status values produce clear error messages
- [ ] Ingestor module compiles with `cargo check -p ingestor`

## Test Requirements
- [ ] Ingestion of advisory with status "New" writes correct enum value
- [ ] Ingestion of advisory with status "Fixed" writes correct enum value
- [ ] Ingestion of advisory with unrecognized status produces an error, not a silent default
- [ ] End-to-end ingestion test: ingest advisory, query via API, verify status is correct string

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for enum status

[sdlc-workflow] Description digest: sha256-md:8cf1f3e809e4177d01ef5bb1098b7cded55cf902a966d9a1681569fcaea0d89c
