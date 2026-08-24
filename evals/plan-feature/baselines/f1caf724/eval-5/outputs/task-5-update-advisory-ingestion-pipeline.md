## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and setting a foreign key. The ingestion code currently parses the advisory status from the feed, looks up or inserts the status in the `advisory_status` table, and sets `status_id` on the advisory row. After this change, the pipeline maps the status string to the `AdvisoryStatusEnum` variant and sets it directly on the advisory insert.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert + FK assignment with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants; remove any `advisory_status` entity imports

## Implementation Notes
The ingestion pipeline in `modules/ingestor/src/graph/advisory/mod.rs` currently performs:
1. Parse status string from advisory feed
2. Query or insert into `advisory_status` table to get `status_id`
3. Set `status_id` on the advisory `ActiveModel`

After this change:
1. Parse status string from advisory feed
2. Map string to `AdvisoryStatusEnum` variant (New, Analyzing, Fixed, Rejected)
3. Set `status` field directly on the advisory `ActiveModel`

Add a mapping function or match expression:
```rust
fn parse_advisory_status(s: &str) -> Result<AdvisoryStatusEnum, AppError> {
    match s {
        "New" => Ok(AdvisoryStatusEnum::New),
        "Analyzing" => Ok(AdvisoryStatusEnum::Analyzing),
        "Fixed" => Ok(AdvisoryStatusEnum::Fixed),
        "Rejected" => Ok(AdvisoryStatusEnum::Rejected),
        other => Err(AppError::BadRequest(format!("Unknown advisory status: {}", other))),
    }
}
```

Handle case-insensitive matching if the feed may provide status values in different cases.

Per CONVENTIONS.md §Error handling: all service code returns `Result<T, AppError>` with `.context()` wrapping for error propagation.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's handler file scope.

## Reuse Candidates
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3; import and use directly for status assignment
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for the ingestion pattern used by SBOM ingestion (similar parse-and-store flow)

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to the `status` column
- [ ] No references to `advisory_status` table or entity remain in the ingestor module
- [ ] Status string mapping handles all four valid values (New, Analyzing, Fixed, Rejected)
- [ ] Invalid status strings produce a clear error via `AppError`
- [ ] Ingestion of existing advisory feeds continues to work correctly

## Test Requirements
- [ ] Verify advisory ingestion correctly maps "New", "Analyzing", "Fixed", "Rejected" to enum variants
- [ ] Verify advisory ingestion rejects unknown status strings with an appropriate error
- [ ] Verify ingested advisories have correct status values in the database

## Verification Commands
- `cargo check -p trustify-ingestor` — ingestor module compiles successfully
- `cargo test -p trustify-ingestor -- advisory` — advisory ingestion tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
