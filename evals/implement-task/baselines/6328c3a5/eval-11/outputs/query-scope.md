# Query-Scope Verification: TC-9209

## What the Task Targets

The task description explicitly states: "Re-process all **SPDX SBOMs** to extract package supplier information." It further clarifies: "Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier information populated during ingestion."

**Target scope**: SPDX SBOMs only (a subset of all SBOMs in the database).

This is a subset-restricting qualifier. The word "all" in the task title refers to "all SPDX SBOMs," not "all SBOMs." The Description section makes this unambiguous by contrasting SPDX (needs re-processing) against CycloneDX (already populated).

---

## What Query Scope Was Chosen

**Filtered query**: Query the `sbom` table with a `WHERE` clause on the `labels` jsonb column to select only SPDX documents.

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx';
```

In SeaORM (Rust ORM used by the project):

```rust
sbom::Entity::find()
    .filter(Expr::cust_with_values("labels->>'type' = $1", ["spdx"]))
    .all(db)
    .await?;
```

This query loads only SPDX SBOM records from the database. CycloneDX records are never fetched, never parsed, and never processed.

---

## Why This Query Scope

### 1. The `labels` column supports filtering

The task's Implementation Notes confirm that the `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb`. The column stores document type metadata:

- SPDX documents: `{"type": "spdx"}`
- CycloneDX documents: `{"type": "cyclonedx"}`

This means the filtering can be expressed at the database query level using PostgreSQL's native jsonb operators (`->>`, `@>`, etc.). There is no need to load all records and filter in application code.

### 2. Performance impact of an unfiltered query

The Implementation Notes state: "Production environments have hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents."

An unfiltered query such as `Sbom::find().all(db)` or `Document::all()` would:

| Impact | Description |
|--------|-------------|
| **I/O** | Read hundreds of thousands of unnecessary rows from PostgreSQL |
| **Memory** | Allocate and hold all SBOM records in memory simultaneously |
| **Processing** | For each loaded record, fetch its source document and attempt to parse it before discovering it is CycloneDX and skipping it |
| **Runtime** | Migration runtime proportional to total document count instead of SPDX count |
| **Database load** | Unnecessary strain on production database during migration execution |

When the SPDX subset is small relative to the total SBOM count, the performance difference between a filtered and unfiltered query is orders of magnitude.

### 3. The task explicitly requires exclusion

Acceptance criteria state: "CycloneDX documents are not loaded or processed by the migration." This is not just a performance optimization -- it is a correctness requirement. An unfiltered query that loads CycloneDX documents and then skips them in application code would technically violate this criterion, as the documents are still "loaded" from the database even if not "processed."

### 4. Scope mismatch detection (per skill guidance)

Following the implement-task skill's **Query-scope verification** step:

- **Target scope**: SPDX SBOMs only (subset-restricting language: "all SPDX SBOMs", "Only SPDX SBOMs")
- **Available filter**: `labels->>'type' = 'spdx'` on the `sbom` entity's jsonb column
- **Narrower query possible**: Yes -- the `labels` column directly supports the required filter
- **Performance impact of broad query**: Loading hundreds of thousands of unnecessary CycloneDX records

A query like `Sbom::find().all(db)` or `Document::all()` would be flagged as a scope mismatch: the task targets a subset, a narrower query is possible at the data source, and the performance impact of loading all records is significant.

---

## Conclusion

The filtered query `WHERE labels->>'type' = 'spdx'` is the correct approach because:

1. It matches the task's target scope (SPDX only)
2. The database schema supports it (jsonb `labels` column)
3. It satisfies the acceptance criterion that CycloneDX documents are not loaded
4. It avoids loading hundreds of thousands of irrelevant records in production
