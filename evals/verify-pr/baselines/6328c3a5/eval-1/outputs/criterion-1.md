# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through changes in both the endpoint and service layers.

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- A `license: Option<String>` field is added to the `PackageListParams` struct, which means Axum will automatically parse the `?license=MIT` query parameter from the URL.
- When `license` is `Some`, the `validate_license_param` function is called, which splits on commas and validates each identifier via `spdx::Expression::parse(id)`. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.
- The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- The `list` method signature is updated to accept `license_filter: Option<&[String]>`.
- When `license_filter` is `Some`, a `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())` is applied as a filter, and an `InnerJoin` to the `PackageLicense` relation is added. This ensures only packages whose license column matches one of the provided identifiers are returned.
- For a single value `["MIT"]`, the `is_in` clause effectively becomes `WHERE package_license.license IN ('MIT')`, returning only MIT-licensed packages.

**Test coverage** (`tests/api/package.rs`):
- The test `test_list_packages_single_license_filter` seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT). It then requests `GET /api/v2/package?license=MIT` and asserts:
  - Status is 200 OK
  - Exactly 2 items are returned
  - All returned items have `license == "MIT"`
- This directly validates the criterion.
