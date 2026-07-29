# Criterion 1: GET /api/v2/package?license=MIT returns only packages with MIT license

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through the following code path:

### Query Parameter Parsing (list.rs)

The `PackageListParams` struct adds a new `license: Option<String>` field. When a request arrives at `GET /api/v2/package?license=MIT`, Axum's `Query` extractor deserializes the query string into `PackageListParams`, populating `license` with `Some("MIT")`.

### Validation (list.rs)

In `list_packages`, when `params.license` is `Some`, the handler calls `validate_license_param("MIT")`. This function:
1. Splits the input on commas: produces `["MIT"]`
2. Trims whitespace from each token
3. Validates each token with `spdx::Expression::parse(id)` -- "MIT" is a valid SPDX identifier, so validation passes
4. Returns `Ok(vec!["MIT".to_string()])`

### Service Layer Filtering (service/mod.rs)

The validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`. When `license_filter` is `Some(["MIT"])`:
1. A `Condition::any()` filter is constructed with `package_license::Column::License.is_in(["MIT"])`, which generates an SQL `WHERE package_license.license IN ('MIT')` clause
2. An `InnerJoin` is added on `package::Relation::PackageLicense` to join the package table with the package_license table
3. The count query (`total`) and items query both operate on this filtered dataset

### Test Coverage

The test `test_list_packages_single_license_filter` directly validates this criterion:
- Seeds 3 packages: pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (MIT)
- Queries `GET /api/v2/package?license=MIT`
- Asserts `StatusCode::OK`
- Asserts `body.items.len() == 2` (only the two MIT packages)
- Asserts `body.items.iter().all(|p| p.license == "MIT")` (all returned packages have MIT license)

### Conclusion

The endpoint correctly parses the single license query parameter, validates it against the SPDX specification, applies an inner join with a WHERE IN clause to filter results, and returns only matching packages. The test confirms the expected behavior.
