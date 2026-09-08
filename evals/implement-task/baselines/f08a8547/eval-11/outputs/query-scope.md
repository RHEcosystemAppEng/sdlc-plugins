# Query-Scope Verification: TC-9209

## What the Task Targets

The task description specifies a **subset** of SBOM documents: **SPDX SBOMs only**.

Key subset-restricting language from the task description:

- "re-processes all **SPDX** SBOMs" (title and description)
- "**Only SPDX SBOMs** need re-processing -- CycloneDX documents already have supplier information populated during ingestion"
- Acceptance criterion: "CycloneDX documents are **not loaded or processed** by the migration"
- Implementation note: "Production environments have **hundreds of thousands of CycloneDX documents** alongside a **smaller number of SPDX documents**. The migration should only load and process SPDX documents to avoid unnecessary I/O."

The task targets **SPDX SBOMs** -- a subset of all SBOM documents in the database,
distinguished from CycloneDX documents by the `labels->>'type'` JSONB field.

## Query Scope Chosen

**Filtered query at the database level:**

```sql
SELECT id FROM sbom WHERE labels->>'type' = 'spdx'
```

This query restricts the result set to only SPDX documents by filtering on the
`labels` JSONB column. CycloneDX documents (which have `labels->>'type' = 'cyclonedx'`)
are excluded from the result set entirely.

## Why This Scope

### The alternative (rejected): Unfiltered query with application-level filtering

An unfiltered approach would look like:

```rust
// BAD: loads ALL SBOMs including hundreds of thousands of CycloneDX documents
let all_sboms = Sbom::find().all(db).await?;
for sbom in all_sboms {
    if sbom.labels.get("type") == Some("spdx") {
        // process...
    }
}
```

This approach is wrong for two reasons:

1. **Performance**: Production has hundreds of thousands of CycloneDX documents.
   Loading them all into memory only to skip them wastes I/O, memory, and database
   connection time. The migration would read orders of magnitude more data than it
   needs.

2. **Acceptance criteria violation**: The acceptance criteria explicitly state
   "CycloneDX documents are not loaded or processed." An unfiltered query loads
   CycloneDX documents even if it skips processing them.

### The chosen approach: Database-level filtering

```rust
// GOOD: loads ONLY SPDX SBOMs at the database level
let spdx_sboms = db.query_all(Statement::from_string(
    DbBackend::Postgres,
    "SELECT id FROM sbom WHERE labels->>'type' = 'spdx'".to_string(),
)).await?;
```

This is correct because:

1. **Filter is expressible at the data source**: The `labels` JSONB column supports
   the `->>` operator for key extraction, and the `type` key reliably distinguishes
   SPDX from CycloneDX documents. There is no need to load documents and inspect
   them in application code.

2. **Performance**: Only the relevant SPDX records are transferred from the database,
   reducing I/O proportionally to the actual target set size.

3. **Matches task intent**: The task says "re-process all SPDX SBOMs" -- the query
   returns exactly the set of SPDX SBOMs and nothing else.

4. **Satisfies acceptance criteria**: CycloneDX documents are never loaded from the
   database, fulfilling the "not loaded or processed" requirement.

## SKILL.md Query-Scope Verification Checklist

| Step | Result |
|------|--------|
| **Extract target scope** | Task targets "all SPDX SBOMs" -- subset restricted by document type (SPDX vs CycloneDX) |
| **Compare query scope** | Query uses `WHERE labels->>'type' = 'spdx'` -- filters to the target subset at the database level |
| **Flag scope mismatches** | No mismatch. A broad query (`Sbom::find().all()`) would be a scope mismatch because the `labels->>'type'` column supports filtering. The chosen query correctly narrows to the target subset. |
| **Accept intentional broad queries** | Not applicable -- filtering IS expressible at the query level and is used. |

## Summary

The query scope matches the task's target scope. The migration queries only SPDX SBOMs
by filtering on `labels->>'type' = 'spdx'` at the SQL level. CycloneDX documents are
excluded from the query results entirely, avoiding unnecessary I/O in production
environments where CycloneDX documents vastly outnumber SPDX documents.
