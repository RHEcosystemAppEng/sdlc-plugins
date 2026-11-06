**Summary:** Replace advisory_status joins with the advisory.status enum column in all advisory queries

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Change every advisory read path to use the new `advisory.status` enum column (Task 3) and drop the `advisory_status` join. This covers:

- the advisory service layer;
- the list and get endpoints, including status filtering;
- the response models;
- any other module that reads advisory status, such as search.

The Feature's main goal is to remove the join so that advisory list p95 latency drops by about 40ms. The API response shape must not change: `status` stays a string field with the same values.

Use case UC-1: filtering the advisory list by `status = "Fixed"` must produce `WHERE advisory.status = 'Fixed'` with no join.

## Files to Modify
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` fetch, list and search: remove the `advisory_status` join or `find_also_related`, select `advisory.status` directly, and filter on the enum column
- `modules/fundamental/src/advisory/endpoints/list.rs` — `GET /api/v2/advisory`: parse the `status` filter query value into `AdvisoryStatus` and pass it to the service
- `modules/fundamental/src/advisory/endpoints/get.rs` — `GET /api/v2/advisory/{id}`: stop loading status through the lookup relation
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary`: build `status` from `advisory::Model.status` instead of the joined `advisory_status` row, keeping the serialized string unchanged
- `modules/fundamental/src/advisory/model/details.rs` — `AdvisoryDetails`: same as the summary
- `modules/search/src/service/mod.rs` — `SearchService` full-text search across entities: if advisory results join `advisory_status` or read `status_id`, switch them to `advisory.status`
- `common/src/db/query.rs` — shared filter helpers: if the generic filter casts to text or fails on PostgreSQL enum columns, add enum-column support so `status = 'Fixed'` compiles to a direct comparison
- `tests/api/advisory.rs` — update the advisory endpoint integration tests for the new schema and add status filter coverage
- `tests/api/search.rs` — update the search integration tests if they seed or assert advisory status

## API Changes
- `GET /api/v2/advisory` — MODIFY (internal only): the status filter now queries `advisory.status` directly. The request parameters and the `PaginatedResults<AdvisorySummary>` response shape are unchanged
- `GET /api/v2/advisory/{id}` — MODIFY (internal only): status comes from the `advisory.status` column. The `AdvisoryDetails` response shape is unchanged

## Implementation Notes
- **Call-site enumeration (cross-cutting change):** removing `advisory::Model.status_id` and the `advisory_status` entity changes a shared type. Every consumer must be updated, not only the ones the Feature mentions. Possible call sites from repository analysis:
  - `modules/fundamental/src/advisory/service/advisory.rs`
  - `modules/fundamental/src/advisory/endpoints/list.rs`
  - `modules/fundamental/src/advisory/endpoints/get.rs`
  - `modules/fundamental/src/advisory/model/summary.rs`
  - `modules/fundamental/src/advisory/model/details.rs`
  - `modules/search/src/service/mod.rs`
  - `common/src/db/query.rs`
  - `tests/api/advisory.rs`
  - `tests/api/search.rs`

  Ingestion (`modules/ingestor/src/graph/advisory/mod.rs`) is handled in Task 5. Before you start, run `grep -rn "advisory_status\|status_id" --include=*.rs .` and include every match outside `migration/` in this task. If it finds a consumer not listed here, such as SBOM details in `modules/fundamental/src/sbom/service/sbom.rs` reading advisory status through `sbom_advisory`, update that too and note it in the PR. The codebase search is authoritative.
- Use the shared helpers in `common/src/db/query.rs` for filtering, pagination and sorting. Do not write a custom WHERE builder in the advisory service. Only extend the helper if it cannot compare an enum column. Any extension must stay generic, not advisory-specific.
- Parse the `status` query parameter with the `AdvisoryStatus` `FromStr` from Task 3. An unknown status value must return a 400 through `AppError` (`common/src/error.rs`). It must not be silently ignored and must not fall back to returning all advisories. A silently ignored filter would make a typo look like a successful but unfiltered result.
- Keep the response models' `status` field a `String`, or an `AdvisoryStatus` that serializes to the same string, so the JSON stays byte-compatible (Customer Considerations: no user-facing API changes).
- Follow the module pattern `model/ + service/ + endpoints/`. Handlers return `Result<T, AppError>` with `.context()` wrapping, and list endpoints return `PaginatedResults<T>` (`common/src/model/paginated.rs`).
- Do not change the `tower-http` caching configuration in `modules/fundamental/src/advisory/endpoints/mod.rs`. The route registration is unchanged.
- Constraints (docs/constraints.md):
  - §2.1–2.3: Conventional Commit, task-key footer, `Assisted-by:` trailer.
  - §3.3: `gh pr create --base TC-9005`.
  - §5.1–5.4: scoped files, inspect first, reuse the query helpers.
  - §5.6: trace UC-1 end to end, from query param through service to SQL to response.
  - §5.8: parity between the list, get and search paths.

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination and sorting helpers. Use these for the status filter instead of hand-written SQL
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper. Leave unchanged
- `common/src/error.rs::AppError` — use it for the 400 on an invalid status filter value
- `entity/src/advisory.rs::AdvisoryStatus` (from Task 3) — enum and `FromStr` for parsing and filtering

## Acceptance Criteria
- [ ] `modules/fundamental/src/advisory/service/advisory.rs`: no query joins `advisory_status`, and fetch, list and search read `advisory.status` directly
- [ ] `modules/fundamental/src/advisory/endpoints/list.rs`: filtering by `status=Fixed` produces a query with `WHERE advisory.status = 'Fixed'` and no join (UC-1)
- [ ] `modules/fundamental/src/advisory/endpoints/get.rs`: `GET /api/v2/advisory/{id}` returns the correct status without loading a lookup relation
- [ ] `modules/fundamental/src/advisory/model/summary.rs` and `details.rs`: `status` is built from the enum column, and the JSON field name and string values are unchanged
- [ ] `modules/search/src/service/mod.rs`: advisory search results no longer reference `advisory_status` or `status_id`
- [ ] `common/src/db/query.rs`: the shared filter helpers can filter on the enum column, either unchanged or with a generic extension
- [ ] An invalid `status` filter value returns HTTP 400 and does not return an unfiltered list
- [ ] `grep -rn "advisory_status\|status_id" --include=*.rs` outside `migration/` returns no matches, apart from the PostgreSQL enum type name `advisory_status_enum` in the entity mapping
- [ ] The workspace compiles and all existing advisory and search integration tests pass with updated fixtures

## Test Requirements
- [ ] `tests/api/advisory.rs`: list advisories with each status value and assert only matching advisories are returned (`assert_eq!(resp.status(), StatusCode::OK)` pattern)
- [ ] `tests/api/advisory.rs`: list with no status filter returns all advisories, and each item's `status` is one of the four strings
- [ ] `tests/api/advisory.rs`: `GET /api/v2/advisory/{id}` returns the expected `status` string
- [ ] `tests/api/advisory.rs`: an invalid status filter (e.g., `status=Bogus`) returns `StatusCode::BAD_REQUEST`, not an unfiltered 200
- [ ] `tests/api/advisory.rs`: response JSON snapshot or field assertions confirm the response shape is unchanged (the `status` field is still a string)
- [ ] `tests/api/search.rs`: search returning advisories still includes the correct status
- [ ] Optional: capture the advisory list query plan or latency before and after, to support the ~40ms p95 goal, and note the result in the PR

## Verification Commands
- `cargo test -p tests --test api` (or the workspace's integration test target) — advisory and search tests pass
- `grep -rn "advisory_status\|status_id" --include=*.rs . | grep -v '^./migration/' | grep -v advisory_status_enum` — no output
- `curl -s 'http://localhost:8080/api/v2/advisory?status=Fixed' | jq '.items[].status' | sort -u` — prints only `"Fixed"`

## Documentation Updates
- `README.md` — if it describes the advisory data model or the `advisory_status` table, update it to describe the `status` enum column (the internal architecture doc update is tracked in Task 6)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 3 — Update SeaORM advisory entity to use AdvisoryStatus enum column and remove advisory_status entity
