# Query-Scope Verification Analysis — TC-9209

## Target Scope Extraction

The task Description states:

> "Create a data migration that re-processes **all SPDX SBOMs** to extract package supplier information"

And further clarifies:

> "**Only SPDX SBOMs** need re-processing — CycloneDX documents already have supplier information populated during ingestion."

This is subset-restricting language. The task targets **SPDX SBOMs only** — not all SBOMs. CycloneDX documents are explicitly excluded.

## Available Filtering Mechanism

The Implementation Notes describe the filtering mechanism:

> "The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores metadata about each document. SPDX documents have `{"type": "spdx"}` in their labels, while CycloneDX documents have `{"type": "cyclonedx"}`."

The `labels` jsonb column on the `sbom` entity supports database-level filtering by document type. PostgreSQL's jsonb operators (`->>`, `@>`) allow efficient filtering without loading documents into application memory.

## Query Scope Decision

**Chosen approach**: Filtered query at the database level.

```sql
SELECT id FROM sbom WHERE labels->>'type' = 'spdx'
```

Or using SeaORM's query builder equivalent:

```rust
Sbom::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(db)
    .await?
```

This query loads only SPDX SBOM records from the database. CycloneDX documents are excluded at the query level and are never fetched, parsed, or processed.

## Rejected Alternatives

### Unfiltered query (rejected)

```rust
// DO NOT USE:
Sbom::find().all(db).await?
// then filter in application code:
.filter(|s| s.labels["type"] == "spdx")
```

**Why rejected**: The Implementation Notes explicitly state that "production environments have hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents." Loading all documents and discarding CycloneDX ones in application code would:

1. **Unnecessary I/O**: Fetch hundreds of thousands of rows that are immediately discarded
2. **Memory pressure**: Load all SBOM records into application memory at once
3. **Database load**: Force the database to scan and return the full table instead of a filtered subset
4. **Network overhead**: Transfer large result sets across the database connection

Since the `labels` jsonb column already supports filtering by document type, there is no technical reason to use an unfiltered query. The database can efficiently select only SPDX records, reducing I/O by orders of magnitude in production environments.

### Application-level type check after full load (rejected)

```rust
// DO NOT USE:
let all_sboms = Sbom::find().all(db).await?;
for sbom in all_sboms {
    if sbom.labels.get("type") == Some("spdx") {
        // process
    }
}
```

**Why rejected**: Same performance concerns as the unfiltered query. The `labels->>'type'` filter can be expressed at the query level, making application-level filtering unnecessary and wasteful.

## Conclusion

The task targets a subset (SPDX SBOMs). The `sbom` entity's `labels` column (jsonb) supports filtering by document type at the database level. The plan uses a filtered query (`WHERE labels->>'type' = 'spdx'`) to select only SPDX documents, avoiding the performance impact of loading hundreds of thousands of non-target CycloneDX records in production environments.
