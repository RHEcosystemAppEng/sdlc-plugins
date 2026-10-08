## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Result: PASS**

### Evidence

The PR implements single-license filtering through the following code path:

1. **Query parameter extraction** (`modules/fundamental/src/package/endpoints/list.rs`): The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor deserializes from the URL query string. When a request arrives with `?license=MIT`, this field is populated with `Some("MIT")`.

2. **Validation** (`list.rs` -- `validate_license_param`): The handler calls `validate_license_param(license)` which splits by comma (yielding `["MIT"]` for a single value), trims whitespace, and validates each identifier via `spdx::Expression::parse(id)`. A valid SPDX identifier like `MIT` passes validation and the function returns `Ok(vec!["MIT".to_string()])`.

3. **Filter application** (`modules/fundamental/src/package/service/mod.rs`): The `PackageService::list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, the query is augmented with:
   - `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))` -- this produces a SQL `WHERE package_license.license IN ('MIT')` clause
   - An `InnerJoin` on `package::Relation::PackageLicense` to connect the package table to the license table

   This ensures only packages whose associated license matches `MIT` are returned.

4. **Test coverage** (`tests/api/package.rs` -- `test_list_packages_single_license_filter`): The test seeds three packages (two MIT, one Apache-2.0), queries with `?license=MIT`, and asserts:
   - Response status is `200 OK`
   - Result contains exactly 2 items
   - All returned items have `license == "MIT"`

The implementation correctly filters packages by a single license identifier and the test validates the behavior end-to-end.
