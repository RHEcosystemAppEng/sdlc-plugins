# File 1: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Pre-implementation Inspection

Before modifying, would use Serena to understand the current state:

1. `mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")` -- see AdvisoryService struct and all its methods.
2. `mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)` -- read the `fetch` method to understand the query pattern, transactional context usage, and error handling.
3. `mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)` -- read the `list` method to see how it queries entities and returns results.
4. `mcp__serena_backend__find_referencing_symbols("AdvisoryService")` -- identify all callers to ensure no backward compatibility issues.

## Changes

### Add `severity_summary` method to `AdvisoryService`

**Location**: Inside the `impl AdvisoryService` block, after the existing methods (`fetch`, `list`, `search`).

**New method**:

```rust
/// Aggregates advisory severity counts for a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (Critical, High,
/// Medium, Low) and a total count. Advisories are deduplicated by advisory ID
/// before counting.
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
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))
        .context("looking up SBOM for severity summary")?;

    // Query the sbom_advisory join table to find all advisories linked to this SBOM,
    // then join to advisory to get severity. Use DISTINCT on advisory ID to deduplicate.
    let advisories = sbom_advisory::Entity::find()
        .filter(sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(advisory::Entity)
        .distinct_on([advisory::Column::Id])
        .all(tx.connection())
        .await
        .context("querying advisories for severity summary")?;

    // Count by severity level
    let mut summary = SeveritySummary::default();
    for (_join, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            let advisory_summary = AdvisorySummary::from(advisory);
            match advisory_summary.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or missing severity -- not counted in named buckets
            }
        }
    }
    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

### Required imports to add at the top of the file

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use entity::sbom_advisory;
use entity::advisory;
```

(Would verify which of these are already imported via Serena/Grep before adding.)

## Rationale

- Method signature follows the established `verb_noun` naming and `(&self, id: Id, tx: &Transactional<'_>)` parameter pattern from sibling methods `fetch` and `list`.
- SBOM existence check follows the pattern used in other service methods that validate entity existence before proceeding.
- Error handling uses `.context()` wrapping consistent with `common/src/error.rs` pattern.
- Deduplication via `distinct_on` satisfies acceptance criterion 3.
- Default SeveritySummary with all zeros satisfies acceptance criterion 4.
