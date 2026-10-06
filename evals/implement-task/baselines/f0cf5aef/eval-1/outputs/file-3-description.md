# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` struct that
queries and aggregates advisory severity counts for a given SBOM.

## Pre-implementation inspection

Before modifying, inspect the existing service:
```
mcp__serena_backend__get_symbols_overview("modules/fundamental/src/advisory/service/advisory.rs")
mcp__serena_backend__find_symbol("AdvisoryService::fetch", include_body=true)
mcp__serena_backend__find_symbol("AdvisoryService::list", include_body=true)
```

Also inspect the join table entity and the severity field:
```
mcp__serena_backend__get_symbols_overview("entity/src/sbom_advisory.rs")
mcp__serena_backend__find_symbol("AdvisorySummary", include_body=true)
```

Check that `AdvisorySummary` in `model/summary.rs` has a `severity` field and
understand its type (likely a `String` or an enum).

Check backward compatibility:
```
mcp__serena_backend__find_referencing_symbols("AdvisoryService")
```

## Changes

Add a new `pub async fn severity_summary` method to the `impl AdvisoryService` block.
Use `mcp__serena_backend__insert_after_symbol` to add it after the last existing method,
or use Edit as fallback.

### Method signature

```rust
/// Computes aggregated advisory severity counts for the specified SBOM.
///
/// Queries all advisories linked to the SBOM via the `sbom_advisory` join table,
/// deduplicates by advisory ID, and returns counts grouped by severity level.
/// Returns a `SeveritySummary` with all counts defaulting to zero when no
/// advisories exist at a given severity level.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
```

### Method body (conceptual)

```rust
    // Verify the SBOM exists, return 404 if not found
    // (follow the pattern from fetch -- check entity existence first)
    
    // Query sbom_advisory join table for all advisory IDs linked to this SBOM
    // Join with advisory table to get severity field
    // Use .distinct() or equivalent to deduplicate by advisory ID
    
    // Initialize SeveritySummary with Default (all zeros)
    let mut summary = SeveritySummary::default();
    
    // Iterate results, match on severity level, increment counters
    for advisory in advisories {
        match advisory.severity.as_deref().unwrap_or_default() {
            "critical" | "Critical" => summary.critical += 1,
            "high" | "High" => summary.high += 1,
            "medium" | "Medium" => summary.medium += 1,
            "low" | "Low" => summary.low += 1,
            _ => {} // Unknown severities are not counted
        }
    }
    
    summary.total = summary.critical + summary.high + summary.medium + summary.low;
    
    Ok(summary)
```

### Required imports

Add to the file's imports:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

## Design decisions

- **SBOM existence check**: Return 404 when SBOM ID does not exist, matching AC requirement and existing SBOM endpoint behavior. Follow the pattern used in `fetch` for entity-not-found errors.
- **Deduplication**: Use `.distinct()` on advisory ID in the query, or collect into a `HashSet<Id>` if deduplication must happen in Rust. This satisfies AC "Counts only unique advisories."
- **Defensive property access**: Use `.unwrap_or_default()` on the severity field in case it is `Option<String>` -- guards against null severity values from the database.
- **Case-insensitive matching**: Match both capitalized and lowercase severity strings to handle inconsistent data.
- **Performance**: Single query with join satisfies AC "Response time under 200ms for SBOMs with up to 500 advisories." The indexed join table ensures efficient lookup.

## Convention conformance

- Method signature matches sibling pattern: `&self, id: Id, tx: &Transactional<'_>` parameters
- Return type `Result<T, AppError>` matches all existing service methods
- Error wrapping with `.context()` matches existing error handling strategy
- Doc comment on public method per skill guidance
