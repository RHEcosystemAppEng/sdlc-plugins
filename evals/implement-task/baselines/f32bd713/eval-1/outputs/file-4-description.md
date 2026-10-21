# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action**: Modify

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that queries the
`sbom_advisory` join table, joins to the advisory table to get severity levels,
deduplicates by advisory ID, and returns a `SeveritySummary` struct with counts per
severity level.

## Pre-implementation inspection

Before modifying this file, would inspect using Serena:

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` -- understand the full structure: impl blocks, existing methods (fetch, list, search), field types
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` -- read the full method body to understand: parameter types, transaction usage, query patterns, error handling, return type
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` -- read another method for cross-reference
- `mcp__serena_backend__get_symbols_overview` on `entity/src/sbom_advisory.rs` -- understand the join table entity (columns, relations)
- `mcp__serena_backend__get_symbols_overview` on `entity/src/advisory.rs` -- understand the advisory entity (severity field name and type)
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` -- read the severity field type to know how to count by level
- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` -- check for trait implementations, callers, and ensure the new method doesn't conflict
- `mcp__serena_backend__search_for_pattern` for `Transactional` -- confirm the transaction type import path

Also check for existing severity aggregation logic to avoid duplication:
- Grep for `severity` and `count` or `aggregate` in `modules/fundamental/src/advisory/`
- Grep for `severity_summary` across the codebase

## Detailed changes

Would add a new method `severity_summary` to the `impl AdvisoryService` block, placed after the existing `list` or `search` method (using `mcp__serena_backend__insert_after_symbol` on the last existing method):

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Queries advisories linked to the specified SBOM via the `sbom_advisory` join table,
/// deduplicates by advisory ID, and returns counts per severity level.
pub async fn severity_summary(
    &self,
    sbom_id: &Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Verify the SBOM exists; return 404-mapped error if not
    let _sbom = self
        .sbom_service
        .fetch(sbom_id, tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM {sbom_id} not found")))?;

    // Query advisories linked to this SBOM, deduplicated by advisory ID
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .inner_join(advisory::Entity)
        .select_also(advisory::Entity)
        .group_by(advisory::Column::Id)
        .all(tx.connection())
        .await
        .context("failed to query SBOM advisories")?;

    // Count by severity level
    let mut summary = SeveritySummary::default();
    for (_join_row, maybe_advisory) in &advisories {
        if let Some(adv) = maybe_advisory {
            match adv.severity.as_deref().unwrap_or_default() {
                "critical" => summary.critical += 1,
                "high" => summary.high += 1,
                "medium" => summary.medium += 1,
                "low" => summary.low += 1,
                _ => {} // unknown severity levels are not counted
            }
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

**Additional imports** needed at the top of the file:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
```

## Conventions applied

- Method signature follows the existing pattern: `&self`, domain ID parameter (`&Id`), transaction (`&Transactional<'_>`)
- Error wrapping with `.context()` matching the `common/src/error.rs` pattern
- Returns `Result<SeveritySummary, anyhow::Error>` matching sibling method return types
- SeaORM query pattern matching existing service methods
- SBOM existence check returns 404 when not found, consistent with existing SBOM endpoints (acceptance criterion)
- Deduplication via `group_by(advisory::Column::Id)` satisfying the uniqueness acceptance criterion
- `///` doc comment on the method describing purpose and behavior
- Defensive property access on advisory severity with `.unwrap_or_default()` (per SKILL.md defensive access guidance)
- Unknown severity levels silently ignored (reasonable default -- task only requires critical/high/medium/low)

## Notes

- The exact query pattern (SeaORM join syntax, column names) would be confirmed by Serena inspection of the entity files
- The severity field type on the advisory entity needs verification -- may be an enum rather than a string, which would change the match pattern
- If `AdvisoryService` does not have direct access to `sbom_service`, may need to inject it or use the SBOM entity directly for the existence check
- The SBOM existence check approach would be verified against how other endpoints handle 404 for missing entities
