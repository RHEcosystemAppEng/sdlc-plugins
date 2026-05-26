# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly on the advisory row instead of first inserting into the `advisory_status` lookup table and then referencing it via foreign key. This simplifies the ingestion path by eliminating the lookup table write and the subsequent FK reference.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — Remove logic that inserts into or looks up from the `advisory_status` table; map the status string from the advisory feed directly to an `AdvisoryStatusEnum` variant; set the `status` field on the advisory `ActiveModel` instead of `status_id`
- `modules/ingestor/src/service/mod.rs` — Update `IngestorService` if it references advisory status lookup table operations or status_id assignment

## Implementation Notes
- The current ingestion flow likely: (1) looks up or inserts the status in `advisory_status`, (2) gets the `id`, (3) sets `status_id` on the advisory. Replace this with: (1) parse the status string, (2) map to `AdvisoryStatusEnum` variant, (3) set `status` on the advisory `ActiveModel`.
- Use a match expression to convert the feed status string to `AdvisoryStatusEnum`:
  ```
  match status_str {
      "New" => AdvisoryStatusEnum::New,
      "Analyzing" => AdvisoryStatusEnum::Analyzing,
      "Fixed" => AdvisoryStatusEnum::Fixed,
      "Rejected" => AdvisoryStatusEnum::Rejected,
      _ => return Err(...)  // handle unknown status
  }
  ```
- Follow the existing pattern in `modules/ingestor/src/graph/sbom/mod.rs` for how SBOM ingestion handles entity creation without lookup tables.
- Remove any `use entity::advisory_status` imports from the ingestor module.
- Per constraints doc section 5 (Code Change Rules): inspect the existing ingestion code before modifying to understand the current flow.
- Per constraints doc section 2 (Commit Rules): commit message must reference TC-9005 and follow Conventional Commits format.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — SBOM ingestion showing the established pattern for entity creation without lookup table indirection
- `entity/src/advisory.rs::AdvisoryStatusEnum` — The enum type defined in Task 3 that the ingestion code must use for the status field

## Acceptance Criteria
- [ ] Advisory ingestion writes the `status` enum value directly on the advisory row
- [ ] No references to `advisory_status` table or `status_id` remain in the ingestor module
- [ ] Unknown status strings are handled with an appropriate error (not silently ignored)
- [ ] `cargo check -p trustify-module-ingestor` succeeds

## Test Requirements
- [ ] Ingestion of an advisory with each valid status (New, Analyzing, Fixed, Rejected) succeeds and stores the correct enum value
- [ ] Ingestion of an advisory with an unknown status produces an appropriate error
- [ ] End-to-end ingestion test: ingest an advisory, then query it via the advisory service and verify the status is correct

## Verification Commands
- `cargo check -p trustify-module-ingestor` — compiles without errors
- `cargo test -p trustify-module-ingestor` — all existing tests pass

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum
