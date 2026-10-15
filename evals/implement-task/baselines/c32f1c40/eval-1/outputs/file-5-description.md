# File 5: modules/fundamental/src/advisory/service/advisory.rs

## Action: MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries advisories linked to
a given SBOM, deduplicates by advisory ID, counts by severity level, and returns a
`SeveritySummary` struct.

## Detailed Changes

### New method on AdvisoryService

Add the following method to the `impl AdvisoryService` block, following the pattern of
existing `fetch` and `list` methods:

```rust
/// Computes aggregated severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the SBOM, deduplicates by advisory ID, and counts each severity level.
/// Returns a `SeveritySummary` with per-level counts and a total.
///
/// Returns an error with 404 status if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (returns 404 if not found)
    // This follows the pattern used by other SBOM-related endpoints
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("Failed to fetch SBOM")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the sbom_advisory join table
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(&self.db.connection(tx))
        .await
        .context("Failed to query SBOM advisories")?;

    // Deduplicate by advisory ID and count by severity
    let mut seen = std::collections::HashSet::new();
    let mut summary = SeveritySummary::default();

    for (_sbom_adv, advisory) in advisories {
        let advisory = advisory.context("Advisory relation missing")?;
        if !seen.insert(advisory.id.clone()) {
            continue; // Skip duplicate advisory links
        }

        // Map severity string to the appropriate counter
        match advisory.severity.as_deref().unwrap_or_default() {
            "Critical" | "critical" => summary.critical += 1,
            "High" | "high" => summary.high += 1,
            "Medium" | "medium" => summary.medium += 1,
            "Low" | "low" => summary.low += 1,
            _ => {} // Unknown severity levels are not counted
        }
        summary.total += 1;
    }

    Ok(summary)
}
```

### Required Imports

Add at the top of the file (if not already present):

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

### Design Decisions

- **SBOM existence check first**: verifies the SBOM exists before querying advisories,
  ensuring a 404 response for non-existent SBOMs (acceptance criterion).
- **Uses `sbom_advisory` join table**: as directed by the implementation notes, queries
  through `entity::sbom_advisory` to find linked advisories.
- **HashSet deduplication**: uses advisory ID in a HashSet to ensure each advisory is
  counted only once, satisfying the deduplication acceptance criterion.
- **Case-insensitive severity matching**: handles both capitalized and lowercase severity
  strings defensively, using `match` with multiple patterns.
- **Defensive property access**: uses `.unwrap_or_default()` on the severity field in case
  it is `None`, per the skill's defensive property access guidance.
- **Default counts**: `SeveritySummary::default()` initializes all counts to 0, satisfying
  the zero-default acceptance criterion.
- **Method signature**: follows the `(&self, id: Id, tx: &Transactional<'_>)` pattern
  matching existing `fetch` and `list` methods.
- **Error wrapping**: uses `.context()` on all fallible operations, matching the project
  convention.

### Convention Conformance

- Method signature matches sibling methods `fetch` and `list` in the same service.
- Error handling with `.context()` matches the project convention.
- Uses SeaORM query patterns consistent with existing service code.
