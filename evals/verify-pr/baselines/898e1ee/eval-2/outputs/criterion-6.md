# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The existing 404 behavior for non-existent SBOM IDs is preserved in the PR. The handler code shows:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This is followed by an error handling pattern (visible in the context lines of the diff) that returns a 404 response when the SBOM is not found. The `.ok_or(AppError::NotFound(...))` or equivalent pattern is part of the existing code and has not been modified by this PR.

The PR adds threshold filtering logic *after* the SBOM fetch succeeds. The new code only executes when a valid SBOM has been retrieved. If the SBOM does not exist, the handler returns 404 before reaching the threshold filtering code.

The flow is:
1. Fetch SBOM by ID -- if not found, return 404 (existing behavior, unchanged)
2. Aggregate severities (existing behavior, unchanged)
3. Apply threshold filter (new behavior, only reached if SBOM exists)
4. Return filtered response

Since the 404 path is upstream of all new code, the existing behavior is preserved.

### Note on test coverage

While the existing 404 behavior is preserved in the implementation, the task's Test Requirements specify "Test non-existent SBOM ID returns 404," and no test file (`tests/api/advisory_summary.rs`) was created in this PR. The absence of tests does not affect this criterion (which is about implementation behavior), but it is relevant to the overall verification (see Scope Containment).

### Evidence

- File: `modules/fundamental/src/advisory/endpoints/get.rs`
- The SBOM fetch and 404 error handling code is unchanged in the diff
- New threshold filtering code appears after the SBOM fetch, so 404 behavior is preserved
