## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict:** PASS

### Reasoning

The PR adds a `license` field of type `Option<String>` to the `PackageListParams` struct in `list.rs`, which Axum's `Query` extractor will deserialize from the query string parameter `?license=MIT`.

When the `license` parameter is present, the handler calls `validate_license_param(license)` which:
1. Splits the value on commas (for a single value like `"MIT"`, this produces a one-element vector)
2. Validates each identifier via `spdx::Expression::parse(id)`, which will succeed for `"MIT"` as it is a valid SPDX identifier
3. Returns `Ok(vec!["MIT".to_string()])`

The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`. In the service layer:
1. The `if let Some(licenses)` branch activates
2. `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` creates a WHERE clause matching `package_license.license IN ('MIT')`
3. `JoinType::InnerJoin` on `package::Relation::PackageLicense.def()` joins the package_license table

This ensures only packages with a matching license row (MIT) are included in the results. The return type remains `Json<PaginatedResults<PackageSummary>>`, so only MIT-licensed packages are returned.

The integration test `test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, filters by MIT, and asserts that exactly 2 MIT packages are returned and all have `license == "MIT"`.

### Evidence

- `list.rs`: `pub license: Option<String>` field added to `PackageListParams`
- `list.rs`: `validate_license_param` function splits on comma, validates via `Expression::parse`
- `service/mod.rs`: `is_in(licenses.iter().cloned())` with `InnerJoin` on `PackageLicense`
- `tests/api/package.rs`: `test_list_packages_single_license_filter` covers this exact scenario
