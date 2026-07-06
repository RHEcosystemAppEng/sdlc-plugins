# File 4: `modules/fundamental/src/advisory/service/advisory.rs` (MODIFY)

## Purpose

Add a `severity_summary` method to the existing `AdvisoryService` that queries
advisories linked to a given SBOM and aggregates counts by severity level.

## Detailed Changes

### New method to add

Add the following method to the `impl AdvisoryService` block, after the existing
`fetch` and `list` methods:

```rust
/// Computes aggregated advisory severity counts for the specified SBOM.
///
/// Queries the `sbom_advisory` join table to find all advisories linked to the
/// given SBOM, deduplicates by advisory ID, and returns a `SeveritySummary`
/// with counts per severity level (Critical, High, Medium, Low) and a total.
///
/// Returns an error (mapped to 404) if the SBOM does not exist.
pub async fn severity_summary(
    &self,
    sbom_id: Id,
    tx: &Transactional<'_>,
) -> Result<SeveritySummary, AppError> {
    // 1. Verify SBOM exists; return 404 if not found
    //    (follow the pattern used by existing fetch methods that check entity existence)

    // 2. Query sbom_advisory join table for all advisory IDs linked to this SBOM
    //    Use entity::sbom_advisory to build the query
    //    JOIN with entity::advisory to get the severity field

    // 3. Deduplicate by advisory ID
    //    Use SELECT DISTINCT on advisory_id or GROUP BY advisory_id

    // 4. Count by severity level
    //    Iterate results and count each severity value:
    //    "critical" -> summary.critical += 1
    //    "high"     -> summary.high += 1
    //    "medium"   -> summary.medium += 1
    //    "low"      -> summary.low += 1
    //    Increment summary.total for each unique advisory

    // 5. Return the populated SeveritySummary
    //    (all fields default to 0 via Default derive, so missing levels are already 0)

    Ok(summary)
}
```

### Implementation approach

Two viable approaches for the aggregation:

**Option A (preferred) -- Single query with GROUP BY:**
Use SeaORM to execute a single query that JOINs `sbom_advisory` with `advisory`,
filters by `sbom_id`, groups by `severity`, and counts distinct advisory IDs.
This is most efficient and handles deduplication at the database level.

```sql
SELECT a.severity, COUNT(DISTINCT sa.advisory_id) as count
FROM sbom_advisory sa
JOIN advisory a ON sa.advisory_id = a.id
WHERE sa.sbom_id = $1
GROUP BY a.severity
```

Then map the result rows into the `SeveritySummary` struct.

**Option B -- Fetch and count in Rust:**
Fetch all distinct `(advisory_id, severity)` tuples and count in application code.
Less efficient but simpler to write with SeaORM's query builder.

### Design decisions

- **Method signature matches siblings**: `fetch` and `list` both take `&self` plus
  domain-specific parameters and `tx: &Transactional<'_>`. The new method follows
  this exact pattern.
- **SBOM existence check first**: returning 404 for non-existent SBOMs matches the
  behavior of existing SBOM endpoints and satisfies acceptance criterion #2.
- **Deduplication at query level**: using `DISTINCT` or `GROUP BY` in the SQL ensures
  correctness and performance, satisfying acceptance criteria #3 and #5.
- **Error wrapping with `.context()`**: any database error is wrapped with a descriptive
  context string before propagation, matching the error handling convention.

### Conventions followed

- Method added to existing `impl AdvisoryService` block (not a separate impl).
- Method name follows `verb_noun` pattern (though `severity_summary` is a noun phrase,
  this matches the aggregation nature; alternative `get_severity_summary` is also
  acceptable).
- Return type is `Result<SeveritySummary, AppError>`.
- Uses `Transactional` for database access consistency.
- Doc comment explaining what the method does and its error behavior.
