# Task 6 — Update advisory ingestion pipeline to write enum status directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. This simplifies the ingestion flow and removes the dependency on the now-dropped lookup table.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace the logic that inserts/looks up status in the `advisory_status` table with direct enum value mapping; when parsing an advisory from the feed, map the status string to `AdvisoryStatusEnum` and set it directly on the advisory entity's `status` field
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it contains any references to `advisory_status` table operations or status ID resolution

## Implementation Notes
- The current ingestion flow likely does: (1) parse status from feed, (2) find or insert into `advisory_status` table to get an ID, (3) set `status_id` on the advisory record. Replace this with: (1) parse status from feed, (2) map to `AdvisoryStatusEnum` variant, (3) set `status` enum field on the advisory record
- Use a match or from-string conversion to map feed status strings to `AdvisoryStatusEnum`:
  ```rust
  let status = match status_str.as_str() {
      "New" => AdvisoryStatusEnum::New,
      "Analyzing" => AdvisoryStatusEnum::Analyzing,
      "Fixed" => AdvisoryStatusEnum::Fixed,
      "Rejected" => AdvisoryStatusEnum::Rejected,
      other => return Err(anyhow!("Unknown advisory status: {}", other)),
  };
  ```
- Remove any `use` imports of the `advisory_status` entity from the ingestion modules
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for error handling and entity insertion
- Maintain `.context()` error wrapping per the project's error handling pattern

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference ingestion pattern for parsing, entity creation, and error handling
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3 that this task uses for direct status mapping

## Acceptance Criteria
- [ ] Advisory ingestion writes enum status values directly to the `advisory.status` column
- [ ] No references to `advisory_status` lookup table remain in the ingestion pipeline
- [ ] All four status values (New, Analyzing, Fixed, Rejected) are correctly mapped from feed input
- [ ] Unknown status strings are handled with an appropriate error

## Test Requirements
- [ ] Ingestion of an advisory with status "New" correctly sets the enum value
- [ ] Ingestion of an advisory with status "Fixed" correctly sets the enum value
- [ ] Ingestion of an advisory with an unknown status string returns an error
- [ ] End-to-end ingestion flow works without the advisory_status table

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles without errors
- `cargo test -p ingestor` — existing ingestion tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
