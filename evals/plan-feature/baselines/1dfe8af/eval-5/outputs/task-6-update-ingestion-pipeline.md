# Task 6 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it by foreign key. This simplifies the ingestion flow and removes a round-trip insert that is no longer needed.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace the lookup-table insert logic (which currently inserts or finds the status in `advisory_status` and sets `status_id`) with direct enum value assignment on the advisory `ActiveModel`; remove any imports of the `advisory_status` entity
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references advisory_status entity or passes status_id values; ensure status mapping from feed strings to `AdvisoryStatusEnum` variants is handled here or in the graph module

## Implementation Notes
The current ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` likely:
1. Parses the advisory status string from the feed
2. Looks up or inserts the status in `advisory_status` table
3. Sets `status_id` on the advisory `ActiveModel`

Replace steps 2-3 with:
1. Parse the status string to `AdvisoryStatusEnum` using `FromStr` or a match statement
2. Set `status` directly on the advisory `ActiveModel`:
```rust
advisory_model.status = Set(AdvisoryStatusEnum::from_str(&status_str)
    .context("invalid advisory status")?);
```

Handle invalid status strings with a clear error message using the `AppError` pattern from `common/src/error.rs`.

Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` scope.

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` values directly to `advisory.status`
- [ ] No references to `advisory_status` entity remain in the ingestor module
- [ ] Invalid status strings in the feed produce a clear error (not a panic)
- [ ] Ingestion of advisories with all four status values works correctly

## Test Requirements
- [ ] Ingest a test advisory with each of the four status values and verify correct enum storage
- [ ] Ingest a test advisory with an invalid status string and verify error handling
- [ ] `cargo build -p ingestor` compiles successfully

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:f1b5c8d67a0e2493b6d9f4a75e8c3b26d7a0f9e45b1c6d8304a2e5f7c9b1d4e3
