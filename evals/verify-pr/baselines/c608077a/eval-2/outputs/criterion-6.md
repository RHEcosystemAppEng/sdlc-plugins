# Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict: PASS**

## Reasoning

The SBOM lookup is unchanged context in the diff and still runs before any of the new threshold logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
    ...
```

The PR adds only:
- a `Query(params): Query<SummaryParams>` extractor whose single field is `Option<String>`, so it cannot reject a request before the lookup runs, and
- post-aggregation filtering, which runs only after the SBOM has been found.

The existing not-found path, which maps to 404 through `AppError`, is therefore preserved as it was.

Caveat: this conclusion comes from reading the diff alone. The required test "non-existent SBOM ID returns 404" was not written, because `tests/api/advisory_summary.rs` is absent, so no regression test protects this behavior.

## Evidence
- `get.rs`: unchanged `SbomService::new(&db).fetch(sbom_id.id)` context lines ahead of the new code
- No changes to the error-mapping lines
