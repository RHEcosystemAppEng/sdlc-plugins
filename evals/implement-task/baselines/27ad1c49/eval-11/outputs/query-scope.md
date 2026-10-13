# Query-Scope Verification: TC-9209

## Step 9 - Query-scope verification

### 1. Target scope extraction

The task description contains explicit subset-restricting language:

- **Summary**: "Re-process all **SPDX** SBOMs to extract package supplier information"
- **Description**: "Create a data migration that re-processes all **SPDX SBOMs**"
- **Description**: "Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier information populated during ingestion."
- **Acceptance Criteria**: "CycloneDX documents are not loaded or processed by the migration"

The target scope is a **subset** of all SBOM records: only those whose document type is SPDX. CycloneDX SBOMs are explicitly excluded.

### 2. Query scope comparison

The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores metadata about each document. Per the Implementation Notes:

- SPDX documents have `{"type": "spdx"}` in their labels
- CycloneDX documents have `{"type": "cyclonedx"}` in their labels

This means the database **supports filtering by document type at the query level** using a JSONB filter on the `labels` column. A filtered query is both possible and appropriate:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx'
```

In SeaORM (the project's ORM), this translates to a query condition on the `labels` column using a JSON path expression, e.g.:

```rust
use sea_orm::prelude::*;
use entity::sbom;

sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(&db)
    .await?
```

### 3. Scope mismatch flagging

An unfiltered query such as `Sbom::find().all(&db)` (equivalent to `SELECT * FROM sbom`) would load **all** SBOM records indiscriminately, including all CycloneDX documents. This is a scope mismatch:

| Dimension | Target scope | Unfiltered query scope |
|-----------|-------------|----------------------|
| Document types | SPDX only | All (SPDX + CycloneDX + any future types) |
| Record count (production) | Smaller subset | Hundreds of thousands of records |

**Available filter**: The `labels` JSONB column on the `sbom` table supports `labels->>'type' = 'spdx'` filtering directly at the database level. This filter is expressible in the ORM query and does not require loading records into application memory first.

**Performance impact of loading all documents**: Production environments have **hundreds of thousands of CycloneDX documents** alongside a smaller number of SPDX documents. An unfiltered query would:

- Load hundreds of thousands of unnecessary records into application memory
- Fetch source documents (via `SourceDocument::find_by_sbom_id`) for records that will never be processed
- Waste database I/O, network bandwidth, and memory
- Significantly increase migration runtime for no benefit
- Risk OOM (out-of-memory) conditions on constrained environments

Application-level filtering (load all, then filter in Rust) would still incur the full I/O and memory cost of fetching every record before discarding the non-target ones.

### 4. Decision

**Use a filtered query.** The migration must query only SPDX SBOMs at the database level:

```rust
sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .all(&db)
    .await?
```

This approach:

- Matches the task's target scope exactly (SPDX only)
- Satisfies the acceptance criterion "CycloneDX documents are not loaded or processed"
- Avoids loading hundreds of thousands of irrelevant CycloneDX records
- Pushes filtering to the database where it can leverage indexes
- Keeps application memory usage proportional to the target subset

**Rejected alternatives:**

- `Sbom::find().all(&db)` followed by `.filter(|s| s.labels["type"] == "spdx")` in Rust -- this loads all records into memory before filtering, defeating the purpose of database-level filtering. With hundreds of thousands of non-target CycloneDX records in production, this wastes I/O and memory.
- `Sbom::find().all(&db)` without any filtering -- violates the acceptance criterion and processes documents that already have supplier information.
