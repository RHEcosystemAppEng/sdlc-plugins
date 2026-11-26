# Query-Scope Verification — TC-9209

Per implement-task Step 9 "Query-scope verification" (this task is a data migration that iterates database records).

## 1. Target scope (from task Description)

Subset-restricting language found:
- "re-processes all **SPDX** SBOMs" — type qualifier
- "iterate over each **SPDX** SBOM document"
- "**Only SPDX SBOMs** need re-processing — CycloneDX documents already have supplier information"
- Acceptance Criterion: "CycloneDX documents are **not loaded** or processed by the migration"
- Implementation Notes: production has hundreds of thousands of CycloneDX docs vs a smaller number of SPDX docs; "only load and process SPDX documents to avoid unnecessary I/O"

**Target scope: SBOMs where document type = SPDX** (a subset of the `sbom` table).

## 2. Available filter at the data source

`entity/src/sbom.rs` has a `labels` column (`jsonb`). SPDX rows have `{"type": "spdx"}`, CycloneDX rows `{"type": "cyclonedx"}`. So the subset is expressible directly in SQL: `labels->>'type' = 'spdx'`.

## 3. Chosen query scope

```sql
SELECT sbom_id FROM sbom WHERE labels->>'type' = 'spdx' ORDER BY sbom_id LIMIT/OFFSET (paginated)
```

SeaORM:

```rust
sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
    .select_only()
    .column(sbom::Column::SbomId)
    .into_tuple::<Uuid>()
    .paginate(db, BATCH_SIZE)
```

Then per SPDX SBOM: `SourceDocument::find_by_sbom_id(id)` to load raw bytes, and `sbom_package` updates filtered by `sbom_id`.

**Rejected alternative**: `sbom::Entity::find().all(db)` (or `Document::all()`) followed by in-memory checking of the type / attempting to parse each document. That loads every SBOM — including hundreds of thousands of CycloneDX rows and potentially their source documents — only to discard them. This is exactly the mismatch the check is designed to flag, and it would violate the acceptance criterion "CycloneDX documents are not loaded".

## 4. Why

- Scope match: the query returns precisely the target subset; no CycloneDX row is ever fetched, so the "not loaded" criterion holds by construction, not by an in-loop `if`.
- Performance: avoids reading the much larger CycloneDX population and its `source_document` blobs; I/O is proportional to the number of SPDX docs.
- Memory: select only IDs and paginate, fetch each source document individually, so the migration does not hold all documents in memory.
- Write scope also restricted: `sbom_package` updates are filtered by the current SPDX `sbom_id`, so CycloneDX package rows are never modified.
- A code comment in the migration documents the filter and the reason (query-scope rationale).
- Optional consideration: if `labels->>'type'` is not indexed, the filter is still a single sequential scan over `sbom` metadata (cheap relative to loading documents); an expression index is not added because it is outside the task's file scope.

## Result

| Item | Value |
|---|---|
| Target scope | SPDX SBOMs only |
| Actual query scope | `sbom` rows with `labels->>'type' = 'spdx'` (paginated IDs) |
| Available filter | `sbom.labels` jsonb `type` key |
| Mismatch? | No — filtered at the data source |
| Performance impact | CycloneDX rows/documents (hundreds of thousands) never loaded |
