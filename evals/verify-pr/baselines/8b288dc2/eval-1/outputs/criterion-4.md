## Criterion 4: Filter integrates with existing pagination -- filtered results are paginated correctly

### Evidence

**Service layer (`service/mod.rs`):**
- The license filter is applied to the `query` variable *before* the pagination logic:
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
- The `total` count is computed from the filtered query (after the WHERE clause is applied), so `total` reflects the number of matching packages, not all packages.
- The subsequent `items` query applies offset/limit to the same filtered query, producing a correct page of filtered results.

**Test (`tests/api/package.rs`):**
- `test_list_packages_license_filter_with_pagination` seeds 5 MIT packages (`pkg-0` through `pkg-4`) and 1 Apache-2.0 package (`pkg-other`).
- Queries `GET /api/v2/package?license=MIT&limit=2&offset=0`.
- Asserts `body.items.len() == 2` (page size is 2).
- Asserts `body.total == 5` (total MIT packages is 5, not 6 which would include the Apache-2.0 package).
- This confirms the filter is applied before both the count and the paginated item fetch.

### Verdict: PASS

The filter is correctly composed into the query before pagination. The `total` field reflects the filtered count (5 MIT packages, not 6 total), and the `items` field respects the `limit` parameter (2 items returned). This confirms proper integration with existing pagination.
