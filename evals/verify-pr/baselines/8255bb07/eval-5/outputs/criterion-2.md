# Criterion 2: Response PURLs do not contain `?` query parameters

## Acceptance Criterion

> Response PURLs do not contain `?` query parameters (no qualifiers present)

## Verdict: PASS

## Reasoning

The PR ensures that no qualifier parameters appear in response PURLs through two mechanisms:

### Implementation

In `modules/fundamental/src/purl/service/mod.rs`, the mapping logic applies `p.without_qualifiers()` before converting to string:

```rust
.map(|p| {
    let simplified = p.without_qualifiers();
    PurlSummary {
        purl: simplified.to_string(),
    }
})
```

The `without_qualifiers()` method (referenced in the task's Implementation Notes as existing in `common/src/purl.rs`) produces a PURL string that excludes the `?key=value` qualifier suffix.

### Test evidence

Multiple tests explicitly assert the absence of `?` in response PURLs:

1. In `test_recommend_purls_basic`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

2. In `test_simplified_purl_no_version`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   ```

3. In `test_simplified_purl_mixed_types`:
   ```rust
   assert!(!body.items[0].purl.contains("vcs_url"));
   ```
   (This checks for a specific qualifier key rather than `?`, but combined with the equality assertion `assert_eq!(body.items[0].purl, "pkg:npm/%40angular/core@16.0.0")` it confirms no qualifiers.)

4. In `test_simplified_purl_ordering_preserved`:
   ```rust
   assert!(!body.items[0].purl.contains('?'));
   assert!(!body.items[1].purl.contains('?'));
   ```

The test seeds use PURLs with qualifiers (e.g., `?repository_url=...&type=jar`), but the assertions confirm the response PURLs have no `?` query parameters. This demonstrates the qualifier stripping works correctly.

This criterion is satisfied.
