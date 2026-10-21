# Query-Scope Verification: TC-9209

## What the Task Targets

The task description says: "Create a data migration that re-processes **all SPDX SBOMs** to extract package supplier information." It further clarifies: "**Only SPDX SBOMs** need re-processing -- CycloneDX documents already have supplier information populated during ingestion."

This is a **subset operation**: the task targets SPDX SBOMs specifically, not all SBOMs in the database.

## Target Scope Extraction

Subset-restricting language identified in the task description:

- "all SPDX SBOMs" -- type qualifier restricting to SPDX format only
- "Only SPDX SBOMs need re-processing" -- explicit exclusion of CycloneDX
- "CycloneDX documents already have supplier information populated" -- rationale for exclusion

The target scope is: **SPDX-type SBOM documents only** (a subset of all SBOMs).

## Available Filtering Mechanism

The task's Implementation Notes describe the filtering mechanism:

> The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb` that stores metadata about each document. SPDX documents have `{"type": "spdx"}` in their labels, while CycloneDX documents have `{"type": "cyclonedx"}`.

This means the `labels` jsonb column directly supports filtering by document type at the database query level using:

```sql
SELECT * FROM sbom WHERE labels->>'type' = 'spdx';
```

In SeaORM, this can be expressed as a filtered query using JSON path extraction on the `labels` column.

## Query Scope Chosen: FILTERED

The migration must use a **filtered query** that selects only SPDX SBOMs:

```
Sbom::find().filter(labels->>'type' = 'spdx')
```

This filters at the data source (PostgreSQL), returning only the SPDX subset.

## Why NOT an Unfiltered Query

An unfiltered query such as `Sbom::find().all(db)` (equivalent to `SELECT * FROM sbom`) or `Document::all()` followed by application-level filtering (e.g., `if record.labels.type == "spdx" { ... }`) would be incorrect for the following reasons:

### 1. Performance Impact

The Implementation Notes state: "Production environments have **hundreds of thousands of CycloneDX documents** alongside a **smaller number of SPDX documents**."

An unfiltered query would:

- **Database I/O**: Read hundreds of thousands of CycloneDX rows from disk that are immediately discarded. This creates unnecessary load on the database, potentially impacting other queries during the migration window.
- **Network transfer**: Transfer all those rows from PostgreSQL to the application, consuming network bandwidth and increasing migration latency.
- **Application memory**: Materialize hundreds of thousands of `Sbom` structs in application memory, most of which serve no purpose. Depending on the ORM's batch strategy, this could cause memory pressure or OOM conditions.
- **Wall-clock time**: The migration would take orders of magnitude longer than necessary, processing (or at least loading and discarding) records that do not need any work.

With a filtered query, only the "smaller number of SPDX documents" are loaded, making the migration dramatically faster and lighter on resources.

### 2. Semantic Correctness

The task explicitly states "CycloneDX documents are not loaded or processed by the migration" as an acceptance criterion. An unfiltered query that loads all records and then filters in application code technically "loads" CycloneDX documents even if it does not "process" them. A filtered query satisfies both the letter and spirit of the requirement.

### 3. Available Filter Column

The `labels` jsonb column with `{"type": "spdx"}` / `{"type": "cyclonedx"}` values is purpose-built for this kind of filtering. PostgreSQL supports efficient jsonb extraction (`labels->>'type'`), and a GIN or btree index on the expression (if present) would make the filtered query even faster. There is no technical reason to avoid database-level filtering.

## Conclusion

| Aspect | Value |
|--------|-------|
| Target scope | SPDX SBOMs only (subset of all SBOMs) |
| Query scope chosen | Filtered: `WHERE labels->>'type' = 'spdx'` |
| Filtering mechanism | `sbom.labels` jsonb column, type key |
| Rationale | Production has hundreds of thousands of CycloneDX records; loading them would cause excessive I/O, memory usage, and migration runtime for zero benefit. The labels column supports direct filtering at the database level. |
| Anti-patterns avoided | `Sbom::find().all()` (unfiltered load), `Document::all()` (unfiltered load), application-level `if type == "spdx"` filtering after loading all records |
