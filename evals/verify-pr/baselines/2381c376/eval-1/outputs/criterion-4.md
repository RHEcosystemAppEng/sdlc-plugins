## Criterion 4: Filter integrates with existing pagination -- filtered results are paginated correctly

### Verdict: PASS

### Analysis

**Code evidence in the diff:**

1. **Filter applied before count and pagination** (`service/mod.rs`): The license filter is applied to the query *before* the total count and before pagination (offset/limit) are applied:
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
   This means:
   - `total` reflects the count of *filtered* results (not all packages).
   - The paginated `items` are drawn from the *filtered* set.
   - Existing offset/limit parameters continue to work on the filtered query.

2. **Parameter coexistence** (`list.rs`): The `PackageListParams` struct includes `offset`, `limit`, and `license` as independent optional fields, allowing them to be combined in a single request.

**Test evidence:**

The test `test_list_packages_license_filter_with_pagination` in `tests/api/package.rs`:
- Seeds 5 MIT-licensed packages and 1 Apache-2.0 package (6 total).
- Requests `GET /api/v2/package?license=MIT&limit=2&offset=0`.
- Asserts the response status is 200 OK.
- Asserts `body.items.len() == 2` (limit is respected).
- Asserts `body.total == 5` (total reflects filtered count of MIT packages, not all 6).

This directly verifies that filtering and pagination work together correctly.
