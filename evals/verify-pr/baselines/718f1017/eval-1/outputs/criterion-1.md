## Acceptance Criterion 1

**Criterion**: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict**: PASS

### Evidence

**Endpoint parameter parsing** (`modules/fundamental/src/package/endpoints/list.rs`):
The `PackageListParams` struct now includes `pub license: Option<String>`, which Axum's `Query` extractor automatically populates from the `?license=MIT` query parameter.

**Validation** (`modules/fundamental/src/package/endpoints/list.rs`):
The `validate_license_param` function parses the license string. For a single value like `"MIT"`, `split(',')` produces a single-element vector `["MIT"]`. `Expression::parse("MIT")` succeeds since MIT is a valid SPDX identifier, so the function returns `Ok(vec!["MIT".to_string()])`.

**Service-layer filtering** (`modules/fundamental/src/package/service/mod.rs`):
The `list` method receives `license_filter: Option<&[String]>` with value `Some(&["MIT"])`. The conditional block applies:
```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```
This joins the `package_license` table and filters where `license IN ('MIT')`, ensuring only MIT-licensed packages are returned.

**Test coverage** (`tests/api/package.rs`):
`test_list_packages_single_license_filter` seeds packages with MIT and Apache-2.0 licenses, queries `?license=MIT`, and asserts:
- Response status is 200 OK
- `body.items.len()` equals 2 (the two MIT packages)
- All returned items have `license == "MIT"`
