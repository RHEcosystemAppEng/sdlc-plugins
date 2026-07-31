# File 1: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose
Add the `severity_summary` method to the existing `AdvisoryService` struct.

## Pre-Implementation Inspection
Before modifying, read the file using `mcp__serena_backend__get_symbols_overview` to understand the existing service structure. Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand their signature pattern, error handling, and transaction usage.

## Changes

### Add `severity_summary` method to `AdvisoryService`

Add a new method following the same pattern as existing `fetch` and `list` methods:

```rust
/// Returns a summary of advisory severity counts for the given SBOM.
///
/// Queries the sbom_advisory join table for all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("failed to fetch advisories for SBOM")?;

    // If SBOM doesn't exist, return 404
    // (verify SBOM exists first using sbom entity lookup)
    let _sbom = sbom::Entity::find_by_id(sbom_id)
        .one(tx.connection())
        .await
        .context("failed to fetch SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {sbom_id} not found")))?;

    // Fetch full advisory details to get severity, deduplicate by advisory ID
    let unique_advisory_ids: HashSet<_> = advisories
        .iter()
        .map(|sa| sa.advisory_id)
        .collect();

    let mut critical = 0u64;
    let mut high = 0u64;
    let mut medium = 0u64;
    let mut low = 0u64;

    for advisory_id in unique_advisory_ids {
        let advisory = advisory::Entity::find_by_id(advisory_id)
            .one(tx.connection())
            .await
            .context("failed to fetch advisory details")?;
        
        if let Some(adv) = advisory {
            match adv.severity.as_deref() {
                Some("Critical") => critical += 1,
                Some("High") => high += 1,
                Some("Medium") => medium += 1,
                Some("Low") => low += 1,
                _ => {}
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

### Required imports to add
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

## Error Handling
Uses `Result<SeveritySummary, AppError>` with `.context()` wrapping, matching the pattern in `common/src/error.rs` and the existing service methods.
