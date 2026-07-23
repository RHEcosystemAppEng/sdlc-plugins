# File 4: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Pre-implementation inspection

Before modifying this file, perform the following inspections:

- **`modules/fundamental/src/advisory/service/advisory.rs`** -- Use `mcp__serena_backend__get_symbols_overview` to see the full structure of `AdvisoryService` and its existing methods (`fetch`, `list`, `search`). Then use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand:
  - Method signature pattern (parameters, return type)
  - How `&self`, `Id`, and `&Transactional<'_>` are used
  - How errors are handled with `Result<T, AppError>` and `.context()`
  - How database queries are constructed using SeaORM
- **`entity/src/sbom_advisory.rs`** -- Inspect the join table entity to understand the relationship columns (sbom_id, advisory_id) needed for the query
- **`modules/fundamental/src/advisory/model/summary.rs`** -- Inspect the `AdvisorySummary` struct to understand the `severity` field type and how to extract severity values
- **`common/src/error.rs`** -- Use `mcp__serena_backend__find_symbol` to confirm `AppError` type definition and `.context()` usage
- Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers and ensure the new method does not conflict with existing usage

## Detailed changes

Add the following method to the `AdvisoryService` impl block (using `mcp__serena_backend__insert_after_symbol` after the last existing method):

```rust
/// Aggregates advisory severity counts for the specified SBOM.
///
/// Queries the sbom_advisory join table to find all advisories linked
/// to the given SBOM, deduplicates by advisory ID, and counts the
/// number of advisories at each severity level.
///
/// Returns a 404 error if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (returns 404 if not found)
    let _sbom = self
        .sbom_service
        .fetch(sbom_id.clone(), tx)
        .await
        .context("Failed to verify SBOM existence")?
        .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))?;

    // Query advisories linked to this SBOM via the join table
    let advisories = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id.clone()))
        .all(tx.connection())
        .await
        .context("Failed to query SBOM advisories")?;

    // Collect unique advisory IDs to deduplicate
    let unique_advisory_ids: HashSet<_> = advisories
        .iter()
        .map(|sa| sa.advisory_id.clone())
        .collect();

    // Fetch advisory details and count by severity
    let mut summary = SeveritySummary::default();
    for advisory_id in unique_advisory_ids {
        let advisory = self
            .fetch(advisory_id, tx)
            .await
            .context("Failed to fetch advisory details")?;

        if let Some(advisory) = advisory {
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or None severity -- not counted in specific levels but included in total
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

## Conventions followed

- Method signature matches existing methods: `&self`, entity ID, `&Transactional<'_>` parameters
- Returns `Result<T, AppError>` with `.context()` for error wrapping
- Uses SeaORM query patterns consistent with `fetch` and `list` methods
- Documentation comment on the method
- Deduplicates by advisory ID before counting (acceptance criteria)
- Defaults all counts to 0 via `SeveritySummary::default()` (acceptance criteria)
