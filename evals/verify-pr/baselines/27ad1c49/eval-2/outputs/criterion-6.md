# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The criterion requires that the existing 404 behavior for non-existent SBOM IDs is preserved after the changes. This is a regression-prevention criterion -- the new threshold filtering logic should not break the existing SBOM lookup.

### Code path analysis

The handler in `get.rs` performs the SBOM lookup before any threshold filtering:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to fetch SBOM")?;
```

This code is **unchanged** in the PR diff. The `?` operator propagates any error from `SbomService::fetch()`, which returns a 404 `AppError` when the SBOM ID does not exist. The threshold filtering logic only runs **after** the SBOM is successfully fetched.

### Verification

The flow is:
1. Parse the SBOM ID from the path parameter
2. Fetch the SBOM -- if not found, return 404 (existing behavior, unchanged)
3. Aggregate advisory severities -- if the SBOM exists, this proceeds
4. Apply optional threshold filtering (new code)
5. Return the response

Since the SBOM lookup is performed first and the error propagation is unchanged, a non-existent SBOM ID will still produce a 404 response before any threshold filtering logic executes. The existing behavior is preserved.

### Caveat

While the code path analysis confirms the 404 behavior is preserved, no integration test was added to verify this (the task's Test Requirements include "Test non-existent SBOM ID returns 404" but no test file was created in this PR). The criterion itself is satisfied at the code level.
