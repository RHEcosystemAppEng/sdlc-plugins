## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently parses advisory feeds, looks up or creates a status row in `advisory_status`, and sets `advisory.status_id`. After this change, the pipeline maps the status string from the feed directly to the `AdvisoryStatusEnum` value and writes it to the `advisory.status` column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace status lookup table insert with direct enum value assignment; map feed status strings to `AdvisoryStatusEnum` variants; remove all references to the `advisory_status` table

## Implementation Notes
- The ingestion pipeline currently performs: (1) parse status from feed, (2) insert/lookup in `advisory_status` table, (3) set `advisory.status_id` FK. Replace with: (1) parse status from feed, (2) map to `AdvisoryStatusEnum` variant, (3) set `advisory.status` directly
- Implement a mapping function from feed status strings to `AdvisoryStatusEnum` variants. Handle case-insensitive matching (e.g., "new" -> `AdvisoryStatusEnum::New`)
- Add error handling for unknown status strings in the feed -- log a warning and either default to a safe value or return an error, depending on the existing error handling pattern in the ingestion module
- Per CONVENTIONS.md §Framework: use SeaORM's ActiveModel pattern for setting the enum field value during ingestion.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's SeaORM database scope.
- Reference the SBOM ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for the established ingestion code structure

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- existing ingestion module demonstrating the project's ingestion pattern (parsing, storing, linking)
- `modules/ingestor/src/service/mod.rs` -- `IngestorService` showing the service-level ingestion orchestration pattern
- `entity/src/advisory.rs` -- updated advisory entity with `AdvisoryStatusEnum` (from Task 3)

## Acceptance Criteria
- [ ] Advisory ingestion writes the `status` enum value directly to the `advisory.status` column
- [ ] No references to the `advisory_status` lookup table remain in the ingestion pipeline
- [ ] Status string from feed is correctly mapped to `AdvisoryStatusEnum` variants (New, Analyzing, Fixed, Rejected)
- [ ] Unknown status strings in the feed produce an appropriate error or warning rather than a silent failure
- [ ] Ingested advisories are queryable by the updated advisory service (Task 4)

## Test Requirements
- [ ] Test: ingesting an advisory with status "New" results in `advisory.status = 'New'` enum value in the database
- [ ] Test: ingesting advisories with each valid status value (New, Analyzing, Fixed, Rejected) stores the correct enum value
- [ ] Test: ingesting an advisory with an unrecognized status string produces an error or warning (not a silent skip)
- [ ] Test: verify end-to-end flow -- ingest advisory, then query via advisory list endpoint and confirm correct status

## Verification Commands
- `cargo test -p ingestor -- advisory` -- ingestion module tests pass
- `cargo check -p ingestor` -- ingestion module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
