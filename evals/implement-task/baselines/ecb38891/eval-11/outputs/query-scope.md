# Query-Scope Verification Analysis for TC-9209

## Target Scope Extraction

The task Description section contains explicit subset-restricting language:

- **"Re-processes all SPDX SBOMs"** -- the qualifier "SPDX" restricts the target scope to a specific document type, not all SBOMs.
- **"Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier information populated during ingestion."** -- this sentence explicitly excludes CycloneDX documents from the migration scope.

The target scope is therefore: **SPDX SBOMs only**, which is a strict subset of all SBOM records in the database.

## Available Filtering Mechanism

The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores metadata about each document. According to the Implementation Notes:

- SPDX documents have `{"type": "spdx"}` in their labels
- CycloneDX documents have `{"type": "cyclonedx"}` in their labels

This means the `labels` column supports **database-level filtering by document type**. A query can filter directly using a jsonb operator such as `labels->>'type' = 'spdx'` (or the SeaORM equivalent) to select only SPDX documents at the SQL level, without requiring application-level filtering.

## Query Scope Decision

**Chosen approach: Filtered query at the database level.**

The migration query must use a filtered query that selects only SPDX documents:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx'
```

In SeaORM, this translates to a condition on the `labels` column using a JSON path expression, e.g.:

```rust
use sea_orm::prelude::*;
use entity::sbom;

sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(&db)
    .await?
```

This ensures only SPDX records are loaded from the database.

## Rejected Approach: Unfiltered Query

An unfiltered query such as `Sbom::find().all(&db)` or `sbom::Entity::find().all(&db)` followed by an application-level type check (e.g., `.filter(|s| s.labels["type"] == "spdx")`) is explicitly rejected for the following reasons:

### Performance Impact

Production environments have **hundreds of thousands of CycloneDX documents** alongside a smaller number of SPDX documents. Loading all SBOM records indiscriminately would:

1. **Unnecessary I/O**: Fetch hundreds of thousands of CycloneDX records from PostgreSQL that will be immediately discarded, consuming significant database bandwidth and memory.
2. **Memory pressure**: Materializing hundreds of thousands of ORM entity instances in application memory, only to discard the vast majority, creates unnecessary memory pressure and risks OOM conditions during migration.
3. **Database load**: The unfiltered query forces PostgreSQL to read and transfer far more rows than needed, increasing lock contention and I/O wait times during the migration window.
4. **Migration duration**: Processing time scales linearly with the number of records loaded. An unfiltered query would make the migration take orders of magnitude longer than necessary.

The `labels` column's jsonb type supports the `->>'type'` operator natively in PostgreSQL, making the filtered query both possible and efficient. There is no technical reason to use an unfiltered query when database-level filtering is available.

## Summary

| Aspect | Value |
|---|---|
| Target scope | SPDX SBOMs only (subset of all SBOMs) |
| Subset indicator | "all SPDX SBOMs", "Only SPDX SBOMs need re-processing" |
| Filter mechanism | `labels` column (jsonb) with `->>'type' = 'spdx'` |
| Filter level | Database-level (SQL WHERE clause), not application-level |
| Rejected approach | `Sbom::find()` / unfiltered query + application-level discard |
| Rejection reason | Performance: hundreds of thousands of non-target CycloneDX records in production |
