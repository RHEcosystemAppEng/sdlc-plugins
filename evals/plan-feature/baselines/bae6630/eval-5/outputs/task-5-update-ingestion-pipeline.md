## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it by foreign key. This simplifies the ingestion path and aligns it with the new enum-based schema.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Replace the lookup table insert-and-reference pattern with direct enum value assignment on the advisory insert/update

## Implementation Notes
In `modules/ingestor/src/graph/advisory/mod.rs`, the current ingestion flow:

1. Maps the status string from the advisory feed to a lookup table row in `advisory_status`.
2. Retrieves or inserts the `advisory_status` row to get the `id`.
3. Sets `advisory.status_id` to that `id`.

Replace this with:

1. Map the status string from the advisory feed to an `AdvisoryStatusEnum` variant (e.g., `"Fixed"` maps to `AdvisoryStatusEnum::Fixed`).
2. Set `advisory.status` to the enum variant directly on the `ActiveModel`.

Import `AdvisoryStatusEnum` from the entity crate (`entity::advisory::AdvisoryStatusEnum`). Remove any code that queries or inserts into the `advisory_status` table during ingestion.

Follow the existing ingestion patterns in `modules/ingestor/src/graph/sbom/mod.rs` for how ActiveModel fields are populated during ingestion.

Handle invalid status strings from the feed gracefully — log a warning and default to `AdvisoryStatusEnum::New` or return an error, consistent with the existing error handling pattern using `AppError` from `common/src/error.rs`.

## Acceptance Criteria
- [ ] Ingestion pipeline sets `advisory.status` to an `AdvisoryStatusEnum` variant directly
- [ ] No ingestion code reads from or writes to the `advisory_status` lookup table
- [ ] Invalid status strings from the feed are handled gracefully (logged/errored, not panicked)
- [ ] Ingestion compiles with `cargo check -p ingestor`

## Test Requirements
- [ ] Ingestion of an advisory with each valid status (New, Analyzing, Fixed, Rejected) writes the correct enum value
- [ ] Ingestion of an advisory with an invalid status string produces an appropriate error or default

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

## Digest
[sdlc-workflow] Description digest: sha256-md:bde6dec93bb688473a136db8d60ebb4bad8482332a7a1119b62eb19c43a1ae55
