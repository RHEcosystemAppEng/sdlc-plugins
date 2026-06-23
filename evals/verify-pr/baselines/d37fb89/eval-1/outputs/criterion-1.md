# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through changes in both the endpoint and service layers.

### Endpoint Layer (`modules/fundamental/src/package/endpoints/list.rs`)

- A `license: Option<String>` field is added to the `PackageListParams` struct, enabling Axum's `Query` extractor to parse the `?license=MIT` query parameter from the URL.
- When `params.license` is `Some`, the handler calls `validate_license_param(license)`, which splits on commas, trims whitespace, and validates each identifier against the `spdx::Expression::parse` function. For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.
- The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

### Service Layer (`modules/fundamental/src/package/service/mod.rs`)

- The `list` method signature is extended to accept `license_filter: Option<&[String]>`.
- When `license_filter` is `Some`, the method applies:
  - A `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())` -- for a single license value like `["MIT"]`, this generates a `WHERE package_license.license IN ('MIT')` clause.
  - An `InnerJoin` to the `PackageLicense` table via `package::Relation::PackageLicense.def()`.
- This ensures only packages with a matching license row are returned.

### Test Coverage

- `test_list_packages_single_license_filter` seeds 3 packages (2 MIT, 1 Apache-2.0), queries `?license=MIT`, and asserts:
  - Response status is 200 OK
  - Exactly 2 items returned
  - All items have `license == "MIT"`

This directly exercises the criterion's scenario and validates the filtering logic end-to-end.
