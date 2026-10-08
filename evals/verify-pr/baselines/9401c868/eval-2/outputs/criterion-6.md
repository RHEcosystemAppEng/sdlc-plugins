## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

### Result: PASS

### Analysis

The existing SBOM lookup logic is preserved and unmodified in the diff:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

The `SbomService::fetch()` method (defined in `modules/fundamental/src/sbom/service/sbom.rs`) is not modified by this PR. Per the repository conventions, service methods return `Result<T, AppError>`, and a fetch for a non-existent entity returns an `AppError` that maps to a 404 response (via `AppError`'s `IntoResponse` implementation in `common/src/error.rs`).

The PR's changes are all below the SBOM fetch call, in the advisory aggregation and filtering logic. The error propagation path for non-existent SBOM IDs is untouched.

Note: While the existing 404 behavior is preserved, the task's test requirements include "Test non-existent SBOM ID returns 404" which requires a test in `tests/api/advisory_summary.rs`. That test file is absent from the PR (see scope containment analysis).
