# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity
counts for a given SBOM.

## Current State

`AdvisoryService` has existing methods: `fetch`, `list`, `search`. Each method takes
`&self`, relevant parameters, and `tx: &Transactional<'_>`, and returns
`Result<T, AppError>`.

## Changes

Add the following method to the `impl AdvisoryService` block:

```rust
/// Aggregates advisory severity counts for the given SBOM.
///
/// Queries advisories linked to the SBOM via the `sbom_advisory` join table,
/// deduplicates by advisory ID, and counts per severity level. Returns a
/// `SeveritySummary` with counts for Critical, High, Medium, Low, and total.
///
/// Returns `AppError` (404) if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify SBOM exists; return 404 if not found
    // (follow the pattern used by fetch/list for SBOM existence checks)

    // Query sbom_advisory join table filtered by sbom_id
    // Join with advisory table to get severity field
    // Use DISTINCT on advisory ID to deduplicate
    // Group results and count per severity level

    // Build SeveritySummary from query results
    let mut summary = SeveritySummary::default();

    // For each advisory linked to the SBOM:
    //   match severity {
    //       "critical" => summary.critical += 1,
    //       "high"     => summary.high += 1,
    //       "medium"   => summary.medium += 1,
    //       "low"      => summary.low += 1,
    //       _          => {} // unknown severity levels are excluded from counts
    //   }
    //   summary.total += 1;

    Ok(summary)
}
```

## Implementation Details

### SBOM Existence Check

Before querying advisories, verify the SBOM exists. Follow the pattern used by existing
service methods (e.g., `SbomService::fetch`). If the SBOM is not found, return an
`AppError` that maps to HTTP 404, using `.context()` wrapping:

```rust
let _sbom = SbomService::fetch(&self, sbom_id, tx)
    .await?
    .ok_or_else(|| AppError::not_found(format!("SBOM {} not found", sbom_id)))
    .context("checking SBOM existence")?;
```

### Advisory Query

Use the `sbom_advisory` join table (defined in `entity/src/sbom_advisory.rs`) to find
advisories linked to the SBOM:

```rust
// Pseudo-query using SeaORM:
// SELECT DISTINCT advisory.id, advisory.severity
// FROM sbom_advisory
// JOIN advisory ON sbom_advisory.advisory_id = advisory.id
// WHERE sbom_advisory.sbom_id = $sbom_id
```

The key detail is deduplication by advisory ID -- the same advisory may be linked to
an SBOM through multiple paths (e.g., multiple affected packages). Using `DISTINCT`
or collecting into a `HashSet<advisory_id>` ensures each advisory is counted once.

### Severity Counting

The `AdvisorySummary` struct (in `model/summary.rs`) has a `severity` field. After
fetching the distinct advisories, iterate and match the severity string to increment
the appropriate counter. Case-insensitive matching is recommended since upstream data
may vary.

### Performance

For SBOMs with up to 500 advisories, a single SQL query with JOIN + DISTINCT + GROUP BY
should complete well under 200ms. Alternatively, fetching distinct advisories and counting
in application code is acceptable for this scale.

## Conventions Applied

- Method signature: `&self, id: Id, tx: &Transactional<'_>` matching `fetch` and `list`
- Return type: `Result<T, AppError>` with `.context()` wrapping
- Method naming: `severity_summary` following `verb_noun` / descriptive noun pattern
- Doc comment with `///` explaining purpose, parameters, and error behavior
