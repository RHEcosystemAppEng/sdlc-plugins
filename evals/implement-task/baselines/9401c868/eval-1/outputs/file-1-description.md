# File 1: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct.

## Pre-Implementation Analysis

Before modifying, would use Serena to inspect the file:
- `mcp__serena_backend__get_symbols_overview` on this file to see AdvisoryService methods
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to understand the method signature pattern
- `mcp__serena_backend__find_symbol` on `AdvisoryService::list` for secondary reference
- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to verify no breaking changes

Also would search for:
- `sbom_advisory` usage patterns via `mcp__serena_backend__search_for_pattern`
- `AdvisorySummary::severity` field usage to understand how severity is accessed
- Existing deduplication patterns in the service layer

## Changes

### Add import for the new model

At the top of the file, add an import for the `SeveritySummary` struct:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Add `severity_summary` method to `AdvisoryService` impl block

Following the pattern of existing `fetch` and `list` methods (which take `&self`, entity ID, and `tx: &Transactional<'_>`), add a new method:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// specified SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with counts for Critical, High, Medium, and Low,
/// plus a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Query sbom_advisory join table for advisories linked to this SBOM
    let sbom_advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("failed to query sbom_advisory join table")?;

    // If no SBOM exists (would verify via SBOM lookup first)
    // Return 404 consistent with existing SBOM endpoints

    // Collect unique advisory IDs to deduplicate
    let unique_advisory_ids: HashSet<_> = sbom_advisories
        .iter()
        .map(|sa| sa.advisory_id.clone())
        .collect();

    // Fetch each unique advisory's summary to read severity
    let mut critical = 0u64;
    let mut high = 0u64;
    let mut medium = 0u64;
    let mut low = 0u64;

    for advisory_id in &unique_advisory_ids {
        // Use existing fetch method or direct query to get advisory with severity
        let advisory = self.fetch(advisory_id.clone(), tx)
            .await
            .context("failed to fetch advisory for severity aggregation")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref().unwrap_or_default() {
                "Critical" => critical += 1,
                "High" => high += 1,
                "Medium" => medium += 1,
                "Low" => low += 1,
                _ => {} // Unknown severity levels are not counted
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

## Key Decisions

- **Pattern followed**: Same signature pattern as `fetch` method (`&self, id: Id, tx: &Transactional<'_>`)
- **Deduplication**: Uses `HashSet` on advisory IDs to ensure unique counting per acceptance criteria
- **Error handling**: Uses `.context()` wrapping returning `AppError`, matching sibling methods
- **Defensive access**: Uses `.unwrap_or_default()` on severity field for defensive property access on external data
- **Documentation**: Doc comment on the new method explaining what it does, parameters, and return value

## Symbols Modified

- `AdvisoryService` impl block: new method `severity_summary` added via `mcp__serena_backend__insert_after_symbol` (after the last existing method)
