# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The existing fetch-and-check pattern is preserved in the diff. The handler still calls:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("...")?;
```

This line (visible in the diff context at the original line range) fetches the SBOM by ID and propagates any error via the `?` operator. If the SBOM does not exist, the service returns an error that maps to a 404 response through the `AppError` mechanism (as documented in `common/src/error.rs`).

The new threshold filtering code executes only after the SBOM has been successfully fetched, so the 404 behavior for non-existent SBOM IDs remains intact. No changes were made that would alter the error handling path.

Note: While the behavior is preserved, no integration test was added to verify this (the required `tests/api/advisory_summary.rs` file is absent from the diff).
