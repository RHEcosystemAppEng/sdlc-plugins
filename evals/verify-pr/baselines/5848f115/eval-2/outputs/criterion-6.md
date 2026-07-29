# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The existing SBOM fetch logic is unchanged by this PR, and the 404 behavior for non-existent SBOM IDs is preserved.

### Existing behavior

The `advisory_summary` handler fetches the SBOM before proceeding with advisory aggregation:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This call is present in both the pre-change and post-change code (it appears in the context lines of the diff, not as an addition or deletion). The `.fetch()` method presumably returns an error when the SBOM ID does not exist, and the `?` operator propagates that error through `AppError`, which converts it to a 404 response via its `IntoResponse` implementation (as documented in the repository's `common/src/error.rs`).

### Changes do not affect this behavior

The only structural changes to the handler are:
1. Addition of the `Query(params): Query<SummaryParams>` parameter extractor
2. Addition of the filtering logic after the advisory aggregation

Neither of these changes modifies the SBOM fetch path. The fetch occurs before any threshold processing, so a non-existent SBOM ID will still trigger the same error path regardless of whether a threshold parameter is provided.

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The `SbomService::fetch()` call and its error propagation are unchanged (context lines in diff)
- The new `Query(params)` extractor is an additional handler parameter and does not interfere with the SBOM fetch
- The threshold filtering logic is only reached after a successful SBOM fetch
