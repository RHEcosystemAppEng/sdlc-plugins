## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. The pipeline must map status strings from the advisory feed to `AdvisoryStatusEnum` variants.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace the lookup table insert-and-reference pattern with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants; remove any code that reads from or writes to the `advisory_status` table

## Implementation Notes
- The current ingestion flow likely: (1) checks if the status exists in `advisory_status`, (2) inserts it if not, (3) uses the returned `id` as `status_id` on the advisory. Replace this with: (1) parse the status string to `AdvisoryStatusEnum`, (2) set `status` directly on the advisory `ActiveModel`.
- Handle unmapped status strings gracefully — if the feed provides a status that does not match any enum variant, log a warning and either skip the advisory or default to a sensible value (e.g., `New`). Document the decision in the code.
- Per CONVENTIONS.md §Error Handling: use `Result<T, AppError>` with `.context()` wrapping for ingestion operations.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust service file scope.
- Per CONVENTIONS.md §Framework: use SeaORM `ActiveModel` for inserting advisory records with the enum status field.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust file scope.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for SBOM ingestion patterns; follow the same structure for advisory ingestion
- `entity/src/advisory.rs` — the updated advisory entity with `AdvisoryStatusEnum`; import and use directly

## Acceptance Criteria
- [ ] Advisory ingestion writes the `status` enum value directly to the `advisory` table
- [ ] No code in the ingestion pipeline reads from or writes to the `advisory_status` table
- [ ] Status string mapping handles all four valid values: New, Analyzing, Fixed, Rejected
- [ ] Unmapped or invalid status strings are handled gracefully with appropriate logging
- [ ] The ingestor crate compiles without errors

## Test Requirements
- [ ] Verify advisory ingestion with each valid status value produces correct enum column value
- [ ] Verify advisory ingestion with an unknown status string handles the error gracefully
- [ ] Verify round-trip: ingest an advisory, then read it back via the service layer and confirm the status is correct

## Verification Commands
- `cargo check -p trustify-ingestor` — verify the ingestor crate compiles
- `cargo test -p trustify-ingestor` — run existing ingestor tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
