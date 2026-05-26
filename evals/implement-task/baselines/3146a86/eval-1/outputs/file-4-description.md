# File 4: MODIFY — `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose
Add `severity_summary` method to the AdvisoryService.

## Changes

Add a new method to `AdvisoryService` following the pattern of existing `fetch` and `list` methods:

```rust
/// Aggregates advisory severity counts for a given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Join with advisory table to get severity field from AdvisorySummary
    // Deduplicate by advisory ID
    // Count occurrences of each severity level
    // Return SeveritySummary with counts and total
}
```

## Key Implementation Details

- Method signature follows `fetch` and `list` pattern: `&self`, typed ID parameter, `&Transactional<'_>` for database access
- Uses `sbom_advisory` join table (`entity/src/sbom_advisory.rs`) to find advisories linked to the SBOM
- Reads the `severity` field from `AdvisorySummary` to count by level
- Deduplicates by advisory ID before counting
- Returns `Result<SeveritySummary, anyhow::Error>` with `.context()` error wrapping
- Defaults all counts to 0 via `SeveritySummary::default()` when no advisories exist
