# Query-Scope Verification: TC-9209

## What the Task Targets

The task description states:

> "Create a data migration that re-processes **all SPDX SBOMs** to extract package
> supplier information that was previously ignored during ingestion."

And further clarifies:

> "**Only SPDX SBOMs** need re-processing -- CycloneDX documents already have supplier
> information populated during ingestion."

**Target scope**: All SBOM records of type SPDX. CycloneDX records are explicitly excluded.

## Subset-Restricting Language Identified

The description contains clear subset-restricting language:

- "all SPDX SBOMs" -- type qualifier restricting to SPDX documents only
- "Only SPDX SBOMs need re-processing" -- explicit exclusion of non-SPDX types
- "CycloneDX documents already have supplier information" -- rationale for exclusion

## Available Database Filter

The task's Implementation Notes describe the filtering mechanism:

> "The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that
> stores metadata about each document. SPDX documents have `{"type": "spdx"}` in their
> labels, while CycloneDX documents have `{"type": "cyclonedx"}`."

This means the subset filter **can** be expressed at the database query level using:

```sql
WHERE labels->>'type' = 'spdx'
```

## Query Scope Chosen

**Filtered query**: The migration queries only SPDX SBOMs at the database level using
the `labels->>'type' = 'spdx'` filter on the `sbom` table.

```rust
sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(db)
    .await?;
```

## Why This Scope Was Chosen

### Performance impact of an unfiltered query

The Implementation Notes explicitly warn:

> "Production environments have **hundreds of thousands of CycloneDX documents** alongside
> a **smaller number of SPDX documents**. The migration should only load and process SPDX
> documents to avoid unnecessary I/O."

An unfiltered query (e.g., `sbom::Entity::find().all(db)`) would:

1. **Load hundreds of thousands of unnecessary records** into application memory
2. **Fetch source documents** for each CycloneDX SBOM (massive I/O waste)
3. **Parse documents** that don't need re-processing
4. Risk **out-of-memory errors** or excessive migration runtime in production

### The filter is expressible at the data source

The `labels` jsonb column with the `type` key provides a clean, indexable filter.
PostgreSQL's jsonb extraction operator (`->>`) supports this natively. There is no
technical reason to defer filtering to the application layer.

### Scope match confirmation

| Dimension | Target scope | Actual query scope | Match? |
|---|---|---|---|
| Document type | SPDX only | `labels->>'type' = 'spdx'` | Yes |
| Record status | All (no status filter mentioned) | All matching type filter | Yes |
| Date range | All (no date restriction) | All matching type filter | Yes |

The query scope exactly matches the task's target scope. No broader-than-necessary
loading occurs, and no documents outside the target set are fetched or processed.

## Conclusion

The chosen query scope is **correctly narrowed** to match the task's target scope.
The migration filters at the database level using the available `labels` jsonb column,
avoiding unnecessary I/O against hundreds of thousands of CycloneDX documents that
do not need re-processing. This satisfies both the task's functional requirements
(process only SPDX SBOMs) and the performance constraint (avoid loading CycloneDX
documents).
