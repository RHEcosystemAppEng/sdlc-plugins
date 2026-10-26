## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum status values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline currently maps advisory status strings from ingested feeds to rows in the `advisory_status` table and writes the `status_id`. After this change, the pipeline maps status strings directly to `AdvisoryStatusEnum` values and writes them to the `status` enum column.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace the lookup table insert-and-reference pattern with direct enum value assignment; update the advisory insertion to set `status: AdvisoryStatusEnum::<variant>` instead of `status_id: <looked-up-id>`

## Implementation Notes
The current ingestion flow likely follows this pattern:
1. Parse status string from the advisory feed
2. Look up or insert the status in the `advisory_status` table
3. Use the returned `status_id` as a foreign key on the advisory insert

Replace this with:
1. Parse status string from the advisory feed
2. Map the string to an `AdvisoryStatusEnum` variant using `match` or `TryFrom`
3. Set the `status` field directly on the advisory `ActiveModel`

Add a mapping function that converts raw status strings to enum variants with proper error handling for unknown values:

```rust
fn parse_advisory_status(raw: &str) -> Result<AdvisoryStatusEnum, AppError> {
    match raw {
        "New" | "new" => Ok(AdvisoryStatusEnum::New),
        "Analyzing" | "analyzing" => Ok(AdvisoryStatusEnum::Analyzing),
        "Fixed" | "fixed" => Ok(AdvisoryStatusEnum::Fixed),
        "Rejected" | "rejected" => Ok(AdvisoryStatusEnum::Rejected),
        other => Err(AppError::BadRequest(format!("Unknown advisory status: {}", other))),
    }
}
```

Remove any code that queries or inserts into the `advisory_status` table. After this change, the ingestor module should have no dependency on the `advisory_status` entity.

Per CONVENTIONS.md §Error Handling: all service/handler functions return `Result<T, AppError>` with `.context()` wrapping. Apply this to the new status parsing error path.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's `.rs` module file scope.

## Reuse Candidates
- `common/src/error.rs::AppError` — error enum for consistent error handling; use for unknown status string errors during ingestion
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3 that this task must use for mapping

## Acceptance Criteria
- [ ] Advisory ingestion writes enum values directly to the `advisory.status` column
- [ ] No code in the ingestor module references the `advisory_status` table or `status_id` column
- [ ] Unknown status strings from advisory feeds produce a clear error (not a panic or silent failure)
- [ ] The ingestion pipeline handles all four valid status values (New, Analyzing, Fixed, Rejected)
- [ ] The ingestor module compiles without errors (`cargo check -p trustify-module-ingestor`)

## Test Requirements
- [ ] Verify ingestion of an advisory with each valid status value (New, Analyzing, Fixed, Rejected) writes the correct enum value
- [ ] Verify ingestion of an advisory with an unknown status string returns an appropriate error
- [ ] Verify no queries or inserts to the `advisory_status` table occur during ingestion

## Verification Commands
- `cargo check -p trustify-module-ingestor` — module compiles without errors
- `grep -r "advisory_status" modules/ingestor/` — returns no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
