# Task 5 — Update advisory ingestion pipeline to write enum status directly

**Priority:** High
**Fix Versions:** RHTPA 2.0.0
**Labels:** ai-generated-jira

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the status as an enum value directly on the `advisory` row instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. The pipeline should map the status string from the advisory feed to the `AdvisoryStatusEnum` Rust enum and set it on the advisory entity during insertion.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` — replace status lookup table insert + FK assignment with direct enum column assignment; map incoming status strings to `AdvisoryStatusEnum` variants
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it contains any advisory status lookup table references

## Implementation Notes
- The current ingestion flow likely:
  1. Looks up or inserts a row in `advisory_status` for the given status string
  2. Uses the returned `id` to set `advisory.status_id`
- The new flow should:
  1. Parse the status string from the feed into an `AdvisoryStatusEnum` variant
  2. Set `advisory.status = AdvisoryStatusEnum::Fixed` (or whichever variant matches) directly
- Add validation/error handling for unrecognized status strings — if the feed contains a status not in the enum (New, Analyzing, Fixed, Rejected), return an appropriate error rather than silently dropping the advisory
- Per CONVENTIONS.md Key Conventions: all handlers return `Result<T, AppError>` with `.context()` wrapping (Error handling convention). Use `.context("Failed to parse advisory status")` on the status parsing.
  Applies: task modifies `modules/ingestor/src/graph/advisory/mod.rs` matching the convention's Rust module scope.
- Follow the ingestion patterns established in `modules/ingestor/src/graph/sbom/mod.rs` for how entities are constructed and inserted

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` — reference for entity ingestion pattern (parse, construct, insert) without lookup table dependencies
- `entity/src/advisory_status_enum.rs` — the enum definition created in Task 3, to be imported and used for status mapping

## Acceptance Criteria
- [ ] Advisory ingestion writes the enum status value directly to the `advisory.status` column
- [ ] No code references the `advisory_status` lookup table for ingestion
- [ ] Unrecognized status strings produce a clear error
- [ ] Ingestion of advisories with all four valid statuses (New, Analyzing, Fixed, Rejected) succeeds

## Test Requirements
- [ ] Verify the ingestor module compiles (`cargo check -p ingestor`)
- [ ] Verify ingestion of an advisory with status "Fixed" writes the correct enum value
- [ ] Verify ingestion of an advisory with an unrecognized status produces an error

## Verification Commands
- `cargo check -p ingestor` — ingestor module compiles without errors

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main

[sdlc-workflow] Description digest: sha256-md:e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2c3d4e5f6
