## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently maps advisory feed status strings to lookup table rows — it must now map them to `AdvisoryStatusEnum` values and set the enum column directly during advisory insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insertion logic with direct enum value assignment; map incoming status strings from the advisory feed to `AdvisoryStatusEnum` variants; remove any code that inserts into or queries the `advisory_status` table
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` entity or lookup table operations

## Implementation Notes
- The ingestion pipeline currently likely does two operations: (1) find or create a row in `advisory_status` for the status string, and (2) set `advisory.status_id` to that row's ID. Replace this with: (1) parse the status string to `AdvisoryStatusEnum` variant, and (2) set `advisory.status` to the enum value directly.
- For parsing status strings, implement or use a `FromStr` / `TryFrom<String>` implementation on `AdvisoryStatusEnum`:
  ```rust
  let status = match status_string.as_str() {
      "New" | "new" => AdvisoryStatusEnum::New,
      "Analyzing" | "analyzing" => AdvisoryStatusEnum::Analyzing,
      "Fixed" | "fixed" => AdvisoryStatusEnum::Fixed,
      "Rejected" | "rejected" => AdvisoryStatusEnum::Rejected,
      _ => return Err(AppError::from(anyhow::anyhow!("Unknown advisory status: {}", status_string))),
  };
  ```
- Handle invalid or unrecognized status strings with proper error handling — do not silently drop advisories with unknown statuses.
- Per CONVENTIONS.md §Error handling: wrap errors with `.context()` for clear error messages during ingestion failures.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/advisory/mod.rs` — existing advisory ingestion logic shows the current parse-store-correlate pattern
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for ingestion patterns that write directly to entity columns without lookup tables
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum definition (from Task 3) provides the variant names and string mappings

## Acceptance Criteria
- [ ] Ingestion pipeline maps advisory feed status strings to `AdvisoryStatusEnum` variants
- [ ] Ingestion pipeline sets `advisory.status` enum column directly during insertion
- [ ] No code in the ingestor module references `advisory_status` entity or lookup table
- [ ] Invalid status strings produce clear error messages, not silent failures
- [ ] `cargo check -p ingestor` compiles without errors

## Test Requirements
- [ ] Verify ingestion of an advisory with status "New" writes `AdvisoryStatusEnum::New` to the enum column
- [ ] Verify ingestion of an advisory with status "Fixed" writes `AdvisoryStatusEnum::Fixed`
- [ ] Verify ingestion of an advisory with an unrecognized status produces an appropriate error
- [ ] Verify end-to-end: ingest an advisory, then retrieve it via the advisory list endpoint and confirm the status field is correct

## Verification Commands
- `cargo check -p ingestor` — compiles without errors
- `grep -r "advisory_status" modules/ingestor/` — returns no matches
- `cargo test -p ingestor` — all existing tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
