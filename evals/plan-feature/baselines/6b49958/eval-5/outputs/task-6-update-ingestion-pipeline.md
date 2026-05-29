## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. This simplifies ingestion by removing the lookup-table-insert step.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace the logic that inserts into `advisory_status` table and uses the returned ID as `status_id` with direct enum value assignment to the `status` column

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`, locate the ingestion logic that currently: (1) looks up or inserts the status string into the `advisory_status` table, (2) retrieves the row ID, and (3) sets `status_id` on the advisory insert. Replace this with: (1) parse the status string to `AdvisoryStatusEnum`, (2) set `status` directly on the advisory `ActiveModel`.
- Use `AdvisoryStatusEnum::try_from(status_string)` or a match statement to convert ingested status strings to the enum type. Handle invalid status values by returning an appropriate error using the `AppError` pattern from `common/src/error.rs`.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for how graph ingestion modules interact with entity models.
- Remove any imports of `entity::advisory_status` and any helper functions that interact with the lookup table.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — demonstrates the ingestion graph pattern for inserting entities with direct field values
- `modules/ingestor/src/service/mod.rs` — `IngestorService` that orchestrates ingestion; useful for understanding the call chain

## Acceptance Criteria
- [ ] Advisory ingestion writes `status` enum values directly to the `advisory` table
- [ ] No inserts or lookups to the `advisory_status` table occur during ingestion
- [ ] Invalid status strings in the ingestion feed produce an appropriate error
- [ ] All four valid status values (New, Analyzing, Fixed, Rejected) are correctly mapped from ingestion input to enum values

## Test Requirements
- [ ] Test ingestion of advisories with each valid status value
- [ ] Test ingestion with an invalid status string returns an error
- [ ] Test that no `advisory_status` table operations occur during ingestion

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256:9ec41166d63b8e11f89c18e419a173c607fb0b0d0d172d725f8f936ecf677361
