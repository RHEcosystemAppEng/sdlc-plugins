# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The PR implements single-license filtering through the following code path:

1. **Query parameter parsing** (`list.rs`): The `PackageListParams` struct adds a `pub license: Option<String>` field. When a request includes `?license=MIT`, Axum's `Query` extractor deserializes this into `Some("MIT")`.

2. **Validation** (`list.rs`): The `validate_license_param` function splits the license string on commas and validates each identifier against the SPDX expression parser (`Expression::parse(id)`). For a single value like `"MIT"`, this produces a `Vec<String>` containing one element: `["MIT"]`.

3. **Service integration** (`list.rs`): The handler passes `license_filter.as_deref()` (an `Option<&[String]>`) to `PackageService::list()`.

4. **Database filtering** (`service/mod.rs`): When `license_filter` is `Some(licenses)`, the service applies:
   - A `Condition::any()` with `package_license::Column::License.is_in(licenses.iter().cloned())` -- this generates a SQL `WHERE license IN ('MIT')` clause
   - An `InnerJoin` to `PackageLicense` to link packages to their licenses

   This ensures only packages whose license column matches "MIT" are returned.

5. **Test coverage** (`tests/api/package.rs`): The `test_list_packages_single_license_filter` test seeds three packages (two with MIT, one with Apache-2.0), queries `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items are returned
   - All returned items have `license == "MIT"`

The implementation correctly filters packages to return only those matching the specified single license identifier.
