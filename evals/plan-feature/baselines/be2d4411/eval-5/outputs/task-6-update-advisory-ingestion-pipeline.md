## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The ingestion pipeline currently parses advisory feeds, maps status strings, inserts status rows into the lookup table, and then references the lookup row ID when inserting advisories. After this change, the pipeline maps status strings directly to `AdvisoryStatusEnum` values and writes them inline with the advisory insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — update advisory ingestion logic to write `AdvisoryStatusEnum` value directly to `advisory.status` column instead of inserting into `advisory_status` table and using the FK; remove any `advisory_status` table insert or lookup logic

## Implementation Notes
- In `graph/advisory/mod.rs`, locate the code that inserts or looks up an `advisory_status` row (likely a `find_or_insert` pattern on the `advisory_status` table). Remove this entirely.
- Replace with a direct mapping from the parsed status string to `AdvisoryStatusEnum`:
  ```rust
  let status = match status_str.to_lowercase().as_str() {
      "new" => AdvisoryStatusEnum::New,
      "analyzing" => AdvisoryStatusEnum::Analyzing,
      "fixed" => AdvisoryStatusEnum::Fixed,
      "rejected" => AdvisoryStatusEnum::Rejected,
      _ => return Err(AppError::BadRequest(format!("Unknown advisory status: {}", status_str))),
  };
  ```
- Set `advisory_model.status = Set(status)` directly on the `ActiveModel` before insert.
- Remove any `use entity::advisory_status` imports.
- Handle the error case where an ingested advisory has an unrecognized status value — return `AppError::BadRequest` with the invalid value.
- Per repo Key Conventions: error handling uses `Result<T, AppError>` with `.context()` wrapping.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion pattern showing how ingestion modules parse input, build `ActiveModel`, and insert into the database
- `modules/ingestor/src/graph/advisory/mod.rs` — current implementation (pre-modification) showing the existing advisory ingestion flow to refactor

## Acceptance Criteria
- [ ] Ingestion pipeline writes `AdvisoryStatusEnum` value directly to `advisory.status` column
- [ ] No `advisory_status` table inserts or lookups remain in the ingestion code
- [ ] Unrecognized status values are rejected with a clear error message
- [ ] All four valid status values (New, Analyzing, Fixed, Rejected) are correctly mapped
- [ ] Ingestion pipeline compiles and produces correct advisory records

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" writes `New` enum value to `advisory.status`
- [ ] Verify ingestion of an advisory with status "Fixed" writes `Fixed` enum value
- [ ] Verify ingestion of an advisory with unknown status "Archived" returns an appropriate error
- [ ] Verify no writes to `advisory_status` table occur during ingestion

## Verification Commands
- `cargo build -p trustify-ingestor` — verify ingestor module compiles
- `cargo test -p trustify-ingestor -- advisory` — run advisory ingestion tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

## Labels
- ai-generated-jira

## additional_fields
- priority: High
- fixVersions: RHTPA 2.0.0

[sdlc-workflow] Description digest: sha256-md:2cf4c228fa61998e9dddd022dcb82ad29d3e52912985f4bd846815d42d1dee1b
