# File 6: modules/fundamental/src/advisory/service/advisory.rs

## Operation: MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, loads advisory severity data, deduplicates by advisory ID, counts by severity level, and returns a `SeveritySummary` struct.

## Sibling Reference

Follows the pattern of existing `fetch` and `list` methods on `AdvisoryService` for method signature, error handling, and transactional parameter usage.

## Detailed Changes

### 1. Add import for the new model

At the top of the file, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also ensure imports for the `sbom_advisory` entity and any collection types (e.g., `HashSet`) are present:

```rust
use entity::sbom_advisory;
use std::collections::HashSet;
```

### 2. Add `severity_summary` method to `impl AdvisoryService`

```rust
/// Retrieves aggregated severity counts for advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the specified SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with counts for critical, high, medium, and low
/// severity levels, plus a total.
///
/// Returns `AppError::NotFound` if the SBOM does not exist.
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
        .context("Failed to verify SBOM existence")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the join table
    let advisory_links = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisory links")?;

    // Deduplicate by advisory ID and collect unique advisory IDs
    let mut seen_ids = HashSet::new();
    let unique_advisory_ids: Vec<_> = advisory_links
        .iter()
        .filter(|link| seen_ids.insert(link.advisory_id.clone()))
        .map(|link| link.advisory_id.clone())
        .collect();

    // Fetch advisory summaries and count by severity
    let mut summary = SeveritySummary::default();
    for advisory_id in &unique_advisory_ids {
        let advisory = self
            .fetch(advisory_id.clone(), tx)
            .await
            .context("Failed to fetch advisory details")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref().unwrap_or_default() {
                "critical" | "Critical" => summary.critical += 1,
                "high" | "High" => summary.high += 1,
                "medium" | "Medium" => summary.medium += 1,
                "low" | "Low" => summary.low += 1,
                _ => {} // Unknown severity levels are not counted
            }
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Design Decisions

- **Method signature**: `async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>` follows the established pattern of `fetch` and `list` methods.
- **SBOM existence check**: Verifies the SBOM exists before querying advisories, returning 404 if not found. This satisfies acceptance criterion 2 ("Returns 404 when SBOM ID does not exist").
- **Deduplication via HashSet**: Uses a `HashSet<AdvisoryId>` to track seen advisory IDs, ensuring each advisory is counted only once. This satisfies acceptance criterion 3 ("Counts only unique advisories").
- **Default to zero**: `SeveritySummary::default()` initializes all counts to 0 via the `Default` derive. This satisfies acceptance criterion 4 ("All severity levels default to 0").
- **Case-insensitive severity matching**: Matches both lowercase and capitalized severity strings to handle potential inconsistencies in advisory data.
- **Defensive property access**: Uses `.as_deref().unwrap_or_default()` on the severity field to guard against null/None values, following the skill's defensive property access guidance.
- **Total computation**: Computed as the sum of all severity levels after counting, ensuring consistency.
- **Error wrapping**: All fallible operations use `.context()` for descriptive error messages, matching the established error handling convention.
- **Doc comment**: Comprehensive `///` documentation on the public method explaining behavior, parameters, and error conditions.

## Performance Consideration

The current implementation fetches each advisory individually in a loop. For SBOMs with up to 500 advisories (acceptance criterion 5: response time under 200ms), this might be slow if each fetch hits the database. An optimization would be to batch-fetch all advisory IDs in a single query and join with the advisory table to get severities in one round trip. However, the initial implementation follows the existing `fetch` pattern for consistency. If performance testing reveals it exceeds 200ms, the query would be refactored to a single joined query:

```rust
// Optimized: single query with join
let results = sbom_advisory::Entity::find()
    .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
    .inner_join(advisory::Entity)
    .select_also(advisory::Column::Severity)
    .group_by(advisory::Column::Id)
    .all(tx.connection())
    .await?;
```

This note would be included as a code comment in the implementation for reviewer awareness.

## Conventions Applied

- Method signature matches `fetch` and `list` patterns
- `Result<T, AppError>` return type
- `.context()` error wrapping on every fallible operation
- `&self` receiver (service is borrowed, not consumed)
- `Id` type for identifiers (not raw strings)
- `Transactional<'_>` for database transaction context
