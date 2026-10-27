# Query-Scope Verification Analysis: TC-9209

## Task Target Scope

The task description contains explicit subset-restricting language:

- Summary: "Re-process all **SPDX SBOMs**" — targets SPDX documents specifically, not all SBOMs
- Description: "Create a data migration that re-processes all **SPDX SBOMs** to extract package supplier information"
- Description: "**Only SPDX SBOMs** need re-processing — CycloneDX documents already have supplier information populated during ingestion"
- Acceptance Criteria: "CycloneDX documents are **not loaded or processed** by the migration"

**Conclusion**: The task targets a **subset** of the sbom table — specifically documents with type "spdx". This is not a full-table migration.

## Available Filter Mechanism

The Implementation Notes provide the filter mechanism:

> "The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores metadata about each document. SPDX documents have `{"type": "spdx"}` in their labels, while CycloneDX documents have `{"type": "cyclonedx"}`."

The `labels` jsonb column on the `sbom` entity directly supports filtering by document type at the database level. PostgreSQL's `->>` operator can extract the `type` key as text for comparison. This means the subset restriction can be expressed as a database-level WHERE clause rather than requiring application-level filtering after loading all records.

**Filter expression**: `WHERE labels->>'type' = 'spdx'`

This translates to a SeaORM query:
```rust
sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(db)
    .await?
```

## Query Scope Decision

**Chosen approach**: Filtered query at the database level.

**Rejected approach**: Unfiltered query (e.g., `Sbom::find().all(db)` or `sbom::Entity::find().all(db)`) followed by application-level filtering to discard CycloneDX documents.

### Why filtered query is essential

1. **Production data volume**: The Implementation Notes explicitly state that "production environments have hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents." Loading all documents would mean fetching hundreds of thousands of records that will be immediately discarded — wasting database I/O, network bandwidth, and application memory.

2. **Database-level filtering is available**: The `labels` jsonb column with the `->>` operator provides a direct, efficient filter path. There is no technical reason to load all records when a WHERE clause can eliminate non-target documents at the source.

3. **Acceptance criteria explicitly require it**: The criterion "CycloneDX documents are not loaded or processed by the migration" requires that CycloneDX documents are not even loaded from the database, not just "not processed." A filtered query satisfies this — an unfiltered query followed by application filtering would violate it because the documents would be loaded into memory.

4. **Migration performance**: Data migrations run against production databases. An unfiltered query on a table with hundreds of thousands of rows would cause unnecessary load on the database and extend migration runtime significantly. In extreme cases, it could cause memory exhaustion if the result set is too large to hold in memory.

## Performance Impact Summary

| Approach | Records loaded | Performance |
|----------|---------------|-------------|
| `sbom::Entity::find().filter(labels->>'type' = 'spdx')` | ~thousands (SPDX only) | Efficient — minimal I/O |
| `sbom::Entity::find().all(db)` (unfiltered) | ~hundreds of thousands (all types) | Wasteful — loads 100x+ more records than needed |

The filtered query avoids loading hundreds of thousands of CycloneDX documents that would be immediately discarded, reducing both I/O and memory usage by orders of magnitude.
