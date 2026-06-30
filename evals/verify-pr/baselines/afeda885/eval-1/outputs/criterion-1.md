## Criterion 1: `GET /api/v2/package?license=MIT` returns only packages with MIT license

**Verdict: PASS**

### Reasoning

The PR diff adds a `license` query parameter to the `PackageListParams` struct in `modules/fundamental/src/package/endpoints/list.rs`:

```rust
pub license: Option<String>,
```

When this parameter is present, the `validate_license_param` function parses and validates it, then passes the resulting identifiers to `PackageService::list()`. In `modules/fundamental/src/package/service/mod.rs`, the service applies a filter using SeaORM's `Condition::any()` with `is_in()`:

```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

When a single license value like `MIT` is provided, the `validate_license_param` function splits on commas (producing a single-element vector `["MIT"]`), validates it as a valid SPDX expression, and the service filters packages whose `package_license.license` column matches `MIT` via an inner join. This ensures only packages with the MIT license are returned.

The integration test `test_list_packages_single_license_filter` in `tests/api/package.rs` directly verifies this behavior by seeding packages with MIT and Apache-2.0 licenses, filtering by MIT, and asserting that only 2 MIT-licensed packages are returned with `assert!(body.items.iter().all(|p| p.license == "MIT"))`.

This criterion is satisfied by both the implementation and test coverage.
