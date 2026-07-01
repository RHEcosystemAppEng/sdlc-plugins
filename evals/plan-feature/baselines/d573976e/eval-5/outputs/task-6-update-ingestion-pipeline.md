## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `AdvisoryStatusEnum` values directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via FK. The pipeline must map incoming status strings from advisory feeds to the correct enum variant and insert them directly on the advisory row.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace the lookup table insert-or-find logic (which currently writes to `advisory_status` and retrieves an ID) with direct enum value assignment; map incoming status strings to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it orchestrates status resolution or references the lookup table; update imports for `AdvisoryStatusEnum`

## Implementation Notes
- The current ingestion flow likely: (1) parses the status string from the advisory feed, (2) looks up or inserts a row in `advisory_status`, (3) uses the resulting `id` as `status_id` on the advisory row
- Replace this with: (1) parse the status string, (2) map it to an `AdvisoryStatusEnum` variant using pattern matching, (3) set the `status` field directly on the `ActiveModel`
- Implement a robust string-to-enum mapping function that handles case variations in the feed data:
  ```rust
  fn parse_status(s: &str) -> Result<AdvisoryStatusEnum, AppError> {
      match s.to_lowercase().as_str() {
          "new" => Ok(AdvisoryStatusEnum::New),
          "analyzing" => Ok(AdvisoryStatusEnum::Analyzing),
          "fixed" => Ok(AdvisoryStatusEnum::Fixed),
          "rejected" => Ok(AdvisoryStatusEnum::Rejected),
          _ => Err(AppError::BadRequest(format!("Unknown advisory status: {}", s))),
      }
  }
  ```
- Remove any imports of `advisory_status::Entity` or `advisory_status::ActiveModel` from the ingestor module
- Error handling for unknown status values should use `AppError` with `.context()` per project conventions
- Follow the existing ingestion pattern in `modules/ingestor/src/graph/sbom/mod.rs` for how entities are constructed and inserted

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for the ingestion pattern: parse → construct entity → insert, without lookup table indirection
- `modules/ingestor/src/graph/advisory/mod.rs` — current implementation to understand the existing status resolution flow before modifying
- `common/src/error.rs` — `AppError` enum for error handling patterns

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status`
- [ ] No code in the ingestor module references `advisory_status` entity or table
- [ ] All four status values (New, Analyzing, Fixed, Rejected) are correctly mapped from feed input
- [ ] Unknown status values produce a clear error rather than a panic or silent failure
- [ ] Ingested advisories have the correct status value when queried via the API

## Test Requirements
- [ ] Integration test: ingest an advisory with each of the four status values and verify the correct enum value is stored
- [ ] Integration test: ingest an advisory with an unknown status value and verify an error is returned
- [ ] Verify end-to-end: ingest an advisory, then query it via `GET /api/v2/advisory/{id}` and confirm the status matches

## Verification Commands
- `cargo test -p ingestor` — ingestor tests pass
- `cargo test -p tests --test advisory` — end-to-end advisory tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions
