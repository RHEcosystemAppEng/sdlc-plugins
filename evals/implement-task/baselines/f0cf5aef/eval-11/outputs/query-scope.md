# Query-Scope Verification Analysis for TC-9209

## What the Task Targets

The task description states:

> "Create a data migration that re-processes **all SPDX SBOMs** to extract package
> supplier information."

And explicitly clarifies:

> "**Only SPDX SBOMs** need re-processing -- CycloneDX documents already have supplier
> information populated during ingestion."

The target scope is a **SUBSET** of all SBOM documents: specifically, only those with
SPDX document type. CycloneDX documents are explicitly excluded from the operation.

---

## Available Filtering Mechanism

The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that
stores metadata about each document:

- SPDX documents: `{"type": "spdx"}`
- CycloneDX documents: `{"type": "cyclonedx"}`

This column provides a **database-level filter** that can distinguish SPDX from
CycloneDX documents directly in the SQL query, without loading any records into
application memory.

---

## Query Scope Chosen: FILTERED

The migration must use a **filtered database query** that restricts results to SPDX
documents only:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx'
```

In SeaORM (Rust):

```rust
sbom::Entity::find()
    .filter(Expr::cust_with_values("labels->>'type' = $1", ["spdx"]))
    .all(&db)
    .await?
```

---

## Why Filtered (Not Unfiltered)

### Performance impact of loading ALL documents

The task's Implementation Notes explicitly state:

> "Production environments have hundreds of thousands of CycloneDX documents alongside
> a smaller number of SPDX documents."

An unfiltered query (e.g., `sbom::Entity::find().all()`, `Sbom::find()`, or
`Document::all()`) would:

1. **Load hundreds of thousands of unnecessary CycloneDX records** from PostgreSQL into
   application memory -- records that the migration has no reason to touch.
2. **Consume excessive memory** proportional to the total document count rather than the
   SPDX subset.
3. **Waste I/O bandwidth** transferring data from PostgreSQL that will be immediately
   discarded by application-level filtering.
4. **Increase migration runtime** dramatically due to unnecessary data transfer and
   object allocation.
5. **Risk OOM failures** in production environments where the full document set may
   exceed available application memory.

Even if followed by an application-level filter (e.g., `.filter(|s| s.labels.type == "spdx")`),
the damage is already done -- the database has transferred all records across the wire and
the ORM has deserialized them into Rust structs.

### Explicitly rejected approaches

| Approach | Why rejected |
|----------|-------------|
| `sbom::Entity::find().all()` with app-level filtering | Loads ALL records (hundreds of thousands of CycloneDX docs) into memory, then discards most. The `labels` column supports database-level filtering, making this unnecessary. |
| `Sbom::find()` (unparameterized) | Same as above -- returns all SBOM records without filtering. |
| `Document::all()` with post-load type check | Loads every document indiscriminately. The subset-restricting language in the task description ("all SPDX SBOMs", "Only SPDX SBOMs") directly indicates a filtered query is required. |
| Loading all, then `if labels.type == "spdx" { process }` | Technically correct but grossly inefficient. PostgreSQL's jsonb operators (`->>`) are indexed and fast; the filter belongs in the WHERE clause, not in a Rust loop body. |

### Why the filtered query is correct

1. **The task targets a subset**: "all SPDX SBOMs" is a subset of "all SBOMs". The
   subset-restricting qualifier is the document type (SPDX vs CycloneDX).
2. **A narrower query is possible at the data source**: The `labels` jsonb column with
   `type` key directly supports `WHERE labels->>'type' = 'spdx'` filtering in PostgreSQL.
3. **The filter matches the acceptance criterion**: "CycloneDX documents are not loaded
   or processed by the migration" -- this criterion is only fully satisfied by excluding
   CycloneDX at the query level, not by loading and skipping them.
4. **Performance impact is material**: Hundreds of thousands of unnecessary records loaded
   vs. only the SPDX subset. This is not a marginal optimization -- it is the difference
   between a migration that runs in seconds/minutes and one that risks OOM or takes hours.

---

## Conclusion

The query scope for this migration **must** be filtered at the database level using
`labels->>'type' = 'spdx'`. This matches the task's target scope (SPDX SBOMs only),
satisfies the acceptance criterion that CycloneDX documents are not loaded or processed,
and avoids the severe performance penalty of loading hundreds of thousands of irrelevant
CycloneDX records into application memory.
