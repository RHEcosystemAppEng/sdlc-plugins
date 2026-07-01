## Criterion 6: Endpoint returns 404 for non-existent SBOM IDs (existing behavior preserved)

**Result: PASS**

### Analysis

The diff preserves the existing SBOM fetch logic:

```rust
let sbom = SbomService::new(&db)
    .fetch(sbom_id.id)
```

This existing code (visible in the diff context) fetches the SBOM by ID using `SbomService::fetch()`. The pre-existing behavior returns a 404 via `AppError::NotFound` when the SBOM does not exist. The diff does not modify or remove this lookup -- it only adds filtering logic after the SBOM is successfully fetched and the advisory summary is aggregated.

The 404 behavior for non-existent SBOM IDs is an existing behavior that the task requires to be preserved. Since the diff does not alter the SBOM lookup flow, this behavior remains intact.

Note: While the task's test requirements include testing the 404 case for non-existent SBOM IDs, the absence of the entire test file (`tests/api/advisory_summary.rs`) is addressed separately. The acceptance criterion itself is about preserving the behavior, which the code does.

### Evidence

The diff context (lines 31-37 of the modified `get.rs`) shows the SBOM fetch call is unchanged. The new filtering logic is added after this point, only executing when the SBOM exists and the advisory summary has been successfully aggregated.

### Verdict

PASS -- The existing 404 behavior for non-existent SBOM IDs is preserved; the diff does not modify the SBOM lookup logic.
