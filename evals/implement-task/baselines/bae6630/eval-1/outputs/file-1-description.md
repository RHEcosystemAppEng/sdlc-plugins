# File 1: modules/fundamental/src/advisory/service/advisory.rs

**Action**: Modify (existing file)

## Pre-Implementation Inspection

Before modifying, inspect this file using:
- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` to see the full symbol structure of `AdvisoryService`
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` and `AdvisoryService::list` to understand the exact method signature, return type, and error handling pattern
- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new method integrates correctly

## Changes

Add a new `severity_summary` method to `AdvisoryService`. This method:

1. Takes `&self, sbom_id: Id, tx: &Transactional<'_>` as parameters, following the same signature pattern as existing `fetch` and `list` methods.

2. Queries the `sbom_advisory` join table (from `entity/src/sbom_advisory.rs`) to find all advisories linked to the given SBOM ID.

3. For each linked advisory, retrieves the `AdvisorySummary` and accesses its `severity` field.

4. Deduplicates advisories by advisory ID (counts each unique advisory only once, even if linked multiple times via different paths).

5. Aggregates severity counts into a `SeveritySummary` struct:
   - `critical: u32` -- count of advisories with Critical severity
   - `high: u32` -- count of advisories with High severity
   - `medium: u32` -- count of advisories with Medium severity
   - `low: u32` -- count of advisories with Low severity
   - `total: u32` -- total unique advisory count

6. Returns `Result<SeveritySummary, AppError>`.

7. Handles the case where the SBOM ID does not exist by returning a 404 `AppError` (check SBOM existence before querying advisories, following the pattern used by other service methods).

8. All severity levels default to 0 when no advisories exist at that level.

9. Uses `.context()` for error wrapping, matching the pattern in `common/src/error.rs`.

### New imports needed

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Method skeleton

```rust
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    // 2. Query sbom_advisory join table for all advisory IDs linked to sbom_id
    // 3. Deduplicate by advisory ID
    // 4. For each unique advisory, fetch its severity from AdvisorySummary
    // 5. Count by severity level
    // 6. Return SeveritySummary with counts
}
```
