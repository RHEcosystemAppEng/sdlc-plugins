# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Criterion Text

`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

### Code Changes

In `modules/fundamental/src/purl/service/mod.rs`, the response mapping was changed from:

```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

to:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method is called on each PURL entity before serializing to string. According to the implementation notes in the task, the `PackageUrl` builder in `common/src/purl.rs` supports constructing PURLs with or without qualifiers, and `without_qualifiers()` is the documented API for this. This ensures the returned PURL string contains only the type, namespace, name, and version -- no query parameters.

### Supporting Query Change

The qualifier join was also removed from the query:

```rust
// Before
.join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
// After (join removed entirely)
```

And the corresponding `use sea_orm::JoinType;` import was removed from `recommend.rs`. This is consistent -- since qualifiers are no longer included in the response, there is no need to join the qualifier table.

### Test Coverage

The updated `test_recommend_purls_basic` test directly validates this criterion:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This asserts the response contains a versioned PURL (`@3.12`) without any qualifier string (no `?repository_url=...`).

Additionally, the new `test_simplified_purl_ordering_preserved` in `purl_simplify.rs` seeds PURLs with qualifiers (`?type=jar`) and verifies the response lacks qualifiers:

```rust
assert!(!body.items[0].purl.contains('?'));
assert!(!body.items[1].purl.contains('?'));
```

### CI Confirmation

All CI checks pass, confirming the tests validate this behavior end-to-end against the test database.

## Conclusion

The code change correctly calls `without_qualifiers()` before serialization, the qualifier join is removed from the query, and tests explicitly assert the response format. This criterion is satisfied.
