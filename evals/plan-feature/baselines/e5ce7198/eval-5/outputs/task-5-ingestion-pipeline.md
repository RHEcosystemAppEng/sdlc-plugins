## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory ingestion pipeline to write the `advisory_status_enum` value directly to the `advisory.status` column instead of inserting into the `advisory_status` lookup table and referencing it via foreign key. This simplifies ingestion by removing the intermediate lookup table write.

## Files to Modify
- `modules/ingestor/src/graph/advisory/mod.rs` -- update advisory ingestion logic to map status strings to `AdvisoryStatusEnum` values and write directly to the `status` column; remove any code that inserts into or references the `advisory_status` table
- `modules/ingestor/src/service/mod.rs` -- update `IngestorService` if it references advisory status lookup table operations

## Implementation Notes
In `modules/ingestor/src/graph/advisory/mod.rs`, the current ingestion flow parses an advisory from the feed, looks up or creates a row in the `advisory_status` table, and sets `advisory.status_id` to the resulting foreign key. Replace this with:
1. Map the status string from the feed to the `AdvisoryStatusEnum` variant (e.g., `"New"` -> `AdvisoryStatusEnum::New`)
2. Set the `status` field directly on the advisory `ActiveModel` using the enum value
3. Remove any code that queries, inserts into, or references the `advisory_status` entity

Handle invalid status strings gracefully by returning an `AppError` with appropriate context, following the error handling pattern in `common/src/error.rs`.

Follow the existing ingestion patterns in `modules/ingestor/src/graph/sbom/mod.rs` for the parse-store flow structure.

## Reuse Candidates
- `modules/ingestor/src/graph/sbom/mod.rs` -- reference for ingestion graph module structure and parse-store pattern
- `common/src/error.rs` -- `AppError` for error handling on invalid status strings

## Acceptance Criteria
- [ ] Advisory ingestion writes `AdvisoryStatusEnum` values directly to `advisory.status`
- [ ] No code references the `advisory_status` table or entity in the ingestor module
- [ ] Invalid status strings from feeds produce clear error messages
- [ ] Ingestion of advisories with all four status values (New, Analyzing, Fixed, Rejected) succeeds

## Test Requirements
- [ ] Verify ingestion of an advisory with each valid status value writes the correct enum value
- [ ] Verify ingestion with an invalid status string returns an appropriate error
- [ ] Verify end-to-end ingestion: ingest an advisory, then fetch it via the API and confirm the status field is correct

## Verification Commands
- `cargo check -p trustify-ingestor` -- ingestor module compiles without errors

## Dependencies
- Depends on: Task 1 -- Create feature branch TC-9005 from main
- Depends on: Task 3 -- Entity definitions update (ingestion depends on the updated `AdvisoryStatusEnum` type)

## Jira Metadata
additional_fields: {"labels": ["ai-generated-jira"], "priority": {"name": "High"}, "fixVersions": [{"name": "RHTPA 2.0.0"}]}

[sdlc-workflow] Description digest: sha256-md:f0479cf226d82349d63c7d186f29c4ecf614a1f2c332f720c5394bb02f6cea93
