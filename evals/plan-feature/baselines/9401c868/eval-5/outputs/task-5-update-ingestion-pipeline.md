## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory` table instead of inserting into the `advisory_status` lookup table and linking via foreign key. The pipeline must map status strings from the advisory feed to `AdvisoryStatusEnum` values and set them directly on the advisory row during insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace the lookup table insert and FK assignment with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it contains advisory status handling logic or references to the `advisory_status` entity

## Implementation Notes
- Currently the ingestion pipeline follows this pattern: (1) insert a row into `advisory_status` table, (2) retrieve the inserted ID, (3) set `advisory.status_id = id` on the advisory row
- The new pattern: (1) map the status string from the feed to an `AdvisoryStatusEnum` variant, (2) set `advisory.status = enum_value` directly on the advisory ActiveModel
- Use a match expression to map ingested status strings to enum variants:
  ```rust
  let status = match status_str.as_str() {
      "New" => AdvisoryStatusEnum::New,
      "Analyzing" => AdvisoryStatusEnum::Analyzing,
      "Fixed" => AdvisoryStatusEnum::Fixed,
      "Rejected" => AdvisoryStatusEnum::Rejected,
      other => return Err(anyhow::anyhow!("Unknown advisory status: {}", other)).context("advisory ingestion"),
  };
  ```
- Remove all references to the `advisory_status` entity and table from the ingestion code
- Handle unknown status values with clear error messages using the `AppError` pattern with `.context()` wrapping

Per CONVENTIONS.md section "Error handling": all handlers return `Result<T, AppError>` with `.context()` wrapping.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- SBOM ingestion pattern showing how entities are inserted directly without lookup table indirection; follow the same `ActiveModel` insert pattern
- `modules/ingestor/src/graph/advisory/mod.rs` -- current advisory ingestion logic to understand the existing pattern before refactoring

## Acceptance Criteria
- [ ] Advisory ingestion writes enum status value directly to `advisory.status` column
- [ ] No writes to the `advisory_status` lookup table occur during ingestion (table no longer exists)
- [ ] Status string mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Unknown or invalid status values produce a clear, actionable error message
- [ ] Ingestion pipeline processes advisory feeds successfully end-to-end with the new schema
- [ ] No `use` imports reference the removed `advisory_status` entity

## Test Requirements
- [ ] Ingestion of an advisory with status "New" succeeds and stores the correct enum value
- [ ] Ingestion of an advisory with status "Analyzing" succeeds and stores the correct enum value
- [ ] Ingestion of an advisory with status "Fixed" succeeds and stores the correct enum value
- [ ] Ingestion of an advisory with status "Rejected" succeeds and stores the correct enum value
- [ ] Ingestion of an advisory with an unknown status value produces an appropriate error
- [ ] End-to-end test: ingest advisory, query via API, verify status value is correct

## Verification Commands
- `cargo check -p ingestor` -- ingestor module compiles without error
- `cargo test -p ingestor` -- ingestor module tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
