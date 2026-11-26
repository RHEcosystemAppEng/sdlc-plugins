**Summary:** Replace advisory_status joins with advisory.status column in queries and endpoints

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update every advisory read path to use the `advisory.status` enum column directly instead of joining the dropped `advisory_status` table. This covers the advisory service (fetch, list, search, and status filtering), the advisory response models and endpoints, and cross-module consumers that read advisory status (SBOM service and the search service). The API response shape must stay identical — `status` remains a string with the same values.

Part of TC-9005 (UC-1: advisory list filtered by status queries `advisory` with `WHERE status = 'Fixed'` and no join).

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — remove `advisory_status` joins in fetch/list/search; filter on `advisory::Column::Status`
- `modules/fundamental/src/advisory/model/summary.rs` — populate `AdvisorySummary.status` from `advisory::Model.status`
- `modules/fundamental/src/advisory/model/details.rs` — populate `AdvisoryDetails.status` from `advisory::Model.status`
- `modules/fundamental/src/advisory/endpoints/list.rs` — parse the status query filter into `AdvisoryStatus`; reject invalid values
- `modules/fundamental/src/advisory/endpoints/get.rs` — remove any lookup-table join used to load status
- `modules/fundamental/src/sbom/service/sbom.rs` — replace any `advisory_status` join used when loading advisories linked to an SBOM
- `modules/search/src/service/mod.rs` — replace any `advisory_status` join used in advisory full-text search results
- `tests/api/advisory.rs` — update/add integration tests for list, filter, and get
- `tests/api/search.rs` — assert advisory search results still carry the correct status

## Implementation Notes
- Cross-cutting call-site enumeration: before editing, run `grep -rn "advisory_status\|status_id\|AdvisoryStatus" modules/ common/ server/ tests/` and update **every** match. The Files to Modify list above enumerates all advisory-status consumers identified from the repository structure (advisory service/models/endpoints, SBOM service, search service); the grep is authoritative — if it finds additional call sites, include them and add an acceptance criterion for each. If `sbom.rs` or `search/service/mod.rs` do not reference the lookup table, leave them unchanged and note that in the PR.
- Replace `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())` / `find_also_related(advisory_status::Entity)` patterns with direct column reads; filter with `advisory::Column::Status.eq(AdvisoryStatus::Fixed)`.
- Status filter in `endpoints/list.rs`: convert the query string using the fallible `AdvisoryStatus` conversion from Task 3; an unknown status must produce `AppError` (400 Bad Request), not be silently ignored (returning unfiltered results would be a silent wrong answer).
- Response models keep `status: String` (or serialize `AdvisoryStatus` to the identical string) — no OpenAPI/response shape change.
- Per CONVENTIONS.md §Query helpers: implement the status filter through the shared filtering/pagination helpers rather than hand-built SQL. Applies: task modifies modules/fundamental/src/advisory/service/advisory.rs matching the convention's service query `.rs` scope. Example: `common/src/db/query.rs`.
- Per CONVENTIONS.md §Error handling: handlers keep returning `Result<T, AppError>` and wrap fallible calls with `.context()`; invalid status filters map to an `AppError` variant. Applies: task modifies modules/fundamental/src/advisory/endpoints/list.rs matching the convention's handler `.rs` scope. Example: `modules/fundamental/src/sbom/endpoints/list.rs`.
- Per CONVENTIONS.md §Response types: the list endpoint continues to return `PaginatedResults<AdvisorySummary>`. Applies: task modifies modules/fundamental/src/advisory/endpoints/list.rs matching the convention's list endpoint `.rs` scope. Example: `common/src/model/paginated.rs`.
- Per CONVENTIONS.md §Module pattern: keep changes within the existing `model/ + service/ + endpoints/` layout of the advisory module — no new layers. Applies: task modifies modules/fundamental/src/advisory/service/advisory.rs matching the convention's domain module `.rs` scope. Example: `modules/fundamental/src/sbom/`.
- Per CONVENTIONS.md §Testing: integration tests hit the real PostgreSQL test database and assert with `assert_eq!(resp.status(), StatusCode::OK)`. Applies: task modifies tests/api/advisory.rs matching the convention's `tests/api/*.rs` scope. Example: `tests/api/sbom.rs`.
- Constraints (docs/constraints.md): §1.4 scoped changes; §2.1–2.3 commit rules; §3.3 PR `--base TC-9005`; §5.1 only listed files (plus any additional call sites found by the grep, called out in the PR); §5.4 reuse `common/src/db/query.rs`; §5.6 trace the status from DB column → service → model → JSON response; §5.8 parity across advisory, SBOM, and search consumers.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers for the status filter
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper (unchanged)
- `common/src/error.rs::AppError` — error type for invalid status filter values
- `entity/src/advisory.rs::AdvisoryStatus` — enum and fallible string conversion introduced in Task 3; do not write a second status mapping

## Acceptance Criteria
- [ ] `modules/fundamental/src/advisory/service/advisory.rs`: fetch, list, and search no longer join `advisory_status`; status filter uses `advisory.status`
- [ ] `modules/fundamental/src/advisory/model/summary.rs`: `AdvisorySummary.status` populated from the enum column
- [ ] `modules/fundamental/src/advisory/model/details.rs`: `AdvisoryDetails.status` populated from the enum column
- [ ] `modules/fundamental/src/advisory/endpoints/list.rs`: `GET /api/v2/advisory?status=Fixed` returns only Fixed advisories; an invalid status value returns 400 instead of unfiltered results
- [ ] `modules/fundamental/src/advisory/endpoints/get.rs`: `GET /api/v2/advisory/{id}` returns the correct status string
- [ ] `modules/fundamental/src/sbom/service/sbom.rs`: no `advisory_status` references remain
- [ ] `modules/search/src/service/mod.rs`: no `advisory_status` references remain; advisory search results report correct status
- [ ] Response JSON for list and get endpoints is byte-for-byte shape compatible with the pre-change response (status still a string with values New/Analyzing/Fixed/Rejected)
- [ ] Repository-wide grep finds no remaining references to `advisory_status` (table/entity) or `status_id` outside migrations

## Test Requirements
- [ ] Integration test (`tests/api/advisory.rs`): list advisories with each status filter value and assert only matching advisories are returned
- [ ] Integration test: invalid status filter (e.g., `status=Pending`) returns 400 Bad Request
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns the expected `status` string for each of the four statuses
- [ ] Integration test: response shape of list/get is unchanged (assert `status` is a JSON string field)
- [ ] Integration test (`tests/api/search.rs`): advisory search results include the correct status
- [ ] Existing `tests/api/sbom.rs` tests pass unchanged

## Verification Commands
- `cargo test -p tests` — all API integration tests pass
- `grep -rn "advisory_status::\|status_id" modules/ common/ server/` — no matches
- `curl -s 'http://localhost:8080/api/v2/advisory?status=Fixed' | jq '[.items[].status] | unique'` — returns `["Fixed"]`

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum
