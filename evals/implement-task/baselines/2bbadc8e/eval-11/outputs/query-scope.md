# Query-Scope Verification: TC-9209

This document records the query-scope verification analysis performed as part of
Step 9 of the implement-task workflow.

---

## 1. Target Scope Extraction

The task description contains explicit subset-restricting language:

- **"Re-process all SPDX SBOMs"** -- the word "SPDX" qualifies the target set; not all SBOMs.
- **"Only SPDX SBOMs need re-processing -- CycloneDX documents already have supplier information populated during ingestion."** -- explicitly excludes CycloneDX documents.
- **"Production environments have hundreds of thousands of CycloneDX documents alongside a smaller number of SPDX documents."** -- quantifies the scale difference.

**Target scope:** SPDX SBOM documents only (a strict subset of all SBOMs).

---

## 2. Available Filtering Mechanism

The task's Implementation Notes document the filtering mechanism:

> The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores
> metadata about each document. SPDX documents have `{"type": "spdx"}` in their labels,
> while CycloneDX documents have `{"type": "cyclonedx"}`.

This means the database supports a direct filter:

```sql
WHERE labels->>'type' = 'spdx'
```

In SeaORM:

```rust
sbom::Entity::find()
    .filter(Expr::cust("labels->>'type' = 'spdx'"))
```

The filter is expressible at the query level using existing columns. No application-level
post-filtering is necessary.

---

## 3. Query Scope Chosen

**Filtered query:** `sbom::Entity::find().filter(Expr::cust("labels->>'type' = 'spdx'"))`

This loads only SPDX SBOMs from the database, matching the task's target scope exactly.

---

## 4. Rejected Alternatives

### Alternative A: Unfiltered entity load with application-level filtering

```rust
// REJECTED: Do not use this pattern
let all_sboms = sbom::Entity::find().all(db).await?;
let spdx_sboms: Vec<_> = all_sboms
    .into_iter()
    .filter(|s| s.labels.get("type") == Some(&json!("spdx")))
    .collect();
```

**Why rejected:**

- **Performance:** Production has hundreds of thousands of CycloneDX documents. Loading all
  SBOM records into memory when only a fraction are SPDX is wasteful. The memory footprint
  includes the full entity data for every row.
- **Cascading I/O:** The migration fetches the source document for each SBOM it processes.
  If all SBOMs are loaded first and filtered in application code, the filter runs after the
  initial bulk load, but the I/O cost of loading hundreds of thousands of entity records from
  PostgreSQL is already incurred. Furthermore, if filtering were accidentally placed after
  source document retrieval (a plausible coding mistake), the migration would fetch source
  documents for every SBOM in the database.
- **Unnecessary work:** The database can perform this filter efficiently using a GIN or
  btree index on the jsonb column. Pushing the filter to application code bypasses the
  database's query optimizer.

### Alternative B: `Sbom::find()` without any filter (processing all documents)

```rust
// REJECTED: Do not use this pattern
let sboms = sbom::Entity::find().all(db).await?;
for sbom in sboms {
    let source = SourceDocument::find_by_sbom_id(sbom.id).one(db).await?;
    // Parse and extract suppliers for ALL documents, including CycloneDX
}
```

**Why rejected:**

- Violates the task's explicit requirement: "Only SPDX SBOMs need re-processing."
- Violates Acceptance Criterion 2: "CycloneDX documents are not loaded or processed."
- Would attempt to run SPDX-specific supplier extraction on CycloneDX documents, which
  have a different format and would either fail or produce incorrect results.
- Would process hundreds of thousands of unnecessary documents in production.

---

## 5. Performance Impact

| Approach | Records Loaded | Source Docs Fetched | Estimated Impact |
|---|---|---|---|
| Filtered query (`labels->>'type' = 'spdx'`) | SPDX only (thousands) | SPDX only (thousands) | Proportional to target set |
| Unfiltered `Sbom::find()` | All (hundreds of thousands) | Depends on filter placement | 10-100x memory and I/O overhead |

The filtered query ensures the migration's resource consumption is proportional to the
number of documents that actually need re-processing, not the total document count in the
database.

---

## 6. Conclusion

The query scope matches the task's target scope. The `labels->>'type'` column provides
a database-level filter that narrows the query to SPDX documents only. Using an unfiltered
query would load hundreds of thousands of CycloneDX documents unnecessarily, causing
significant performance degradation in production with no functional benefit. The filtered
query is both correct (matches the task requirements) and efficient (avoids unnecessary I/O).
