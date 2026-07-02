# Implementation Plan for TC-9203: Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` supporting single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation reuses existing query helpers, follows the established advisory severity filter pattern, and joins through the existing `package_license` entity.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What changes:**

- Add an optional `license` field (type `Option<String>`) to the query parameter struct used by the `GET /api/v2/package` handler, following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, extract the `license` query parameter and pass it to `PackageService::list()`.
- Use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated license string into individual values and generate the appropriate SQL `IN` clause. Do NOT write custom parsing logic -- `apply_filter` already handles both single and multi-value comma-separated parameters.
- If the license parameter is present but contains invalid values, return a `400 Bad Request` response using the existing `AppError` pattern.

**Reuse applied:**

- Reuse `apply_filter` from `common/src/db/query.rs` directly for comma-separated parameter parsing and SQL IN clause generation.
- Follow the query struct pattern from `modules/fundamental/src/advisory/endpoints/list.rs` (the severity filter) -- add the `license` field to the existing Query struct in the same way severity is declared as an optional filter field there.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What changes:**

- Modify the `PackageService::list()` method signature to accept an optional license filter parameter (e.g., `license: Option<Vec<String>>`).
- When the license filter is provided, add a JOIN to the `package_license` table using the `entity::package_license` SeaORM entity from `entity/src/package_license.rs`, filtering where `package_license.license` is IN the provided license values.
- When the license filter is absent, the query remains unchanged (no regression).
- Follow the same error handling pattern used in other service methods: `Result<PaginatedResults<PackageSummary>, AppError>` with `.context()` wrapping.

**Reuse applied:**

- Use the `package_license` entity from `entity/src/package_license.rs` for the JOIN query rather than writing raw SQL. The entity already defines the `package_id` and `license` columns and their relationships, so the JOIN can be expressed using SeaORM's `JoinType::InnerJoin` with the entity's `Relation` definitions.
- Follow the same service-level filtering pattern as `AdvisoryService` in `modules/fundamental/src/advisory/service/advisory.rs`.

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**What changes:**

- Create integration tests for the license filter endpoint, following the test patterns established in sibling test files (`tests/api/advisory.rs`, `tests/api/sbom.rs`).
- Test cases:
  1. **Single license filter** -- `GET /api/v2/package?license=MIT` returns only packages with MIT license. Assert on specific package fields, not just count.
  2. **Comma-separated multi-value filter** -- `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that returned packages have one of the expected licenses.
  3. **No license filter** -- `GET /api/v2/package` returns all packages (verify no regression by comparing against a known set).
  4. **Invalid license value** -- `GET /api/v2/package?license=` or malformed value returns `400 Bad Request`.
- Each test function gets a doc comment (`///`) explaining what it verifies.
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments.
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` patterns consistent with sibling tests.
- Register this test file in `tests/Cargo.toml` if required by the project's test configuration.

## Files NOT Modified (out of scope)

- `entity/src/package_license.rs` -- used as-is for the JOIN; no modifications needed.
- `common/src/db/query.rs` -- `apply_filter` is reused directly; no modifications needed.
- `modules/fundamental/src/advisory/endpoints/list.rs` -- referenced as a pattern only; not modified.
- `modules/fundamental/src/package/endpoints/mod.rs` -- route registration unchanged since the existing `GET /api/v2/package` route already points to `list.rs`; the new query parameter is extracted automatically from the request.

## Implementation Sequence

1. Modify `modules/fundamental/src/package/endpoints/list.rs` -- add the `license` field to the Query struct and wire it through the handler using `apply_filter`.
2. Modify `modules/fundamental/src/package/service/mod.rs` -- add the license filter JOIN logic using `entity::package_license`.
3. Create `tests/api/package_license_filter.rs` -- write integration tests covering all acceptance criteria.
4. Run `cargo test` to verify all tests pass.
5. Run CI checks from `CONVENTIONS.md` if present.

## Acceptance Criteria Verification

| Criterion | How Verified |
|---|---|
| `GET /api/v2/package?license=MIT` returns only MIT packages | Integration test: single license filter |
| `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either | Integration test: multi-value filter |
| `GET /api/v2/package` without license returns all packages | Integration test: no filter regression |
| Response shape `PaginatedResults<PackageSummary>` unchanged | No changes to model structs; verified by existing tests continuing to pass |
| Invalid license values return 400 | Integration test: invalid license value |
