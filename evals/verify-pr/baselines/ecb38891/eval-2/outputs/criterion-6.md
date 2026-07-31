# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The existing 404 behavior for non-existent SBOM IDs is preserved unchanged in the PR diff.

### Code Under Review

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This code block is part of the unchanged context lines in the diff (no `+` or `-` prefix), confirming the existing fetch-and-error pattern is untouched.

### Analysis

The `advisory_summary` handler's SBOM lookup logic uses `SbomService::new(&db).fetch(sbom_id.id)` followed by an `.ok_or(...)` pattern (visible in the surrounding context of the diff). This pattern returns a 404 error via `AppError` when the SBOM is not found.

The PR diff does not modify this error handling path. The new threshold filtering logic is applied only after a successful SBOM fetch, so non-existent SBOM IDs will continue to produce 404 responses before any threshold logic is reached.

The existing behavior is preserved.

### Note

While the existing behavior is preserved, the task also requires a test for this scenario (`Test non-existent SBOM ID returns 404`). That test is absent from the diff since `tests/api/advisory_summary.rs` was not created. The absence of the test file is tracked under the Scope Containment finding.
