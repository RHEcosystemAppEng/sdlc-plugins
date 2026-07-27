## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and creating a foreign key reference. The ingestion pipeline must map status strings from advisory feeds to `AdvisoryStatusEnum` values.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert with direct enum value assignment; map status strings from advisory feeds to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references `advisory_status` entity or table for status handling

## Implementation Notes
- The current ingestion flow writes a row to `advisory_status` first, then references it via FK when inserting the advisory. The new flow sets the `status` field directly on the advisory `ActiveModel` with the enum value.
- Map incoming status strings to `AdvisoryStatusEnum` variants: "New" -> `AdvisoryStatusEnum::New`, "Analyzing" -> `AdvisoryStatusEnum::Analyzing`, "Fixed" -> `AdvisoryStatusEnum::Fixed`, "Rejected" -> `AdvisoryStatusEnum::Rejected`
- Handle case-insensitive matching for robustness (advisory feeds may use inconsistent casing)
- Produce a clear error message for unrecognized status values rather than silently defaulting
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` for error handling in ingestion functions.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's handler/service file scope.
- See `modules/ingestor/src/graph/sbom/mod.rs` for the standard ingestion pattern (SBOM ingestion follows a similar parse-store-link flow)
- Remove any `use entity::advisory_status` imports from ingestion code

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference ingestion implementation following the standard parse-store-link pattern
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3 that this task uses for status mapping

## Acceptance Criteria
- [ ] Ingestion pipeline writes `advisory_status_enum` values directly to the `status` column
- [ ] No references to `advisory_status` entity or lookup table remain in ingestion code
- [ ] Status string mapping handles all four valid values (New, Analyzing, Fixed, Rejected)
- [ ] Invalid status strings produce meaningful error messages

## Test Requirements
- [ ] Ingestion of advisories with each status value succeeds
- [ ] Ingestion with an invalid status value produces a clear error
- [ ] Ingestion pipeline compiles without errors (`cargo check -p ingestor`)

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions (ingestion uses the updated entity type with AdvisoryStatusEnum)
