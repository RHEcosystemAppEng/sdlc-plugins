## Criterion 1

**Text:** `GET /api/v2/package?license=MIT` returns only packages with MIT license

**What was checked:**

1. The `PackageListParams` struct in `list.rs` now includes a `license: Option<String>` field, which Axum's `Query` extractor will populate from the `?license=MIT` query parameter.
2. The `validate_license_param` function parses the license string, splitting on commas. For a single value like `MIT`, it produces a `Vec` containing one element.
3. The `list_packages` handler passes the validated license identifiers to `PackageService::list()`.
4. In `service/mod.rs`, the `list` method applies an `is_in` filter on `package_license::Column::License` via an inner join to the `PackageLicense` table. This ensures only rows whose license column matches one of the provided identifiers are returned.
5. The integration test `test_list_packages_single_license_filter` seeds three packages (two MIT, one Apache-2.0), queries `?license=MIT`, and asserts exactly 2 results are returned with all items having `license == "MIT"`.

**Code evidence:**

From `list.rs`:
```rust
pub license: Option<String>,
```

From `service/mod.rs`:
```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}
```

From `tests/api/package.rs`:
```rust
let resp = ctx.get("/api/v2/package?license=MIT").await;
assert_eq!(resp.status(), StatusCode::OK);
let body: PaginatedResults<PackageSummary> = resp.json().await;
assert_eq!(body.items.len(), 2);
assert!(body.items.iter().all(|p| p.license == "MIT"));
```

**Verdict:** PASS
