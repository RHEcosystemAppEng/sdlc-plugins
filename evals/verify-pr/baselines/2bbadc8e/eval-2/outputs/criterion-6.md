# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs

## Criterion
Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The diff preserves the existing 404 behavior for non-existent SBOM IDs. The handler still includes:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ...
```

The existing `SbomService::fetch()` call returns an error when the SBOM ID does not exist, which is propagated via the `?` operator and the `AppError` handling (which maps not-found errors to 404 responses). This behavior is part of the pre-existing code that was not modified in the diff.

The diff adds threshold filtering AFTER the SBOM lookup, so the 404 behavior for non-existent SBOMs is preserved — the function returns an error before reaching the filtering logic.

**Note:** While the 404 behavior is preserved in the endpoint code, no test was added to verify this behavior (tests/api/advisory_summary.rs is absent from the diff). The criterion asks about endpoint behavior, which is preserved.

**Evidence:** The `SbomService::new(&db).fetch(sbom_id.id)` call and subsequent error propagation remain unchanged in the diff.
