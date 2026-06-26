# Implementation Plan: TC-9203 -- Add package license filter to list endpoint

## Overview

Add a `license` query parameter to `GET /api/v2/package` supporting single-value and comma-separated multi-value filtering by SPDX license identifier. The implementation reuses existing filter infrastructure rather than creating new utility functions.

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Purpose:** Add `license` query parameter extraction and filtering to the package list endpoint handler.

**Changes:**

- **Add `license` field to the Query struct:** Following the pattern in `modules/fundamental/src/advisory/endpoints/list.rs` (where `severity` is an optional query parameter), add an `Option<String>` field named `license` to the existing query parameter struct used by the `GET /api/v2/package` handler. This mirrors the advisory endpoint's Query struct pattern exactly.

- **Pass the license filter to the service layer:** In the handler function, extract `query.license` and pass it to `PackageService::list()` as an additional parameter. If `license` is `None`, no filter is applied (preserving backward compatibility).

- **Validate license input:** Add validation for the `license` parameter value. If the value is present but empty or contains invalid characters, return a `400 Bad Request` response using the existing `AppError` enum from `common/src/error.rs`. Follow the same validation pattern used for other query parameters in sibling endpoint files.

- **No new utility functions:** The comma-separated parsing and SQL IN clause generation is handled entirely by `common/src/db/query.rs::apply_filter` -- do not create any new parsing or filter helper functions.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Purpose:** Add license filter logic to the `PackageService` list method.

**Changes:**

- **Add license filter parameter:** Extend the `PackageService::list()` method signature to accept an optional license filter parameter (`Option<String>` or equivalent).

- **Build the JOIN query using `entity/src/package_license.rs`:** When a license filter is provided, join through the `package_license` entity (from `entity/src/package_license.rs`) to filter packages by their associated license SPDX identifier. Use SeaORM's join capabilities with the existing `package_license` entity rather than writing raw SQL.

- **Apply the filter using `apply_filter`:** Call `common/src/db/query.rs::apply_filter` to handle the comma-separated license value string. `apply_filter` parses comma-separated values and generates the appropriate SQL `IN` clause, supporting both single values (`license=MIT`) and multi-value (`license=MIT,Apache-2.0`). This is the same function used by the advisory endpoint's severity filter.

- **Preserve existing behavior when no filter:** When the license parameter is `None`, skip the JOIN and filter entirely so that the existing behavior (return all packages) is unchanged.

- **Return type unchanged:** The method continues to return `PaginatedResults<PackageSummary>`, preserving the response shape.

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests verifying the license filter behavior.

**Test cases (following patterns from sibling test files `tests/api/advisory.rs` and `tests/api/sbom.rs`):**

1. **`test_list_packages_filter_single_license`** -- Verifies that `GET /api/v2/package?license=MIT` returns only packages with the MIT license. Asserts on specific package identifiers in the response, not just the count.

2. **`test_list_packages_filter_multiple_licenses`** -- Verifies that `GET /api/v2/package?license=MIT,Apache-2.0` returns packages matching either license. Asserts that results include packages with both MIT and Apache-2.0 licenses.

3. **`test_list_packages_no_license_filter`** -- Verifies that `GET /api/v2/package` without a license parameter returns all packages (no regression). Compares against expected total count.

4. **`test_list_packages_invalid_license`** -- Verifies that an invalid license value returns `400 Bad Request`. Asserts on `resp.status() == StatusCode::BAD_REQUEST`.

**Conventions applied:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` pattern from sibling tests
- Use `PaginatedResults<PackageSummary>` for response deserialization
- Follow `test_<endpoint>_<scenario>` naming convention
- Each test function gets a `///` doc comment explaining what it verifies
- Non-trivial tests include `// Given`, `// When`, `// Then` section comments
- Tests run against a real PostgreSQL test database (integration test pattern)

---

## Module Registration

- The new test file `tests/api/package_license_filter.rs` must be registered as a test module in `tests/Cargo.toml` or a `mod.rs` file if the test suite uses one (following the pattern of existing test files like `sbom.rs` and `advisory.rs`).

---

## Reuse Summary

| Reuse Candidate | How Used |
|---|---|
| `common/src/db/query.rs::apply_filter` | Called directly in `PackageService::list()` to parse comma-separated license values and generate SQL IN clause -- no new parsing logic written |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Filter pattern replicated: optional field on Query struct, extraction in handler, pass-through to service layer |
| `entity/src/package_license.rs` | Used as the SeaORM entity for the JOIN between packages and licenses -- no raw SQL written |

---

## What This Plan Does NOT Do

- Does not create any new utility functions for comma-separated value parsing (reuses `apply_filter`)
- Does not modify the response shape (`PaginatedResults<PackageSummary>` remains unchanged)
- Does not touch files outside the defined scope (Files to Modify + Files to Create)
- Does not modify endpoint registration (`endpoints/mod.rs`) or route mounting (`server/main.rs`) -- the existing route for `GET /api/v2/package` is unchanged, only the handler's query parameter acceptance is extended
