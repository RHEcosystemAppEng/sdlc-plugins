## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Evidence

**Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
- The `PackageListParams` struct now includes `pub license: Option<String>`, which means the query parameter `?license=MIT` will be deserialized into this field.
- In `list_packages`, when `params.license` is `Some`, `validate_license_param(license)` is called, which splits by comma, trims, and validates each identifier via `spdx::Expression::parse(id)`. For a single value like "MIT", this produces `vec!["MIT"]`.
- The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

**Service layer** (`modules/fundamental/src/package/service/mod.rs`):
- When `license_filter` is `Some(licenses)`, a `Condition::any()` is constructed with `package_license::Column::License.is_in(licenses.iter().cloned())`. For a single-element vec `["MIT"]`, this generates a SQL `WHERE package_license.license IN ('MIT')` condition.
- An `InnerJoin` with `package::Relation::PackageLicense` is added, ensuring only packages that have a matching license join row are returned.

**Test coverage** (`tests/api/package.rs`):
- `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, requests `?license=MIT`, and asserts:
  - Status 200 OK
  - Exactly 2 items returned (the 2 MIT packages)
  - All returned items have `license == "MIT"`

The implementation correctly filters packages by a single license identifier and the test validates this behavior.
