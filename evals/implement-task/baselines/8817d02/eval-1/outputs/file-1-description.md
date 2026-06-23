# File 1: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Change Type
Modify existing file

## Description
Add a `severity_summary` method to the existing `AdvisoryService` struct. This method aggregates advisory severity counts for a given SBOM by querying the `sbom_advisory` join table and counting advisories per severity level.

## Detailed Changes

### Add new method to `AdvisoryService` impl block

Following the existing pattern of `fetch` and `list` methods, add a new `severity_summary` method:

```rust
/// Returns an aggregated summary of advisory severity counts for the given SBOM.
///
/// Queries the sbom_advisory join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a SeveritySummary with counts for Critical, High, Medium, and Low
/// severity levels plus a total count.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Given an SBOM ID, verify the SBOM exists first
    let sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("failed to fetch SBOM for severity summary")?;

    if sbom.is_none() {
        return Err(AppError::NotFound("SBOM not found".to_string()).into());
    }

    // Query sbom_advisory join table to find linked advisories
    // Use DISTINCT on advisory ID to deduplicate
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("failed to query advisories for SBOM")?;

    // Deduplicate by advisory ID and count by severity
    let mut seen_ids = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            if seen_ids.insert(advisory.id.clone()) {
                match advisory.severity.as_deref() {
                    Some("critical") => summary.critical += 1,
                    Some("high") => summary.high += 1,
                    Some("medium") => summary.medium += 1,
                    Some("low") => summary.low += 1,
                    _ => {} // Unknown or null severity — not counted
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

### Add required imports

At the top of the file, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

## Conventions Followed
- Method signature matches `fetch`/`list` pattern: `&self, id: Id, tx: &Transactional<'_>`
- Error wrapping uses `.context("descriptive message")` matching `common/src/error.rs` pattern
- Returns `Result<T, anyhow::Error>` consistent with other service methods
- Documentation comment on the new public method
- SBOM existence check returns 404 consistent with existing SBOM endpoints
