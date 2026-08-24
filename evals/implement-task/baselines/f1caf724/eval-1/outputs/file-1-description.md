# File 1: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Pre-Implementation Inspection

Before modifying this file, read it using `mcp__serena_backend__get_symbols_overview` to see all existing methods in AdvisoryService, then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand their exact signatures and patterns.

## Changes

### Add `severity_summary` method to AdvisoryService

Add a new method following the pattern of existing `fetch` and `list` methods:

```rust
/// Returns a summary of advisory severity counts for a given SBOM.
///
/// Queries the sbom_advisory join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts advisories per
/// severity level (Critical, High, Medium, Low).
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(&self.db.connection(tx))
        .await
        .context("failed to query advisory severity summary")?;

    // Deduplicate by advisory ID
    let mut seen = std::collections::HashSet::new();
    let mut critical = 0u32;
    let mut high = 0u32;
    let mut medium = 0u32;
    let mut low = 0u32;

    for (_sbom_advisory, advisory) in &advisories {
        if let Some(adv) = advisory {
            if seen.insert(adv.id.clone()) {
                // Map severity field to counts
                match adv.severity.as_deref() {
                    Some("critical") => critical += 1,
                    Some("high") => high += 1,
                    Some("medium") => medium += 1,
                    Some("low") => low += 1,
                    _ => {} // unknown severity levels are not counted
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

### Import additions

Add to the imports section:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```
