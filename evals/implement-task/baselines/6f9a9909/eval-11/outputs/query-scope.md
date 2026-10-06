# Query-Scope Verification Analysis for TC-9209

## What the Task Targets

The task description specifies: "re-processes **all SPDX SBOMs** to extract package supplier
information." The key subset-restricting language is:

- "all SPDX SBOMs" -- targets only SPDX-type documents, not all SBOMs
- "Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier
  information populated during ingestion" -- explicitly excludes CycloneDX
- "Production environments have hundreds of thousands of CycloneDX documents alongside
  a smaller number of SPDX documents" -- reinforces that SPDX is a small subset

The target scope is therefore: **SPDX SBOMs only**, which is a subset of all SBOM
records in the database.

## Available Filtering Mechanism

The task's Implementation Notes document the filtering mechanism:

> The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that
> stores metadata about each document. SPDX documents have `{"type": "spdx"}` in their
> labels, while CycloneDX documents have `{"type": "cyclonedx"}`.

This means the database supports filtering at the query level using:

```sql
WHERE labels->>'type' = 'spdx'
```

## Query Scope Chosen

**Filtered query** -- the migration queries only SPDX SBOMs by filtering on the
`labels` jsonb column at the database level:

```rust
Sbom::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(db)
    .await?
```

This translates to the SQL:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx';
```

## Why This Scope

### Correctness

The task explicitly states that only SPDX SBOMs need re-processing. CycloneDX documents
already have supplier information populated during ingestion. A filtered query ensures:

1. Only SPDX documents are loaded and processed (matching the task's target scope).
2. CycloneDX documents are never loaded, parsed, or updated -- satisfying the acceptance
   criterion "CycloneDX documents are not loaded or processed by the migration."

### Performance

The task warns that production has "hundreds of thousands of CycloneDX documents alongside
a smaller number of SPDX documents." An unfiltered query (`Sbom::find().all(db)`) would:

- **Fetch** hundreds of thousands of unnecessary rows from the database.
- **Transfer** those rows over the database connection, consuming network and memory.
- **Allocate** Rust structs for each record, only to discard them during application-level
  filtering.
- **Extend** migration runtime by orders of magnitude compared to a filtered query.

By filtering at the database level, the migration avoids all of this unnecessary I/O.
The database engine can use indexes (if available on `labels->>'type'`) to efficiently
locate only the SPDX records.

### Alternative Considered and Rejected

An alternative approach would be to load all SBOMs and filter in application code:

```rust
// NOT recommended
let all_sboms = Sbom::find().all(db).await?;
let spdx_sboms: Vec<_> = all_sboms.into_iter()
    .filter(|s| s.labels.get("type") == Some("spdx"))
    .collect();
```

This was rejected because:
- The `labels->>'type'` filter is expressible at the query level (it is a standard
  PostgreSQL jsonb operator supported by SeaORM's `Expr::cust()`).
- Loading hundreds of thousands of records to discard them is wasteful when the
  database can perform the filtering far more efficiently.
- The SKILL.md's query-scope verification step (Step 9) explicitly flags this pattern:
  "if the task targets a subset but a narrower query is possible at the data source
  (via columns, indexes, ORM scopes, or API parameters), flag for review."

## Summary

| Dimension | Value |
|-----------|-------|
| **Target scope** | All SPDX SBOMs (subset of all SBOMs) |
| **Query scope** | Filtered: `labels->>'type' = 'spdx'` |
| **Scope match** | Yes -- query scope matches target scope exactly |
| **Filter mechanism** | PostgreSQL jsonb operator on `labels` column |
| **Performance impact** | Avoids loading hundreds of thousands of CycloneDX records |
| **Correctness impact** | Ensures CycloneDX documents are never touched by the migration |
