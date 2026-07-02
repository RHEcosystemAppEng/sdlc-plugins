## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST API endpoints to use the `status` enum column for filtering and query operations. The endpoint handlers in `modules/fundamental/src/advisory/endpoints/` must pass status filter parameters as enum values instead of relying on the joined `advisory_status` table. The response shape remains unchanged (status is still a string in the API response), so this is a backend-internal change with no user-facing API contract modification.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to use `AdvisoryStatusEnum` for query filtering instead of joining `advisory_status`
- `modules/fundamental/src/advisory/endpoints/get.rs` — update individual advisory retrieval if it references status via join
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if status filter parameter types change

## Implementation Notes
- In `list.rs`, the status filter query parameter is likely a string that was previously used to filter via `.filter(advisory_status::Column::Name.eq(value))`. Update this to parse the string into `AdvisoryStatusEnum` and filter via `.filter(advisory::Column::Status.eq(parsed_enum))`.
- Add validation for the status filter parameter — if a client provides an invalid status string, return a 400 Bad Request with a clear error message listing valid values (New, Analyzing, Fixed, Rejected).
- The response serialization should not change — the enum `Display` or `Serialize` implementation should produce the same string values that the lookup table previously stored.
- In `get.rs`, if the detail endpoint joins `advisory_status`, remove the join and use the direct column.
- Follow the endpoint pattern in `modules/fundamental/src/sbom/endpoints/list.rs` for Axum handler structure.
- All handlers must return `Result<T, AppError>` per the repository's error handling convention.
- Per repo Key Conventions: framework is Axum for HTTP; error handling uses `Result<T, AppError>` with `.context()` wrapping; endpoint registration follows the pattern in each module's `endpoints/mod.rs`.

## Reuse Candidates
- `modules/fundamental/src/sbom/endpoints/list.rs` — reference for list endpoint handler pattern with query parameters and pagination
- `modules/fundamental/src/advisory/endpoints/list.rs` — current implementation (pre-modification) showing the existing filter logic to update
- `common/src/db/query.rs` — shared query builder helpers that the endpoint delegates to

## Acceptance Criteria
- [ ] Advisory list endpoint accepts status filter and queries enum column directly
- [ ] Advisory list endpoint returns correct results when filtering by status
- [ ] Advisory get endpoint returns correct status from enum column
- [ ] Invalid status filter values return 400 Bad Request with valid values listed
- [ ] API response shape is unchanged (status is still a string field)
- [ ] No references to `advisory_status` table remain in endpoint code

## Test Requirements
- [ ] Verify `GET /api/v2/advisory?status=Fixed` returns only advisories with Fixed status
- [ ] Verify `GET /api/v2/advisory?status=InvalidValue` returns 400 error
- [ ] Verify `GET /api/v2/advisory/{id}` returns advisory with correct status string
- [ ] Verify response shape matches the pre-migration format

## Verification Commands
- `cargo build -p trustify-fundamental` — verify endpoint code compiles
- `cargo test -p trustify-fundamental -- advisory::endpoints` — run endpoint-specific tests

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 4 — Update advisory service and model to use status enum column

## Labels
- ai-generated-jira

## additional_fields
- priority: High
- fixVersions: RHTPA 2.0.0

[sdlc-workflow] Description digest: sha256-md:25affe6a5e41fb409d5896dd84bfa44d3a7dc32d7b3c45b34a00aa782480a079
