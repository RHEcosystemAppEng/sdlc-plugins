# Query-Scope Verification: TC-9209

## What the Task Targets

The task description contains explicit subset-restricting language:

> "Create a data migration that re-processes **all SPDX SBOMs** to extract package
> supplier information"

> "**Only SPDX SBOMs** need re-processing -- CycloneDX documents already have supplier
> information populated during ingestion."

**Target scope**: SPDX SBOM documents only. CycloneDX documents are explicitly excluded.

## Available Filtering Mechanism

The task's Implementation Notes describe the filtering mechanism:

> "The `sbom` entity (`entity/src/sbom.rs`) has a `labels` column of type `jsonb`
> that stores metadata about each document. SPDX documents have `{"type": "spdx"}`
> in their labels, while CycloneDX documents have `{"type": "cyclonedx"}`."

The `labels` JSONB column on the `sbom` table supports filtering at the database
level using `labels->>'type' = 'spdx'`. This is a standard PostgreSQL JSONB
operator that can be used in a WHERE clause.

## Query Scope Chosen

**Filtered query**: `SELECT ... FROM sbom WHERE labels->>'type' = 'spdx'`

The migration queries only SPDX SBOM records by filtering on the `labels` JSONB
column. This pushes the subset restriction to the database level rather than loading
all records and filtering in application code.

## Why This Scope

### Performance impact

The Implementation Notes state:

> "Production environments have hundreds of thousands of CycloneDX documents alongside
> a smaller number of SPDX documents. The migration should only load and process SPDX
> documents to avoid unnecessary I/O."

An unfiltered query (e.g., `Sbom::find()` or `SELECT * FROM sbom`) would:
- Load hundreds of thousands of CycloneDX records from the database into application memory
- Require application-level type checking to skip CycloneDX records
- Potentially trigger source document fetches for CycloneDX records before the type
  check occurs (depending on implementation order)
- Cause unnecessary I/O, memory pressure, and migration runtime in production

A filtered query avoids all of this by returning only the SPDX subset from the database.

### Correctness

The filter also serves a correctness function: CycloneDX documents already have
supplier information populated during ingestion. Processing them again could
overwrite correct data with incorrectly parsed data (since the `suppliers()`
function is designed for SPDX format, not CycloneDX).

### Scope match assessment

| Dimension | Target Scope | Actual Query Scope | Match? |
|---|---|---|---|
| Document type | SPDX only | `labels->>'type' = 'spdx'` | Yes |
| Record count | All SPDX SBOMs | No additional LIMIT/pagination | Yes |
| Exclusions | CycloneDX documents | Excluded by WHERE clause | Yes |

**Result**: The query scope matches the task's target scope. The available JSONB
filter is used to restrict the query at the data source, avoiding unnecessary I/O
for the hundreds of thousands of CycloneDX documents in production.

### Skill guidance reference

This analysis follows the implement-task skill's "Query-scope verification" sub-step
(Step 9), which requires:

1. Extracting target scope from the task Description (done: "all SPDX SBOMs")
2. Comparing query scope against the target subset (done: filtered query matches)
3. Flagging scope mismatches when a narrower query is possible but not used
   (not applicable: the filtered query is used)
4. Accepting intentional broad queries only when filtering cannot be expressed at the
   query level (not applicable: filtering is expressible and used)

No scope mismatch flag is needed -- the implementation correctly filters at the
database level using the available `labels->>'type'` column.
