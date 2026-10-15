# Query-Scope Verification for TC-9209

This document records the query-scope verification analysis performed as part of
Step 9 of the implement-task skill, following the "Query-scope verification"
sub-section.

---

## 1. Target Scope Extraction

The task description contains explicit subset-restricting language:

- **Title**: "Re-process all **SPDX SBOMs**" -- the qualifier "SPDX" restricts the
  target to a specific document type, not all SBOMs.
- **Description**: "Create a data migration that re-processes all **SPDX SBOMs** to
  extract package supplier information."
- **Explicit exclusion**: "Only SPDX SBOMs need re-processing -- CycloneDX documents
  already have supplier information populated during ingestion."
- **Acceptance criteria**: "CycloneDX documents are not loaded or processed by the
  migration."
- **Implementation notes**: "Production environments have hundreds of thousands of
  CycloneDX documents alongside a smaller number of SPDX documents. The migration
  should only load and process SPDX documents to avoid unnecessary I/O."

**Target scope**: SPDX SBOM documents only (a subset of all SBOM documents).

---

## 2. Query Scope Chosen

**Filtered query at the database level**:

```sql
SELECT id FROM sbom WHERE labels->>'type' = 'spdx'
```

This query uses the `labels` JSONB column on the `sbom` entity to filter directly
at the data source, returning only SPDX documents. CycloneDX documents (which have
`labels->>'type' = 'cyclonedx'`) are excluded by the WHERE clause and are never
loaded into application memory.

---

## 3. Why This Scope Was Chosen

### Available filter mechanism

The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb`.
The task's implementation notes confirm that SPDX documents have
`{"type": "spdx"}` in their labels, while CycloneDX documents have
`{"type": "cyclonedx"}`. This column directly supports filtering by document type
at the query level -- no application-side filtering is needed.

### Why NOT load all documents and filter in application code

An unfiltered query such as `Sbom::find().all(db)` or `Document::all()` would load
every SBOM record from the database -- including the hundreds of thousands of
CycloneDX documents that do not need processing. This approach has severe
consequences:

- **I/O waste**: The database must read, serialize, and transmit hundreds of
  thousands of rows that will be immediately discarded. In production, this could
  mean loading 100,000+ CycloneDX records to process a few thousand SPDX records.
- **Memory pressure**: All loaded records occupy application memory simultaneously
  (or require streaming/pagination logic that adds complexity for no benefit).
- **Migration runtime**: The migration would run orders of magnitude slower than
  necessary, extending database lock durations and increasing the risk of timeouts
  or connection pool exhaustion.
- **Source document loading amplification**: For each loaded SBOM, the migration
  fetches the corresponding `source_document` (raw bytes). Loading CycloneDX source
  documents -- which can be large -- only to discard them compounds the I/O waste.
- **Violation of acceptance criteria**: The acceptance criteria explicitly state
  "CycloneDX documents are not loaded or processed by the migration." An unfiltered
  query that loads all documents and then skips CycloneDX in a loop still loads
  them, violating this criterion.

### Performance impact summary

| Approach | Records loaded | Source docs fetched | Estimated I/O |
|----------|---------------|-------------------|---------------|
| Filtered query (`labels->>'type' = 'spdx'`) | Thousands (SPDX only) | Thousands | Proportional to target set |
| Unfiltered query (`Sbom::find().all()`) | Hundreds of thousands (all types) | Hundreds of thousands (if naive) or thousands (if filtered post-load) | 10-100x higher for record loading alone |

The filtered query reduces the working set by orders of magnitude and ensures the
migration's runtime and resource consumption are proportional to the actual target
set.

---

## 4. Conclusion

The query scope (filtered by `labels->>'type' = 'spdx'`) matches the task's target
scope (SPDX SBOMs only). The filter is expressible at the database level using the
existing `labels` JSONB column, and using it avoids loading hundreds of thousands of
irrelevant CycloneDX records. No scope mismatch exists. No broader query is needed
or justified.
