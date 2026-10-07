# Query-Scope Verification: TC-9209

## Target Scope Extraction

The task Description contains explicit subset-restricting language:

> "Create a data migration that re-processes all **SPDX SBOMs** to extract package supplier information"

> "Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier information populated during ingestion."

The target scope is **SPDX SBOMs only** -- a strict subset of all SBOM documents in the database. CycloneDX documents are explicitly excluded.

## Available Database-Level Filter

The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb`. Per the Implementation Notes, this column stores document-type metadata:

- SPDX documents: `{"type": "spdx"}`
- CycloneDX documents: `{"type": "cyclonedx"}`

This means the document type distinction is **available at the database level** as a filterable column. A query can use a condition such as:

```sql
WHERE labels->>'type' = 'spdx'
```

In SeaORM, this translates to a `Condition` filter on the `labels` column using a JSON extraction expression, which pushes the filtering down to PostgreSQL rather than performing it in application code.

## Query Scope Decision: Filtered Query

**Chosen scope:** Filtered query selecting only rows where `labels->>'type' = 'spdx'`.

**Rejected alternative:** An unfiltered query such as `Sbom::find()` (SeaORM's equivalent of `SELECT * FROM sbom`) or `Document::all()` followed by an application-level type check (e.g., `if doc.labels["type"] == "spdx" { ... } else { continue; }`).

## Rationale

### Performance impact of loading all documents

The Implementation Notes state:

> "Production environments have hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents."

An unfiltered query like `Sbom::find()` would load **all** SBOM records -- including hundreds of thousands of CycloneDX documents that the migration has no reason to touch. For each loaded record, the migration would then need to:

1. Deserialize the row from the database result set.
2. Inspect the `labels` field in application code.
3. Discard the vast majority of records (CycloneDX) without doing any useful work.

This imposes significant unnecessary costs:
- **Database I/O**: transferring hundreds of thousands of rows across the database connection when only a fraction are needed.
- **Memory pressure**: materializing all rows in the application's memory, potentially causing OOM in constrained migration environments.
- **Elapsed time**: the migration would take orders of magnitude longer than necessary, increasing the maintenance window.
- **Lock contention**: holding database resources open for the duration of a full-table scan when a targeted index-friendly query would release them quickly.

### Why filtered query is correct

Since the `labels` jsonb column already encodes the document type, PostgreSQL can evaluate `labels->>'type' = 'spdx'` during the scan phase, returning only the target subset. This:
- Eliminates transfer and deserialization of non-target rows.
- Reduces memory footprint to only SPDX documents.
- Can leverage a GIN or expression index on `labels->>'type'` if one exists, making the query even more efficient.
- Aligns the query scope precisely with the task's stated target scope (SPDX SBOMs only).

## Conclusion

The migration MUST use a filtered query at the database level -- e.g., `Sbom::find().filter(labels_type_eq("spdx"))` or an equivalent SeaORM condition -- to select only SPDX documents. An unfiltered query that loads all documents and discards CycloneDX records in application code is explicitly rejected due to the severe performance impact on production environments with hundreds of thousands of non-target records.
