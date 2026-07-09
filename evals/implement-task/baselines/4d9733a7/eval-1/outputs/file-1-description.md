# File 1: modules/fundamental/src/advisory/service/advisory.rs

**Action**: Modify (existing file)

## Current State

This file contains the `AdvisoryService` struct with existing methods `fetch`, `list`, and `search` for advisory operations. Each method follows the pattern of accepting `&self`, an identifier parameter, and `tx: &Transactional<'_>` for transaction support, returning `Result<T, AppError>`.

## Changes

### Add `severity_summary` method to `AdvisoryService`

Add a new public async method `severity_summary` that aggregates advisory severity counts for a given SBOM:

```rust
/// Returns a summary of advisory severity counts for the specified SBOM.
///
/// Queries advisories linked to the SBOM via the `sbom_advisory` join table,
/// deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Query the sbom_advisory join table to find advisory IDs linked to sbom_id
    // 2. Join with advisory data to get AdvisorySummary records (which have severity field)
    // 3. Deduplicate by advisory ID (use .distinct() or collect into HashSet)
    // 4. Count each severity level: Critical, High, Medium, Low
    // 5. Compute total count
    // 6. Return SeveritySummary { critical, high, medium, low, total }
}
```

**Implementation details**:
- Use SeaORM query builder to join `sbom_advisory` with advisory entity
- Filter by `sbom_id` on the join table
- Use the `severity` field from `AdvisorySummary` (in `advisory/model/summary.rs`) to categorize
- Deduplicate advisories by their unique ID before counting (acceptance criterion: counts only unique advisories)
- Default all severity levels to 0 when no advisories exist at that level
- Wrap database errors with `.context("Failed to aggregate advisory severity for SBOM")` matching the error handling convention
- Return 404-equivalent error if the SBOM ID does not exist (check SBOM existence first)

### Add import

Add `use crate::advisory::model::severity_summary::SeveritySummary;` to the imports section.
