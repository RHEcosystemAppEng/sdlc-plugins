## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update every advisory read path to use the new `advisory.status` enum column instead of joining the `advisory_status` lookup table. This removes the join from advisory list, get, status-filter, and search queries (UC-1: filtering by `status = 'Fixed'` becomes `WHERE status = 'Fixed'` with no join), which is the main performance goal of TC-9005 (~40ms p95 reduction on the advisory list endpoint). The API response shape must remain identical — `status` is still returned as a string.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove the `advisory_status` join from `AdvisoryService` fetch/list/search queries; select and filter on `advisory::Column::Status`
- `modules/fundamental/src/advisory/model/summary.rs` — populate `AdvisorySummary` status from `advisory::Model.status` instead of the joined lookup row
- `modules/fundamental/src/advisory/model/details.rs` — populate `AdvisoryDetails` status from `advisory::Model.status` instead of the joined lookup row
- `modules/fundamental/src/advisory/endpoints/list.rs` — parse the `status` filter query parameter into `AdvisoryStatus` and pass it to the service; return a 400 for unknown status values
- `modules/fundamental/src/advisory/endpoints/get.rs` — remove any lookup-table join/loading when building the advisory details response
- `modules/search/src/service/mod.rs` — update `SearchService` advisory search to read/filter `advisory.status` directly instead of joining `advisory_status`
- `tests/api/advisory.rs` — update and extend advisory endpoint integration tests for the enum-backed status

## API Changes
- `GET /api/v2/advisory` — MODIFY (internal only): status filtering now uses the `advisory.status` enum column; request parameters and response shape (`PaginatedResults<AdvisorySummary>`, `status` as string) unchanged
- `GET /api/v2/advisory/{id}` — MODIFY (internal only): status read from `advisory.status`; response shape unchanged
- `GET /api/v2/search` — MODIFY (internal only): advisory results read status from `advisory.status`; response shape unchanged

## Implementation Notes
- **Call-site enumeration (cross-cutting change):** removing the `advisory_status` entity (Task 3) breaks every consumer of the lookup table. Based on the repository structure, the consumers are the advisory service, model, and endpoints in `modules/fundamental/src/advisory/` and the full-text search in `modules/search/src/service/mod.rs`; all are listed in Files to Modify, with one acceptance criterion each. At implementation time, run `grep -rn "advisory_status\|status_id" modules/ common/ server/ tests/` to confirm no other call sites exist (e.g., `modules/fundamental/src/sbom/service/sbom.rs` if SBOM details embed advisory status via `entity/src/sbom_advisory.rs`). If additional call sites are found, update them in this task and note them in the PR — the codebase search is authoritative over this list.
- Use the shared filtering helpers in `common/src/db/query.rs` for the status filter (apply `advisory::Column::Status.eq(status)`), rather than hand-building a filter; keep pagination via the same helpers and the response wrapper `PaginatedResults<T>` from `common/src/model/paginated.rs`.
- Parse the status query parameter with the canonical `AdvisoryStatus` string parser added in Task 3 (`entity/src/advisory.rs`); an unknown value must return `AppError` (400) rather than silently ignoring the filter and returning the unfiltered list.
- Keep `AdvisorySummary`/`AdvisoryDetails` `status` serialized as the same string values as today (no response-shape change per Customer Considerations). If the model currently holds `status: String`, either keep `String` and convert from `AdvisoryStatus`, or switch to `AdvisoryStatus` whose serde output is identical — verify via the integration tests' JSON assertions.
- Per CONVENTIONS.md §Error handling: all handlers return `Result<T, AppError>` with `.context()` wrapping. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's endpoint handler scope. See `common/src/error.rs` (`AppError`) and the existing handler in `modules/fundamental/src/advisory/endpoints/get.rs`.
- Per CONVENTIONS.md §Query helpers: use shared filtering, pagination, and sorting via `common/src/db/query.rs`. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service query scope. See the existing list query in `modules/fundamental/src/sbom/service/sbom.rs` (`SbomService` list) for the pattern.
- Per CONVENTIONS.md §Response types: list endpoints return `PaginatedResults<T>`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's list endpoint scope. See `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` hit a real PostgreSQL test database and use `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies `tests/api/advisory.rs` matching the convention's `tests/api/` integration test scope. See existing tests in `tests/api/advisory.rs` and `tests/api/search.rs`.
- Commit rules (docs/constraints.md §2): Conventional Commits (e.g., `perf(advisory): query status enum column instead of advisory_status join`), footer `Implements <task-key>`, `Assisted-by:` trailer.
- PR rules (docs/constraints.md §3): `gh pr create --base TC-9005`; post the PR link on this Jira task.
- Code change rules (docs/constraints.md §5): change only the listed files (plus any additional call sites discovered by the grep above, documented in the PR); compare the advisory service changes with the search service for parity in how status is filtered.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering/pagination/sorting helpers; use for the status filter instead of custom query code
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper (unchanged shape)
- `common/src/error.rs::AppError` — error type for the 400 response on invalid status values
- `entity/src/advisory.rs::AdvisoryStatus` — enum and string parser introduced by Task 3; reuse for filter parsing and serialization

## Acceptance Criteria
- [ ] `AdvisoryService` (`modules/fundamental/src/advisory/service/advisory.rs`) fetch, list, and search queries contain no join to `advisory_status` and filter status via `advisory.status`
- [ ] `AdvisorySummary` (`modules/fundamental/src/advisory/model/summary.rs`) status is populated from `advisory.status`
- [ ] `AdvisoryDetails` (`modules/fundamental/src/advisory/model/details.rs`) status is populated from `advisory.status`
- [ ] `GET /api/v2/advisory?status=Fixed` (`endpoints/list.rs`) returns only advisories with status `Fixed`, with an unchanged response shape
- [ ] `GET /api/v2/advisory` with an unknown status value returns 400 instead of an unfiltered list
- [ ] `GET /api/v2/advisory/{id}` (`endpoints/get.rs`) returns the advisory status string unchanged from the pre-migration response
- [ ] `SearchService` (`modules/search/src/service/mod.rs`) advisory search no longer joins `advisory_status` and returns the correct status
- [ ] No reference to `advisory_status` or `status_id` remains anywhere in `modules/`, `common/`, `server/`, or `tests/`

## Test Requirements
- [ ] Integration test in `tests/api/advisory.rs`: ingest/seed advisories with each of the four statuses, call `GET /api/v2/advisory?status=Fixed`, assert `StatusCode::OK` and that only `Fixed` advisories are returned
- [ ] Integration test: `GET /api/v2/advisory?status=Bogus` returns `StatusCode::BAD_REQUEST`
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns `status` as the expected string (e.g., `"Analyzing"`), confirming the response shape is unchanged
- [ ] Integration test in `tests/api/search.rs` (or `tests/api/advisory.rs`): search results for an advisory include the correct status string
- [ ] Existing advisory and search integration tests pass without modification to their response-shape assertions

## Verification Commands
- `grep -rn "advisory_status\|status_id" modules/ common/ server/ tests/` — no matches
- `cargo test -p tests` — advisory and search integration tests pass
- `curl -s 'http://localhost:8080/api/v2/advisory?status=Fixed'` — returns only `Fixed` advisories with `status` as a string

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum
