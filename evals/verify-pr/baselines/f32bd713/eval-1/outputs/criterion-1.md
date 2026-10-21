## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Reasoning

The PR implements single-license filtering through the following code path:

1. **Query parameter parsing:** The `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs` adds a new `license: Option<String>` field. When the request includes `?license=MIT`, Axum's `Query` extractor deserializes this into `Some("MIT")`.

2. **Validation:** The `validate_license_param` function splits the license string on commas and validates each identifier against the SPDX expression parser (`spdx::Expression::parse(id)`). For a single value like `"MIT"`, this produces a `Vec<String>` containing one element: `["MIT"]`.

3. **Filter application:** In `modules/fundamental/src/package/service/mod.rs`, the `list` method now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, it applies:
   - A `Condition::any()` filter with `package_license::Column::License.is_in(licenses.iter().cloned())` -- this generates a SQL `WHERE license IN ('MIT')` clause
   - An `InnerJoin` on `package::Relation::PackageLicense` to join the package-license mapping table

   This ensures only packages whose license matches "MIT" are returned.

4. **Response shape:** The return type remains `Result<Json<PaginatedResults<PackageSummary>>, AppError>`, preserving the existing response format.

5. **Test coverage:** The `test_list_packages_single_license_filter` integration test in `tests/api/package.rs` directly verifies this criterion:
   - Seeds three packages (two with MIT, one with Apache-2.0)
   - Sends `GET /api/v2/package?license=MIT`
   - Asserts response status is 200 OK
   - Asserts exactly 2 items are returned
   - Asserts all returned items have `license == "MIT"`

### Evidence

- `list.rs` line: `pub license: Option<String>` added to `PackageListParams`
- `list.rs` function: `validate_license_param` parses and validates SPDX identifiers
- `mod.rs` filter: `Condition::any().add(package_license::Column::License.is_in(licenses.iter().cloned()))`
- `mod.rs` join: `query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def())`
- Test: `test_list_packages_single_license_filter` verifies the behavior end-to-end
