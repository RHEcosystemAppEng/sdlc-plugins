# Criterion 1: Versioned PURLs without qualifiers

## Criterion Text
`GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## What was checked
Examined the changes in `modules/fundamental/src/purl/service/mod.rs` to verify that the recommend method strips qualifiers from returned PURLs while preserving version information.

## Evidence

In the service layer (`modules/fundamental/src/purl/service/mod.rs`), the `.map()` closure was changed from:

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

The `without_qualifiers()` method is called on each Purl model before converting to string, which strips qualifier parameters while preserving the versioned PURL format.

The JOIN to PurlQualifier was also removed:
```rust
// Removed: .join(JoinType::LeftJoin, purl::Relation::PurlQualifier.def());
```

The test `test_recommend_purls_basic` confirms the expected output:
```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This shows the PURL retains the version (`@3.12`) but has no qualifiers.

## Verdict
PASS
