# File 4: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct. This method queries the `sbom_advisory` join table to find all advisories linked to a given SBOM, fetches their severity values, deduplicates by advisory ID, counts occurrences per severity level, and returns a `SeveritySummary`.

## Sibling Reference

- Existing `fetch` method in `AdvisoryService` — pattern for ID lookup, transaction usage, and 404 error handling
- Existing `list` method in `AdvisoryService` — pattern for querying multiple records with joins
- `entity/src/sbom_advisory.rs` — join table entity for SBOM-to-advisory relationships
- `modules/fundamental/src/advisory/model/summary.rs` — `AdvisorySummary` struct with `severity` field used for counting

## Changes

### 1. Add import for the new model

At the top of the file, alongside existing model imports, add:

```rust
use crate::advisory::model::severity_summary::SeveritySummary;
use std::collections::HashSet;
```

### 2. Add `severity_summary` method to `impl AdvisoryService`

Insert the following method inside the existing `impl AdvisoryService` block, after the existing `list` or `search` method:

```rust
/// Aggregate advisory severity counts for a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (Critical, High,
/// Medium, Low) and a total. Advisories are deduplicated by advisory ID.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify the SBOM exists; return 404 if not found.
    //    (Follow the pattern used in fetch() for entity existence checks)
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("verifying SBOM existence for severity summary")?
        .ok_or_else(|| AppError::NotFound("SBOM not found".into()))?;

    // 2. Query sbom_advisory join table for all advisory IDs linked to this SBOM.
    //    Then fetch the corresponding advisory records to access severity.
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .find_also_related(entity::advisory::Entity)
        .all(&self.db.connection(&tx))
        .await
        .context("querying advisories for SBOM")?;

    // 3. Deduplicate by advisory ID and count by severity level.
    let mut seen = HashSet::new();
    let mut critical: i64 = 0;
    let mut high: i64 = 0;
    let mut medium: i64 = 0;
    let mut low: i64 = 0;

    for (_sbom_advisory, advisory_opt) in &advisories {
        if let Some(advisory) = advisory_opt {
            if seen.insert(advisory.id.clone()) {
                match advisory.severity.as_deref() {
                    Some("Critical") | Some("critical") => critical += 1,
                    Some("High") | Some("high") => high += 1,
                    Some("Medium") | Some("medium") => medium += 1,
                    Some("Low") | Some("low") => low += 1,
                    _ => {} // Unknown or None severity — not counted
                }
            }
        }
    }

    Ok(SeveritySummary::new(critical, high, medium, low))
}
```

## Conventions Followed

- Method signature matches existing service methods: `&self`, entity ID, `Transactional<'_>`
- Returns `Result<T, AppError>` — consistent with all service methods
- `.context()` wrapping on every `?` propagation — matches error handling convention
- SBOM existence check follows the fetch-then-404 pattern from existing code
- Deduplication via `HashSet` on advisory ID — ensures unique counts
- Case-insensitive severity matching via explicit match arms — defensive against data inconsistencies
- Doc comment on the method — matches existing method documentation style

## Notes

- The exact entity field for severity (`advisory.severity`) and its type (`Option<String>`) should be confirmed by inspecting `entity/src/advisory.rs` and `modules/fundamental/src/advisory/model/summary.rs` during pre-implementation analysis
- If `AdvisorySummary` provides a higher-level accessor for severity, that should be used instead of raw entity field access
- The `sbom_service` field name assumes `AdvisoryService` holds a reference to `SbomService` for cross-module lookups; if not, the SBOM existence check would query the SBOM entity directly via SeaORM
- The query approach (single join query + in-memory deduplication/counting) avoids N+1 queries and meets performance requirements
