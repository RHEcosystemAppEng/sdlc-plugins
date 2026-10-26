# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The diff satisfies this criterion through both implementation and testing.

**Implementation**: In `modules/fundamental/src/package/endpoints/list.rs`, a `license` field of type `Option<String>` is added to `PackageListParams`. When present, the value is passed through `validate_license_param()` which splits on commas, validates each identifier via `spdx::Expression::parse()`, and returns the list. For a single value like `MIT`, this produces a one-element vector. The validated identifiers are then passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

In `modules/fundamental/src/package/service/mod.rs`, when `license_filter` is `Some`, the query builder adds a `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())` and joins to the `PackageLicense` table via `InnerJoin`. For a single license value, this effectively produces a `WHERE package_license.license IN ('MIT')` clause with an inner join, ensuring only packages with a matching license record are returned.

**Test coverage**: The test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds three packages (two with MIT, one with Apache-2.0), queries `?license=MIT`, and asserts:
- Response status is 200 OK
- Exactly 2 items are returned
- All returned items have `license == "MIT"`

This directly verifies the criterion.
