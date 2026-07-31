# Query-Scope Verification: TC-9209

## What the Task Targets

The task description states: "Create a data migration that re-processes all **SPDX SBOMs**
to extract package supplier information." It further clarifies: "Only SPDX SBOMs need
re-processing -- CycloneDX documents already have supplier information populated during
ingestion."

**Target scope**: SPDX SBOM documents only -- a subset of all SBOM documents in the system.

## Subset-Restricting Language Identified

The following phrases in the task description restrict the scope to a subset:

1. "all SPDX SBOMs" -- type qualifier limiting to SPDX documents
2. "Only SPDX SBOMs need re-processing" -- explicit exclusion of other types
3. "CycloneDX documents already have supplier information" -- states CycloneDX is out of scope

## Available Database Filter

The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores
document metadata. Per the Implementation Notes:

- SPDX documents have `{"type": "spdx"}` in their labels
- CycloneDX documents have `{"type": "cyclonedx"}` in their labels

This means the subset restriction **can be expressed at the query level** using a jsonb
field extraction filter:

```sql
WHERE labels->>'type' = 'spdx'
```

In SeaORM, this translates to:

```rust
sbom::Entity::find().filter(Expr::cust("labels->>'type' = 'spdx'"))
```

## Query Scope Chosen: FILTERED

**Chosen approach**: A filtered database query that selects only SPDX SBOMs at the data
source, before any records enter application memory.

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx'
```

## Why NOT an Unfiltered Query

An unfiltered query such as `Sbom::find()` (equivalent to `SELECT * FROM sbom`) or
`Document::all()` followed by application-level filtering (e.g., `.filter(|s| s.labels.type == "spdx")`)
would be incorrect for this task. Here is why:

### Performance Impact

The Implementation Notes explicitly state: "Production environments have hundreds of
thousands of CycloneDX documents alongside a smaller number of SPDX documents."

An unfiltered query would:

1. **Load hundreds of thousands of unnecessary records into memory** -- the vast majority
   being CycloneDX documents that do not need processing. This wastes memory proportional
   to the total document count rather than the SPDX subset.

2. **Trigger unnecessary I/O** -- each loaded SBOM record would then require fetching its
   source document (the raw SBOM bytes) to determine its type. For hundreds of thousands
   of CycloneDX records, this means hundreds of thousands of source document reads that
   are immediately discarded. This could saturate database connections and disk I/O.

3. **Risk migration timeout or OOM** -- data migrations run with finite time and memory
   budgets. Loading the full dataset when only a small fraction is needed risks exceeding
   both limits in production.

4. **Violate the acceptance criteria** -- acceptance criterion #2 states "CycloneDX
   documents are not loaded or processed by the migration." An unfiltered query that loads
   all records and then filters in application code would load CycloneDX documents, violating
   this criterion even if it doesn't process them further.

### Correctness of Database-Level Filtering

The `labels` jsonb column on the `sbom` entity is the authoritative source for document
type classification. The labels are populated during ingestion and reliably distinguish
SPDX from CycloneDX documents. PostgreSQL's jsonb operator `->>'type'` efficiently
extracts the type field for filtering, and this operation can benefit from a GIN index
on the `labels` column if one exists.

## Summary

| Aspect | Value |
|---|---|
| Task target scope | SPDX SBOMs only (subset of all SBOMs) |
| Query scope chosen | Filtered: `WHERE labels->>'type' = 'spdx'` |
| Filter mechanism | `sbom.labels` jsonb column, `->>'type'` extraction |
| Rejected approach | `Sbom::find()` / `Document::all()` + application-level filtering |
| Rejection reason | Loads hundreds of thousands of CycloneDX records unnecessarily; performance impact (memory, I/O, timeout risk); violates acceptance criteria |
| Skill step reference | Step 9, "Query-scope verification" |
