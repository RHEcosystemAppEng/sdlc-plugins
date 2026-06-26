# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The implementation satisfies this criterion through the following code path:

1. **Query parameter parsing**: The `PackageListParams` struct in `list.rs` now includes `pub license: Option<String>`, which Axum's `Query` extractor automatically deserializes from the URL query string. When a request includes `?license=MIT`, this field is populated with `Some("MIT")`.

2. **Validation**: The `validate_license_param` function splits the license string on commas and validates each identifier using `spdx::Expression::parse()`. For a single value like `"MIT"`, this produces a `Vec<String>` containing one element: `["MIT"]`.

3. **Filtering**: In the `list_packages` handler, the validated identifiers are passed to `PackageService::list()` as `license_filter: Option<&[String]>`. The service method applies the filter:
   ```rust
   if let Some(licenses) = license_filter {
       query = query.filter(
           Condition::any()
               .add(package_license::Column::License.is_in(licenses.iter().cloned()))
       );
       query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   }
   ```
   The `InnerJoin` on the `PackageLicense` relation combined with the `is_in` filter ensures only packages whose license column matches `"MIT"` are returned.

4. **Test coverage**: `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), filters by `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned
   - All returned items have `license == "MIT"`

The code correctly implements single-license filtering with validation and test coverage.
