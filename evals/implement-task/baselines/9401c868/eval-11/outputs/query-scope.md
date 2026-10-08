# Query-Scope Verification Analysis for TC-9209

## What the Task Targets

The task description states:

> "Create a data migration that re-processes **all SPDX SBOMs** to extract package supplier
> information that was previously ignored during ingestion."

And explicitly:

> "**Only SPDX SBOMs** need re-processing -- CycloneDX documents already have supplier
> information populated during ingestion."

The target scope is **SPDX SBOMs only** -- a strict subset of all SBOM documents in the
database. CycloneDX documents are explicitly excluded.

## Available Filter Mechanism

The task's Implementation Notes document the filtering mechanism:

> "The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores
> metadata about each document. SPDX documents have `{"type": "spdx"}` in their labels,
> while CycloneDX documents have `{"type": "cyclonedx"}`."

This means the `labels` jsonb column on the `sbom` table directly supports filtering by
document type at the database query level using:

```sql
labels->>'type' = 'spdx'
```

## Query Scope Chosen: Filtered

The migration must use a **filtered query** that selects only SPDX SBOMs:

```rust
sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(db)
    .await?
```

This filters at the database level, ensuring only SPDX documents are loaded into memory
and processed.

## Why an Unfiltered Query is Rejected

An unfiltered query such as:

```rust
sbom::Entity::find().all(db).await?
```

or the equivalent `SELECT * FROM sbom` is **explicitly rejected** for the following reasons:

### 1. Performance impact

The task's Implementation Notes state:

> "Production environments have **hundreds of thousands of CycloneDX documents** alongside
> a smaller number of SPDX documents."

An unfiltered query would load hundreds of thousands of CycloneDX records that do not need
processing. Even if the migration were to skip them in application code (e.g., via an
`if labels.type == "spdx"` check after loading), the damage is already done:

- **Database I/O**: the query reads and transmits all rows over the connection
- **Memory**: all records are deserialized and held in memory before filtering
- **Source document fetches**: if source documents are loaded inside the loop before
  the type check, each CycloneDX document triggers an unnecessary disk/network read
- **Migration runtime**: in production, this could mean minutes or hours of unnecessary
  work versus seconds for the filtered subset

### 2. The filter is expressible at the data source

The `labels->>'type'` expression is a standard PostgreSQL jsonb accessor that works
directly in a WHERE clause. There is no technical barrier to filtering at the query level.
The column exists on every row, the values are known (`"spdx"` vs `"cyclonedx"`), and
SeaORM supports custom expressions via `Expr::cust()`.

When a subset filter is available at the data source and the task explicitly targets that
subset, using an unfiltered query is a scope mismatch per the skill's query-scope
verification rules.

### 3. Task intent is explicit

The task does not say "process all SBOMs and skip non-SPDX ones in code." It says "re-process
all SPDX SBOMs." The intent is to operate on the SPDX subset, and the database query should
reflect that intent directly.

## Summary

| Dimension | Value |
|-----------|-------|
| **Target scope** | SPDX SBOMs only (`labels->>'type' = 'spdx'`) |
| **Query scope chosen** | Filtered: `labels->>'type' = 'spdx'` in the WHERE clause |
| **Available filter** | `labels` jsonb column on `sbom` entity with `type` key |
| **Unfiltered query** | Rejected -- loads hundreds of thousands of unnecessary CycloneDX records with severe performance impact |
| **Performance impact of unfiltered** | Unnecessary I/O, memory, and runtime proportional to the full CycloneDX document count (hundreds of thousands of records) |
| **Rationale** | Filter is expressible at the data source; task explicitly targets a subset; unfiltered loading violates the principle of query-scope alignment |
