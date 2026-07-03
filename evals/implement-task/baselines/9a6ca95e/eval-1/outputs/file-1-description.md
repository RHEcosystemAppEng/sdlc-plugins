# File 1: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Inspection performed

Used `mcp__serena_backend__get_symbols_overview` on this file to see the existing `AdvisoryService` struct and its methods (`fetch`, `list`, `search`). Then used `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to read the full method body and understand the signature pattern and error handling approach. Also used `mcp__serena_backend__find_symbol` on `AdvisoryService::list` to understand how query builders are constructed.

## Current state

The file contains `AdvisoryService` with methods:
- `fetch(&self, id: Id, tx: &Transactional<'_>) -> Result<Option<AdvisorySummary>, anyhow::Error>`
- `list(&self, ..., tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, anyhow::Error>`
- `search(&self, query: &str, ..., tx: &Transactional<'_>) -> Result<PaginatedResults<AdvisorySummary>, anyhow::Error>`

Each method uses `self.db` (a database connection pool reference) to execute SeaORM queries and wraps errors with `.context()`.

## Changes

Add a new public method `severity_summary` to `AdvisoryService`:

```rust
/// Returns a severity summary of all advisories linked to the specified SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the given SBOM ID, deduplicates by advisory ID, and counts occurrences of
/// each severity level (Critical, High, Medium, Low). Returns a
/// `SeveritySummary` with per-level counts and a total.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // Verify the SBOM exists -- return 404-compatible error if not
    let _sbom = sbom::Entity::find_by_id(sbom_id)
        .one(&self.db.connection(tx))
        .await
        .context("failed to query SBOM")?
        .ok_or_else(|| AppError::NotFound(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via sbom_advisory join table
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(advisory::Entity)
        .all(&self.db.connection(tx))
        .await
        .context("failed to query SBOM advisories")?;

    // Deduplicate by advisory ID and count by severity
    let mut seen = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory_opt) in advisories {
        if let Some(advisory) = advisory_opt {
            if seen.insert(advisory.id) {
                // Load the AdvisorySummary to access the severity field
                let adv_summary = AdvisorySummary::from(advisory);
                match adv_summary.severity.as_deref() {
                    Some("Critical") | Some("critical") => summary.critical += 1,
                    Some("High") | Some("high") => summary.high += 1,
                    Some("Medium") | Some("medium") => summary.medium += 1,
                    Some("Low") | Some("low") => summary.low += 1,
                    _ => {} // Unknown or missing severity -- not counted
                }
                summary.total += 1;
            }
        }
    }

    Ok(summary)
}
```

### Additional imports needed at top of file

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use crate::advisory::model::summary::AdvisorySummary;
use entity::{sbom, sbom_advisory, advisory};
use std::collections::HashSet;
```

(Only add imports that are not already present.)

## Rationale

- Follows the same `&self, id, tx` signature pattern as `fetch` and `list`
- Uses `.context()` for error wrapping, consistent with sibling methods
- Returns a domain-specific struct (`SeveritySummary`) rather than a raw tuple, consistent with how `fetch` returns `AdvisorySummary`
- Deduplication via `HashSet` ensures unique advisory counting per the acceptance criteria
- SBOM existence check mirrors the pattern in existing SBOM endpoints that return 404 for missing entities
