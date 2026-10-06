## Criterion 4

**Text:** Filter integrates with existing pagination -- filtered results are paginated correctly

**What was checked:**

1. In `service/mod.rs`, the license filter is applied to the query before the total count and item retrieval. The existing `total = query.clone().count(...)` and `items = query.offset().limit()...` logic operates on the already-filtered query, so pagination is applied to the filtered result set.
2. The `PackageListParams` struct retains `offset: Option<i64>` and `limit: Option<i64>` alongside the new `license` field, and all three are passed to the service layer.
3. The integration test `test_list_packages_license_filter_with_pagination` seeds 5 MIT packages and 1 Apache-2.0 package, queries `?license=MIT&limit=2&offset=0`, and asserts `body.items.len() == 2` (page size) and `body.total == 5` (total filtered count, not 6).

**Code evidence:**

From `service/mod.rs` (filter applied before pagination):
```rust
if let Some(licenses) = license_filter {
    query = query.filter(
        Condition::any()
            .add(package_license::Column::License.is_in(licenses.iter().cloned()))
    );
    query = query.join(JoinType::InnerJoin, package::Relation::PackageLicense.def());
}

let total = query.clone().count(&self.db).await?;

let items = query
```

From `tests/api/package.rs`:
```rust
let resp = ctx.get("/api/v2/package?license=MIT&limit=2&offset=0").await;
assert_eq!(resp.status(), StatusCode::OK);
let body: PaginatedResults<PackageSummary> = resp.json().await;
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 5);
```

**Verdict:** PASS
