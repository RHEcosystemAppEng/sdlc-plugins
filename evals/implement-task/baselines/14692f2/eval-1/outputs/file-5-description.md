# File 5: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Purpose
Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, deduplicates by advisory ID, retrieves severity levels from associated `AdvisorySummary` records, and returns a `SeveritySummary` with per-severity counts.

## Detailed Changes

### New Import
Add import for `SeveritySummary`:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also import the `sbom_advisory` entity if not already imported:

```rust
use entity::sbom_advisory;
```

### New Method: `severity_summary`

Add the following method to the `impl AdvisoryService` block, following the existing pattern of `fetch` and `list` methods:

```rust
/// Computes aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the specified SBOM, deduplicates by advisory ID, and counts advisories
/// at each severity level (Critical, High, Medium, Low).
///
/// Returns a 404 error if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: &Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    // (follow the same SBOM existence check pattern used by existing SBOM endpoints)

    // Query sbom_advisory join table for all advisory IDs linked to this SBOM
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx)
        .await
        .context("Failed to query SBOM advisory links")?;

    // Deduplicate by advisory ID using a HashSet
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id)
        .collect();

    // If no advisories found, return all zeros (valid SBOM with no advisories)
    if unique_advisory_ids.is_empty() {
        return Ok(SeveritySummary::default());
    }

    // Fetch AdvisorySummary for each unique advisory to get severity levels
    // Use the existing fetch/list pattern to retrieve advisory details
    let mut summary = SeveritySummary::default();

    for advisory_id in &unique_advisory_ids {
        // Retrieve the advisory and its severity field from AdvisorySummary
        let advisory = self.fetch(advisory_id, tx)
            .await
            .context("Failed to fetch advisory for severity aggregation")?;

        // Count by severity level using the severity field from AdvisorySummary
        match advisory.severity.as_deref() {
            Some("Critical") | Some("critical") => summary.critical += 1,
            Some("High") | Some("high") => summary.high += 1,
            Some("Medium") | Some("medium") => summary.medium += 1,
            Some("Low") | Some("low") => summary.low += 1,
            _ => {} // Unknown or None severity levels are not counted
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Pattern Notes
- **Method signature**: Follows `fetch` and `list` method pattern with `&self, id: &Id, tx: &Transactional<'_>`
- **SBOM existence check**: Must verify the SBOM exists first and return 404 if not, consistent with existing SBOM endpoint behavior
- **Deduplication**: Uses `HashSet` on advisory IDs before counting, per acceptance criteria requiring unique advisory counts
- **Severity matching**: Case-insensitive matching on severity string values from `AdvisorySummary.severity` field
- **Error wrapping**: Uses `.context()` on all fallible operations, matching the `AppError` pattern in `common/src/error.rs`

## Conventions Applied
- **Method signature**: `(&self, id, tx)` pattern matching existing service methods
- **Error handling**: `Result<T, AppError>` with `.context()` wrapping
- **Database access**: Uses SeaORM entity queries following existing patterns
- **Documentation**: Doc comment explaining method purpose, behavior, and error conditions
