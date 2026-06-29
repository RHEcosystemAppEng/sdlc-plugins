# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR implements this criterion through two coordinated changes:

### Endpoint Layer (`modules/fundamental/src/package/endpoints/list.rs`)

1. **Parameter parsing:** The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will automatically deserialize from the `?license=MIT` query parameter.

2. **Validation:** The `validate_license_param` function splits the license string by comma, trims whitespace, and validates each identifier against the SPDX expression parser (`spdx::Expression::parse`). "MIT" is a valid SPDX identifier, so it passes validation.

3. **Filter construction:** In `list_packages`, when `params.license` is `Some("MIT")`, the code calls `validate_license_param("MIT")` which returns `Ok(vec!["MIT".to_string()])`. This is passed to `PackageService::list` as `Some(&["MIT"])`.

### Service Layer (`modules/fundamental/src/package/service/mod.rs`)

4. **Query filtering:** When `license_filter` is `Some(["MIT"])`, the service builds a SeaORM query with:
   - `Condition::any().add(package_license::Column::License.is_in(["MIT"]))` -- filters to rows where the license column matches "MIT"
   - `JoinType::InnerJoin` on `package::Relation::PackageLicense` -- joins the package table to the package_license table

   This ensures only packages with a matching license in the `package_license` table are returned.

5. **Pagination preserved:** The `total` count is computed after filtering (`query.clone().count()`), so it reflects only MIT-licensed packages. The `items` query also operates on the filtered set.

### Test Coverage

The test `test_list_packages_single_license_filter` in `tests/api/package.rs` directly exercises this criterion:
- Seeds 3 packages: pkg-a (MIT), pkg-b (Apache-2.0), pkg-c (MIT)
- Requests `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts exactly 2 items returned
- Asserts all returned items have `license == "MIT"`

This test validates the end-to-end behavior described by the criterion.
