# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR modifies `modules/fundamental/src/purl/service/mod.rs` to strip qualifiers from the PURL response. Specifically, the service layer change introduces:

```rust
let simplified = p.without_qualifiers();
PurlSummary {
    purl: simplified.to_string(),
}
```

This calls `without_qualifiers()` on each PURL model before serializing it to string, which produces a versioned PURL without the `?key=value` qualifier suffix.

The `recommend.rs` endpoint file also removes the `use sea_orm::JoinType;` import, confirming the qualifier join is no longer needed.

The test file `tests/api/purl_recommend.rs` updates `test_recommend_purls_basic` to assert:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns `pkg:maven/org.apache/commons-lang3@3.12` (versioned, no qualifiers) rather than the previous `pkg:maven/org.apache/commons-lang3@3.12?repository_url=https://repo1.maven.org&type=jar`.

The code changes directly implement this criterion. The endpoint serialization path now strips qualifiers before building the response.
