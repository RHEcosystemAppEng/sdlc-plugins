# Query-Scope Verification — TC-9209

## 1. Target scope extracted from the task

The task Description and Notes contain language that restricts the work to a subset:
- "re-processes **all SPDX SBOMs**": a type qualifier.
- "**Only SPDX SBOMs** need re-processing — CycloneDX documents already have supplier information populated during ingestion."
- Implementation Notes: "Production environments have hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents. The migration should **only load and process SPDX documents** to avoid unnecessary I/O."
- Acceptance Criterion: "CycloneDX documents are **not loaded** or processed by the migration."

**Target scope:** `sbom` rows whose document type is SPDX. This is a subset of all SBOMs, and a small minority in production.

## 2. Available filter at the data source

- `entity/src/sbom.rs` has a `labels` column of type `jsonb`.
- SPDX rows have `{"type": "spdx"}` and CycloneDX rows have `{"type": "cyclonedx"}`.
- So the filter `labels->>'type' = 'spdx'` can be written directly in SQL / SeaORM.

## 3. Query scope chosen

```rust
sbom::Entity::find()
    .select_only()
    .column(sbom::Column::SbomId)
    .filter(Expr::cust("labels->>'type' = 'spdx'"))   // or the equivalent JSON-path helper / bound param
    .filter(sbom::Column::SbomId.gt(last_id))        // keyset pagination
    .order_by_asc(sbom::Column::SbomId)
    .limit(BATCH_SIZE)
```

Equivalent SQL:

```sql
SELECT sbom_id FROM sbom
WHERE labels->>'type' = 'spdx' AND sbom_id > $1
ORDER BY sbom_id
LIMIT 500;
```

Then `SourceDocument::find_by_sbom_id(id)` is called **only for those filtered IDs**, so raw document bytes are fetched only for SPDX documents.

## 4. Rejected alternative

`sbom::Entity::find().all(db)` (equivalent to `Document::all()`), followed by checking the type in Rust or by trying to parse each source document as SPDX. It was rejected because:
- It loads every SBOM row, including hundreds of thousands of CycloneDX ones, into memory.
- It would probably also fetch each CycloneDX `source_document` blob just to discover it is not SPDX. That is a large amount of unnecessary I/O.
- It violates the acceptance criterion "CycloneDX documents are not loaded".

Flag in the skill's format, if such code were found:
| Target scope | Actual query scope | Available filter | Performance impact |
|---|---|---|---|
| SPDX SBOMs only | All SBOMs (`find().all()`) | `labels->>'type' = 'spdx'` on jsonb `labels` | Loads and fetches source documents for hundreds of thousands of CycloneDX rows needlessly; high memory and I/O, long migration time |

## 5. Why this scope

- It matches the task's target subset exactly, so there is **no scope mismatch**.
- Filtering happens at the database, so CycloneDX rows are never sent over the wire.
- Selecting only `sbom_id` and paginating by keyset keeps memory bounded however many SPDX documents exist.
- A comment in the migration code records the reasoning: SPDX only, CycloneDX already populated at ingestion, filtered at the DB.

## 6. Secondary query scopes

- `sbom_package` update: scoped by `sbom_id = <spdx id>` plus the package identifier, so only rows belonging to SPDX SBOMs are touched. This also guarantees CycloneDX `sbom_package` rows are unaffected, which the `backfill_skips_cyclonedx` test checks.
- `source_document` lookup: per filtered `sbom_id` only.

## 7. Optional follow-up (out of scope, flagged only)

A `labels->>'type'` filter on a large table with no index means a sequential scan. That is acceptable for a one-time migration, since it reads only the narrow `sbom` rows and not the blobs. An expression index `CREATE INDEX ON sbom ((labels->>'type'))` could be proposed separately. It is not added, because doing so would go beyond Files to Create and Files to Modify.
