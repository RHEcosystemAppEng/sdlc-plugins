# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add an optional `license` query parameter to `GET /api/v2/package` that filters packages by SPDX license identifier. Support single-value (`?license=MIT`) and comma-separated multi-value (`?license=MIT,Apache-2.0`) filtering, following the existing advisory severity filter pattern.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**What changes:**
- Add an optional `license: Option<String>` field to the query parameter struct (following the same pattern as the `severity` field in `modules/fundamental/src/advisory/endpoints/list.rs`).
- In the handler function, extract the `license` query parameter and pass it to `PackageService::list()`.
- Add validation for the license parameter value — if present but containing invalid SPDX identifiers, return 400 Bad Request using `AppError`.

**How (referencing reuse):**
- Mirror the advisory list endpoint's `Query` struct pattern: add `pub license: Option<String>` alongside existing pagination/sorting fields.
- Pass `query.license` to the service layer, keeping the endpoint handler thin — no filtering logic here.

### 2. `modules/fundamental/src/package/service/mod.rs`

**What changes:**
- Update the `list` method signature on `PackageService` to accept an optional `license: Option<String>` parameter (or accept the full query struct).
- When `license` is `Some(value)`, use `apply_filter` from `common/src/db/query.rs` to parse the comma-separated values and build a SQL `IN` clause.
- Join through the `package_license` entity (`entity/src/package_license.rs`) to filter packages by their associated license records.
- When `license` is `None`, skip the join and filter entirely — existing behavior unchanged.

**How (referencing reuse):**
- Call `apply_filter(&mut query_builder, "package_license.license", &license_value)` (or the equivalent SeaORM column reference) to handle comma-separated parsing and IN clause generation. This avoids duplicating any splitting/filtering logic.
- Use the `package_license::Entity` from `entity/src/package_license.rs` for the JOIN — `package_license::Column::PackageId` joins to `package::Column::Id`, then filter on `package_license::Column::License`.
- Wrap any database errors with `.context()` per project conventions, returning `Result<PaginatedResults<PackageSummary>, AppError>`.

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**What it contains:**
Integration tests for the license filter feature, following the existing test patterns in `tests/api/advisory.rs` and `tests/api/sbom.rs`.

**Test cases:**

1. **`test_filter_single_license`** — Seed test DB with packages having MIT, Apache-2.0, and GPL-3.0 licenses. Send `GET /api/v2/package?license=MIT`. Assert response is 200, body is `PaginatedResults<PackageSummary>`, and all returned packages have license == "MIT".

2. **`test_filter_comma_separated_licenses`** — Same seed data. Send `GET /api/v2/package?license=MIT,Apache-2.0`. Assert response is 200 and returned packages have license in {MIT, Apache-2.0}. Assert GPL-3.0 package is excluded.

3. **`test_no_license_filter_returns_all`** — Same seed data. Send `GET /api/v2/package` (no license param). Assert response is 200 and all seeded packages are returned. This is the regression guard.

4. **`test_invalid_license_returns_400`** — Send `GET /api/v2/package?license=` (empty value) or a clearly invalid string. Assert response is 400 Bad Request.

**Conventions followed:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` / `StatusCode::BAD_REQUEST` pattern.
- Hit real PostgreSQL test database (per project testing convention).
- Register the test module in `tests/api/` (may need a `mod.rs` or `Cargo.toml` update).

### 4. `tests/api/mod.rs` (modify, if module-based test registration is used)

Add `mod package_license_filter;` to register the new test file. If tests are registered via `Cargo.toml` `[[test]]` entries instead, add the appropriate entry there.

## Implementation Sequence

1. **Read existing patterns** — Read `modules/fundamental/src/advisory/endpoints/list.rs` to capture the exact Query struct pattern, handler structure, and how `apply_filter` is called. Read `common/src/db/query.rs` to understand `apply_filter`'s signature and behavior. Read `entity/src/package_license.rs` to understand the entity columns.

2. **Modify service layer** (`package/service/mod.rs`) — Add the license filter parameter and filtering logic using `apply_filter` and the `package_license` entity join.

3. **Modify endpoint** (`package/endpoints/list.rs`) — Add `license` to the Query struct, extract it in the handler, pass to service, add validation.

4. **Create tests** (`tests/api/package_license_filter.rs`) — Write all four test cases.

5. **Verify** — Run `cargo test` to confirm all tests pass and no regressions in existing tests.

## What This Plan Does NOT Do

- Does not change the response shape (`PaginatedResults<PackageSummary>`) — the response remains identical.
- Does not duplicate filtering logic — reuses `apply_filter` from `common/src/db/query.rs`.
- Does not write raw SQL — uses SeaORM entities and the shared query builder.
- Does not require database migrations — the `package_license` table already exists.
- Does not modify any other endpoints.
