## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline should map the status string from the advisory feed to the `AdvisoryStatusEnum` Rust enum and set it directly on the advisory record during ingestion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace the lookup table insertion and FK reference logic with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants; remove any imports or references to the `advisory_status` entity
- `modules/ingestor/src/service/mod.rs` -- remove any `advisory_status` references from the `IngestorService` if present

## Implementation Notes
- The ingestion pipeline currently: (1) checks if the status exists in `advisory_status`, (2) inserts it if missing, (3) uses the returned ID as the `status_id` FK. Replace this with: (1) map the status string to `AdvisoryStatusEnum` variant, (2) set `status` directly on the advisory `ActiveModel`.
- For mapping status strings to enum variants, use a match expression or `FromStr` implementation:
  ```rust
  let status = match status_str {
      "New" => AdvisoryStatusEnum::New,
      "Analyzing" => AdvisoryStatusEnum::Analyzing,
      "Fixed" => AdvisoryStatusEnum::Fixed,
      "Rejected" => AdvisoryStatusEnum::Rejected,
      _ => return Err(anyhow!("Unknown advisory status: {}", status_str)),
  };
  ```
- Follow the ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for reference on direct field assignment during ingestion.
- Ensure error handling for unknown status values is robust -- the ingestion pipeline should fail cleanly with a descriptive error rather than panicking.
- Per docs/constraints.md section 2 (Commit Rules): commit messages must follow Conventional Commits format, reference TC-9005 in the footer, and include the `--trailer="Assisted-by: Claude Code"`.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- reference for ingestion graph patterns with direct entity field assignment
- `entity/src/advisory.rs::AdvisoryStatusEnum` -- the enum type defined in Task 3

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` values directly to the `advisory.status` column
- [ ] No remaining references to `advisory_status` lookup table in the ingestion pipeline
- [ ] Unknown status strings produce a descriptive error, not a panic
- [ ] Ingestion of advisories with all four valid statuses succeeds

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" writes the correct enum value
- [ ] Verify ingestion of an advisory with status "Fixed" writes the correct enum value
- [ ] Verify ingestion of an advisory with an unknown status produces a descriptive error
- [ ] Verify ingested advisories are queryable via the updated service layer

## Verification Commands
- `cargo check -p ingestor` -- ingestor module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions
