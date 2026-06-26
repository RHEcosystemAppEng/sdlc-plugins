# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the `sbom_advisory` join table, fetches associated advisory severities, deduplicates by advisory ID, and returns aggregated counts per severity level.

## Sibling files inspected

- `modules/fundamental/src/advisory/service/advisory.rs` (current state) -- `AdvisoryService` struct with `fetch` and `list` methods. Both take `&self` and `tx: &Transactional<'_>`. `fetch` takes an `Id` parameter and returns a single entity. `list` returns paginated results.
- `modules/fundamental/src/sbom/service/sbom.rs` -- `SbomService` with `fetch`, `list`, `ingest` methods following the same signature pattern.

## Conventions applied

- Method signature follows existing pattern: `pub async fn severity_summary(&self, sbom_id: Id, tx: &Transactional<'_>) -> Result<SeveritySummary, AppError>`
- Error wrapping uses `.context("descriptive message")` matching `common/src/error.rs` pattern
- SeaORM query builder for database operations
- Deduplication via `HashSet<Id>` or SQL `DISTINCT` to count unique advisories only

## Detailed changes

Add the following method to the `impl AdvisoryService` block:

```rust
/// Returns aggregated severity counts for all advisories linked to a given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// specified SBOM, deduplicates by advisory ID, and counts advisories at each
/// severity level (Critical, High, Medium, Low).
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists first (return 404 if not found)
    // This follows the pattern used by existing SBOM endpoints
    let _sbom = SbomService::fetch(&self, sbom_id, tx)
        .await?
        .ok_or_else(|| AppError::not_found(format!("SBOM with id {} not found", sbom_id)))
        .context("fetching SBOM for severity summary")?;

    // Query sbom_advisory join table for all advisories linked to this SBOM
    let advisory_links = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .all(tx)
        .await
        .context("querying SBOM advisory links")?;

    // Collect unique advisory IDs to handle deduplication
    let mut seen_advisory_ids = HashSet::new();
    let mut summary = SeveritySummary::default();

    for link in &advisory_links {
        if !seen_advisory_ids.insert(link.advisory_id) {
            continue; // Skip duplicate advisory links
        }

        // Fetch the advisory to get its severity
        if let Some(advisory) = self.fetch(link.advisory_id, tx).await? {
            match advisory.severity.as_deref() {
                Some("Critical") | Some("critical") => summary.critical += 1,
                Some("High") | Some("high") => summary.high += 1,
                Some("Medium") | Some("medium") => summary.medium += 1,
                Some("Low") | Some("low") => summary.low += 1,
                _ => {} // Unknown or None severity -- not counted in specific levels
            }
            summary.total += 1;
        }
    }

    Ok(summary)
}
```

### Alternative implementation (optimized single query)

For better performance (acceptance criterion: under 200ms for 500 advisories), the implementation could use a single SQL query with GROUP BY instead of fetching each advisory individually:

```rust
/// Returns aggregated severity counts for all advisories linked to a given SBOM.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify SBOM exists (404 if not)
    // ... (same as above)

    // Single query: JOIN sbom_advisory with advisory, GROUP BY severity
    // using DISTINCT advisory_id for deduplication
    let counts = entity::sbom_advisory::Entity::find()
        .filter(entity::sbom_advisory::Column::SbomId.eq(sbom_id))
        .inner_join(entity::advisory::Entity)
        .select_only()
        .column(entity::advisory::Column::Severity)
        .column_as(entity::advisory::Column::Id.count_distinct(), "count")
        .group_by(entity::advisory::Column::Severity)
        .into_tuple::<(Option<String>, i64)>()
        .all(tx)
        .await
        .context("querying advisory severity counts")?;

    let mut summary = SeveritySummary::default();
    for (severity, count) in &counts {
        let count = *count as u64;
        match severity.as_deref() {
            Some("Critical") | Some("critical") => summary.critical = count,
            Some("High") | Some("high") => summary.high = count,
            Some("Medium") | Some("medium") => summary.medium = count,
            Some("Low") | Some("low") => summary.low = count,
            _ => {}
        }
        summary.total += count;
    }

    Ok(summary)
}
```

The optimized version is preferred as it satisfies the performance requirement with a single database round-trip. The exact approach would be confirmed after inspecting the actual SeaORM entity relationships and column definitions via Serena.

## Rationale

- Method signature matches existing `fetch`/`list` patterns (`&self`, `Id`, `&Transactional<'_>`)
- 404 check on SBOM existence matches the acceptance criterion and existing SBOM endpoint behavior
- Deduplication by advisory ID satisfies the "counts only unique advisories" criterion
- `SeveritySummary::default()` ensures all counts start at 0
- `.context()` wrapping on all fallible operations matches the error handling convention
