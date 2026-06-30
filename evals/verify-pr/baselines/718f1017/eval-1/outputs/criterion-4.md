## Acceptance Criterion 4

**Criterion**: Filter integrates with existing pagination -- filtered results are paginated correctly

**Verdict**: PASS

### Evidence

**Filter-before-paginate ordering** (`modules/fundamental/src/package/service/mod.rs`):
The license filter is applied to the query before the pagination logic:
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
    // ... existing offset/limit logic follows
```

The `total` count is computed from the filtered query (`query.clone().count()`), meaning it reflects the count of filtered results, not the total unfiltered count. The `offset` and `limit` are then applied to the same filtered query, ensuring correct pagination over the filtered result set.

**Endpoint wiring** (`modules/fundamental/src/package/endpoints/list.rs`):
The handler passes both pagination and filter parameters to the service:
```rust
.list(params.offset, params.limit, license_filter.as_deref())
```
The existing `PaginatedResults` wrapper is used without modification, so the response includes both `items` (the current page of filtered results) and `total` (the total count of filtered results).

**Test coverage** (`tests/api/package.rs`):
`test_list_packages_license_filter_with_pagination` seeds 5 MIT packages and 1 Apache-2.0 package, then queries `?license=MIT&limit=2&offset=0` and asserts:
- `body.items.len()` equals 2 (respects the `limit=2` parameter)
- `body.total` equals 5 (total MIT packages, not total of all packages including Apache-2.0)

This confirms that pagination operates on the filtered result set, not the unfiltered one.
