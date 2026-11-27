# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: MET (PASS), behavior preserved, but not tested**

## Evidence (get.rs, unchanged context lines)

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

## Reasoning

- The SBOM lookup that produces the not-found error comes before the new code and was not modified. The diff shows it only as context lines.
- The threshold logic runs only after the SBOM fetch succeeds, so it cannot hide or change the 404 path.
- Adding the `Query(params)` extractor does not affect path resolution. One edge case: axum rejects malformed query strings, but that is unrelated to SBOM existence.

The criterion is about preserving existing behavior, and that behavior is preserved, so it is met. However, the required test ("Test non-existent SBOM ID returns 404") was not written, because `tests/api/advisory_summary.rs` is absent from the PR.
