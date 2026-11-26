# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS (behavior preserved; no test added)**

## Evidence (modules/fundamental/src/advisory/endpoints/get.rs)

The existing lookup is unchanged context in the diff:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

## Reasoning

- The PR does not touch the SBOM lookup or its not-found error handling. The changes are the new `Query(params)` extractor and the code that runs after aggregation.
- The new extractor `Query<SummaryParams>` has a single `Option<String>` field, so it cannot fail on any threshold value. It does not cause a different error ahead of the 404 path, and existing 404 behavior is preserved.
- Gap: the Test Requirements include "Test non-existent SBOM ID returns 404", but no test was added because `tests/api/advisory_summary.rs` is missing. The behavior is preserved but not verified by the PR.

The criterion is met at the code level. The missing test is reported under Test Requirements and Scope Containment.
