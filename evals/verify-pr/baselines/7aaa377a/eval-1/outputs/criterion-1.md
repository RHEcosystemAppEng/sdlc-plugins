## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

### Analysis

This criterion requires that the license query parameter filters packages to return only those matching the specified SPDX license identifier.

### Evidence from the PR diff

**1. Query parameter extraction (list.rs)**

The `PackageListParams` struct now includes the `license` field:

```rust
pub struct PackageListParams {
    pub offset: Option<i64>,
    pub limit: Option<i64>,
    pub license: Option<String>,
}
```

Axum's `Query<PackageListParams>` extractor automatically deserializes `?license=MIT` into `params.license = Some("MIT")`.

**2. Validation (list.rs)**

The `validate_license_param` function parses the license string using `spdx::Expression::parse`, ensuring only valid SPDX identifiers are accepted. For a single value like `"MIT"`, it splits on comma (producing `["MIT"]`), validates the expression, and returns `Ok(vec!["MIT".to_string()])`.

**3. Service-layer filtering (service/mod.rs)**

The `PackageService::list` method receives the validated license identifiers as `Option<&[String]>`. When present, it applies a filter:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

This inner-joins the `package_license` table and filters with `IS IN ('MIT')`, which returns only packages whose license column matches "MIT". The `InnerJoin` ensures that packages without a license entry in the join table are excluded.

**4. Integration test coverage (tests/api/package.rs)**

The test `test_list_packages_single_license_filter` seeds three packages (pkg-a with MIT, pkg-b with Apache-2.0, pkg-c with MIT), then requests `?license=MIT` and asserts:
- Status is 200 OK
- Exactly 2 items are returned
- All returned items have `license == "MIT"`

This directly validates the criterion's expected behavior.

### Conclusion

The endpoint correctly parses the `license` query parameter, validates it as a valid SPDX expression, and filters the database query to return only matching packages. The test confirms the filtering works end-to-end.
