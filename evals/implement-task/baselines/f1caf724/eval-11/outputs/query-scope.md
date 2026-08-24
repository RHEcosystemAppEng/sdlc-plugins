# Query-Scope Verification Analysis: TC-9209

## 1. Target Scope Extraction

The task Description contains clear subset-restricting language that identifies the target scope as a subset of all SBOM documents:

- **"Re-process all SPDX SBOMs"** -- the qualifier "SPDX" restricts the scope to a specific document type, not all SBOMs
- **"Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier information populated during ingestion"** -- explicitly excludes CycloneDX documents from the target scope
- **"The migration should only load and process SPDX documents to avoid unnecessary I/O"** -- directly states that the query must filter at the data source

**Conclusion**: The task targets a subset -- specifically **SPDX SBOMs**, not all SBOMs. CycloneDX documents are explicitly out of scope and must not be loaded.

## 2. Database-Level Filter Verification

The Implementation Notes describe the filtering mechanism available at the database level:

- The `sbom` entity (`entity/src/sbom.rs`) has a **`labels` column of type `jsonb`** that stores metadata about each document
- SPDX documents have `{"type": "spdx"}` in their labels
- CycloneDX documents have `{"type": "cyclonedx"}` in their labels

This means the database supports filtering by document type using PostgreSQL's native jsonb operators:
```sql
WHERE labels->>'type' = 'spdx'
```

This filter can be expressed at the query level using SeaORM's expression API:
```rust
Sbom::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(&db)
    .await?
```

**Verification result**: The `labels` jsonb column **does support** filtering by document type at the database level. No application-level filtering is required -- the database can return only the SPDX records directly.

## 3. Query Scope Decision

### REJECTED: Unfiltered query with application-level filtering

The following approach is explicitly rejected:

```rust
// DO NOT USE: Loads ALL documents including hundreds of thousands of CycloneDX records
let all_sboms = Sbom::find().all(&db).await?;
let spdx_only: Vec<_> = all_sboms.into_iter()
    .filter(|s| s.labels.get("type") == Some("spdx"))
    .collect();
```

This approach fails for several reasons:

1. **Performance impact**: Production environments have **hundreds of thousands of CycloneDX documents** alongside a smaller number of SPDX documents. Loading all records means transferring hundreds of thousands of unnecessary rows from PostgreSQL to the application, consuming memory, network bandwidth, and database connection time.

2. **Unnecessary I/O**: The task Implementation Notes explicitly state: "Production environments have hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents. The migration should only load and process SPDX documents to avoid unnecessary I/O."

3. **Violates acceptance criteria**: The acceptance criteria state "CycloneDX documents are not loaded or processed by the migration." An unfiltered query like `Sbom::find()` followed by application-level filtering does load CycloneDX documents -- it simply discards them after loading. This violates the acceptance criterion.

4. **Database can filter efficiently**: Since the `labels` jsonb column supports the `->>'type'` operator, there is no technical reason to load all records. PostgreSQL can evaluate the filter and return only matching rows.

Similarly rejected are patterns such as:
- `Document::all()` followed by a type check
- Iterating the entire `sbom` table and skipping non-SPDX records
- Using `LIMIT`/`OFFSET` pagination over all documents with application-level filtering

### ACCEPTED: Filtered query at the database level

```rust
// CORRECT: Pushes the filter to PostgreSQL, only SPDX records are returned
let spdx_sboms = Sbom::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(&db)
    .await?;
```

This approach:
- Filters at the data source (PostgreSQL) using the jsonb `->>'type'` operator
- Returns only SPDX records to the application
- Avoids loading hundreds of thousands of CycloneDX documents
- Satisfies the acceptance criterion that CycloneDX documents are not loaded
- Scales correctly regardless of how many CycloneDX documents exist in production

## 4. Summary

| Aspect | Value |
|--------|-------|
| **Task target scope** | SPDX SBOMs only (subset of all SBOMs) |
| **Subset-indicating language** | "all SPDX SBOMs", "Only SPDX SBOMs need re-processing" |
| **Filter column** | `sbom.labels` (jsonb) |
| **Filter expression** | `labels->>'type' = 'spdx'` |
| **Database supports filter?** | Yes -- jsonb column with `->>'type'` operator |
| **Query approach** | Filtered query at database level |
| **Unfiltered query rejected?** | Yes -- `Sbom::find()` / `Document::all()` explicitly rejected |
| **Performance rationale** | Hundreds of thousands of CycloneDX documents in production would be loaded unnecessarily |
