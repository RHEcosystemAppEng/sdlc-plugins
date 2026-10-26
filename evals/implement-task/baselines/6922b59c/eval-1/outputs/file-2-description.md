# File 2: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Pre-Implementation Inspection

Before modifying, would use:
1. `mcp__serena_backend__get_symbols_overview` on this file to see AdvisoryService struct and all method signatures
2. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to understand the method pattern (parameters, return type, error handling, transaction usage)
3. `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` to understand the list/aggregation pattern
4. `mcp__serena_backend__search_for_pattern` for `sbom_advisory` to understand how the join table is queried
5. `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `model/summary.rs` to understand the `severity` field type

Would also check:
- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to ensure no callers would be broken by adding a new method
- Existing imports at the top of the file to understand available types

## Changes

Add a new `severity_summary` method to the `impl AdvisoryService` block. The method follows the same signature pattern as `fetch` and `list`:

```rust
/// Aggregates advisory severity counts for the given SBOM.
///
/// Returns a summary with counts per severity level (Critical, High, Medium, Low)
/// and a total count. Advisories are deduplicated by advisory ID before counting.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Verify the SBOM exists; return 404-compatible error if not
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("failed to fetch SBOM")?
        .ok_or_else(|| anyhow::anyhow!("SBOM not found"))
        .context("SBOM does not exist")?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx)
        .await
        .context("failed to query advisories for SBOM")?;

    // Deduplicate by advisory ID and count by severity
    let mut seen = std::collections::HashSet::new();
    let mut critical = 0u64;
    let mut high = 0u64;
    let mut medium = 0u64;
    let mut low = 0u64;

    for (_sbom_adv, advisory) in &advisories {
        if let Some(adv) = advisory {
            if seen.insert(adv.id.clone()) {
                // Build AdvisorySummary to access the severity field
                // (following the pattern used by existing list/fetch methods)
                match adv.severity.as_deref() {
                    Some("Critical") | Some("critical") => critical += 1,
                    Some("High") | Some("high") => high += 1,
                    Some("Medium") | Some("medium") => medium += 1,
                    Some("Low") | Some("low") => low += 1,
                    _ => {} // Unknown or None severity -- not counted
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

### Imports to Add

At the top of the file, add necessary imports:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

## Notes

- The exact query approach depends on what SeaORM entity relationships are already set up between `sbom_advisory` and `advisory`. Would verify using `mcp__serena_backend__find_symbol` on the entity definitions before writing the query.
- The severity field access pattern (`adv.severity`) depends on how AdvisorySummary stores severity -- would verify the actual field name and type by inspecting `model/summary.rs`.
- SBOM existence check follows the pattern of returning a 404-compatible error, consistent with existing SBOM endpoints.
- Deduplication uses a HashSet on advisory ID to ensure unique counting.
- If the actual codebase uses a different pattern for accessing severity (e.g., an enum instead of a string), the match arms would be adjusted accordingly.
- Performance: for SBOMs with up to 500 advisories, a single query with in-memory aggregation is sufficient. For larger datasets, a SQL GROUP BY aggregation could be used instead, but the current approach keeps implementation consistent with sibling methods.
