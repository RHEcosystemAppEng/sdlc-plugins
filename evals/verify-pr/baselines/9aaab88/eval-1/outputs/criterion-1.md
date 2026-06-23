## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

### Analysis

The PR adds the `license` field as `Option<String>` to the `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs`. When present, the handler calls `validate_license_param(license)` which splits the value by comma, trims whitespace, and validates each identifier via `spdx::Expression::parse()`. Valid identifiers are passed to the service layer.

In `modules/fundamental/src/package/service/mod.rs`, the `list` method now accepts `license_filter: Option<&[String]>`. When provided, it applies a `Condition::any()` filter using `package_license::Column::License.is_in(licenses.iter().cloned())` with an `InnerJoin` on `package::Relation::PackageLicense`. For a single license value like `MIT`, the `is_in` clause contains one element, effectively filtering to only MIT-licensed packages.

### Test Coverage

The test `test_list_packages_single_license_filter` in `tests/api/package.rs`:
- Seeds packages with MIT and Apache-2.0 licenses
- Queries `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned (the two MIT packages)
- Asserts all returned packages have `license == "MIT"`

This directly validates the acceptance criterion.
