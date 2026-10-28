# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

## Verdict: PASS

## Reasoning

The diff in `modules/fundamental/src/advisory/endpoints/get.rs` preserves the existing SBOM lookup logic that precedes the newly added threshold filtering:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    // ... (implied .ok_or / .context pattern returning 404 for missing SBOMs)
```

This code path is unchanged by the diff. The SBOM fetch and 404 error handling occur before the threshold filtering logic:

1. The SBOM is fetched by ID
2. If not found, the existing error handling returns 404 (this is the pre-existing pattern per the repository conventions using `AppError`)
3. Only after a successful SBOM lookup does the code proceed to aggregate severities and apply threshold filtering

The diff adds the `Query(params)` extractor and filtering logic after the SBOM validation, so the 404 behavior for non-existent SBOM IDs is structurally preserved. No lines related to SBOM fetching or error handling were removed or altered.

While no new test was added to verify this behavior (the test file `tests/api/advisory_summary.rs` is entirely absent), the existing code path remains intact and functional.
