# File 4: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose
Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Reference Files to Inspect First
- `modules/fundamental/src/advisory/service/advisory.rs` -- Read the existing `fetch` and `list` methods to understand the method signature pattern, query construction, and transaction usage.
- `entity/src/sbom_advisory.rs` -- Understand the join table schema for linking SBOMs to advisories.
- `modules/fundamental/src/advisory/model/summary.rs` -- Understand the `severity` field on `AdvisorySummary` to know how severity values are represented.

## Changes

Add a new `severity_summary` method to the `AdvisoryService` impl block, following the same pattern as `fetch` and `list`:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries all advisories linked to the specified SBOM via the `sbom_advisory`
/// join table, deduplicates by advisory ID, and counts advisories per severity
/// level (Critical, High, Medium, Low).
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query sbom_advisory join table to find all advisories linked to this SBOM
    // 2. Join with advisory table to get severity information
    // 3. Deduplicate by advisory ID (use DISTINCT or group-by)
    // 4. Count by severity level
    // 5. Build and return SeveritySummary with counts per level and total

    // If SBOM does not exist, return 404 error consistent with other SBOM endpoints
    // Use .context("failed to aggregate advisory severity") for error wrapping
}
```

## Implementation Details

The method should:

1. **Verify SBOM exists**: Check that the given SBOM ID corresponds to an existing SBOM. If not, return a not-found AppError (consistent with existing SBOM endpoints).

2. **Query advisories via join table**: Use the `sbom_advisory` entity from `entity/src/sbom_advisory.rs` to find all advisories linked to the SBOM.

3. **Fetch severity data**: For each linked advisory, obtain the severity level (using the same approach as `AdvisorySummary`'s `severity` field).

4. **Deduplicate**: Ensure each advisory is counted only once, even if linked multiple times (use `DISTINCT` on advisory ID or collect into a HashSet).

5. **Aggregate counts**: Count advisories per severity level (Critical, High, Medium, Low) and compute the total.

6. **Return SeveritySummary**: Construct and return the `SeveritySummary` struct with the aggregated counts.

## Notes
- The exact query construction (SeaORM query builder syntax, join syntax) must be confirmed by reading the existing `fetch` and `list` methods.
- Error handling uses `Result<SeveritySummary, AppError>` with `.context()` wrapping, matching the pattern in sibling service methods and `common/src/error.rs`.
- The method signature follows the established pattern: `(&self, id: Id, tx: &Transactional<'_>)`.
- An import for `SeveritySummary` from the model module will be needed at the top of the file.
