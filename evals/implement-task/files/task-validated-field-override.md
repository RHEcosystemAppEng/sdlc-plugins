<!-- SYNTHETIC TEST DATA — task where a generic merge path can override a newly validated field -->

# Mock Jira Task

**Key**: TC-9212
**Summary**: Add validated data classification to the SBOM ingest payload builder
**Status**: To Do
**Labels**: ai-generated-jira
**Linked Issues**: is incorporated by TC-9001

---

## Repository
trustify-backend

## Target Branch
main

## Description
Add a `data_classification` field to the SBOM ingest payload built by
`SbomService::build_ingest_payload()`. Only `public`, `internal` and `restricted` are
valid values; anything else must be rejected before the payload is sent. The payload
builder already accepts a caller-supplied `extra_fields` map that is merged into the
payload last, after the standardized fields are written.

## Files to Modify
- `modules/fundamental/src/sbom/service/sbom.rs` — add the validated `data_classification`
  field to `build_ingest_payload()` and ensure the later `extra_fields` merge cannot
  replace or remove it
- `modules/fundamental/src/sbom/model/details.rs` — add the `data_classification` field to
  `SbomDetails`

## Files to Create
- `tests/service/sbom_ingest_payload.rs` — unit tests for the payload builder

## API Changes
- `POST /api/v2/sbom/ingest` — request body gains `data_classification`, one of
  `public`, `internal`, `restricted`

## Implementation Notes
- `build_ingest_payload()` in `modules/fundamental/src/sbom/service/sbom.rs` currently
  writes the standardized fields into a map and then merges `extra_fields` into the same
  map at the end of the function
- Validate `data_classification` against the allowed set and return `AppError` with
  `.context()` on an invalid value, matching `common/src/error.rs`
- Existing callers pass `extra_fields` through unchanged; do not rename the parameter
- Response and payload types follow the struct patterns in `modules/fundamental/src/sbom/model/`

## Acceptance Criteria
- [ ] `build_ingest_payload()` rejects a `data_classification` outside the allowed set
- [ ] A payload built with a valid classification always carries that value
- [ ] A caller-supplied `extra_fields` entry cannot change the validated classification

## Test Requirements
- [ ] Test that each allowed classification is accepted and lands in the payload
- [ ] Test that a disallowed classification is rejected
- [ ] Test that `extra_fields` containing the classification key cannot override the validated value

## Dependencies
- Depends on: None
