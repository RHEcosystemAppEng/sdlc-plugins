# Criterion 4: Existing pagination and sorting behavior is preserved

**Verdict: FAIL**

## Reasoning
- **Pagination.** OFFSET/LIMIT still run on raw purl rows, but deduplication now runs afterwards on the fetched page. When qualifier variants exist:
  - a request with `limit=N` can return fewer than N items even though more exist;
  - offsets no longer match positions in the deduplicated result, so a PURL can appear on more than one page;
  - `total` (raw row count) no longer matches the number of items a client can actually page through. For example, two variants of `@3.12` give `items.len()==1` with `total==2`.

  Clients that compute page counts from `total` will get inconsistent results. For data without qualifier variants, pagination behaves as before.
- **Sorting.** Neither the base query nor the new query has an `ORDER BY`, so this PR does not make sorting worse. However, the new deduplication step only works correctly if the rows arrive in a particular order, and the query does not guarantee one. The unspecified order that was harmless before now affects whether the results are correct.
- `.select_only().column(Id).group_by(Id)` on the count query does nothing useful once the join is removed, and does not make `total` reflect the deduplicated set.

## Test evidence
- `test_simplified_purl_ordering_preserved` is named for ordering but asserts no element order. It checks only `items.len()==2`, the absence of `?`, and `total==3`. It also seeds three distinct versions, so deduplication never happens and the `total` mismatch never shows up.
- The unchanged base test `test_recommend_purls_pagination` (5 distinct versions, `limit=2`, `total==5`) still passes, but it has no qualifier variants either.
- No test combines pagination with qualifier variants.

## Conclusion
Pagination is preserved only in the trivial case with no duplicates. Once deduplication applies, the pagination contract (`items` agreeing with `total` and `offset`/`limit`) breaks. FAIL. The fix is the same as in the criterion 3 sub-task.
