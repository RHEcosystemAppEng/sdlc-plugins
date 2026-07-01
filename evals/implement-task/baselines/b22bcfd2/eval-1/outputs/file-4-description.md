# File 4: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to `AdvisoryService` that queries the database for advisory severity counts linked to a given SBOM.

## Pre-Implementation Inspection

- `mcp__serena_backend__get_symbols_overview` on `modules/fundamental/src/advisory/service/advisory.rs` to see full structure of `AdvisoryService`
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::fetch` to understand method signature, query pattern, and error handling
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisoryService::list` to understand list/aggregation query pattern
- `mcp__serena_backend__find_symbol` with `include_body=true` on `AdvisorySummary` in `model/summary.rs` to see the `severity` field type
- Read `entity/src/sbom_advisory.rs` to understand the join table schema (columns, relations)
- `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all existing callers and ensure the new method does not conflict

## Detailed Changes

Add a new method `severity_summary` to the `AdvisoryService` impl block:

```rust
/// Aggregates advisory severity counts for advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories associated with
/// the specified SBOM ID, deduplicates by advisory ID, reads each advisory's
/// severity level, and returns a `SeveritySummary` with per-level counts and a total.
///
/// Returns an error mapped to 404 if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, anyhow::Error> {
    // First verify the SBOM exists (return 404 if not)
    // Use existing SBOM lookup pattern from sbom service

    // Query sbom_advisory join table for all advisories linked to this SBOM
    // Join with advisory table to get severity field
    // Use DISTINCT on advisory ID to deduplicate

    // Initialize SeveritySummary with defaults (all zeros)
    let mut summary = SeveritySummary::default();

    // Iterate over unique advisories and count by severity level
    for advisory in advisories {
        match advisory.severity.as_deref() {
            Some("Critical") | Some("critical") => summary.critical += 1,
            Some("High") | Some("high") => summary.high += 1,
            Some("Medium") | Some("medium") => summary.medium += 1,
            Some("Low") | Some("low") => summary.low += 1,
            _ => {} // Unknown or None severity -- do not count
        }
    }

    summary.total = summary.critical + summary.high + summary.medium + summary.low;

    Ok(summary)
}
```

## Notes

- Method signature follows the existing pattern: `&self`, primary ID, and `&Transactional<'_>`
- The SBOM existence check ensures 404 is returned for non-existent SBOMs (acceptance criterion)
- Deduplication by advisory ID satisfies acceptance criterion "Counts only unique advisories"
- `SeveritySummary::default()` gives all zeros, satisfying "All severity levels default to 0"
- The exact query construction (SeaORM entities, joins, selects) will be determined by inspecting `entity/src/sbom_advisory.rs` and the existing `fetch`/`list` patterns
- The severity string matching pattern will be confirmed by inspecting the `severity` field type in `AdvisorySummary`
- Consider using a single SQL query with GROUP BY for performance (acceptance criterion: under 200ms for 500 advisories) rather than loading all advisories into memory
- Import `SeveritySummary` from `crate::advisory::model::severity_summary::SeveritySummary`
