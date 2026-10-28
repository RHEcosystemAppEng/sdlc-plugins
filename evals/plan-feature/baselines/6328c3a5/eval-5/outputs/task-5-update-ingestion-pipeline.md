## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write advisory status as an enum value directly on the `advisory` table row, instead of inserting into the `advisory_status` lookup table and creating a foreign key reference. The pipeline must map status strings from the advisory feed to `AdvisoryStatusEnum` values.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- replace lookup table insert and FK assignment with direct enum value assignment on the advisory row

## Implementation Notes
- The current ingestion flow inserts a row into `advisory_status` and then sets `advisory.status_id` to reference it. Replace this with setting `advisory.status = AdvisoryStatusEnum::from_str(status_string)`.
- Add a mapping function or use SeaORM's `FromStr` derive to convert the feed's status string (e.g., "New", "Analyzing", "Fixed", "Rejected") to the `AdvisoryStatusEnum` variant.
- Handle unknown status values gracefully: if the feed contains a status string that does not match any enum variant, log a warning and default to `AdvisoryStatusEnum::New` or return an error, depending on the existing error handling pattern in the ingestion pipeline.
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for structure and error handling.

Per CONVENTIONS.md §Error Handling: maintain `Result<T, AppError>` with `.context()` wrapping on ingestion operations.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- sibling ingestion module showing the project's ingestion patterns
- `entity/src/advisory.rs` -- `AdvisoryStatusEnum` type definition (from Task 3)

## Acceptance Criteria
- [ ] Advisory ingestion writes the `status` enum value directly on the advisory row
- [ ] No inserts to the (now-dropped) `advisory_status` lookup table
- [ ] Status string from the feed is correctly mapped to `AdvisoryStatusEnum` variants
- [ ] Unknown status values are handled gracefully (logged warning or error)

## Test Requirements
- [ ] Ingestion of an advisory with status "Fixed" results in `advisory.status = Fixed` enum value
- [ ] Ingestion of an advisory with each valid status (New, Analyzing, Fixed, Rejected) produces the correct enum value
- [ ] Ingestion of an advisory with an unknown status value is handled without panic

## Verification Commands
- `cargo check -p ingestor` -- ingestor module compiles without errors
- `cargo test -p ingestor` -- ingestor module tests pass

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Update SeaORM entity definitions for advisory status enum
