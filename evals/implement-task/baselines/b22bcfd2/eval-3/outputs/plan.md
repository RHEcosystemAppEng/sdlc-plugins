# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint, supporting both single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation follows the existing advisory severity filter pattern and reuses shared query-building infrastructure.

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add license query parameter extraction and filtering to the package list endpoint handler.

**Changes:**

- **Add `license` field to the Query struct:** Following the pattern in `modules/fundamental/src/advisory/endpoints/list.rs`, add an optional `license: Option<String>` field to the existing query parameter struct used by the `GET /api/v2/package` handler. The advisory list endpoint already has a `severity` field in its Query struct that follows this exact pattern -- mirror it for `license`.

- **Pass the license filter to the service layer:** After extracting query parameters, pass `query.license` to `PackageService::list()` (or the equivalent service method). This follows the same call pattern used in the advisory list endpoint, where the severity filter is forwarded from the endpoint handler to `AdvisoryService`.

- **Input validation:** Add validation that rejects invalid license values with a `400 Bad Request` response. Use the existing `AppError` enum from `common/src/error.rs` to return the error, consistent with how other endpoints handle bad input. Validate before calling the service layer.

- **No changes to the response shape:** The handler continues to return `PaginatedResults<PackageSummary>`. Only the input (query parameters) changes.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filtering logic to the PackageService list method.

**Changes:**

- **Accept a license filter parameter:** Modify the `list` method (or equivalent) on `PackageService` to accept an optional license filter parameter (e.g., `license: Option<String>`).

- **Reuse `apply_filter` from `common/src/db/query.rs`:** Call `apply_filter` to handle the comma-separated multi-value parsing and SQL `IN` clause generation. This function already handles splitting comma-separated values into individual terms and generating the appropriate `WHERE column IN (...)` clause. Do NOT write custom parsing logic for comma-separated values -- `apply_filter` provides this exact capability.

- **JOIN through `entity/src/package_license.rs`:** Use the `package_license` SeaORM entity to construct the JOIN between the `package` table and the `package_license` table. The entity already defines the relationship and column mappings. Build the join using SeaORM's relation/join API with the entity, rather than writing raw SQL joins. This filters packages to only those whose associated license in the `package_license` table matches the filter value(s).

- **Conditional application:** Only apply the license filter and JOIN when the `license` parameter is `Some`. When `None`, the query remains unchanged (no regression for unfiltered requests).

## Files to Create

### 1. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the license filter feature.

**Changes:**

- **Follow sibling test conventions:** Model the test file after existing tests in `tests/api/` (e.g., `advisory.rs`, `sbom.rs`). Use the same test setup, database seeding, and assertion patterns (`assert_eq!(resp.status(), StatusCode::OK)` followed by body deserialization).

- **Test cases to implement:**

  1. **`test_filter_packages_by_single_license`** -- Verify that `GET /api/v2/package?license=MIT` returns only packages with MIT license. Seed the database with packages having different licenses (MIT, Apache-2.0, GPL-3.0). Assert that the response contains only MIT-licensed packages by checking specific package identifiers, not just the count.

  2. **`test_filter_packages_by_multiple_licenses`** -- Verify that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Assert that both MIT and Apache-2.0 packages are present and GPL-3.0 packages are absent.

  3. **`test_list_packages_without_license_filter`** -- Verify that `GET /api/v2/package` (no license parameter) returns all packages unchanged. This is a regression test ensuring the new parameter does not affect default behavior.

  4. **`test_filter_packages_by_invalid_license`** -- Verify that an invalid license value returns `400 Bad Request`. Assert on the status code.

- **Document every test function:** Add a `///` doc comment before each test function explaining what it verifies.

- **Use given-when-then structure:** Add `// Given`, `// When`, `// Then` section comments inside each test body.

- **Value-based assertions:** Assert on specific package identifiers/names in the response, not just `items.len()`.

- **Register in test module:** Ensure the new test file is declared as a module in the test crate's `mod.rs` or `main.rs` so that `cargo test` discovers it.

## Code Reuse Strategy

The implementation deliberately avoids creating any new utility functions for query parameter parsing or filter application. All filtering logic is composed from existing infrastructure:

1. **`common/src/db/query.rs::apply_filter`** -- Reused directly for comma-separated multi-value parsing and SQL IN clause generation. No wrapper, no duplication.

2. **`modules/fundamental/src/advisory/endpoints/list.rs`** -- The severity filter pattern (Query struct with optional filter field, forwarded to service) is replicated structurally for the license filter. Same pattern, different field name and target column.

3. **`entity/src/package_license.rs`** -- The existing SeaORM entity is used for the JOIN query. No raw SQL, no new entity definitions.

## Data-Flow Trace

- **Input:** HTTP query parameter `license` extracted from `GET /api/v2/package?license=...` request
- **Validation:** Endpoint handler validates the license value(s) before forwarding
- **Processing:** `PackageService::list()` receives the filter, calls `apply_filter` to parse comma-separated values, joins through `package_license` entity, applies WHERE clause
- **Output:** Filtered `PaginatedResults<PackageSummary>` returned to client -- same response shape as before

## Scope Boundaries

- Only the files listed in "Files to Modify" and "Files to Create" are touched.
- No changes to response types, database schema, migrations, or other endpoints.
- No new utility functions that duplicate `apply_filter` functionality.
- No changes to `entity/src/package_license.rs` -- it is read/used, not modified.
