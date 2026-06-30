# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose
Add the `severity_summary` method to `AdvisoryService` that queries the database for advisory severity counts linked to a given SBOM.

## Detailed Changes

Add a new method to the `impl AdvisoryService` block:

```rust
/// Compute severity counts for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts advisories at each
/// severity level (Critical, High, Medium, Low).
///
/// Returns `AppError` with a 404 status if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not
    // (follow the pattern used by SbomService::fetch)
    let _sbom = self.sbom_service.fetch(sbom_id, tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM {sbom_id} not found")))?;

    // Query sbom_advisory join table for advisories linked to this SBOM,
    // join with advisory table to get severity, deduplicate by advisory ID
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("failed to query advisory severity summary")?;

    // Deduplicate by advisory ID and count by severity
    let mut seen = HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory) in &advisories {
        if let Some(adv) = advisory {
            if seen.insert(adv.id) {
                match adv.severity.as_deref() {
                    Some("critical") => summary.critical += 1,
                    Some("high") => summary.high += 1,
                    Some("medium") => summary.medium += 1,
                    Some("low") => summary.low += 1,
                    _ => {} // Unknown or null severity — counted in total but not categorized
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

## Additional Imports Required

At the top of the file, add:
```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Rationale
- Method signature follows the `fetch` and `list` pattern: `&self`, `Id`, `&Transactional<'_>`
- Uses `entity::sbom_advisory` join table as specified in Implementation Notes
- Deduplicates by advisory ID using a `HashSet` to satisfy acceptance criteria
- Returns `AppError` via `.context()` wrapping, matching existing error handling convention
- 404 check on SBOM existence mirrors the pattern in existing SBOM endpoints
- `SeveritySummary::default()` ensures all counts start at 0
