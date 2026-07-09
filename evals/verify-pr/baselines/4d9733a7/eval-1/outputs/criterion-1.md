# Criterion 1: GET /api/v2/package?license=MIT returns only packages with MIT license

## Verdict: PASS

## Reasoning

This criterion requires that when a single license value is provided as a query parameter, only packages matching that license are returned.

### Code Analysis

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

1. The `PackageListParams` struct now includes `pub license: Option<String>` (diff line 15), which means Axum will parse a `?license=MIT` query parameter into this field.

2. In the `list_packages` handler, the license parameter is processed:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   When `license=MIT` is provided, `validate_license_param("MIT")` is called.

3. The `validate_license_param` function splits on comma, trims whitespace, and validates each identifier against `spdx::Expression::parse`. For a single value "MIT", this produces `vec!["MIT"]` after successful SPDX validation.

4. The validated identifiers are passed to the service layer:
   ```rust
   .list(params.offset, params.limit, license_filter.as_deref())
   ```

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

5. The `list` method signature now accepts `license_filter: Option<&[String]>`.

6. When `license_filter` is `Some(licenses)`, the query is filtered:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   This joins the `package_license` table and filters where the license column matches any value in the provided list. For a single value `["MIT"]`, this effectively filters to only MIT-licensed packages.

**Test coverage (`tests/api/package.rs`):**

7. The test `test_list_packages_single_license_filter` directly validates this criterion:
   - Seeds packages: "pkg-a" (MIT), "pkg-b" (Apache-2.0), "pkg-c" (MIT)
   - Requests `GET /api/v2/package?license=MIT`
   - Asserts response status is 200 OK
   - Asserts `body.items.len() == 2` (only the 2 MIT packages)
   - Asserts `body.items.iter().all(|p| p.license == "MIT")` (all returned packages have MIT license)

### Conclusion

The implementation correctly adds license filtering at both the endpoint and service layers. The SPDX validation ensures only valid license identifiers are accepted. The `is_in` query filter with an inner join on the package_license table ensures only packages with matching licenses are returned. The integration test confirms the end-to-end behavior.
