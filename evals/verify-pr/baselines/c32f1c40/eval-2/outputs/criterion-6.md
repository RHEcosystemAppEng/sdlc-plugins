# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing 404 behavior is preserved in the diff. The SBOM fetch-and-validate pattern remains unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to fetch SBOM")?
    .ok_or(AppError::NotFound)?;
```

This code:
1. Calls `SbomService::fetch()` which returns `Option<Sbom>`
2. Maps `None` (non-existent SBOM) to `AppError::NotFound` via `.ok_or()`
3. The `?` operator propagates the error, returning a 404 response

The new threshold filtering code is placed after the SBOM fetch, so non-existent SBOM IDs are rejected before any threshold logic executes.

## Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`, lines 31-34 in the diff (context lines, unchanged)
- The `.ok_or(AppError::NotFound)?` pattern is preserved
- The threshold filtering logic begins at line 41, after the SBOM existence check
