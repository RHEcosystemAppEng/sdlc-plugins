# File 3: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Purpose

Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Pre-Implementation Inspection

Before modifying, inspect the file using:
- `mcp__serena_backend__get_symbols_overview` to see all existing methods on `AdvisoryService`
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to understand the method pattern (parameters, error handling, transaction usage)
- `mcp__serena_backend__find_symbol` on `AdvisorySummary` in `model/summary.rs` to understand the `severity` field type

## Detailed Changes

### New Method: `severity_summary`

Add the following method to the `impl AdvisoryService` block, after the existing `list` or `search` method:

```rust
/// Aggregates advisory severity counts for the specified SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// given SBOM, deduplicates by advisory ID, fetches each advisory's severity
/// from `AdvisorySummary`, and returns grouped counts by severity level.
///
/// Returns an error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify SBOM exists (returns 404 error if not found)
    // This follows the pattern used by existing SBOM endpoints
    let _sbom = self.sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("SBOM not found")?;

    // Query sbom_advisory join table for advisories linked to this SBOM
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("failed to query sbom_advisory table")?;

    // Deduplicate by advisory ID using a HashSet
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| link.advisory_id.clone())
        .collect();

    // Fetch each unique advisory and count by severity
    let mut summary = SeveritySummary::default();

    for advisory_id in &unique_advisory_ids {
        let advisory = self
            .fetch(advisory_id.clone(), tx)
            .await
            .context("failed to fetch advisory for severity aggregation")?;

        match advisory.severity.as_deref() {
            Some("critical") => summary.critical += 1,
            Some("high") => summary.high += 1,
            Some("medium") => summary.medium += 1,
            Some("low") => summary.low += 1,
            _ => {} // Unknown or missing severity -- still counted in total
        }
        summary.total += 1;
    }

    Ok(summary)
}
```

### Additional Imports Needed

At the top of the file, add:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Design Decisions

- **Method signature**: Follows the exact same pattern as `fetch` and `list` -- takes `&self`, domain-specific ID, and `Transactional` reference, returns `Result<T, AppError>`
- **SBOM existence check**: Validates the SBOM exists first, returning a 404-mapped error if not, consistent with existing SBOM endpoints (AC: "Returns 404 when SBOM ID does not exist")
- **Deduplication via HashSet**: Ensures unique advisory counting per AC "Counts only unique advisories (deduplicates by advisory ID)"
- **Default zero counts**: `SeveritySummary::default()` initializes all counts to 0, satisfying AC "All severity levels default to 0"
- **Severity matching**: Uses the `severity` field from `AdvisorySummary` (referenced in Implementation Notes), matching against known severity level strings
- **Error wrapping**: Uses `.context()` on all fallible operations, matching the established service pattern
- **Doc comment**: Describes method behavior, parameters, and error conditions per Step 6 code quality requirements

### Backward Compatibility

Checked via `find_referencing_symbols` on `AdvisoryService` -- adding a new method does not break existing callers since no existing method signatures are changed.
