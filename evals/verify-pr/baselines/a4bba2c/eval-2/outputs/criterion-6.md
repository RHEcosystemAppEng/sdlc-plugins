# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Criterion Text
Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Analysis

The existing 404 behavior for non-existent SBOM IDs is preserved. The diff shows that the SBOM lookup code at the beginning of the handler is unchanged:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    .await
    .context("Failed to aggregate advisory severities")?;
```

This code fetches the SBOM by ID before any threshold filtering occurs. If the SBOM does not exist, the `fetch` method would return an error (likely a 404 via the `AppError` error handling), and the `?` operator would propagate this error before reaching the threshold filtering logic.

The threshold filtering is added after the SBOM fetch and advisory aggregation, so it does not interfere with the existing 404 behavior. The control flow is:
1. Fetch SBOM (returns 404 if not found) -- unchanged
2. Aggregate severities -- unchanged
3. Apply threshold filter -- new code, only reached if steps 1-2 succeed

## Evidence

- The SBOM fetch code (`SbomService::new(&db).fetch(sbom_id.id)`) is unchanged in the diff
- The `?` operator propagates errors from the fetch before threshold filtering is reached
- No modifications were made to the error handling path for missing SBOMs
- The new threshold filtering code is appended after the existing fetch/aggregate logic

Note: While the existing 404 behavior appears preserved in the handler code, no integration test for 404 with non-existent SBOM IDs was added (the test file `tests/api/advisory_summary.rs` is entirely missing from the diff). The criterion specifically asks about preserving existing behavior, which the code does, but the Test Requirements include testing this scenario and that test is absent.
