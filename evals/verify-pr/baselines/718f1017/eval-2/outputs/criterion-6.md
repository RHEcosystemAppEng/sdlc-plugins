## Criterion 6

**Text**: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Verdict**: PASS

**Evidence**: The diff context in `modules/fundamental/src/advisory/endpoints/get.rs` (lines 30-32) shows the existing SBOM fetch logic is preserved:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

The handler signature returns `Result<Json<AdvisorySummary>, AppError>`, and the surrounding context (visible in the diff) retains the `.ok_or(AppError::NotFound)` pattern (or equivalent) that was present before the change. The PR does not modify the SBOM lookup or error handling path for non-existent SBOMs. The existing 404 behavior is preserved unchanged.
