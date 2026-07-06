# Criterion 1: GET /api/v2/purl/recommend returns versioned PURLs without qualifiers

## Acceptance Criterion

> `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies both the endpoint layer and the service layer to strip qualifiers from PURL recommendation responses.

### Endpoint layer (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The endpoint signature and return type are unchanged -- it still returns `Result<Json<PaginatedResults<PurlSummary>>, AppError>`. The only change is removing the unused `use sea_orm::JoinType;` import, which is consistent with the qualifier join being removed from the service layer.

### Service layer (`modules/fundamental/src/purl/service/mod.rs`)

The `recommend` method has been updated:

1. The qualifier join (`JoinType::LeftJoin, purl::Relation::PurlQualifier.def()`) has been removed from the query, so qualifier data is no longer fetched from the database.
2. The mapping logic now calls `p.without_qualifiers()` before serializing, producing versioned PURLs without qualifier parameters.
3. A `.dedup_by(|a, b| a.purl == b.purl)` call handles deduplication after qualifier removal.

### Test evidence

The updated `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` asserts:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the response contains a versioned PURL (`@3.12` version suffix present) without qualifiers (no `?` and no `repository_url=` or `type=` parameters).

The new `test_recommend_purls_dedup` test further confirms:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

The new file `tests/api/purl_simplify.rs` contains additional tests verifying the same behavior across different PURL types (npm, pypi, maven).

This criterion is satisfied by the code changes.
