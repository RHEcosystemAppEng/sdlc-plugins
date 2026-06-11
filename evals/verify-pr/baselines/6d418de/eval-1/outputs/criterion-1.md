# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR implements single-license filtering through a complete chain from endpoint to service layer:

1. **Endpoint layer** (`modules/fundamental/src/package/endpoints/list.rs`):
   - The `PackageListParams` struct adds `pub license: Option<String>`, which Axum's `Query` extractor will parse from the `?license=MIT` query parameter.
   - The `validate_license_param` function splits the license string on commas, trims whitespace, and validates each identifier against the `spdx::Expression::parse()` function. For a single value like `MIT`, this produces a `Vec<String>` containing one element: `["MIT"]`.
   - The handler calls `validate_license_param` when `params.license` is `Some`, converting it to `Some(vec!["MIT"])`, which is passed to `PackageService::list()`.

2. **Service layer** (`modules/fundamental/src/package/service/mod.rs`):
   - The `list` method now accepts `license_filter: Option<&[String]>`.
   - When `license_filter` is `Some(licenses)`, it applies a `Condition::any()` filter using `package_license::Column::License.is_in(licenses.iter().cloned())`.
   - It joins `package::Relation::PackageLicense` via `InnerJoin`, ensuring only packages with a matching license in the `package_license` table are returned.
   - For a single license `["MIT"]`, `is_in` with one element behaves like an equality check, returning only MIT-licensed packages.

3. **Test coverage** (`tests/api/package.rs`):
   - `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries `?license=MIT`, and asserts that exactly 2 packages are returned and all have `license == "MIT"`.

The implementation correctly filters packages by a single SPDX license identifier.
