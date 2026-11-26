**Summary:** Remove advisory_status join from advisory and search queries

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update every advisory read path to use the new `advisory.status` enum column (Task 3) instead of joining the dropped `advisory_status` table. This is the change that delivers the Feature's performance goal: the advisory list with a status filter (UC-1) becomes `WHERE status = 'Fixed'` with no join. The API response shape must stay the same, with status still serialized as the same string (TC-9005, Customer Considerations).

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` fetch, list and search: remove the `advisory_status` join/`find_also_related` and read/filter on `advisory::Column::Status`
- `modules/fundamental/src/advisory/model/summary.rs` — build `AdvisorySummary.status` from `advisory::Model.status` (serialized as the same string), not from the joined lookup row
- `modules/fundamental/src/advisory/model/details.rs` — build `AdvisoryDetails` status from `advisory::Model.status`
- `modules/fundamental/src/advisory/endpoints/list.rs` — `GET /api/v2/advisory` status filter: parse the query value into `AdvisoryStatus` and filter on the column
- `modules/fundamental/src/advisory/endpoints/get.rs` — `GET /api/v2/advisory/{id}`: remove any lookup-table handling and return status from the entity column
- `modules/search/src/service/mod.rs` — `SearchService` advisory results: remove the `advisory_status` join and read `advisory.status`
- `tests/api/advisory.rs` — update and extend advisory endpoint integration tests for the enum column
- `tests/api/search.rs` — update search tests that assert advisory status

## API Changes
- `GET /api/v2/advisory` — MODIFY (internal only): status filter now runs on `advisory.status` with no join. Request parameters and response shape (`PaginatedResults<AdvisorySummary>`, `status` as a string) are unchanged
- `GET /api/v2/advisory/{id}` — MODIFY (internal only): status is read from the entity column. Response shape is unchanged

## Implementation Notes
- **Call-site enumeration (cross-cutting change).** Removing `advisory::Model.status_id` and the `advisory_status` relation affects every consumer of advisory status. From the repository analysis the affected read sites are:
  1. `AdvisoryService` (fetch, list, search) — `modules/fundamental/src/advisory/service/advisory.rs`
  2. `AdvisorySummary` mapping — `modules/fundamental/src/advisory/model/summary.rs`
  3. `AdvisoryDetails` mapping — `modules/fundamental/src/advisory/model/details.rs`
  4. List endpoint status filter — `modules/fundamental/src/advisory/endpoints/list.rs`
  5. Get endpoint — `modules/fundamental/src/advisory/endpoints/get.rs`
  6. `SearchService` — `modules/search/src/service/mod.rs`
  Before opening the PR, run `grep -rn "advisory_status\|status_id" modules/ server/ common/` to confirm no other reader remains. For example, `modules/fundamental/src/sbom/service/sbom.rs` may expose advisory status through `sbom_advisory` in `SbomDetails`. If it does, update it the same way and add it to the PR. The codebase search is authoritative. Ingestion writers are handled in Task 5.
- Propagation pattern (apply at each site): replace `.find_also_related(advisory_status::Entity)` / `.join(JoinType::InnerJoin, advisory::Relation::AdvisoryStatus.def())` with direct use of `advisory::Column::Status`. Replace `status_row.name` with `model.status.to_string()` (or `as_str()`, from Task 3).
- **Status filter (UC-1).** In `endpoints/list.rs`, parse the incoming status string with `AdvisoryStatus::from_str`. An unknown value must return a 400 `AppError` (from `common/src/error.rs`). It must not be dropped silently, which would return the unfiltered list, and it must not return an empty 200. Then apply `advisory::Column::Status.eq(status)`.
- **Response compatibility.** The JSON `status` field in `AdvisorySummary` / `AdvisoryDetails` must keep the same name and the same values (`"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`). If the struct currently has a `String` field, keep it as `String` and convert from the enum. Do not change the serialized type.
- Per CONVENTIONS.md §Query helpers: implement status filtering, pagination and sorting through the shared helpers in `common/src/db/query.rs` rather than hand-rolled query code.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `.rs` service/query file scope.
- Per CONVENTIONS.md §Response types: the list endpoint must keep returning `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` list-endpoint file scope.
- Per CONVENTIONS.md §Error handling: handlers return `Result<T, AppError>` and wrap DB errors with `.context()`. Invalid status values map to a 400 `AppError` variant.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` handler file scope.
- Per CONVENTIONS.md §Module pattern: keep changes inside the existing `model/ + service/ + endpoints/` split of the advisory module. Do not move query logic into endpoints.
  Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's `modules/*/` domain module scope.
- Per CONVENTIONS.md §Caching: if `endpoints/mod.rs` route builders configure `tower-http` caching for advisory lists, check that cache keys still include the status query parameter. Do not change cache configuration otherwise.
  Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's `.rs` endpoint route file scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` run against a real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies `tests/api/advisory.rs` matching the convention's `tests/api/*.rs` integration test scope.
- Constraints (docs/constraints.md): §2 commits must use Conventional Commits, include the `Implements TC-<task>` footer and an `Assisted-by:` trailer. §3 the PR must use `--base TC-9005` and the PR link must be posted to the Jira task. §5 changes stay scoped to the listed files, inspect code before modifying it, reuse the existing query helpers, and trace the full data flow (query → model → response).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination and sorting helpers. Use them for the enum-column status filter
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper (unchanged)
- `common/src/error.rs::AppError` — use its existing bad-request variant for an invalid status filter value
- `entity/src/advisory.rs::AdvisoryStatus` — enum and string conversions from Task 3. Do not re-implement string mapping in the service layer
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — sibling service showing the list/fetch query pattern without lookup joins

## Acceptance Criteria
- [ ] `AdvisoryService` fetch, list and search no longer join `advisory_status`, and filter/read `advisory.status` directly
- [ ] `AdvisorySummary` status comes from `advisory.status`, and the JSON field name and values are unchanged
- [ ] `AdvisoryDetails` status comes from `advisory.status`, and the JSON field name and values are unchanged
- [ ] `GET /api/v2/advisory?status=Fixed` returns only `Fixed` advisories, using a `WHERE status = 'Fixed'` predicate with no join
- [ ] `GET /api/v2/advisory?status=<unknown>` returns 400. It does not return an unfiltered or empty 200 response
- [ ] `GET /api/v2/advisory/{id}` returns status from the entity column with an unchanged response shape
- [ ] `SearchService` advisory results no longer join `advisory_status`, and status is read from `advisory.status`
- [ ] A repo-wide search finds no remaining references to `advisory_status` (the table/entity) or `status_id` outside migrations
- [ ] `cargo build` succeeds for `modules/fundamental`, `modules/search` and `server`

## Test Requirements
- [ ] `tests/api/advisory.rs`: list advisories filtered by each of the four statuses returns only matching rows
- [ ] `tests/api/advisory.rs`: list with an invalid status value returns `StatusCode::BAD_REQUEST`
- [ ] `tests/api/advisory.rs`: the get-by-id response JSON contains the `status` string identical to the pre-migration format (snapshot or field assertion)
- [ ] `tests/api/advisory.rs`: unfiltered list returns a `PaginatedResults` with correct `total` and each item's `status` populated
- [ ] `tests/api/search.rs`: search results that include advisories report the correct `status` string

## Verification Commands
- `cargo test -p tests --test api advisory` — advisory integration tests pass
- `cargo test -p tests --test api search` — search integration tests pass
- `grep -rn "advisory_status::\|status_id" modules/ server/ common/` — no matches

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM Advisory entity to use status enum column
