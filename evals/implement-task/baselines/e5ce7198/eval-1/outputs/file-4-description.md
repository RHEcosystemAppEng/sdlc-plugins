# File 4: modules/fundamental/src/advisory/service/advisory.rs

**Action**: MODIFY

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that queries the database for all advisories linked to a given SBOM, deduplicates them by advisory ID, counts severities, and returns a `SeveritySummary` struct.

## Pre-Modification Inspection

Before making changes, inspect via Serena:
1. `mcp__serena_backend__get_symbols_overview` on the file to see all existing methods
2. `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` and `list` methods to understand their signature pattern (especially how they take `&self`, ID, and transactional context)
3. `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to identify all callers (ensure no backward compatibility issues)

## Detailed Changes

### Add import for SeveritySummary

At the top of the file, add:
```rust
use crate::advisory::model::severity_summary::SeveritySummary;
```

Also add any needed imports for the `sbom_advisory` entity and `HashSet` for deduplication.

### Add `severity_summary` method

Add a new public async method to the `AdvisoryService` impl block, following the pattern of existing `fetch` and `list` methods:

```rust
/// Computes aggregated severity counts for all unique advisories linked to a given SBOM.
///
/// Returns a `SeveritySummary` with counts per severity level (critical, high, medium, low)
/// and a total. Returns a 404 error if the SBOM ID does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists (return 404 if not)
    //    Follow the pattern used in sibling service methods for existence checks

    // 2. Query sbom_advisory join table for all advisory IDs linked to this SBOM
    //    Use SeaORM query builder, following patterns in existing service methods

    // 3. Deduplicate advisory IDs using a HashSet
    //    This satisfies acceptance criterion: "Counts only unique advisories"

    // 4. For each unique advisory, fetch its AdvisorySummary to get the severity field
    //    Or: use a single query joining sbom_advisory -> advisory with GROUP BY severity

    // 5. Count by severity level, building the SeveritySummary struct
    let mut summary = SeveritySummary::default();
    // Iterate and match severity levels, incrementing appropriate counter
    // Increment total for each unique advisory

    Ok(summary)
}
```

### Design Decisions

- **Method signature**: matches existing `fetch` and `list` patterns -- takes `&self`, entity ID, and `&Transactional<'_>` for database context
- **SBOM existence check**: returns 404 via AppError when SBOM doesn't exist, consistent with sibling SBOM endpoints (acceptance criterion #2)
- **Deduplication**: uses HashSet or DISTINCT in query to ensure each advisory is counted once (acceptance criterion #3)
- **Default zeros**: `SeveritySummary::default()` initializes all counts to 0 (acceptance criterion #4)
- **Error wrapping**: uses `.context()` on all fallible operations, matching the established pattern
- **Performance**: consider using a single aggregation query with GROUP BY instead of N+1 queries, to meet the 200ms performance requirement for 500 advisories

### Convention Compliance

- Method follows verb_noun naming: `severity_summary`
- Error handling uses `Result<T, AppError>` with `.context()`
- Doc comment on the method explaining purpose and error behavior
- Method placed within the existing `impl AdvisoryService` block alongside `fetch`, `list`, `search`
