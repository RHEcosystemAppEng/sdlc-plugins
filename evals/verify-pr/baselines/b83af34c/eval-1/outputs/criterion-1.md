# Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

## Verdict: PASS

## Analysis

### Code Changes Supporting This Criterion

**Endpoint layer (`modules/fundamental/src/package/endpoints/list.rs`):**

1. The `PackageListParams` struct now includes `pub license: Option<String>`, which allows the `license` query parameter to be extracted from the request URL by Axum's `Query` extractor. When a client sends `?license=MIT`, the value `"MIT"` is captured in this field.

2. The `validate_license_param` function parses the license string by splitting on commas and validating each identifier against the SPDX expression parser (`spdx::Expression::parse`). For a single value like `"MIT"`, this produces a `Vec<String>` containing `["MIT"]`.

3. In the `list_packages` handler, the optional license parameter is processed:
   ```rust
   let license_filter = match &params.license {
       Some(license) => Some(validate_license_param(license)?),
       None => None,
   };
   ```
   This passes the validated identifiers to the service layer.

**Service layer (`modules/fundamental/src/package/service/mod.rs`):**

4. The `list` method signature now accepts `license_filter: Option<&[String]>`. When `Some(licenses)` is provided, it applies:
   ```rust
   query = query.filter(
       Condition::any()
           .add(package_license::Column::License.is_in(licenses.iter().cloned()))
   );
   query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
   ```
   The `InnerJoin` with the `PackageLicense` relation ensures only packages that have a matching license record are returned. The `is_in` filter with a single value `["MIT"]` effectively creates a `WHERE license IN ('MIT')` clause.

### Test Coverage

The test `test_list_packages_single_license_filter` directly verifies this criterion:
- Seeds three packages: `pkg-a` (MIT), `pkg-b` (Apache-2.0), `pkg-c` (MIT)
- Queries `GET /api/v2/package?license=MIT`
- Asserts response status is 200 OK
- Asserts exactly 2 items are returned
- Asserts all returned items have `license == "MIT"`

This test confirms that the filter excludes non-matching packages (Apache-2.0) and includes all matching packages (both MIT packages).

### Conclusion

The implementation correctly adds the license query parameter, validates it against SPDX, and uses a database-level filter (InnerJoin + is_in) to return only packages with the specified license. The test verifies the behavior end-to-end. Criterion is satisfied.
