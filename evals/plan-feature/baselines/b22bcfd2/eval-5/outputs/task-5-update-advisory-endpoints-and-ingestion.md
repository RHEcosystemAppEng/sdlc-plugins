## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the advisory REST endpoints to use the new enum-based status field and update the advisory ingestion pipeline to write enum values directly instead of inserting into the lookup table. This completes the code-level migration away from the `advisory_status` table.

## Files to Modify
- `modules/fundamental/src/advisory/endpoints/list.rs` — update status filter parameter handling to use `AdvisoryStatusEnum` values; remove any references to advisory_status entity in query construction
- `modules/fundamental/src/advisory/endpoints/get.rs` — update status field mapping in response construction if directly accessing entity fields
- `modules/fundamental/src/advisory/endpoints/mod.rs` — update route registration if any status-related query parameters change type
- `modules/ingestor/src/graph/advisory/mod.rs` — change advisory ingestion to write `AdvisoryStatusEnum` value directly to `advisory.status` column instead of inserting into `advisory_status` table and using the returned ID for `status_id`
- `modules/ingestor/src/service/mod.rs` — update `IngestorService` if it references advisory status insertion logic

## Implementation Notes
In `modules/fundamental/src/advisory/endpoints/list.rs`:
- The current list endpoint accepts a status filter query parameter. Update the filter logic to parse the string parameter into an `AdvisoryStatusEnum` value and filter with `.filter(advisory::Column::Status.eq(parsed_enum_value))`.
- Continue using `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs` for the response type.

In `modules/ingestor/src/graph/advisory/mod.rs`:
- The current ingestion flow inserts a row into `advisory_status` (or looks up an existing one) to get the `status_id`. Replace this with direct enum mapping: parse the status string from the advisory feed into an `AdvisoryStatusEnum` variant and set it on the `advisory` active model's `status` field.
- Remove any `advisory_status::ActiveModel` usage.

In the endpoints:
- Error handling should continue to use `Result<T, AppError>` with `.context()` wrapping per the project conventions.
- Route registration in `modules/fundamental/src/advisory/endpoints/mod.rs` should remain at `/api/v2/advisory`.

## Acceptance Criteria
- [ ] Advisory list endpoint correctly filters by enum status values
- [ ] Advisory get endpoint returns status from enum column
- [ ] Advisory ingestion writes enum values directly without touching advisory_status table
- [ ] All endpoints return `Result<T, AppError>` with proper error handling
- [ ] No remaining references to `advisory_status` entity in endpoints or ingestor code

## Test Requirements
- [ ] GET /api/v2/advisory returns advisories with correct status strings
- [ ] GET /api/v2/advisory with status filter returns only matching advisories
- [ ] GET /api/v2/advisory/{id} returns correct status for a specific advisory
- [ ] Advisory ingestion correctly maps status strings to enum values
- [ ] Ingestion of advisory with unknown status produces a meaningful error

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005
- Depends on: Task 4 — Update advisory service and models
