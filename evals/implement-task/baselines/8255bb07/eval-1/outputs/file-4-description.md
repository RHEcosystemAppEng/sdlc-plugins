# File 4: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct that queries advisories linked to a given SBOM, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary`.

## Pre-Implementation Inspection

Before modifying this file, inspect:
- **`modules/fundamental/src/advisory/service/advisory.rs`** — Read the existing `AdvisoryService` struct and its `fetch` and `list` methods to understand the method signature pattern (`&self`, ID param, `tx: &Transactional<'_>`), error handling (`Result<T, AppError>` with `.context()`), and database query patterns.
- **`entity/src/sbom_advisory.rs`** — Understand the SBOM-Advisory join table entity for constructing the query that finds advisories linked to a given SBOM.
- **`modules/fundamental/src/advisory/model/summary.rs`** — Understand the `AdvisorySummary` struct and its `severity` field, which will be used to classify advisories by severity level.

## Changes

Add the following method to the `impl AdvisoryService` block:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;

/// Computes aggregated severity counts for advisories linked to the specified SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the given SBOM ID, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts for Critical, High, Medium, Low, and total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists; return 404 if not found
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisories")?;

    // Deduplicate by advisory ID
    let mut seen = HashSet::new();
    let mut summary = SeveritySummary::default();

    for sa in &advisories {
        if !seen.insert(sa.advisory_id.clone()) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory to get its severity
        let advisory = self
            .fetch(sa.advisory_id.clone(), tx)
            .await
            .context("Failed to fetch advisory details")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref() {
                Some("Critical") => summary.critical += 1,
                Some("High") => summary.high += 1,
                Some("Medium") => summary.medium += 1,
                Some("Low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- not counted in named buckets
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

## Conventions Applied

- **Method signature**: Follows the same pattern as `fetch` and `list` methods: `(&self, id: Id, tx: &Transactional<'_>)`.
- **Error handling**: Uses `Result<T, AppError>` return type with `.context()` wrapping on every fallible operation, matching the `common/src/error.rs` pattern.
- **404 handling**: Returns `AppError::not_found()` when the SBOM ID does not exist, consistent with existing SBOM endpoints.
- **Deduplication**: Uses `HashSet` to track seen advisory IDs, ensuring unique advisories are counted only once per the acceptance criteria.
- **Default values**: Uses `SeveritySummary::default()` which initializes all counts to 0, satisfying the criterion that all severity levels default to 0.
- **Documentation**: Method has a `///` doc comment explaining its purpose and behavior.
