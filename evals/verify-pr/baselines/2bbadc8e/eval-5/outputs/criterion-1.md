# Criterion 1: Versioned PURLs without qualifiers

**Criterion:** `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

**Verdict:** PASS

**Reasoning:**

The diff in `modules/fundamental/src/purl/service/mod.rs` shows the service layer now calls `p.without_qualifiers()` before serializing the PURL:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

Additionally, the qualifier join was removed from the query:
- Removed: `.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def())`
- The `use sea_orm::JoinType;` import was also removed

The test `test_recommend_purls_basic` in `tests/api/purl_recommend.rs` confirms the assertion now checks for a versioned PURL without qualifiers:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The endpoint handler in `recommend.rs` still returns `Json<PaginatedResults<PurlSummary>>`, meaning the response shape preserves versioned PURLs. The code change achieves the criterion.
