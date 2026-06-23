# Criterion 3: Duplicate entries that were previously distinct due to different qualifiers are deduplicated in the response

## Verdict: PASS

## Reasoning

The PR adds deduplication logic in `modules/fundamental/src/purl/service/mod.rs`:

```rust
.dedup_by(|a, b| a.purl == b.purl)
```

This is applied after the qualifier stripping step (`.map(|p| { let simplified = p.without_qualifiers(); ... })`), so PURLs that were previously distinct due to different qualifier values but share the same type/namespace/name/version will be collapsed to a single entry.

Additionally, the query is updated to use `group_by` for the count:
```rust
let total = query.clone()
    .select_only()
    .column(purl::Column::Id)
    .group_by(purl::Column::Id)
    .count(&self.db).await?;
```

The dedicated test `test_recommend_purls_dedup` in `tests/api/purl_recommend.rs` directly validates this:
- Seeds two PURLs with the same version but different qualifiers (`repo1.maven.org` vs `repo2.maven.org`)
- Asserts only 1 item is returned (deduplicated after qualifier removal)
- Asserts the returned PURL is the versioned form without qualifiers

This confirms that duplicates arising from qualifier removal are properly deduplicated. The criterion is satisfied.
