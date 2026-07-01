# Acceptance Criterion 1

**Criterion:** `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Reasoning

The diff implements a complete flow for single license filtering:

1. **Query parameter parsing:** In `modules/fundamental/src/package/endpoints/list.rs`, the `PackageListParams` struct gains a new field `pub license: Option<String>` (line 15 of the struct). This means Axum's `Query` extractor will parse a `?license=MIT` query parameter from the request URL.

2. **Validation:** The `validate_license_param` function splits the license string by comma, trims whitespace, and validates each identifier using `spdx::Expression::parse(id)`. For a single value like `MIT`, this validates it as a known SPDX expression and returns `Ok(vec!["MIT".to_string()])`.

3. **Filter application:** In the `list_packages` handler, the validated license filter is passed to `PackageService::list()`. In `modules/fundamental/src/package/service/mod.rs`, the service method applies the filter:
   ```rust
   if let Some(licenses) = license_filter {
       query = query.filter(
           Condition::any()
               .add(package_license::Column::License.is_in(licenses.iter().cloned()))
       );
       query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   }
   ```
   This adds an INNER JOIN to the `package_license` table and a WHERE clause filtering by `license IN ('MIT')`, ensuring only packages with MIT license are returned.

4. **Test coverage:** The test `test_list_packages_single_license_filter` in `tests/api/package.rs` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts:
   - Response status is 200 OK
   - Exactly 2 items returned
   - All returned items have `license == "MIT"`

## Evidence

- `modules/fundamental/src/package/endpoints/list.rs`: `pub license: Option<String>` field added to `PackageListParams`
- `modules/fundamental/src/package/endpoints/list.rs`: `validate_license_param` function validates SPDX identifiers
- `modules/fundamental/src/package/service/mod.rs`: `Condition::any().add(package_license::Column::License.is_in(...))` filter applied with INNER JOIN
- `tests/api/package.rs`: `test_list_packages_single_license_filter` validates the behavior
