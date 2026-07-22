# File 3: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose
Add the `severity_summary` method to `AdvisoryService` that queries advisories linked to an SBOM and aggregates counts by severity level.

## Changes

### Import additions (top of file)

Add these imports alongside existing ones:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

### New method on `AdvisoryService` impl block

Add the `severity_summary` method to the existing `impl AdvisoryService` block, after the existing `fetch` and `list` methods:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts occurrences per
/// severity level (Critical, High, Medium, Low).
///
/// Returns a `SeveritySummary` with per-level counts and total.
/// Returns `AppError` with 404 status if the SBOM does not exist.
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
        .ok_or_else(|| AppError::not_found(format!("SBOM with ID {} not found", sbom_id)))
        .context("fetching SBOM for severity summary")?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("querying sbom_advisory join table")?;

    // Deduplicate by advisory ID
    let mut seen = HashSet::new();
    let mut summary = SeveritySummary::default();

    for link in &advisories {
        if !seen.insert(link.advisory_id.clone()) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory summary to get its severity
        if let Some(advisory) = self
            .fetch(link.advisory_id.clone(), tx)
            .await?
        {
            match advisory.severity.as_deref() {
                Some("critical") | Some("Critical") => summary.critical += 1,
                Some("high") | Some("High") => summary.high += 1,
                Some("medium") | Some("Medium") => summary.medium += 1,
                Some("low") | Some("Low") => summary.low += 1,
                _ => {} // Unknown or missing severity — do not count
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Conventions Applied
- Method signature follows existing `fetch`/`list` pattern: `&self`, typed ID parameter, `&Transactional<'_>`.
- Returns `Result<T, AppError>` consistent with all other service methods.
- Uses `.context()` for error wrapping, matching the pattern in `common/src/error.rs`.
- Doc comment on the method explains purpose, parameters, and error behavior.
- SBOM existence check returns 404 consistent with existing SBOM endpoints (acceptance criterion).
- Deduplicates by advisory ID using a `HashSet` (acceptance criterion: "Counts only unique advisories").
- All severity counts default to 0 via `SeveritySummary::default()`.

## Notes
- The exact SBOM existence check may vary depending on what service is injected; this follows the pattern likely used by `fetch` in the same service.
- The severity string matching accounts for case variations that may exist in the data.
- The `entity::sbom_advisory` import references the join table entity defined in `entity/src/sbom_advisory.rs`.
