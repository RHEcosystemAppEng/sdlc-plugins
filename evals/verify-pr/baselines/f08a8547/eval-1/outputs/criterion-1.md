# Criterion 1: GET /api/v2/package?license=MIT returns only packages with MIT license

## Verdict: PASS

## Analysis

This criterion requires that when the `license` query parameter is set to a single value (`MIT`), the endpoint returns only packages matching that license.

### Code Changes

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**
- The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor deserializes from the query string.
- The `list_packages` handler calls `validate_license_param(license)` when the parameter is present, producing a `Vec<String>` with the single entry `["MIT"]`.
- The validated filter is passed to `PackageService::list()` as `license_filter: Option<&[String]>`.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**
- When `license_filter` is `Some`, the service applies a `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())`. For a single value, this produces a WHERE clause equivalent to `WHERE package_license.license IN ('MIT')`.
- An `InnerJoin` to `package::Relation::PackageLicense` ensures only packages with a matching license row are returned.
- The filter is applied before both the `count` query and the paginated `items` query, so only matching packages appear in results and the total count reflects the filtered set.

### Test Coverage

**`tests/api/package.rs::test_list_packages_single_license_filter`:**
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT).
- Queries `GET /api/v2/package?license=MIT`.
- Asserts response status is 200 OK.
- Asserts `body.items.len() == 2` (only the two MIT packages).
- Asserts `body.items.iter().all(|p| p.license == "MIT")` (all returned packages have the MIT license).

### Conclusion

The implementation correctly adds license filtering with single-value support. The query parameter is parsed, validated against SPDX, and used to filter the database query via an IN clause with an inner join. The test covers the exact scenario described in the criterion and verifies both the count and content of returned packages.
