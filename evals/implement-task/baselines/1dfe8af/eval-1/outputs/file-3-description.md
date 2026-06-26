# File 3: modules/fundamental/src/advisory/service/advisory.rs (MODIFY)

## Purpose
Add a `severity_summary` method to `AdvisoryService` that aggregates advisory severity counts for a given SBOM.

## Pre-implementation inspection
- Use `mcp__serena_backend__get_symbols_overview` on this file to see the full structure of `AdvisoryService`.
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `fetch` method to understand the exact pattern: parameter types, return type, transaction handling, error wrapping.
- Use `mcp__serena_backend__find_symbol` with `include_body=true` on the `list` method as a second reference point.
- Read `entity/src/sbom_advisory.rs` to understand the join table structure (columns for sbom_id, advisory_id).
- Read `modules/fundamental/src/advisory/model/summary.rs` to confirm `AdvisorySummary` has a `severity` field and understand its type.
- Use `mcp__serena_backend__find_referencing_symbols` on `AdvisoryService` to confirm no trait impl or interface contract is being broken by adding a new method.

## Detailed Changes

### New method: `severity_summary`

Add a new method to the `impl AdvisoryService` block:

```rust
/// Compute aggregated severity counts for all advisories linked to the given SBOM.
///
/// Queries the `sbom_advisory` join table to find advisories associated with the
/// SBOM, deduplicates by advisory ID, and counts each severity level. Returns a
/// `SeveritySummary` with counts for critical, high, medium, low, and total.
///
/// Returns `AppError` with 404 status if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // Verify the SBOM exists (return 404 if not found)
    // Follow the pattern from fetch() for existence checking.
    // e.g., SbomService::fetch(sbom_id, tx).await?.ok_or_else(|| ...)?;

    // Query sbom_advisory join table for advisories linked to this SBOM
    // Use the entity::sbom_advisory module for the join
    // Apply DISTINCT on advisory_id to deduplicate

    // For each linked advisory, retrieve the severity from AdvisorySummary
    // Count by severity level (Critical, High, Medium, Low)

    // Build and return SeveritySummary
    let mut summary = SeveritySummary::default();
    // ... populate counts ...
    summary.total = summary.critical + summary.high + summary.medium + summary.low;
    Ok(summary)
}
```

### Implementation approach

Two possible approaches (would be decided after reading the actual code):

**Approach A -- Single SQL query with GROUP BY** (preferred for performance):
- JOIN `sbom_advisory` with `advisory` table
- Filter by `sbom_id`
- SELECT DISTINCT advisory_id to deduplicate
- GROUP BY severity, COUNT(*)
- Map results to SeveritySummary fields

**Approach B -- In-memory aggregation** (if SeaORM patterns in siblings favor this):
- Fetch all advisory summaries linked to the SBOM via `sbom_advisory`
- Collect unique advisory IDs using a HashSet
- Count severity levels in a loop
- Build SeveritySummary

The approach choice depends on what sibling methods (`fetch`, `list`) do -- follow their query pattern.

### Error handling
- SBOM not found: return 404 via `AppError` with `.context("SBOM not found")` or equivalent, matching existing 404 patterns in sibling endpoints.
- Database errors: wrapped with `.context()` matching the pattern in `common/src/error.rs`.

### Conventions followed
- Method signature matches siblings: `&self`, domain-specific params, `tx: &Transactional<'_>`.
- Return type is `Result<SeveritySummary, AppError>`.
- Error handling uses `.context()` wrapping.
- Doc comment on the method explaining purpose, behavior, and error conditions.
- Method name follows `verb_noun` pattern (though `severity_summary` is noun-noun, which may match a getter pattern if siblings use that -- would confirm from sibling analysis).
