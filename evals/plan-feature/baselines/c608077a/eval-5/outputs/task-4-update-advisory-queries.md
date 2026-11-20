# Task 4 — Replace advisory_status joins with advisory.status column in advisory and search queries

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update every advisory query in the service and endpoint layers to read and filter on the new `advisory.status` enum column instead of joining the `advisory_status` lookup table. This delivers the Feature's primary goal — eliminating the join from all advisory queries and reducing advisory list p95 latency — while keeping the API response shape identical (status remains a string). Covers UC-1 (advisory list with status filter: `WHERE status = 'Fixed'`, no join).

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove the `advisory_status` join from `AdvisoryService` fetch, list, and search queries; select and filter on `advisory::Column::Status`
- `modules/fundamental/src/advisory/model/summary.rs` — populate `AdvisorySummary` status from `advisory::Model.status` instead of the joined lookup row
- `modules/fundamental/src/advisory/model/details.rs` — populate `AdvisoryDetails` status from `advisory::Model.status` instead of the joined lookup row
- `modules/fundamental/src/advisory/endpoints/list.rs` — parse the status filter query parameter into `AdvisoryStatus` and pass it to the service as a column filter
- `modules/search/src/service/mod.rs` — remove any `advisory_status` join/reference used when searching advisories in `SearchService`; use `advisory.status`
- `tests/api/advisory.rs` — update/add integration tests for list (with and without status filter) and get
- `tests/api/search.rs` — update/add integration test confirming advisory search results still include correct status

## API Changes
- `GET /api/v2/advisory` — MODIFY (internal only): status filter is applied on `advisory.status` without a join; request parameters and response shape unchanged
- `GET /api/v2/advisory/{id}` — MODIFY (internal only): status read from `advisory.status`; response shape unchanged

## Implementation Notes
- Cross-cutting call-site enumeration: the removal of `entity::advisory_status` and `advisory.status_id` (Task 3) breaks every consumer of that entity/column. From the repository structure, the consumers in the query path are: `AdvisoryService` (`modules/fundamental/src/advisory/service/advisory.rs`), the advisory models (`model/summary.rs`, `model/details.rs`), the list endpoint filter (`endpoints/list.rs`), and `SearchService` (`modules/search/src/service/mod.rs`, full-text search across entities including advisories). The ingestion writer is handled in Task 5. Before starting, run `grep -rn "advisory_status\|status_id" modules/ common/ server/ tests/` on the TC-9005 branch; any additional hit outside the ingestor (e.g., `modules/fundamental/src/sbom/service/sbom.rs` if SBOM details embed advisory status via `entity/src/sbom_advisory.rs`) must also be updated in this task — the codebase search is authoritative over this list.
- `modules/fundamental/src/advisory/endpoints/get.rs` only calls the service fetch; after the service change it should compile unchanged — verify and only modify if it references the lookup entity directly.
- Use the shared query helpers in `common/src/db/query.rs` for filtering, pagination, and sorting — express the status filter as a simple column equality filter on `advisory::Column::Status` rather than hand-written SQL.
- List endpoint must keep returning `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`.
- Status filter parsing: convert the incoming filter string with the fallible `AdvisoryStatus` conversion from Task 3. An unrecognized status value must return a `400 Bad Request` via `AppError` (`common/src/error.rs`) — do not silently drop the filter and return the unfiltered list (that would be a silent fail-open on the filter).
- Keep JSON field name and string values for status identical to the current response (Customer Considerations: no user-facing API changes); `AdvisorySummary` already includes a severity field — follow the same pattern for status.
- Per CONVENTIONS.md §Module pattern: keep query logic in `service/`, response structs in `model/`, and HTTP handling in `endpoints/`. Applies: task modifies modules/fundamental/src/advisory/service/advisory.rs matching the convention's domain-module (`model/ + service/ + endpoints/`) scope. See `modules/fundamental/src/sbom/` for the established layout.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` and wrap fallible calls with `.context()`. Applies: task modifies modules/fundamental/src/advisory/endpoints/list.rs matching the convention's endpoint handler scope. See `modules/fundamental/src/sbom/endpoints/list.rs` for the established pattern.
- Per CONVENTIONS.md §Query helpers: use the shared filtering/pagination/sorting helpers instead of custom query code. Applies: task modifies modules/fundamental/src/advisory/service/advisory.rs matching the convention's service query scope. See `common/src/db/query.rs` and its use in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`. Applies: task modifies modules/fundamental/src/advisory/endpoints/list.rs matching the convention's list endpoint scope. See `common/src/model/paginated.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` run against a real PostgreSQL test database and assert with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/advisory.rs matching the convention's `tests/api/` scope. See `tests/api/sbom.rs` for the established pattern.
- Constraints (docs/constraints.md): commits must reference the Jira task ID in the footer (§2.1), follow Conventional Commits (§2.2), and include an `Assisted-by:` trailer (§2.3); the PR must be opened with `--base TC-9005` (§3.3) and its link posted to the Jira task (§3.2); changes scoped to the listed files (§5.1) — if the grep finds additional consumers, add them explicitly in the PR description; inspect before modifying (§5.2); reuse `common/src/db/query.rs` rather than duplicating filter logic (§5.4); compare with sibling SBOM service/endpoints for parity on error handling and caching (§5.8).

## Reuse Candidates
- `common/src/db/query.rs` — shared query builder helpers for filtering, pagination, sorting; use for the `status` column filter
- `common/src/model/paginated.rs::PaginatedResults` — response wrapper the advisory list endpoint must keep returning
- `common/src/error.rs::AppError` — use for the 400 response on invalid status filter values
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — sibling service showing list/fetch query structure without lookup-table joins
- `entity/src/advisory.rs::AdvisoryStatus` (from Task 3) — typed enum for filter parsing and model mapping

## Acceptance Criteria
- [ ] `AdvisoryService` fetch, list, and search queries contain no join to `advisory_status` and no reference to `status_id`
- [ ] `AdvisorySummary` and `AdvisoryDetails` read status from `advisory.status`
- [ ] `GET /api/v2/advisory?...status=Fixed` (existing filter syntax) returns only advisories with status `Fixed`, filtered via `advisory.status` with no join
- [ ] `GET /api/v2/advisory` with an invalid status filter value returns `400 Bad Request` instead of an unfiltered list
- [ ] `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}` response shapes (field names and status string values) are identical to the pre-change responses
- [ ] `SearchService` advisory search contains no reference to `advisory_status`/`status_id` and returns correct status values
- [ ] `grep -rn "advisory_status\|status_id" modules/fundamental modules/search common server tests` returns no matches referring to the dropped table/column (enum type name `advisory_status_enum` excepted)

## Test Requirements
- [ ] `tests/api/advisory.rs`: list advisories with no filter returns all advisories with correct status strings (`assert_eq!(resp.status(), StatusCode::OK)`)
- [ ] `tests/api/advisory.rs`: list with status filter for each of `New`, `Analyzing`, `Fixed`, `Rejected` returns only matching advisories
- [ ] `tests/api/advisory.rs`: list with an invalid status filter value returns `StatusCode::BAD_REQUEST`
- [ ] `tests/api/advisory.rs`: get advisory by id returns the correct status string and unchanged response shape
- [ ] `tests/api/search.rs`: searching for an advisory returns it with the correct status

## Verification Commands
- `cargo test -p tests --test advisory` (or the workspace's integration test invocation for `tests/api/advisory.rs`) — all advisory API tests pass
- `cargo test --workspace` — full test suite passes on the TC-9005 branch
- `grep -rn "advisory_status::" modules/ common/ server/` — no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column
