# File 3: Modify `modules/fundamental/src/advisory/service/advisory.rs`

## Action: MODIFY

## Purpose

Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Detailed Changes

Add a new method to the `AdvisoryService` impl block, following the same signature pattern as existing `fetch` and `list` methods:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;

impl AdvisoryService {
    // ... existing methods (fetch, list, search) ...

    /// Aggregates advisory severity counts for a given SBOM.
    ///
    /// Queries the `sbom_advisory` join table for all advisories linked to the
    /// specified SBOM, deduplicates by advisory ID, and counts advisories per
    /// severity level (Critical, High, Medium, Low).
    ///
    /// Returns a `SeveritySummary` with zero counts if the SBOM has no advisories.
    /// Returns `AppError` with 404 if the SBOM ID does not exist.
    pub async fn severity_summary(
        &self,
        sbom_id: Id,
        tx: &Transactional<'_>,
    ) -> Result<SeveritySummary, AppError> {
        // Given: verify the SBOM exists (return 404 if not found)
        // Use existing SBOM lookup pattern to confirm the SBOM ID is valid.
        // If the SBOM does not exist, return a 404 error consistent with
        // existing SBOM endpoint behavior.

        // When: query sbom_advisory join table for advisories linked to this SBOM
        // Use SeaORM to query entity::sbom_advisory with a filter on sbom_id.
        // For each linked advisory, load the AdvisorySummary to access the
        // severity field.

        // Deduplicate by advisory ID using a HashSet to ensure unique counts
        let mut seen_ids = HashSet::new();
        let mut summary = SeveritySummary::default();

        // Iterate over linked advisories, skipping duplicates
        for advisory in linked_advisories {
            if !seen_ids.insert(advisory.id) {
                continue; // Skip duplicate advisory
            }

            // Count by severity level
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown severity levels are not counted
            }
        }

        summary.total = summary.critical + summary.high + summary.medium + summary.low;

        Ok(summary)
    }
}
```

## Key Implementation Details

1. **SBOM existence check**: before querying advisories, verify the SBOM exists. If not, return `AppError` with appropriate 404 context wrapping, matching existing patterns (e.g., `"SBOM not found".context(...)`).

2. **Join table query**: use `entity::sbom_advisory::Entity::find()` with a filter on `sbom_id` to get all advisory links for the given SBOM. Then load each advisory's `AdvisorySummary` to access the `severity` field.

3. **Deduplication**: use `HashSet<Id>` to track seen advisory IDs and skip duplicates in the count. This satisfies the acceptance criterion "Counts only unique advisories (deduplicates by advisory ID)."

4. **Severity matching**: match on severity string values. Use case-insensitive matching or match both capitalized and lowercase variants to be robust.

5. **Default zeros**: `SeveritySummary::default()` initializes all counts to 0 (via `#[derive(Default)]` on `u32` fields), satisfying the acceptance criterion "All severity levels default to 0 when no advisories exist."

## Conventions Applied

- **Method signature**: follows `&self, <entity_id>: Id, tx: &Transactional<'_>` pattern from existing `fetch` and `list` methods.
- **Error handling**: returns `Result<T, AppError>` with `.context()` wrapping.
- **Service method naming**: follows `verb_noun` convention (though `severity_summary` is noun-noun, it matches the domain concept and is consistent with how the endpoint is named).
