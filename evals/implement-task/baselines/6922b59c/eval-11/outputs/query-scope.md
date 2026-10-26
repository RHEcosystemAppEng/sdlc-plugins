# Query-Scope Verification Analysis -- TC-9209

## Target Scope Extraction

The task **Description** states:

> "Create a data migration that re-processes all **SPDX SBOMs** to extract package supplier
> information that was previously ignored during ingestion."

And further:

> "**Only SPDX SBOMs** need re-processing -- CycloneDX documents already have supplier
> information populated during ingestion."

The target scope is explicitly a **subset**: only SPDX SBOM documents, not all SBOM documents
in the database.

## Available Filter Mechanism

The **Implementation Notes** document the filtering mechanism:

- The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb`.
- SPDX documents have `{"type": "spdx"}` in their labels.
- CycloneDX documents have `{"type": "cyclonedx"}` in their labels.

This means the query can filter at the database level using:

```sql
WHERE labels->>'type' = 'spdx'
```

Or in SeaORM (Rust):

```rust
Sbom::find()
    .filter(sbom::Column::Labels.contains(json!({"type": "spdx"})))
```

## Query Scope Decision: Filtered Query

**Chosen scope**: Filtered query -- only load SPDX SBOM records from the database.

**Rejected alternative**: An unfiltered query such as `Sbom::find().all(db)` (loading all
SBOM records and filtering in application code) is explicitly rejected for the following
reasons:

1. **Performance impact**: The Implementation Notes state that production environments have
   "hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX
   documents." An unfiltered query would load hundreds of thousands of records that will
   immediately be discarded, causing unnecessary I/O, memory allocation, and database load.

2. **Unnecessary source document fetching**: The migration needs to call
   `SourceDocument::find_by_sbom_id(id)` for each record to retrieve the raw document bytes
   for re-parsing. If CycloneDX records are loaded, the migration would either (a) also fetch
   their source documents (wasting even more I/O) or (b) require an application-level type
   check before fetching -- adding complexity that a database filter eliminates entirely.

3. **Filter is expressible at the data source**: The `labels` JSONB column with
   `labels->>'type' = 'spdx'` supports direct filtering at the database level. There is no
   technical barrier to a filtered query. The SKILL.md query-scope verification step is clear:
   "if the task targets a subset but a narrower query is possible at the data source (via
   columns, indexes, ORM scopes, or API parameters), flag for review."

4. **Acceptance criteria alignment**: The acceptance criteria explicitly require "CycloneDX
   documents are not loaded or processed by the migration." A database-level filter satisfies
   this requirement at the query layer, while an unfiltered query would violate it (CycloneDX
   documents would be loaded, even if not processed).

## Summary

| Dimension          | Value                                                |
|--------------------|------------------------------------------------------|
| Target scope       | SPDX SBOMs only (subset of all SBOMs)                |
| Chosen query scope | Filtered: `labels->>'type' = 'spdx'`                 |
| Filter column      | `sbom.labels` (JSONB)                                 |
| Rejected approach  | `Sbom::find().all(db)` -- unfiltered, loads all docs  |
| Rejection reason   | Performance (hundreds of thousands of unnecessary CycloneDX records loaded), violates acceptance criteria |
