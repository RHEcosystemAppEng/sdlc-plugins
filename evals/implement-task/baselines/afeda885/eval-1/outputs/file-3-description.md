# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisories linked to a given SBOM and returns aggregated severity counts.

## Detailed Changes

Add a new method to the `AdvisoryService` impl block, following the existing pattern of `fetch` and `list` methods:

```rust
/// Compute aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts by severity level. Returns
/// a `SeveritySummary` with counts for Critical, High, Medium, Low, and total.
///
/// Returns `AppError` with 404 status if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify SBOM exists (return 404 if not found)
    // Query sbom_advisory join table for advisories linked to this SBOM
    // Fetch AdvisorySummary for each linked advisory
    // Deduplicate by advisory ID using a HashSet or similar
    // Count severity levels from the `severity` field on AdvisorySummary
    // Build and return SeveritySummary with counts and total

    // 1. Verify SBOM exists
    let _sbom = self.sbom_service
        .fetch(sbom_id.clone(), tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM with ID {} not found", sbom_id)))
        .context("Looking up SBOM for severity summary")?;

    // 2. Query advisories linked to this SBOM via sbom_advisory join table
    let linked_advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx)
        .await
        .context("Querying advisories linked to SBOM")?;

    // 3. Deduplicate by advisory ID
    let unique_advisory_ids: HashSet<_> = linked_advisories
        .iter()
        .map(|sa| sa.advisory_id.clone())
        .collect();

    // 4. Fetch severity for each unique advisory and count
    let mut summary = SeveritySummary::default();
    for advisory_id in &unique_advisory_ids {
        if let Some(advisory) = self.fetch(advisory_id.clone(), tx).await? {
            match advisory.severity.as_deref() {
                Some("critical") | Some("Critical") => summary.critical += 1,
                Some("high") | Some("High") => summary.high += 1,
                Some("medium") | Some("Medium") => summary.medium += 1,
                Some("low") | Some("Low") => summary.low += 1,
                _ => {} // Unknown or no severity -- counted in total but not categorized
            }
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Required Imports

Add at the top of the file (if not already present):

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
use common::error::AppError;
use anyhow::Context;
```

## Conventions Applied

- **Method signature**: Follows the existing `fetch` and `list` pattern -- takes `&self`, domain-specific ID parameter, and `tx: &Transactional<'_>`
- **Error handling**: Uses `Result<T, AppError>` with `.context()` wrapping, matching the pattern in `common/src/error.rs`
- **Service method naming**: Uses `severity_summary` following the `verb_noun` naming convention (though this is a noun phrase, it matches the domain concept)
- **Transaction propagation**: Accepts `&Transactional<'_>` and passes it through to all database queries
- **SBOM existence check**: Returns 404 when SBOM ID does not exist, consistent with existing SBOM endpoints (acceptance criterion)
- **Deduplication**: Uses `HashSet` on advisory IDs to count only unique advisories (acceptance criterion)
- **Default zero counts**: Leverages `SeveritySummary::default()` which initializes all counts to 0 (acceptance criterion)
- **Documentation**: Doc comment on the method explaining behavior, parameters, and error cases
