# Query-Scope Verification — TC-9209

Applied per SKILL.md Step 9 "Query-scope verification", because the task is a batch data migration that iterates over database records.

## 1. Target scope (extracted from the task Description)

Language in the task that restricts the record set:
- Description: "re-processes all **SPDX** SBOMs", "iterate over each **SPDX** SBOM document"
- Description: "**Only SPDX SBOMs** need re-processing — CycloneDX documents already have supplier information populated"
- Implementation Notes: "The migration should **only load and process SPDX documents** to avoid unnecessary I/O"
- Acceptance Criterion: "CycloneDX documents are **not loaded or processed** by the migration"

**Target scope**: the subset of `sbom` rows whose document type is SPDX. This is a type qualifier, not "all SBOMs".

## 2. Available filter at the data source

- `entity/src/sbom.rs` has a `labels` column of type `jsonb`.
- SPDX rows have `labels = {"type": "spdx"}` and CycloneDX rows have `{"type": "cyclonedx"}`.
- The filter can therefore be expressed in SQL: `labels->>'type' = 'spdx'`. With SeaORM it is `.filter(Expr::cust("labels->>'type' = 'spdx'"))`, or a JSON containment expression `labels @> '{"type":"spdx"}'`, which can use a GIN index on `labels` if one exists.

## 3. Query scope chosen

```rust
sbom::Entity::find()
    .select_only()
    .column(sbom::Column::SbomId)
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .into_tuple::<Uuid>()
    // paginate (keyset on sbom_id) if SPDX volume is large
    .all(db)
```

```sql
SELECT sbom_id FROM sbom WHERE labels->>'type' = 'spdx' ORDER BY sbom_id;
```

The query then calls `SourceDocument::find_by_sbom_id(id)` once for each SPDX id only, and runs `UPDATE sbom_package ... WHERE sbom_id = <spdx id>`.

## 4. Rejected alternative (the scope mismatch this check flags)

- `sbom::Entity::find().all(db)` (equivalent to `Document::all()`), followed by checking the format in Rust after loading or parsing each document.
- **Scope mismatch flag**:
  - Target scope: SPDX SBOMs only.
  - Actual query scope: all SBOMs (SPDX plus CycloneDX).
  - Available filter: the `sbom.labels->>'type'` jsonb key.
  - Performance impact: production has hundreds of thousands of CycloneDX documents against a much smaller SPDX set. An unfiltered query would load every `sbom` row and, worse, fetch and parse every source document blob from `source_document`. The I/O, memory use and migration runtime would grow with the total SBOM count rather than the SPDX count. It would also break the acceptance criterion "CycloneDX documents are not loaded or processed".

## 5. Why this choice

1. The task explicitly targets a subset defined by a type qualifier ("SPDX").
2. That subset can be filtered at the source through an existing indexed or indexable column (`labels` jsonb), so filtering in application code is unnecessary.
3. Filtering in the database means CycloneDX rows and their source documents are never loaded. This satisfies the acceptance criterion and the Implementation Note about avoiding unnecessary I/O.
4. Projecting only `sbom_id` and fetching source documents one at a time keeps memory use bounded. Keyset pagination is added if the SPDX count is large.
5. The update is limited to `sbom_package` rows for SPDX sbom_ids, so CycloneDX supplier data cannot be overwritten. Test 2 (`backfill_skips_cyclonedx`) covers this.

No intentional broad query is needed, because the full dataset is not required. A code comment above the query will record why it is filtered (SPDX only, CycloneDX already populated, CycloneDX volume).

## Result

**PASS**. The query scope matches the target scope, and the filter is applied at the data source.

Step 4 should also confirm that the label value is exactly `"spdx"` (lowercase) in existing data, for example with a quick `SELECT DISTINCT labels->>'type' FROM sbom` check against a test DB or sibling ingestion code. Otherwise the filter could silently miss rows.
