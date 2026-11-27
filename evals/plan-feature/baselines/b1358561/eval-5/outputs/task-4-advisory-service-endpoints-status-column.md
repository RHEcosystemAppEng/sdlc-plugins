**Summary:** Use advisory.status column in AdvisoryService and advisory endpoints
**Epic:** TC-9005: Advisory status query and ingestion updates

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Remove the `advisory_status` join from all advisory queries in the fundamental module. `AdvisoryService` fetch/list/search and the `GET /api/v2/advisory` / `GET /api/v2/advisory/{id}` endpoints must read and filter on `advisory.status` directly (UC-1: `WHERE status = 'Fixed'`, no join). The response shape is unchanged — `status` is still serialized as a string.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — drop the `advisory_status` join in fetch/list/search; filter on `advisory::Column::Status`
- `modules/fundamental/src/advisory/endpoints/list.rs` — parse the `status` filter query parameter into `AdvisoryStatus`; reject unknown values
- `modules/fundamental/src/advisory/endpoints/get.rs` — remove any status lookup; use `model.status`
- `modules/fundamental/src/advisory/model/summary.rs` — populate `AdvisorySummary` status string from `AdvisoryStatus`
- `modules/fundamental/src/advisory/model/details.rs` — populate `AdvisoryDetails` status string from `AdvisoryStatus`
- `tests/api/advisory.rs` — update/add integration tests for status filtering and response shape

## API Changes
- `GET /api/v2/advisory` — MODIFY (internal only): status filter served from `advisory.status` without join; request/response shape unchanged; unknown `status` filter value returns 400 instead of an empty list
- `GET /api/v2/advisory/{id}` — MODIFY (internal only): status read from `advisory.status`; response shape unchanged

## Implementation Notes
- Use `entity::advisory::AdvisoryStatus` (from Task 3) for the filter and its `Display`/`as_str` for the response string — do not add another string mapping.
- Use the shared filtering/pagination helpers in `common/src/db/query.rs` for the status equality filter, and keep `PaginatedResults<T>` from `common/src/model/paginated.rs` as the list response wrapper.
- **Fail-closed filter:** today an unknown status filter would match no lookup row and return an empty, successful list. With the enum, an unparsable `status` value must return `AppError` (400 Bad Request) — never silently produce `[]`. The guard belongs in `modules/fundamental/src/advisory/endpoints/list.rs` where the query parameter is parsed, before calling `AdvisoryService` list.
- Response strings must remain exactly `New`, `Analyzing`, `Fixed`, `Rejected` so the JSON is byte-compatible with the pre-change API (Customer Considerations).
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` and wrap fallible calls with `.context()`. Applies: task modifies modules/fundamental/src/advisory/endpoints/list.rs matching the convention's Rust handler (`.rs`) scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Query helpers: use `common/src/db/query.rs` for filtering, pagination, sorting. Applies: task modifies modules/fundamental/src/advisory/service/advisory.rs matching the convention's Rust (`.rs`) service scope. Example: `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`. Applies: task modifies modules/fundamental/src/advisory/endpoints/list.rs matching the convention's Rust (`.rs`) list endpoint scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` against real PostgreSQL using `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/advisory.rs matching the convention's Rust (`.rs`) integration test scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §2 commit rules; §3 PR `--base TC-9005`, PR link posted to Jira; §5 scope limited to listed files, inspect before modifying, no duplicated functionality.

## Reuse Candidates
- `common/src/db/query.rs` — shared filter/pagination/sort helpers for the status filter
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper
- `entity/src/advisory.rs::AdvisoryStatus` — enum and string conversion (Task 3)
- `common/src/error.rs::AppError` — 400 for invalid status filter

## Acceptance Criteria
- [ ] No advisory query in `modules/fundamental` references `advisory_status` (table, entity, or relation)
- [ ] `GET /api/v2/advisory?status=Fixed` returns only Fixed advisories, filtered on `advisory.status`
- [ ] `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}` return `status` as the same string values as before (New/Analyzing/Fixed/Rejected)
- [ ] `GET /api/v2/advisory?status=<unknown>` returns 400, not an empty 200 list
- [ ] `AdvisoryService` fetch, list, and search all compile and work against the new schema

## Test Requirements
- [ ] Integration test in `tests/api/advisory.rs`: ingest advisories with all four statuses; `GET /api/v2/advisory?status=Fixed` returns only Fixed ones
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns `status` string matching the stored enum
- [ ] Integration test: response JSON `status` field is a string with unchanged values (shape regression)
- [ ] Fail-closed test: `GET /api/v2/advisory?status=Closed` returns `StatusCode::BAD_REQUEST`

## Verification Commands
- `cargo test -p tests --test advisory` (or workspace equivalent) — advisory API tests pass
- `grep -rn "advisory_status" modules/fundamental/src` — no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity for status enum column
