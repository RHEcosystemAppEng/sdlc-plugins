# Implementation Plan: TC-9203 — Add package license filter to list endpoint

## Overview

Add a `license` query parameter to the `GET /api/v2/package` list endpoint in the
trustify-backend repository. The filter supports exact SPDX identifier matching with
both single-value and comma-separated multi-value input.

**Target Branch:** main
**Repository:** trustify-backend

---

## Files to Modify

### 1. `modules/fundamental/src/package/endpoints/list.rs`

**Current state:** Implements `GET /api/v2/package` without a license filter.

**Changes:**
- Add an optional `license: Option<String>` field to the query parameters struct
  (following the same pattern as the `severity` field in the advisory list endpoint at
  `modules/fundamental/src/advisory/endpoints/list.rs`).
- In the handler function, extract the `license` query parameter and pass it to
  `PackageService::list()`.
- Add input validation: if the `license` parameter contains values that are not valid
  SPDX identifiers, return `400 Bad Request` with a descriptive error message using
  `AppError`.

### 2. `modules/fundamental/src/package/service/mod.rs`

**Current state:** `PackageService::list()` fetches all packages with pagination but
no license filtering.

**Changes:**
- Add an optional `license` parameter to the `list()` method signature (e.g.,
  `license: Option<String>`).
- When the parameter is present, use `apply_filter` from `common/src/db/query.rs` to
  parse the comma-separated values and generate a SQL `IN` clause.
- Join through the `package_license` entity (`entity/src/package_license.rs`) to
  filter packages by their declared license. Use SeaORM's `JoinType::InnerJoin` on
  the `package_license` table, filtering by the `license` column.
- When the parameter is absent, skip the join and filter entirely (preserving current
  behavior — no regression).

---

## Files to Create

### 3. `tests/api/package_license_filter.rs`

**Purpose:** Integration tests for the new license filter on the package list endpoint.

**Test cases (following sibling test conventions from `tests/api/advisory.rs` and
`tests/api/sbom.rs`):**

1. **`test_filter_packages_by_single_license`** — Seed the test database with packages
   having different licenses (MIT, Apache-2.0, GPL-3.0). Request
   `GET /api/v2/package?license=MIT`. Assert that only MIT-licensed packages are
   returned. Validate specific package identifiers in the response, not just count.

2. **`test_filter_packages_by_multiple_licenses`** — Seed with mixed licenses. Request
   `GET /api/v2/package?license=MIT,Apache-2.0`. Assert that packages with either
   MIT or Apache-2.0 are returned, and GPL-3.0 packages are excluded.

3. **`test_no_license_filter_returns_all`** — Seed with mixed licenses. Request
   `GET /api/v2/package` (no license parameter). Assert that all packages are returned.
   Verify total count matches the seeded data.

4. **`test_invalid_license_returns_400`** — Request
   `GET /api/v2/package?license=NOT_A_VALID_LICENSE_!@#`. Assert response status is
   `400 Bad Request`.

**Conventions applied:**
- Use `assert_eq!(resp.status(), StatusCode::OK)` for status checks.
- Deserialize response body into `PaginatedResults<PackageSummary>`.
- Validate both `total_count` and individual item field values.
- Each test function gets a `///` doc comment explaining what it verifies.
- Non-trivial tests use `// Given`, `// When`, `// Then` section comments.
- Follow the `test_<endpoint>_<scenario>` naming pattern.

---

## Files to Inspect (read-only, not modified)

These files are referenced during implementation but require no changes:

| File | Purpose |
|---|---|
| `common/src/db/query.rs` | Reuse `apply_filter` for comma-separated parameter parsing |
| `modules/fundamental/src/advisory/endpoints/list.rs` | Reference pattern for adding a filter query parameter |
| `modules/fundamental/src/advisory/service/advisory.rs` | Reference pattern for applying a service-level filter |
| `entity/src/package_license.rs` | Existing SeaORM entity for the package-license join table |
| `modules/fundamental/src/package/model/summary.rs` | Confirm `PackageSummary` struct shape (includes `license` field) |
| `common/src/model/paginated.rs` | Confirm `PaginatedResults<T>` wrapper (response shape must not change) |
| `common/src/error.rs` | Use `AppError` for 400 Bad Request on invalid license values |
| `tests/api/advisory.rs` | Sibling test file for convention conformance analysis |
| `tests/api/sbom.rs` | Sibling test file for convention conformance analysis |
| `CONVENTIONS.md` | Check for CI verification commands |

---

## Implementation Order

1. **Understand the code (Step 4):** Read the advisory filter pattern in
   `advisory/endpoints/list.rs` and `advisory/service/advisory.rs`. Read
   `common/src/db/query.rs` to understand `apply_filter`. Read
   `entity/src/package_license.rs` for the join table schema. Read sibling tests
   in `tests/api/advisory.rs` for test conventions. Read `CONVENTIONS.md` for CI
   check commands.

2. **Modify service layer:** Update `PackageService::list()` in
   `modules/fundamental/src/package/service/mod.rs` to accept and apply the license
   filter using `apply_filter` and a join on `package_license`.

3. **Modify endpoint layer:** Update the query struct and handler in
   `modules/fundamental/src/package/endpoints/list.rs` to extract the `license`
   query parameter and pass it to the service.

4. **Write tests:** Create `tests/api/package_license_filter.rs` with all four
   test cases.

5. **Run tests and CI checks:** Execute `cargo test` and any CI commands from
   `CONVENTIONS.md`. Fix any failures.

6. **Verify acceptance criteria:** Confirm each criterion is satisfied by the
   test results and code inspection.

7. **Commit, push, open PR** targeting `main` with message:
   `feat(package): add license filter to list endpoint`
   Footer: `Implements TC-9203`

---

## How Existing Code is Reused

See the companion file `reuse-analysis.md` for a detailed breakdown of each Reuse
Candidate and how it is applied.
