# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently writes to the lookup table first and then uses the resulting ID for the advisory row; after this change, it maps the status string from the feed directly to an `AdvisoryStatusEnum` variant and writes it on the advisory row.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert logic with direct enum value mapping; write `AdvisoryStatusEnum` variant to advisory row's `status` field
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` entity or its operations

## Implementation Notes
In `modules/ingestor/src/graph/advisory/mod.rs`, the current flow likely: (1) finds or creates a row in `advisory_status`, (2) uses the returned ID as `status_id` on the advisory insert. Replace this with: (1) map the feed's status string to `AdvisoryStatusEnum` variant, (2) set `status` field on the advisory `ActiveModel` directly.

Use a `match` or `FromStr` implementation on `AdvisoryStatusEnum` to convert the feed string to the enum variant. Handle unknown status values by returning an error with `.context()` wrapping per the error handling convention.

Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` handler scope.

## Acceptance Criteria
- [ ] Ingestion pipeline writes enum value directly to `advisory.status` column
- [ ] Ingestion pipeline no longer references `advisory_status` lookup table
- [ ] Status string from feed is correctly mapped to `AdvisoryStatusEnum` variant
- [ ] Unknown status values produce a clear error

## Test Requirements
- [ ] Advisory ingestion with status "New" writes correct enum value
- [ ] Advisory ingestion with status "Fixed" writes correct enum value
- [ ] Advisory ingestion with unknown status value returns an error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
