## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing via foreign key. The pipeline must map status strings from advisory feeds to `AdvisoryStatusEnum` variants and set the enum value on the advisory row during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace the logic that inserts/looks up a row in the `advisory_status` table and sets `status_id` on the advisory. Instead, map the incoming status string to an `AdvisoryStatusEnum` variant and set the `status` field directly on the `advisory` ActiveModel. Remove any imports or references to the `advisory_status` entity
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references advisory status through the lookup table pattern; ensure it uses the enum type for status handling

## Implementation Notes
The current ingestion flow in `modules/ingestor/src/graph/advisory/mod.rs` likely:
1. Parses status string from the advisory feed
2. Looks up or inserts into `advisory_status` table to get the `status_id`
3. Sets `status_id` on the advisory row

Replace with:
1. Parse status string from the advisory feed
2. Map to `AdvisoryStatusEnum` variant (e.g., `"Fixed"` -> `AdvisoryStatusEnum::Fixed`)
3. Set `status` field directly on the `advisory::ActiveModel`

Import the `AdvisoryStatusEnum` from `entity::advisory`. Handle invalid status strings by returning an appropriate `AppError` with context, following the error handling pattern in `common/src/error.rs`.

Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` as a reference for how ingestion modules interact with entity models.

Per CONVENTIONS.md §Error handling: use `Result<T, AppError>` with `.context()` wrapping for error handling in the ingestion pipeline.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` scope.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatusEnum` — The enum type defined in Task 3; import and use for status mapping
- `modules/ingestor/src/graph/sbom/mod.rs` — Reference ingestion pattern for how to set fields directly on entity ActiveModels
- `common/src/error.rs::AppError` — Error type for handling invalid status strings during ingestion

## Acceptance Criteria
- [ ] Advisory ingestion writes `status` enum value directly to the `advisory` row
- [ ] No references to `advisory_status` table remain in the ingestor module
- [ ] Invalid status strings in advisory feeds produce a clear error with context
- [ ] Status mapping covers all four enum variants: New, Analyzing, Fixed, Rejected
- [ ] `cargo build -p ingestor` compiles without errors

## Test Requirements
- [ ] Ingesting an advisory with status "New" sets the correct enum value on the advisory row
- [ ] Ingesting an advisory with status "Fixed" sets the correct enum value
- [ ] Ingesting an advisory with an unrecognized status string returns an appropriate error
- [ ] End-to-end ingestion pipeline works with the new enum-based status field

## Verification Commands
- `cargo test -p ingestor` — ingestor module tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
