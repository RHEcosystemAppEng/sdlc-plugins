# File 2: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Action: MODIFY

## Purpose
Add a `severity_summary` method to `AdvisoryService` that queries advisories linked to a given SBOM, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary`.

## Conventions Applied
- Method follows `verb_noun` naming pattern (consistent with existing `fetch`, `list`, `search`)
- Method signature follows the established pattern: `&self, sbom_id: Id, tx: &Transactional<'_>`
- Returns `Result<SeveritySummary, AppError>` with `.context()` error wrapping
- Uses the `sbom_advisory` join table as specified in implementation notes

## Detailed Changes

### 1. Add import for the new model

At the top of the file, add:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also ensure imports for the `sbom_advisory` entity and any needed collection types (e.g., `HashSet`) are present:
```rust
use entity::sbom_advisory;
use std::collections::HashSet;
```

### 2. Add `severity_summary` method to `AdvisoryService` impl block

Insert the following method into the existing `impl AdvisoryService` block, after the existing `list` or `search` method:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries all advisories linked to the specified SBOM via the `sbom_advisory`
/// join table, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts per severity level and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM with id {} not found", sbom_id)))
        .context("looking up SBOM for severity summary")?;

    // Query advisories linked to this SBOM via the join table
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("querying sbom_advisory join table")?;

    // Deduplicate by advisory ID and collect unique advisory IDs
    let mut seen = HashSet::new();
    let unique_advisory_ids: Vec<_> = advisory_links
        .iter()
        .filter(|link| seen.insert(link.advisory_id.clone()))
        .map(|link| link.advisory_id.clone())
        .collect();

    // Fetch each unique advisory's summary to get severity
    let mut summary = SeveritySummary::default();
    for advisory_id in &unique_advisory_ids {
        if let Some(advisory) = self.fetch(advisory_id.clone(), tx).await? {
            match advisory.severity.as_deref() {
                Some("critical") => summary.critical += 1,
                Some("high") => summary.high += 1,
                Some("medium") => summary.medium += 1,
                Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- do not count
            }
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Rationale
- The SBOM existence check ensures a 404 is returned for non-existent SBOMs (acceptance criterion)
- Deduplication via `HashSet` ensures unique advisory counts (acceptance criterion)
- The method reuses the existing `fetch` method on `AdvisoryService` to get advisory details, following the reuse-first principle
- Severity matching uses lowercase strings consistent with how `AdvisorySummary.severity` stores values
- Default `SeveritySummary` ensures all counts start at 0 (acceptance criterion)
- The total is computed as the sum of individual counts to ensure consistency
- Error wrapping with `.context()` follows the established error handling convention
