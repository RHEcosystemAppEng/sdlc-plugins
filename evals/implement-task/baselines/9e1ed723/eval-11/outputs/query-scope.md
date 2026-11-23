# Query-Scope Verification — TC-9209

Per implement-task Step 9 "Query-scope verification" (applies because this task is a
data migration iterating database records).

## 1. Target scope extracted from the task

Subset-restricting language found in the Description, Implementation Notes, and Acceptance Criteria:

- Summary/Description: "re-process all **SPDX** SBOMs"; "iterate over each **SPDX** SBOM document"
- "**Only SPDX SBOMs** need re-processing — CycloneDX documents already have supplier information"
- Implementation Notes: "The migration should **only load and process SPDX documents** to avoid unnecessary I/O"
- Acceptance Criterion: "CycloneDX documents are **not loaded** or processed by the migration"

**Target scope**: SBOM records whose document type is SPDX (a type-qualifier subset of `sbom`),
not all SBOMs.

## 2. Available filter at the data source

`sbom.labels` (`jsonb`, `entity/src/sbom.rs`) stores `{"type": "spdx"}` or `{"type": "cyclonedx"}`.
This lets the filter be expressed directly in SQL.

## 3. Query scope chosen

```rust
sbom::Entity::find()
    .filter(Expr::cust(r#"labels->>'type' = 'spdx'"#))   // or labels @> '{"type":"spdx"}'
```

Equivalent SQL:

```sql
SELECT sbom_id FROM sbom WHERE labels->>'type' = 'spdx';
-- index-friendly alternative if a GIN index exists on labels:
SELECT sbom_id FROM sbom WHERE labels @> '{"type": "spdx"}';
```

Results are streamed/paginated in batches. Only IDs are selected; each SPDX SBOM's raw
document is then fetched individually via `SourceDocument::find_by_sbom_id(id)`.

## 4. Rejected alternative (flagged scope mismatch)

| Aspect | Value |
|---|---|
| Target scope | SPDX SBOMs only |
| Rejected query scope | `sbom::Entity::find().all(db)` (all SBOMs), then skipping non-SPDX in Rust, or detecting format by parsing each source document |
| Available filter | `sbom.labels->>'type' = 'spdx'` (jsonb column) |
| Performance impact | Production has hundreds of thousands of CycloneDX SBOMs vs. a smaller number of SPDX. Loading everything would read all `sbom` rows into memory and, worse, fetch/parse every `source_document` blob — orders of magnitude more I/O, and it would violate the "CycloneDX not loaded" acceptance criterion even if those rows were then skipped. |

## 5. Why this scope

- Matches the task's explicit target subset exactly (SPDX only).
- The filter can be expressed at the query level, so the "intentional broad query" exception
  does not apply — no full-dataset scan is justified.
- Satisfies the acceptance criterion literally: CycloneDX rows are never loaded, not merely
  never updated.
- Avoids unnecessary I/O on the large CycloneDX population, as the Implementation Notes require.
- The downstream `UPDATE sbom_package ... WHERE sbom_id = ?` is also scoped per SPDX SBOM,
  so no CycloneDX `sbom_package` rows are touched.

A code comment in the migration documents this rationale beside the query. A test
(`backfill_does_not_touch_cyclonedx`) verifies CycloneDX supplier values stay unchanged.

## Residual items to confirm in Step 4 (via `serena_backend`)

- Exact casing/values in `labels` (`"spdx"` vs `"SPDX"`) — check ingestor code that writes labels.
- Whether a GIN index on `sbom.labels` exists, to choose `@>` vs `->>`.
- Whether `common/src/db/query.rs` already provides a label-filter helper to reuse.
