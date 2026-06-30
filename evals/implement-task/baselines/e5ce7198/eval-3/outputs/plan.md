# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Summary

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by their declared SPDX license identifier. Support single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering. The implementation reuses the existing `apply_filter` helper, follows the established severity filter pattern from the advisory module, and joins through the existing `package_license` entity.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What changes:**

- Add an optional `license: Option<String>` field to the query parameter struct (the struct that Axum deserializes from query parameters for the list endpoint). This follows the identical pattern used by the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`.
- In the handler function, extract the `license` value from the query struct and pass it to the `PackageService::list` method as a new parameter (or as part of an options/filter struct, matching whichever convention the advisory list handler uses).
- No changes to the response type or response construction — `PaginatedResults<PackageSummary>` remains unchanged.

**Reuse:** Mirror the exact pattern from `modules/fundamental/src/advisory/endpoints/list.rs` where the `severity` query parameter is extracted and forwarded to the service layer.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What changes:**

- Modify the `PackageService::list` method signature to accept an optional license filter parameter (e.g., `license: Option<String>` or as a field in a filter struct).
- When the `license` parameter is `Some`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated string into individual values and generate the appropriate SQL `IN` clause condition.
- Join the query through the `package_license` entity (`entity/src/package_license.rs`) to correlate packages with their declared licenses. Use SeaORM's relation/join API (e.g., `join(JoinType::InnerJoin, entity::package_license::Relation::Package.def())`) rather than writing raw SQL.
- When `license` is `None`, do not add the join or filter — preserving existing behavior for requests without the parameter.
- Add validation for license values. If a license value fails validation (e.g., empty string after splitting), return an `AppError` that maps to 400 Bad Request.

**Reuse:**
- Call `apply_filter` from `common/src/db/query.rs` directly — this function already handles parsing comma-separated values and generating the SQL `IN` clause. Do NOT reimplement this parsing logic.
- Use the `package_license` entity from `entity/src/package_license.rs` for the join — do NOT write raw SQL for the package-to-license relationship.
- Follow the same service-layer filtering pattern used in `modules/fundamental/src/advisory/service/advisory.rs` for the severity filter.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**What changes:**

- Create integration tests following the patterns established in `tests/api/advisory.rs` and `tests/api/sbom.rs`.
- Set up test data: insert packages with known licenses (MIT, Apache-2.0, GPL-3.0) into the test database via the existing test fixtures/helpers.
- Test cases:
  1. **Single license filter**: `GET /api/v2/package?license=MIT` returns only MIT-licensed packages; verify the response is `PaginatedResults<PackageSummary>` with correct items.
  2. **Multi-value license filter**: `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license; verify both are included and GPL-3.0 is excluded.
  3. **No filter (regression)**: `GET /api/v2/package` without `license` parameter returns all packages unchanged.
  4. **Invalid license value**: `GET /api/v2/package?license=` (empty value) returns 400 Bad Request.
- Use `assert_eq!(resp.status(), StatusCode::OK)` and `assert_eq!(resp.status(), StatusCode::BAD_REQUEST)` patterns consistent with existing tests.

### 4. `tests/api/mod.rs` (modify, if test module registration is needed)

- Add `mod package_license_filter;` to register the new test module, following the pattern of existing test module declarations.

---

## Implementation Order

1. **Service layer first** (`package/service/mod.rs`): Add the license filter logic with `apply_filter` and the `package_license` join. This is the core business logic.
2. **Endpoint layer** (`package/endpoints/list.rs`): Add the query parameter struct field and forward to the service. This is a thin wiring change.
3. **Tests** (`tests/api/package_license_filter.rs`): Write integration tests to verify all acceptance criteria.
4. **Verify**: Run `cargo test` to confirm all tests pass and `cargo clippy` for lint compliance.

---

## What does NOT change

- `entity/src/package_license.rs` — the entity already exists and maps the package-license relationship; no modifications needed.
- `common/src/db/query.rs` — the `apply_filter` function already handles comma-separated multi-value parsing; no modifications needed.
- `modules/fundamental/src/package/model/summary.rs` — `PackageSummary` already includes a `license` field; the response shape is unchanged.
- `modules/fundamental/src/package/endpoints/mod.rs` — route registration does not change since the endpoint path remains the same (only query parameters change).
- No database migrations required — the `package_license` table already exists.
