# Task 3 — Update SeaORM advisory entity and advisory queries to use the status enum column

**Summary:** Update SeaORM advisory entity and advisory queries to use the status enum column
**Labels:** ai-generated-jira
**Priority:** High (inherited from TC-9005)
**Fix Versions:** RHTPA 2.0.0 (inherited from TC-9005, fixVersion scope = both)

---

## Repository
trustify-backend

## Target Branch
TC-9005

## Description
Update the SeaORM entity layer and every advisory read path to the new schema from Task 2. Model the `advisory_status_enum` PostgreSQL type as a Rust enum. Replace the `status_id` relation on the advisory entity with a `status` enum field. Remove the `advisory_status` entity. Change every advisory query that joins `advisory_status` to read and filter on `advisory.status` directly.

This covers the TC-9005 requirements "Update SeaORM entity definitions" and "Update all advisory queries to use the new `status` column instead of the join (service layer and endpoints)". It also implements UC-1: filtering the advisory list by `status = 'Fixed'` must run `WHERE status = 'Fixed'` against `advisory` with no join.

The public API response shape must not change. `status` is still serialized as the same string values (`"New"`, `"Analyzing"`, `"Fixed"`, `"Rejected"`).

## Files to Modify
- `entity/src/advisory.rs` — add an `AdvisoryStatus` enum (`DeriveActiveEnum`, `rs_type = "String"`, `db_type = "Enum"`, `enum_name = "advisory_status_enum"`) with variants `New`, `Analyzing`, `Fixed`, `Rejected`. Replace the `status_id` field with `status: AdvisoryStatus`. Remove the `Relation` / `Related` impls that point to `advisory_status`.
- `entity/src/lib.rs` — remove the `advisory_status` module declaration and re-export (if present) and export `AdvisoryStatus`
- `modules/fundamental/src/advisory/service/advisory.rs` — `AdvisoryService` fetch, list, and search: remove the join or `find_also_related` on `advisory_status`, select `advisory::Column::Status`, and apply the status filter as `advisory::Column::Status.eq(AdvisoryStatus::X)`
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary`: build the `status` string from `advisory::Model.status` instead of the joined lookup model
- `modules/fundamental/src/advisory/model/details.rs` — `AdvisoryDetails`: same change as `AdvisorySummary`
- `modules/fundamental/src/advisory/endpoints/list.rs` — `GET /api/v2/advisory`: parse the `status` filter query value into `AdvisoryStatus`, and reject unknown values with `AppError` instead of ignoring them
- `modules/fundamental/src/advisory/endpoints/get.rs` — `GET /api/v2/advisory/{id}`: remove any lookup-join-dependent code
- `tests/api/advisory.rs` — update fixtures and setup that insert `advisory_status` rows or set `status_id`, and add the status-filter tests below

Implementer must also check and update these files if they reference `advisory_status` or `advisory::Column::StatusId` (see Cross-cutting call sites):
- `modules/search/src/service/mod.rs` — `SearchService` full-text search across entities, which may join `advisory_status` to return or filter advisory status
- `modules/fundamental/src/sbom/service/sbom.rs` — `SbomService`, which may load linked advisories (through `entity/src/sbom_advisory.rs`) with their status
- `common/src/db/query.rs` — shared filter helpers, if status filtering is done through a generic join-based filter
- `tests/api/search.rs`, `tests/api/sbom.rs` — fixtures that seed `advisory_status`

## API Changes
- `GET /api/v2/advisory` — MODIFY (internal only): the `status` filter now runs against `advisory.status` with no join. The response shape (`PaginatedResults<AdvisorySummary>`) is unchanged and `status` is still a string. An unknown `status` filter value now returns 400 through `AppError` instead of returning an empty list.
- `GET /api/v2/advisory/{id}` — MODIFY (internal only): no lookup join. The response shape (`AdvisoryDetails`) is unchanged.

## Implementation Notes
**Entity file removal:** the feature description names `entity/advisory_status.rs` for removal. The repository structure available during planning lists no `entity/src/advisory_status.rs`. The lookup entity may be defined inline elsewhere, or the structure listing may be incomplete. Locate the `advisory_status` entity definition (for example, with `grep -rn "advisory_status" entity/ modules/ common/ tests/`). If it exists as a separate file, delete it and remove its `mod` line in `entity/src/lib.rs`. This file is not listed under Files to Modify because its path was not confirmed during planning.

**Cross-cutting call sites:** removing the `advisory_status` entity and the `advisory::Column::StatusId` / `Relation::AdvisoryStatus` symbols affects every consumer. Run `grep -rn "advisory_status\|StatusId\|AdvisoryStatus" --include=*.rs .` across the workspace and update every hit outside the ingestor. The ingestor is handled in Task 4. Each hit found must have a matching acceptance check. The compiler is authoritative here: `cargo check --workspace` must report no reference to the removed symbols outside `modules/ingestor/`.

**Enum string mapping:** use `#[sea_orm(string_value = "New")]` and the matching attribute on each variant so the DB labels match the migration exactly (case-sensitive). Add `serde::Serialize` with the default variant naming, or an explicit `impl Display`, so that `AdvisorySummary.status` and `AdvisoryDetails.status` produce the same strings the API returns today.

**Patterns to follow:**
- Per CONVENTIONS.md §Query helpers: build the status filter with the shared filtering helpers in `common/src/db/query.rs` rather than with ad-hoc SQL. Applies: task modifies `modules/fundamental/src/advisory/service/advisory.rs` matching the convention's service-layer query scope. Reference example: the existing list/filter implementation in `modules/fundamental/src/sbom/service/sbom.rs`.
- Per CONVENTIONS.md §Error handling: return `Result<T, AppError>` with `.context()` wrapping, and map an invalid `status` filter to an `AppError` variant from `common/src/error.rs`. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's handler scope. Reference example: `modules/fundamental/src/sbom/endpoints/get.rs`.
- Per CONVENTIONS.md §Response types: keep the list endpoint returning `PaginatedResults<AdvisorySummary>` from `common/src/model/paginated.rs`, with an unchanged shape. Applies: task modifies `modules/fundamental/src/advisory/endpoints/list.rs` matching the convention's list endpoint scope.
- Per CONVENTIONS.md §Testing: integration tests in `tests/api/` run against a real PostgreSQL test database using the `assert_eq!(resp.status(), StatusCode::OK)` pattern. Applies: task modifies `tests/api/advisory.rs` matching the convention's integration test scope. Reference example: existing tests in `tests/api/advisory.rs`.

**Intermediate-state note:** this task removes symbols that `modules/ingestor/src/graph/advisory/mod.rs` still uses until Task 4 lands. While the feature branch sits between Task 3 and Task 4, the workspace build may fail in the ingestor crate. That is expected on the feature branch and is the reason feature-branch mode was chosen. Before merging this task's PR, verify that `cargo check -p entity -p fundamental -p search` (crate names as defined in each crate's `Cargo.toml`) passes.

**Constraints (docs/constraints.md):** §2.1–2.3 (Jira key footer, Conventional Commits, `Assisted-by: Claude Code` trailer). §3.3 (`gh pr create --base TC-9005`). §5.1–5.8 (stay within the files listed above, inspect before modifying, follow the referenced patterns, reuse the shared query helpers, check parity with sibling SBOM and package services for error handling).

## Reuse Candidates
- `common/src/db/query.rs` — shared filtering, pagination, and sorting helpers. Use these for the `status` equality filter instead of a hand-written WHERE clause.
- `common/src/model/paginated.rs::PaginatedResults` — list response wrapper that must stay unchanged
- `common/src/error.rs::AppError` — error type for rejecting an invalid status filter value
- `modules/fundamental/src/sbom/service/sbom.rs::SbomService` — sibling service showing list and filter query structure without lookup joins
- `modules/fundamental/src/package/model/summary.rs::PackageSummary` — sibling summary model showing how a scalar entity column (`license`) maps into a response struct

## Acceptance Criteria
- [ ] `entity/src/advisory.rs` defines `AdvisoryStatus` mapped to `advisory_status_enum` with variants `New`, `Analyzing`, `Fixed`, `Rejected`, and `advisory::Model` has `status: AdvisoryStatus` and no `status_id`
- [ ] The `advisory_status` SeaORM entity is removed and no code outside `modules/ingestor/` references it
- [ ] `AdvisoryService` fetch, list, and search build queries with no join to `advisory_status` (the generated SQL contains no `advisory_status` table reference)
- [ ] `GET /api/v2/advisory?status=Fixed` (or the existing filter syntax) returns only advisories with `status = 'Fixed'`, using a direct column filter
- [ ] `GET /api/v2/advisory` and `GET /api/v2/advisory/{id}` responses keep the same JSON shape, and `status` is serialized as the same string values as before the change
- [ ] An unknown `status` filter value returns an error response (4xx through `AppError`) instead of silently returning an empty result set
- [ ] Every other call site found by the cross-cutting search (including `SearchService` and `SbomService`, if they reference the lookup) reads `advisory.status` directly
- [ ] `cargo check` passes for the `entity`, `fundamental`, and `search` crates

## Test Requirements
- [ ] Integration test in `tests/api/advisory.rs`: seed advisories with each of the four statuses, call the list endpoint filtered by `Fixed`, and assert `StatusCode::OK` and that only `Fixed` advisories are returned
- [ ] Integration test: the list endpoint with no filter returns all advisories and each item's `status` string matches the seeded value (response shape unchanged)
- [ ] Integration test: `GET /api/v2/advisory/{id}` returns the correct `status` string
- [ ] Integration test: an invalid `status` filter value returns a 4xx error, not `200` with an empty list
- [ ] Unit test: `AdvisoryStatus` round-trips between the Rust enum and the DB string value for all four variants
- [ ] Update `tests/api/search.rs` and `tests/api/sbom.rs` fixtures if they seeded `advisory_status`, and confirm those suites still pass

## Verification Commands
- `cargo test -p tests --test advisory` (or the workspace's integration test invocation) — advisory integration tests pass
- `grep -rn "advisory_status" --include=*.rs entity/ modules/fundamental/ modules/search/ common/` — returns no matches except the enum's `enum_name = "advisory_status_enum"` attribute
- `curl -s "http://localhost:8080/api/v2/advisory?status=Fixed" | jq '[.items[].status] | unique'` — returns `["Fixed"]`

## Documentation Updates
- `README.md` — if it describes the advisory data model or the `advisory_status` table, update it to describe the `advisory.status` enum column

## Dependencies
- Depends on: Task 1 — Create feature branch TC-9005 from main
- Depends on: Task 2 — Add migration converting advisory_status lookup table to advisory_status_enum column
