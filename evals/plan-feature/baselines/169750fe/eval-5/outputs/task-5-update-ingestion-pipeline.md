## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write enum values directly to the `status` column on the `advisory` table instead of inserting into the `advisory_status` lookup table. The pipeline currently maps incoming advisory status strings to lookup table rows and stores a foreign key reference; after this change, it maps status strings directly to `AdvisoryStatusEnum` values and stores the enum value inline.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insertion logic with direct enum value mapping; update `ActiveModel` construction to set `status` field with `AdvisoryStatusEnum` value instead of `status_id`

## Implementation Notes
In the advisory ingestion module (`modules/ingestor/src/graph/advisory/mod.rs`), locate the code that:
1. Looks up or inserts a row in the `advisory_status` table to get a `status_id`
2. Sets `status_id` on the advisory `ActiveModel`

Replace this with direct enum mapping:
```rust
let status = match status_string.as_str() {
    "New" => AdvisoryStatusEnum::New,
    "Analyzing" => AdvisoryStatusEnum::Analyzing,
    "Fixed" => AdvisoryStatusEnum::Fixed,
    "Rejected" => AdvisoryStatusEnum::Rejected,
    _ => return Err(AppError::BadRequest(format!("Unknown advisory status: {}", status_string))),
};
model.status = Set(status);
```

Remove any `use` statements for the `advisory_status` entity.

Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping for invalid status string mapping errors.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module scope.

Per CONVENTIONS.md §Module pattern: maintain the graph ingestion module structure.
Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module scope.

## Acceptance Criteria
- [ ] Ingestion pipeline maps status strings directly to `AdvisoryStatusEnum` values
- [ ] Advisory `ActiveModel` sets `status` field with enum value instead of `status_id`
- [ ] No references to `advisory_status` table or entity remain in the ingestor module
- [ ] Invalid status strings produce a meaningful error message
- [ ] Existing ingestion feeds continue to be processed correctly

## Test Requirements
- [ ] Ingestion of advisory with each valid status (New, Analyzing, Fixed, Rejected) succeeds
- [ ] Ingestion of advisory with invalid status produces appropriate error
- [ ] Ingested advisories are queryable via the updated service layer

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update entity definitions (ingestion uses the updated entity types)
