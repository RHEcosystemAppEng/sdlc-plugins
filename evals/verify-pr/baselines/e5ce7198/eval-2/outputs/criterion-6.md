## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Result: PASS**

### Evidence

The diff retains the existing SBOM fetch logic that handles non-existent IDs:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code is present in the original file and is not modified by the diff. The `SbomService::fetch()` method returns a `Result` -- if the SBOM does not exist, the error propagates through the `?` operator and ultimately produces a 404 response via `AppError`'s `IntoResponse` implementation (as documented in `common/src/error.rs`).

Since this behavior is inherited from the existing code and the diff does not alter the SBOM lookup path, the 404 behavior for non-existent SBOM IDs is preserved.

### Conclusion

This criterion passes. The existing 404 behavior for non-existent SBOM IDs is not disturbed by the changes in this diff.
