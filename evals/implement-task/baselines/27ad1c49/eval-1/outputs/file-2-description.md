# File 2: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct that queries the database for advisory severity counts linked to a given SBOM.

## Pre-Implementation Inspection

1. `mcp__serena_backend__get_symbols_overview` on this file to see the `AdvisoryService` struct and all its methods.
2. `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` to understand the method signature pattern:
   - Takes `&self, id: Id, tx: &Transactional<'_>`
   - Returns `Result<Option<AdvisoryDetails>, AppError>` or similar
   - Uses `.context()` for error wrapping
3. `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` to see the list pattern for comparison.
4. Inspect `entity/src/sbom_advisory.rs` to understand the join table entity and its columns.
5. Check `AdvisorySummary` struct's `severity` field type to understand what severity values look like.

## Changes

Add a new method `severity_summary` to the `AdvisoryService` impl block, using `mcp__serena_backend__insert_after_symbol` to place it after the last existing method.

### Method Signature

```rust
/// Returns aggregated advisory severity counts for the specified SBOM.
///
/// Queries the sbom_advisory join table to find all advisories linked to the
/// given SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a SeveritySummary with counts for Critical, High, Medium, Low,
/// and a total count.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
```

### Method Body (Pseudocode)

```rust
    // Verify the SBOM exists; return 404 if not found
    let sbom_exists = /* query sbom table for sbom_id */;
    if !sbom_exists {
        return Err(AppError::NotFound(format!("SBOM {} not found", sbom_id)));
    }

    // Query advisories linked to this SBOM via the sbom_advisory join table
    // Use DISTINCT on advisory ID to deduplicate
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(tx.connection())
        .await
        .context("failed to query advisory severity for SBOM")?;

    // Count by severity level, deduplicating by advisory ID
    let mut seen = HashSet::new();
    let mut critical = 0u64;
    let mut high = 0u64;
    let mut medium = 0u64;
    let mut low = 0u64;

    for (_sbom_adv, advisory) in &advisories {
        if let Some(adv) = advisory {
            if seen.insert(adv.id.clone()) {
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
```

### Required Imports

Add at the top of the file (following existing import organization):

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Defensive Property Access

The advisory entity's `severity` field may be `None` (nullable in the database). The implementation uses `as_deref()` with pattern matching to handle `None` gracefully, and the `Option<advisory>` from the join is handled with `if let Some`.

## Convention Compliance

- Method signature follows the `fetch`/`list` pattern: `&self`, entity ID, `&Transactional<'_>`
- Error handling uses `AppError` with `.context()` wrapping
- Return type is `Result<SeveritySummary, AppError>`
- Documentation comment on the public method explaining behavior and parameters
- Deduplication by advisory ID satisfies acceptance criterion
