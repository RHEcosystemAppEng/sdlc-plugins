# Query-Scope Verification — TC-9209

## 1. Target scope (extracted from the task Description)

Subset-restricting language found in the task:
- Summary: "Re-process all **SPDX** SBOMs"
- Description: "iterate over each **SPDX** SBOM document"; "**Only SPDX SBOMs** need re-processing — CycloneDX documents already have supplier information populated"
- Implementation Notes: "The migration should **only load and process SPDX documents** to avoid unnecessary I/O"; production has "hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents"
- Acceptance Criteria: "CycloneDX documents are **not loaded or processed** by the migration"

**Target scope**: SBOM records whose type is SPDX — a type qualifier, i.e. a strict subset of the `sbom` table. "All" in "all SPDX SBOMs" means all records within that subset, not all SBOMs.

## 2. Available filter at the data source

`entity/src/sbom.rs` has a `labels` column (`jsonb`). SPDX rows carry `{"type": "spdx"}`; CycloneDX rows carry `{"type": "cyclonedx"}`. So the subset can be expressed directly in the query:

```sql
WHERE labels->>'type' = 'spdx'
```

## 3. Query scope chosen

```rust
sbom::Entity::find()
    .select_only()
    .column(sbom::Column::SbomId)
    .filter(Expr::cust_with_values("labels ->> 'type' = $1", ["spdx"]))
    .into_tuple::<Uuid>()
    // paginated in batches for large sets
```

Then for each selected ID only: `SourceDocument::find_by_sbom_id(id)` -> parse -> `suppliers()` -> update `sbom_package`.

Rejected alternative: `sbom::Entity::find().all(db)` (i.e. `Document::all()`) followed by an in-memory check of the type, or by trying to parse every source document. That scope would be wider than the target scope.

## 4. Why

| Aspect | Unfiltered (`find().all()`) | Filtered (`labels->>'type' = 'spdx'`) |
|---|---|---|
| Rows selected from `sbom` | All (hundreds of thousands, mostly CycloneDX) | SPDX only |
| `source_document` fetches | Potentially one per SBOM, including every CycloneDX doc | SPDX docs only |
| Parse attempts | Every document | SPDX documents only |
| AC "CycloneDX not loaded" | Violated (CycloneDX rows are loaded even if skipped later) | Satisfied |
| Risk to CycloneDX data | Possible if a type check is wrong | None, rows never touched |

- The task targets a subset, and a narrower query **is** possible at the data source through the `labels` jsonb column. Under the skill's query-scope rule, using an unfiltered query here would be a scope mismatch to flag. The filtered query is the correct choice.
- Performance: the cost moves from O(all SBOMs) document I/O and parsing to O(SPDX SBOMs). Production is dominated by CycloneDX, so this cuts most of the I/O.
- Correctness: CycloneDX rows can never be modified because they are never selected, which also makes the "CycloneDX not affected" test a meaningful guarantee.
- Only `sbom_id` is selected (not full rows), and IDs are paged, so memory stays bounded. One raw document is in memory at a time.
- Possible follow-up (not in scope): if there is no expression index on `(labels->>'type')`, the filter still scans `sbom` metadata rows. That is cheap compared with loading documents. An expression or GIN index could be suggested in the PR, but it is not added in this task.

## 5. Verification outcome

- Target scope: SPDX SBOMs only
- Query scope: SPDX SBOMs only (DB-level filter on `labels->>'type' = 'spdx'`)
- Mismatch: **none**. No intentional broad query, so no rationale comment is needed for that. A short code comment in the migration will still explain why the filter exists.
