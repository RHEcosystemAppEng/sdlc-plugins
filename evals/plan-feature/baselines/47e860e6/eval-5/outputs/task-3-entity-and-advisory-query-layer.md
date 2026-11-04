## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity definitions to match the new schema from Task 2, and move every advisory read path from the `advisory_status` join to the new `advisory.status` enum column:

- Add an `AdvisoryStatus` enum (`DeriveActiveEnum`, mapped to the PostgreSQL type `advisory_status_enum`) and replace `status_id` with `status: AdvisoryStatus` on the `advisory` entity.
- Remove the `advisory_status` entity and every relation that points to it.
- Remove the `advisory_status` join from the advisory service (fetch, list, search), the advisory endpoints (including the status filter on the list endpoint), and the search service. The status filter becomes `WHERE advisory.status = '<value>'` (UC-1).

The API response shape must stay identical: `status` is still serialized as the same string (`"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`).

The entity change and its consumers are in one task because removing `status_id` and the `advisory_status` entity breaks compilation of every module that references them. Splitting them would leave a non-compiling intermediate PR.

## Files to Modify
- `entity/src/advisory.rs` — add the `AdvisoryStatus` active enum; replace `status_id` with `status: AdvisoryStatus`; remove the `Relation` / `Related` impls that point to `advisory_status`
- `entity/src/lib.rs` — remove the `advisory_status` module declaration and re-export
- `modules/fundamental/src/advisory/service/advisory.rs` — remove the `advisory_status` join from fetch, list, and search; filter and select on `advisory::Column::Status`
- `modules/fundamental/src/advisory/model/summary.rs` — populate `AdvisorySummary`'s status from `advisory.status` instead of the joined lookup row, keeping the serialized string the same
- `modules/fundamental/src/advisory/model/details.rs` — populate `AdvisoryDetails`'s status from `advisory.status`, keeping the serialized string the same
- `modules/fundamental/src/advisory/endpoints/list.rs` — parse the `status` filter query value into `AdvisoryStatus` and return a 400 `AppError` for unknown values instead of silently ignoring the filter
- `modules/fundamental/src/advisory/endpoints/get.rs` — remove any lookup or join on `advisory_status` when building the details response
- `modules/search/src/service/mod.rs` — remove the `advisory_status` join from advisory full-text search; read the status from `advisory.status`
- `modules/fundamental/src/sbom/service/sbom.rs` — audit the SBOM-to-advisory queries (via `sbom_advisory`) and replace any `advisory_status` join with `advisory.status`
- `tests/api/advisory.rs` — update fixtures and assertions for the enum column; add status-filter tests
- `tests/api/search.rs` — update advisory search fixtures and assertions for the enum column
- `entity/src/advisory_status.rs` — DELETE this lookup-table entity, as the Feature requirements specify. This file does not appear in the repository manifest. Confirm it exists before deleting. If the lookup entity is defined inline elsewhere (for example inside `entity/src/advisory.rs`), remove it there instead.

## API Changes
- `GET /api/v2/advisory` — MODIFY (internal only): the status filter queries `advisory.status` directly, without a join. The response shape (`PaginatedResults<AdvisorySummary>`) and the `status` string values are unchanged.
- `GET /api/v2/advisory/{id}` — MODIFY (internal only): status is read from `advisory.status`. The response shape (`AdvisoryDetails`) is unchanged.
- `GET /api/v2/search` — MODIFY (internal only): advisory results read status without a join. The response shape is unchanged.

## Implementation Notes
- **Entity enum mapping:** in `entity/src/advisory.rs` define
  `#[derive(Clone, Debug, PartialEq, Eq, EnumIter, DeriveActiveEnum, Serialize, Deserialize)] #[sea_orm(rs_type = "String", db_type = "Enum", enum_name = "advisory_status_enum")] pub enum AdvisoryStatus { #[sea_orm(string_value = "New")] New, #[sea_orm(string_value = "Analyzing")] Analyzing, #[sea_orm(string_value = "Fixed")] Fixed, #[sea_orm(string_value = "Rejected")] Rejected }`
  The `string_value`s must match the enum labels created in Task 2's `migration/src/m0002_advisory_status_enum/mod.rs` exactly, including case.
- Model the entity changes on the existing join-table entities `entity/src/sbom_advisory.rs` and `entity/src/package_license.rs` for `Relation` / `Related` patterns. Remove only the `advisory_status` relation and keep the `sbom_advisory` relation intact.
- **Cross-cutting call-site enumeration.** Removing `advisory::Column::StatusId` and `advisory_status::Entity` affects every consumer. The manifest-level enumeration covers:
  1. `modules/fundamental/src/advisory/service/advisory.rs` (fetch, list, search)
  2. `modules/fundamental/src/advisory/endpoints/list.rs` (status filter)
  3. `modules/fundamental/src/advisory/endpoints/get.rs`
  4. `modules/fundamental/src/advisory/model/summary.rs` and `details.rs` (status population)
  5. `modules/search/src/service/mod.rs` (cross-entity search)
  6. `modules/fundamental/src/sbom/service/sbom.rs` (advisories surfaced through `sbom_advisory`)
  7. `modules/ingestor/src/graph/advisory/mod.rs` (writer, handled in Task 4)

  No Serena instance is configured for trustify-backend. Before starting, run `grep -rn "advisory_status\|status_id\|StatusId" --include=*.rs .` and treat the grep output as authoritative. Any additional consumer it finds is in scope for this task, except the ingestor writer, which belongs to Task 4.
- Per CONVENTIONS.md §Query helpers: build the status filter with the shared filtering helpers in `common/src/db/query.rs` rather than hand-writing a new filter. With no join, the filter is a plain column condition on `advisory::Column::Status`.
  Applies: task modifies modules/fundamental/src/advisory/service/advisory.rs matching the convention's service-layer query scope.
- Per CONVENTIONS.md §Error handling: the list handler must return `Result<T, AppError>` and wrap fallible calls with `.context()`. Map an unparseable `status` filter value to an `AppError` bad-request variant from `common/src/error.rs`.
  Applies: task modifies modules/fundamental/src/advisory/endpoints/list.rs matching the convention's HTTP handler scope.
- Per CONVENTIONS.md §Response types: the list endpoint keeps returning `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`. Do not change the wrapper.
  Applies: task modifies modules/fundamental/src/advisory/endpoints/list.rs matching the convention's list endpoint scope.
- Per CONVENTIONS.md §Framework: use SeaORM `DeriveActiveEnum` for the enum column. Do not store it as a raw `String`.
  Applies: task modifies entity/src/advisory.rs matching the convention's SeaORM entity scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` run against the real PostgreSQL test database and use the `assert_eq!(resp.status(), StatusCode::OK)` pattern.
  Applies: task modifies tests/api/advisory.rs matching the convention's tests/api integration test scope.
- **Fail-closed status filter (fail-open risk):** today an unknown filter value might quietly match nothing, or be ignored and return all advisories. That would hide parsing bugs after the type change. In `modules/fundamental/src/advisory/endpoints/list.rs`, reject values that do not parse into `AdvisoryStatus` with a 400 error.
- Serialization: keep the JSON value of `status` byte-identical to today (Customer Considerations: "no user-facing API changes"). If `AdvisorySummary` / `AdvisoryDetails` currently hold `status: String`, convert with a `From<AdvisoryStatus>` / `to_value()` mapping rather than changing the field's serialized form.
- Workspace build note: after this task merges into `TC-9005`, `modules/ingestor` may not compile until Task 4 lands, because it still writes `status_id`. That is acceptable on the feature branch. Use the per-crate verification commands below.
- Constraints (docs/constraints.md): Conventional Commits with a TC-9005 footer and the `Assisted-by: Claude Code` trailer (§2.1–2.3). Open the PR with `--base TC-9005` (§3.3). Keep changes scoped to the listed files (§5.1). Inspect before modifying (§5.2). Reuse existing helpers rather than duplicating them (§5.4).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers for the status filter
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper, unchanged
- `common/src/error.rs::AppError` — error type for rejecting invalid status filter values
- `entity/src/sbom_advisory.rs` — existing advisory relation to preserve, and the relation-definition pattern to follow

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatus` mapped to `advisory_status_enum` with the four values, and the `advisory` model has `status: AdvisoryStatus` and no `status_id`
- [ ] The `advisory_status` entity is removed and no code references `advisory_status::Entity` or `advisory::Column::StatusId`
- [ ] `modules/fundamental/src/advisory/service/advisory.rs`: fetch, list, and search no longer join `advisory_status`
- [ ] `modules/fundamental/src/advisory/endpoints/list.rs`: the status filter queries `advisory.status` directly (`WHERE status = 'Fixed'`), and an unknown status value returns HTTP 400
- [ ] `modules/fundamental/src/advisory/endpoints/get.rs`: details are built without the join
- [ ] `modules/fundamental/src/advisory/model/summary.rs` and `details.rs`: status is populated from the enum column with unchanged JSON values
- [ ] `modules/search/src/service/mod.rs`: advisory search no longer joins `advisory_status`
- [ ] `modules/fundamental/src/sbom/service/sbom.rs`: no `advisory_status` join remains in the SBOM-advisory queries
- [ ] The JSON responses of `GET /api/v2/advisory`, `GET /api/v2/advisory/{id}`, and `GET /api/v2/search` are unchanged in shape and `status` values

## Test Requirements
- [ ] `tests/api/advisory.rs`: `GET /api/v2/advisory?status=Fixed` returns only advisories with status `Fixed`, for each of the four statuses
- [ ] `tests/api/advisory.rs`: `GET /api/v2/advisory?status=Bogus` returns `StatusCode::BAD_REQUEST` and does not return the unfiltered list
- [ ] `tests/api/advisory.rs`: `GET /api/v2/advisory/{id}` returns `status` as the same string value as before the migration
- [ ] `tests/api/search.rs`: advisory search results still include the correct `status` string
- [ ] Regression: existing advisory and SBOM integration tests pass unchanged apart from fixture setup

## Verification Commands
- `grep -rn "advisory_status::\|StatusId\|status_id" --include=*.rs entity modules/fundamental modules/search` — no matches
- `cargo check --manifest-path entity/Cargo.toml` — compiles
- `cargo check --manifest-path modules/fundamental/Cargo.toml` — compiles
- `cargo check --manifest-path modules/search/Cargo.toml` — compiles
- `cargo test --manifest-path tests/Cargo.toml` — advisory and search API tests pass (requires Task 2's migration and Task 4 for a full workspace build)

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add advisory_status_enum migration
