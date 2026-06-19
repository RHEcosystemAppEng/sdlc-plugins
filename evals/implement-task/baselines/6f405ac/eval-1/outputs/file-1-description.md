# File 1: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct.

## Detailed Changes

### Add new method `severity_summary` to `AdvisoryService`

Following the existing pattern of `fetch` and `list` methods in this service file:

```rust
/// Returns an aggregated severity summary for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts advisories at each
/// severity level (Critical, High, Medium, Low).
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .find_also_related(entity::advisory::Entity)
        .all(&self.db.connection(tx))
        .await
        .context("failed to query advisories for SBOM")?;

    // Deduplicate by advisory ID using a HashSet
    let mut seen = std::collections::HashSet::new();
    let mut critical = 0u64;
    let mut high = 0u64;
    let mut medium = 0u64;
    let mut low = 0u64;

    for (_sbom_adv, advisory) in &advisories {
        if let Some(adv) = advisory {
            if seen.insert(adv.id.clone()) {
                // Use the AdvisorySummary's severity field to categorize
                match adv.severity.as_deref() {
                    Some("Critical") | Some("critical") => critical += 1,
                    Some("High") | Some("high") => high += 1,
                    Some("Medium") | Some("medium") => medium += 1,
                    Some("Low") | Some("low") => low += 1,
                    _ => {} // Unknown or None severity is not counted
                }
            }
        }
    }

    let total = critical + high + medium + low;

    Ok(SeveritySummary {
        critical,
        high,
        medium,
        low,
        total,
    })
}
```

### Additional imports needed at the top of the file

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Conventions Followed

- Method signature matches existing pattern: `&self`, domain ID, `tx: &Transactional<'_>`
- Returns `Result<T, anyhow::Error>` with `.context()` wrapping
- Uses SeaORM entity queries consistent with existing `fetch` and `list` methods
- Documentation comment using `///` convention
- Deduplicates by advisory ID as required by acceptance criteria
- All severity levels default to 0 when no advisories exist (initialized to 0)
