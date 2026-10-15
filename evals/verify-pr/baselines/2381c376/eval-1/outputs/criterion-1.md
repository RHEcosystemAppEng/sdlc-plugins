## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Analysis

**Code evidence in the diff:**

1. **Query parameter parsing** (`list.rs`): The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will populate from the `?license=MIT` query string.

2. **Validation** (`list.rs`): The `validate_license_param` function splits the license string on commas and validates each identifier against the SPDX expression parser (`Expression::parse(id)`). For a single value like `MIT`, this produces a `Vec<String>` containing `["MIT"]`.

3. **Filtering** (`service/mod.rs`): The `list` method now accepts `license_filter: Option<&[String]>`. When `Some`, it applies:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   This inner-joins the package-license table and filters rows where the license column matches any value in the provided list. For a single-element list `["MIT"]`, this effectively returns only MIT-licensed packages.

4. **Handler wiring** (`list.rs`): The `list_packages` handler extracts the license parameter, validates it, and passes it to `PackageService::list`. The return type remains `Result<Json<PaginatedResults<PackageSummary>>, AppError>`.

**Test evidence:**

The test `test_list_packages_single_license_filter` in `tests/api/package.rs`:
- Seeds three packages: two with MIT, one with Apache-2.0.
- Requests `GET /api/v2/package?license=MIT`.
- Asserts the response status is 200 OK.
- Asserts exactly 2 items are returned.
- Asserts all returned items have `license == "MIT"`.

This directly verifies the criterion.
