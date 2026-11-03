# Query-Scope Verification — TC-9209

This is the Step 9 query-scope check from implement-task. It applies here because the task is a data migration that iterates over database records.

## 1. Target scope (what the task covers)

Words in the task that restrict the scope to a subset:
- Summary: "Re-process all **SPDX** SBOMs"
- Description: "iterate over each **SPDX** SBOM document"; "**Only SPDX** SBOMs need re-processing — CycloneDX documents already have supplier information populated"
- Implementation Notes: "The migration should **only load and process SPDX documents** to avoid unnecessary I/O"; production has "hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents"
- Acceptance Criteria: "CycloneDX documents are **not loaded or processed**"

**Target scope**: rows in `sbom` whose `labels` JSONB has `type = "spdx"`. This is a type-qualifier subset, and it is much smaller than the whole table.

## 2. Query scope considered

| Option | Query | Scope | Verdict |
|---|---|---|---|
| A | `sbom::Entity::find().all(db)` (or `Document::all()`), then check the format in Rust after loading or parsing each source doc | All SBOMs | **Rejected**. This loads every CycloneDX row and possibly its source bytes, which is hundreds of thousands of rows of unnecessary I/O. It breaks the acceptance criterion "CycloneDX not loaded". |
| B | `sbom::Entity::find().filter(Expr::cust_with_values("labels->>'type' = $1", ["spdx"]))` with keyset pagination, selecting only `sbom_id` | SPDX only | **Chosen** |

## 3. Chosen query and why

```sql
SELECT sbom_id FROM sbom
WHERE labels->>'type' = 'spdx'
  AND sbom_id > $last_seen
ORDER BY sbom_id
LIMIT 500;
```

SeaORM form: `sbom::Entity::find().select_only().column(sbom::Column::SbomId).filter(Expr::cust_with_values("labels->>'type' = $1", ["spdx"])).order_by_asc(sbom::Column::SbomId).limit(500)`. This is followed by `SourceDocument::find_by_sbom_id(id)` for each returned id only.

Why:
- **The filter can run at the data source.** `entity/src/sbom.rs` has a `labels` column of type `jsonb`, and SPDX rows are tagged `{"type": "spdx"}`. The JSONB `->>` operator handles the filter in PostgreSQL, so no CycloneDX row reaches the application.
- **The more expensive I/O is avoided too.** The raw source document is fetched only for ids the filtered query returns, so CycloneDX source bytes are never read.
- **Memory stays bounded.** Selecting ids only and paging by keyset (`sbom_id > last`) means the migration never holds the whole SPDX set in memory, even if the SPDX count grows.
- **The update is scoped as well.** `sbom_package` updates are keyed by `sbom_id` (and the package node id) of SPDX SBOMs only, so CycloneDX `sbom_package` rows are never touched.

## 4. Mismatch check result

| Item | Value |
|---|---|
| Target scope | SPDX SBOMs only (`labels->>'type' = 'spdx'`) |
| Actual query scope | SPDX SBOMs only, filtered in SQL |
| Available filter | `sbom.labels` JSONB `type` key |
| Mismatch? | **No.** The query scope matches the target scope. |
| Performance impact | Rows scanned and loaded drop from (SPDX + hundreds of thousands of CycloneDX) to SPDX only. No source documents are fetched for CycloneDX. |

## 5. Notes and follow-ups
- **Index**: without an index, `labels->>'type'` still does a sequential scan on `sbom`, but it returns only SPDX rows. An expression index (`CREATE INDEX ... ON sbom ((labels->>'type'))`) or a GIN index on `labels` would make the filter itself cheap. That is a schema change outside the listed files, so I would raise it with the user rather than add it.
- **Comment in code**: the migration will carry a comment at the query explaining the SPDX-only filter and why CycloneDX is excluded, so the scope decision is visible to reviewers.
- **Test**: `backfill_skips_cyclonedx` asserts that CycloneDX `sbom_package` supplier values are unchanged after the migration runs. This verifies the scope through behaviour.
- **Label variants**: if the label value can differ in case (for example `"SPDX"`), use `lower(labels->>'type') = 'spdx'`. I would check the values the ingestor actually writes before finalising.
