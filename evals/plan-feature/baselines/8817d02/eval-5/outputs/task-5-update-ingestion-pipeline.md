# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Summary

Update advisory ingestion to write enum status values instead of lookup table inserts

## Repository

trustify-backend

## Target Branch

TC-9005

## Description

Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and referencing by FK. The pipeline should map incoming status strings to enum variants and set the status field directly during advisory insertion.

## Files to Modify

- `modules/ingestor/src/graph/advisory/mod.rs` — remove code that inserts into or queries the `advisory_status` lookup table; instead map the status string from the advisory feed to an `AdvisoryStatusEnum` variant and set it on the advisory `ActiveModel` directly
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it contains any references to the `advisory_status` entity or lookup logic

## Implementation Notes

- In `modules/ingestor/src/graph/advisory/mod.rs`, locate the code path that currently: (a) looks up or inserts a row in `advisory_status`, (b) uses the returned ID as `status_id` on the advisory. Replace this with a direct mapping: parse the status string to `AdvisoryStatusEnum` using `FromStr` or a match expression, then set `advisory::ActiveModel { status: Set(enum_value), ... }`.
- Handle invalid status strings gracefully — if a feed provides an unrecognized status value, return an error rather than silently dropping the advisory. Use the `AppError` pattern from `common/src/error.rs`.
- Remove any `use entity::advisory_status` imports from the ingestor module.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for reference on how the SBOM ingestion handles direct field setting.

## Reuse Candidates

- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion patterns (parse, store) without lookup table indirection
- `common/src/error.rs` — `AppError` enum for error handling on invalid status values
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type to use for status values (created in Task 3)

## Acceptance Criteria

- [ ] Advisory ingestion writes enum values directly to the `status` column
- [ ] No code in the ingestor module references the `advisory_status` entity or table
- [ ] Invalid status strings in the feed produce a clear error
- [ ] The ingestor module compiles without errors (`cargo check -p ingestor`)

## Test Requirements

- [ ] Verify that ingesting an advisory with status "New" results in the correct enum value in the database
- [ ] Verify that ingesting an advisory with status "Fixed" results in the correct enum value
- [ ] Verify that ingesting an advisory with an invalid status string produces an appropriate error

## Verification Commands

- `cargo check -p ingestor` — ingestor module compiles without errors

## Dependencies

- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

sha256-md:dc9e82f9ce4d4b91546f669acf5371e8a45c9862b3b80d7298f108b0318211f0
