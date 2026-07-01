# Criterion 1: `GET /api/v2/purl/recommend?purl=pkg:maven/org.apache/commons-lang3` returns versioned PURLs without qualifiers

## Verdict: PASS

## Reasoning

The PR diff shows two changes that together satisfy this criterion:

### 1. Service layer change (`modules/fundamental/src/purl/service/mod.rs`)

The recommendation query was modified to strip qualifiers from returned PURLs. The key change is in the `.map()` closure that transforms query results into `PurlSummary` objects:

**Before (base branch):**
```rust
.map(|p| PurlSummary {
    purl: p.to_string(),
})
```

**After (PR branch):**
```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method (referenced in the task's Implementation Notes as part of the `PackageUrl` builder in `common/src/purl.rs`) is called on each PURL before serialization. This ensures the response contains versioned PURLs without qualifiers.

### 2. Endpoint layer change (`modules/fundamental/src/purl/endpoints/recommend.rs`)

The `JoinType` import was removed since the qualifier join is no longer needed. The endpoint still returns `Json<PaginatedResults<PurlSummary>>`, which is the expected response type.

### 3. Test verification

The `test_recommend_purls_basic` test in `tests/api/purl_recommend.rs` was updated to assert the new behavior:

```rust
assert_eq!(body.items[0].purl, "pkg:maven/org.apache/commons-lang3@3.12");
```

This confirms the endpoint returns versioned PURLs (with `@3.12` version) without qualifiers (no `?repository_url=...&type=jar` suffix).

### Evidence

- `modules/fundamental/src/purl/service/mod.rs`: `p.without_qualifiers()` call strips qualifiers before response serialization
- `tests/api/purl_recommend.rs`: assertion checks for `pkg:maven/org.apache/commons-lang3@3.12` (versioned, no qualifiers)
- The endpoint handler in `recommend.rs` still calls `PurlService::recommend()` which now returns simplified PURLs
