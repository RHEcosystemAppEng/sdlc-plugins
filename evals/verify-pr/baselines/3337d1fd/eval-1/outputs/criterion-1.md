## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

### Verdict: PASS

### Reasoning

This criterion requires that when a single license value is provided as a query parameter, only packages matching that license are returned.

**Endpoint parameter parsing (`list.rs`):**
The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor will deserialize from the query string. When a request includes `?license=MIT`, the `license` field will be `Some("MIT")`.

**Validation (`list.rs`):**
The `validate_license_param` function splits the license string by comma, trims whitespace, and validates each identifier using `spdx::Expression::parse(id)`. For a single value like `"MIT"`, this produces a `Vec<String>` containing one element: `["MIT"]`. The validation ensures `MIT` is a valid SPDX expression before proceeding.

**Filtering (`mod.rs`):**
In `PackageService::list`, the new `license_filter: Option<&[String]>` parameter is used to build a filter:
```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```
This applies an `IS IN` condition on the `package_license.license` column and joins the `PackageLicense` table via inner join. For `["MIT"]`, this filters to only rows where the license column equals `"MIT"`.

**Handler wiring (`list.rs`):**
The `list_packages` handler maps the optional license parameter through `validate_license_param` and passes the result to `PackageService::list`:
```rust
let license_filter = match &params.license {
    Some(license) => Some(validate_license_param(license)?),
    None => None,
};
```
The `?` operator propagates any validation error as an early return.

**Test coverage (`tests/api/package.rs`):**
The test `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), sends `GET /api/v2/package?license=MIT`, and asserts:
- Response status is 200 OK
- Response body contains exactly 2 items
- All items have `license == "MIT"`

This directly validates the criterion's requirement.

### Evidence

- `list.rs`: `PackageListParams.license` field added (line 15 in diff)
- `list.rs`: `validate_license_param` function parses and validates the parameter
- `mod.rs`: `license_filter` parameter added to `PackageService::list`, filter applied via `Condition::any().add(package_license::Column::License.is_in(...))`
- `tests/api/package.rs`: `test_list_packages_single_license_filter` covers this scenario end-to-end
