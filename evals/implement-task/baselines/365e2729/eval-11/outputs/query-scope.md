# Query-Scope Verification — TC-9209

This analysis follows SKILL.md Step 9, "Query-scope verification". It applies because the task is a data migration that iterates over database records.

## 1. Target scope (from the task Description)

The task text restricts the work to a subset in several places:
- Summary: "Re-process all **SPDX** SBOMs"
- Description: "iterate over each **SPDX** SBOM document" and "**Only SPDX SBOMs** need re-processing — CycloneDX documents already have supplier information populated"
- Implementation Notes: "The migration should **only load and process SPDX documents** to avoid unnecessary I/O"
- Acceptance Criteria: "CycloneDX documents are **not loaded** or processed by the migration"

**Target scope:** `sbom` rows whose document type is SPDX. CycloneDX rows are explicitly excluded.

The word "all" in "all SPDX SBOMs" means every SPDX SBOM. It does not mean all SBOMs. The type qualifier "SPDX" is the subset restriction.

## 2. Available filter at the data source

- `sbom.labels` is a `jsonb` column. SPDX rows have `{"type": "spdx"}` and CycloneDX rows have `{"type": "cyclonedx"}` (Implementation Notes, `entity/src/sbom.rs`).
- This means the filter can be written in SQL as `labels->>'type' = 'spdx'`, or as `labels @> '{"type":"spdx"}'`. The second form can use a GIN index on `labels` if one exists.

## 3. Query scope chosen

```sql
SELECT sbom_id
FROM sbom
WHERE labels->>'type' = 'spdx'
  AND sbom_id > $last_id          -- keyset pagination
ORDER BY sbom_id
LIMIT 500;
```

In SeaORM:

```rust
sbom::Entity::find()
    .select_only().column(sbom::Column::SbomId)
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .filter(sbom::Column::SbomId.gt(last_id))
    .order_by_asc(sbom::Column::SbomId)
    .limit(500)
```

For each returned id, the raw document is fetched with `SourceDocument::find_by_sbom_id(id)`. This means source documents are only read for SPDX SBOMs.

## 4. Rejected alternatives

| Approach | Why it was rejected |
|---|---|
| `sbom::Entity::find().all(db)` and then skip non-SPDX rows in Rust | Loads hundreds of thousands of CycloneDX rows into memory just to throw them away. Breaks AC "CycloneDX documents are not loaded". This is the exact anti-pattern in the skill's example ("re-process all SPDX SBOMs" with `Document::all()`, which should be flagged). |
| Iterate all SBOMs, fetch every source document, and detect the format by parsing | Even worse: it reads and parses the full raw bytes of every CycloneDX document, which multiplies I/O. |
| Filtered query without pagination (`.all()` over the SPDX subset) | Scope is correct, but the whole SPDX id list sits in memory at once. Keyset batches keep memory bounded, and the cost is low. |

## 5. Result

- **Target scope:** SPDX SBOMs only
- **Actual query scope:** SPDX SBOMs only, filtered in SQL (`labels->>'type' = 'spdx'`)
- **Mismatch:** none. The scope matches, and the filter runs at the data source rather than in application code.
- **Performance impact:** the work scales with the number of SPDX documents (small) instead of all documents (hundreds of thousands of CycloneDX). No CycloneDX `sbom` rows or `source_document` bytes are read. Selecting only `sbom_id` and paging in batches of 500 keeps memory flat.
- **Code comment:** the query in the migration carries a comment saying the SPDX filter is intentional (`// Query scope: SPDX only, filtered at the database by labels->>'type'`). That way a future reader will not widen it to `find().all()`.
- **Test coverage:** the CycloneDX-untouched test checks the exclusion from the outside, because CycloneDX `sbom_package` rows are identical before and after the migration.
- **Follow-up, advisory only:** if there is no index on `labels` (or on `labels->>'type'`), the filter still works with a sequential scan of `sbom` metadata. That is cheap compared with loading documents. An expression index is not part of this task's scope, so I would mention it in the PR but not add it.
