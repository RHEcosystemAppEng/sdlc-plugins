# Task 5 — Update advisory ingestion pipeline to write enum values directly

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write `advisory_status_enum` values directly to the `advisory.status` column instead of inserting rows into the `advisory_status` lookup table and referencing them via FK. The ingestion pipeline currently maps incoming advisory status strings to lookup table IDs; after this change, it maps them directly to enum values for insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace lookup table insert/reference logic with direct enum value assignment when creating or updating advisory records
- `modules/ingestor/src/service/mod.rs` — update IngestorService if it coordinates status handling through the lookup table

## Implementation Notes
- In `modules/ingestor/src/graph/advisory/mod.rs`: remove any code that inserts into or queries the `advisory_status` table. Replace with direct `AdvisoryStatusEnum` value construction from the parsed advisory feed status string
- Map incoming status strings to enum variants: `"New" -> AdvisoryStatusEnum::New`, `"Analyzing" -> AdvisoryStatusEnum::Analyzing`, `"Fixed" -> AdvisoryStatusEnum::Fixed`, `"Rejected" -> AdvisoryStatusEnum::Rejected`
- Handle edge cases: if the incoming status string does not match any known variant, apply the same error handling pattern used elsewhere in the ingestion pipeline (check `modules/ingestor/src/graph/sbom/mod.rs` for reference)
- Remove any `use entity::advisory_status` imports
- Follow the existing ingestion patterns in `modules/ingestor/src/graph/sbom/mod.rs` for entity insertion patterns
- Per docs/constraints.md section 5 (Code Change Rules): inspect ingestion code before modifying to understand current lookup table interaction

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for entity ingestion patterns (parse, store, link)
- `entity/src/advisory.rs::AdvisoryStatusEnum` — the enum type defined in Task 3 that this task will use for status assignment

## Acceptance Criteria
- [ ] Ingestion pipeline writes `advisory_status_enum` values directly to the `advisory.status` column
- [ ] No remaining references to the `advisory_status` lookup table in the ingestor module
- [ ] All four status values (New, Analyzing, Fixed, Rejected) are correctly mapped from feed input
- [ ] Invalid status strings are handled gracefully following existing error patterns

## Test Requirements
- [ ] Advisory ingestion with status "New" correctly stores `AdvisoryStatusEnum::New` in the status column
- [ ] Advisory ingestion with status "Fixed" correctly stores `AdvisoryStatusEnum::Fixed`
- [ ] Advisory ingestion with an unrecognized status string produces an appropriate error
- [ ] Existing advisory ingestion test scenarios continue to pass with the updated code

## Verification Commands
- `cargo build -p trustify-ingestor` — ingestor module compiles
- `cargo test -p trustify-ingestor` — ingestor module tests pass
- `grep -r "advisory_status" modules/ingestor/src/` — returns no results

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM entity definitions for advisory status enum

[sdlc-workflow] Description digest: sha256-md:0b40a36b9d10e3853405bcac68a5d9be494752a03882ff6d9945aae0af166414
