# Criterion 4: Filter integrates with existing pagination — filtered results are paginated correctly

**Verdict: PASS**

## Code evidence
- `service/mod.rs`: the license filter and join are applied to `query` before:
  - `let total = query.clone().count(&self.db).await?`, so `total` counts the filtered set;
  - the existing items query, which applies `offset` and `limit` to that filtered set.
- `list.rs`: `params.offset` and `params.limit` are still passed to `list` alongside the new filter.

## Test evidence
`test_list_packages_license_filter_with_pagination`:
- seeds 5 MIT packages and 1 Apache-2.0 package;
- requests `?license=MIT&limit=2&offset=0`;
- asserts 200 OK, `items.len() == 2`, and `total == 5`. This confirms that both the page size and the total reflect the filtered set.

CI passes.

## Caveats (non-blocking)
- Only the first page (`offset=0`) is tested.
- The duplicate-row note from Criterion 2 would also affect `total` if a package has several matching license rows.
