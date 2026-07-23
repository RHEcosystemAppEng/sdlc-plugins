# File 2: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose
Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Changes

### Add imports
At the top of the file, add imports for the new model type and any required entity types:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```
Also ensure imports exist for:
- The `sbom_advisory` entity (from `entity::sbom_advisory`)
- `HashSet` (for deduplication by advisory ID)

### Add `severity_summary` method to `AdvisoryService` impl block

Following the existing pattern of `fetch` and `list` methods, add:

```rust
/// Returns aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the sbom_advisory join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a 404 error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists (return 404 if not)
    //    Use the same SBOM existence check pattern as other endpoints

    // 2. Query sbom_advisory join table for all advisory IDs linked to this SBOM
    //    Use SeaORM query builder on entity::sbom_advisory

    // 3. Load AdvisorySummary for each linked advisory to access the severity field
    //    Use the existing fetch/list patterns in this service

    // 4. Deduplicate by advisory ID using a HashSet

    // 5. Count by severity level:
    //    - Match severity string against "Critical", "High", "Medium", "Low"
    //    - Increment the corresponding counter
    //    - Default unrecognized severities to 0 (do not count them)

    // 6. Compute total as sum of all severity counts

    // 7. Return SeveritySummary with all counts
    //    All levels default to 0 when no advisories exist at that level
}
```

### Key implementation details
- **Method signature** matches existing methods: `&self`, domain-specific ID, `tx: &Transactional<'_>`
- **Error handling** uses `.context("Failed to fetch severity summary for SBOM")` wrapping, matching `fetch` and `list`
- **SBOM existence check** replicates the pattern used by existing SBOM endpoints to return 404 for non-existent SBOMs
- **Deduplication** uses `HashSet<Id>` to track seen advisory IDs before counting
- **Severity matching** reads the `severity` field from `AdvisorySummary` (defined in `model/summary.rs`)

## Impact
- Adds one new public method to `AdvisoryService`
- No changes to existing method signatures or behavior
- The method is purely additive -- backward compatible
