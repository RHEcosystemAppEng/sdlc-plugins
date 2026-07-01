# Criterion 4: Filter integrates with existing pagination -- filtered results are paginated correctly

## Verdict: PASS

## Reasoning

The PR integrates the license filter with the existing pagination mechanism by applying the filter before the pagination logic in the service layer. The `total` count reflects the filtered set, and `offset`/`limit` are applied to the filtered query.

### Service Layer (mod.rs)

The license filter is applied to the query before the total count and pagination:

```rust
pub async fn list(
    &self,
    offset: Option<i64>,
    limit: Option<i64>,
    license_filter: Option<&[String]>,
) -> Result<PaginatedResults<PackageSummary>> {
    let mut query = Package::find();

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

The critical ordering is:
1. Filter is applied to `query` (WHERE + JOIN)
2. `total` is computed from the filtered query (`query.clone().count()`)
3. `items` are fetched from the filtered query with offset/limit applied

This means `total` reflects the count of filtered results (not all packages), and the `offset`/`limit` pagination operates on the filtered result set. This is the correct behavior -- the `PaginatedResults` wrapper will report the correct `total` for navigation purposes, and each page contains only license-matching packages.

### Test Coverage

The test `test_list_packages_license_filter_with_pagination` directly validates this integration:

```rust
// Given 5 MIT-licensed packages
for i in 0..5 {
    ctx.seed_package(&format!("pkg-{}", i), "MIT").await;
}
ctx.seed_package("pkg-other", "Apache-2.0").await;

// When filtering by MIT with limit=2 and offset=0
let resp = ctx.get("/api/v2/package?license=MIT&limit=2&offset=0").await;

// Then only 2 items are returned but total reflects all MIT packages
assert_eq!(resp.status(), StatusCode::OK);
let body: PaginatedResults<PackageSummary> = resp.json().await;
assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 5);
```

This test:
- Seeds 5 MIT packages and 1 Apache-2.0 package (6 total)
- Filters by MIT with `limit=2` and `offset=0`
- Asserts `items.len() == 2` (pagination limits items per page)
- Asserts `total == 5` (total reflects filtered count, not 6)

This confirms that the filter is applied before both the count and the pagination slice.

### Pattern Consistency

The implementation follows the existing pattern in the repository. The `common/src/db/query.rs` helpers provide shared filtering and pagination logic, and the service method signature accepts `offset` and `limit` parameters consistent with other list endpoints (e.g., advisory, SBOM).

## Evidence

- `modules/fundamental/src/package/service/mod.rs`: filter applied before `count()` and before `offset`/`limit` slicing
- `tests/api/package.rs`: `test_list_packages_license_filter_with_pagination` asserts `items.len() == 2` and `total == 5` with 5 MIT + 1 Apache-2.0 packages
- Repository convention: `PaginatedResults` from `common/src/model/paginated.rs` wraps the response consistently
