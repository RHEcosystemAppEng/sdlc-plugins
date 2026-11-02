# Criterion 3: Deduplication of entries

**Criterion:** Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

**Verdict: PASS**

## Evidence

1. **Service layer (`modules/fundamental/src/purl/service/mod.rs`):** After stripping qualifiers and serializing PURLs, the code applies deduplication:
   ```rust
   .dedup_by(|a, b| a.purl == b.purl)
   ```
   This removes consecutive entries with identical PURL strings. Since qualifiers were the only distinguishing factor for same-version packages, stripping qualifiers makes them identical, and `dedup_by` collapses them.

2. **Query change (`modules/fundamental/src/purl/service/mod.rs`):** The count query was updated to use `group_by(purl::Column::Id)` to get accurate totals after deduplication:
   ```rust
   let total = query.clone()
       .select_only()
       .column(purl::Column::Id)
       .group_by(purl::Column::Id)
       .count(&self.db).await?;
   ```

3. **Test verification (`tests/api/purl_recommend.rs`):** The new `test_recommend_purls_dedup` function seeds two PURLs with identical namespace/name/version but different qualifiers (repo1 vs repo2), then asserts only 1 entry is returned:
   ```rust
   assert_eq!(body.items.len(), 1);
   assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
   ```
   This directly tests the deduplication behavior.
