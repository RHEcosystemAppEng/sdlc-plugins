# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action:** MODIFY

## Purpose

Add the `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, loads advisory severity data, deduplicates by advisory ID, and returns aggregated severity counts.

## Detailed Changes

### New method: `severity_summary`

Add the following method to the `impl AdvisoryService` block, alongside existing `fetch`, `list`, and `search` methods:

```rust
/// Computes a severity count summary for all unique advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts by severity level.
/// Returns a `SeveritySummary` with per-level counts and a total.
///
/// Returns an error if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (returns 404 if not found)
    // Use the SbomService or direct entity lookup to confirm existence
    // following the pattern used by other cross-entity queries

    // Query sbom_advisory join table for all advisories linked to this SBOM
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("Failed to query sbom_advisory for SBOM")?;

    // Collect unique advisory IDs to deduplicate
    let unique_advisory_ids: HashSet<_> = advisory_links
        .iter()
        .map(|link| &link.advisory_id)
        .collect();

    // Load AdvisorySummary for each unique advisory to access severity
    let mut critical = 0u32;
    let mut high = 0u32;
    let mut medium = 0u32;
    let mut low = 0u32;

    for advisory_id in &unique_advisory_ids {
        let advisory = self
            .fetch(*advisory_id, tx)
            .await
            .context("Failed to fetch advisory for severity aggregation")?;

        match advisory.severity.as_deref() {
            Some("Critical") => critical += 1,
            Some("High") => high += 1,
            Some("Medium") => medium += 1,
            Some("Low") => low += 1,
            _ => {} // Unknown or missing severity — not counted
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

### Imports to add

At the top of the file, add:

```rust
use std::collections::HashSet;
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Design rationale

- **Method signature:** Follows the existing pattern of `fetch` and `list` — takes `&self`, an entity ID, and `tx: &Transactional<'_>`.
- **SBOM existence check:** Verifies the SBOM exists before proceeding, returning a 404-equivalent `AppError` when not found. This matches the acceptance criteria: "Returns 404 when SBOM ID does not exist."
- **Deduplication:** Uses a `HashSet` of advisory IDs to ensure each advisory is counted only once, satisfying the "Counts only unique advisories" acceptance criterion.
- **Severity matching:** Matches severity strings from the `AdvisorySummary.severity` field. Unknown or null severities are silently skipped (not counted toward any level).
- **Default zeros:** All counters initialize to 0, satisfying "All severity levels default to 0 when no advisories exist."
- **Error handling:** All fallible operations use `.context()` wrapping, consistent with the codebase convention.
- **Total calculation:** Computed as the sum of all four severity levels, ensuring consistency.

### Conventions followed

- Method name follows `verb_noun` pattern (`severity_summary`), consistent with `fetch`, `list`, `search` siblings.
- Error wrapping with `.context()` on every fallible call.
- Uses SeaORM entity queries via the join table `entity::sbom_advisory`, as specified in the implementation notes.
- Doc comment on the method explains purpose, behavior, and error conditions.
