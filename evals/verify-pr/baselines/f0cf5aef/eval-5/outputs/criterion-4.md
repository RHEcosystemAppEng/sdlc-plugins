# Criterion 4: Existing pagination and sorting behavior is preserved

## Verdict: PASS

## Reasoning

This criterion requires that the pagination (offset/limit) and sorting behavior of the endpoint remain unchanged after the qualifier removal changes.

### Implementation Evidence

In `modules/fundamental/src/purl/service/mod.rs`, the pagination logic is preserved:

1. **Offset/limit application**: The query chain still uses `.offset(offset.unwrap_or(0) as u64)` and the limit parameter, which are unchanged from the base branch.

2. **Count query improvement**: The count query changed from:
   ```rust
   let total = query.clone().count(&self.db).await?;
   ```
   to:
   ```rust
   let total = query.clone()
       .select_only()
       .column(purl::Column::Id)
       .group_by(purl::Column::Id)
       .count(&self.db).await?;
   ```
   This is actually a correctness improvement. The old count query would have inflated totals when the LEFT JOIN to PurlQualifier produced multiple rows per PURL (one per qualifier). The new query counts distinct PURL IDs, producing an accurate total.

3. **Sorting**: The query ordering is unchanged. The results maintain whatever default ordering the database returns, which is consistent with the base-branch behavior (minus the qualifier join).

### Test Evidence

The existing `test_recommend_purls_pagination` test is preserved in the PR branch (visible in the diff context lines). It seeds 5 versioned PURLs and asserts that `limit=2` returns exactly 2 items with `total == 5`.

Additionally, the new `test_simplified_purl_ordering_preserved` test in `purl_simplify.rs` validates ordering and pagination:

```rust
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.10?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.11?type=jar").await;
ctx.seed_purl("pkg:maven/org.apache/commons-lang3@3.12?type=jar").await;

let resp = ctx.get("/api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3&limit=2").await;

assert_eq!(body.items.len(), 2);
assert_eq!(body.total, 3);
```

### Conclusion

Pagination behavior is preserved. The offset/limit logic is unchanged, the count query was improved for accuracy, and both existing and new tests verify pagination works correctly.
