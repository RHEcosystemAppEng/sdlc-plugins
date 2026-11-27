# Query-Scope Verification — TC-9209 (Step 9, check 12)

The check fires because the task implements a data migration that iterates over database
records, which is a batch operation.

## 1. Target scope (from the task Description)

- "re-processes **all SPDX SBOMs**". The type qualifier is SPDX.
- "Only SPDX SBOMs need re-processing — CycloneDX documents already have supplier information."
- Implementation Notes: production has **hundreds of thousands of CycloneDX** documents
  and a **smaller number of SPDX** documents. "The migration should only load and process
  SPDX documents to avoid unnecessary I/O."
- Acceptance criterion: "CycloneDX documents are **not loaded** or processed."

**Target scope: the subset of `sbom` rows whose `labels` JSONB has `type = "spdx"`.**

## 2. Available filter at the data source

- `entity/src/sbom.rs` has a `labels` column of type `jsonb`. SPDX rows hold `{"type": "spdx"}`
  and CycloneDX rows hold `{"type": "cyclonedx"}`.
- PostgreSQL can filter on it directly with `labels->>'type' = 'spdx'` or
  `labels @> '{"type":"spdx"}'::jsonb`. The containment form can use a GIN index on `labels`.

## 3. Query scope chosen

```sql
SELECT id FROM sbom
WHERE labels @> '{"type":"spdx"}'::jsonb
  AND id > $last_id
ORDER BY id
LIMIT 500;
```

In SeaORM this is `sbom::Entity::find().select_only().column(Id).filter(Expr::cust(r#"labels @> '{"type":"spdx"}'::jsonb"#))`,
keyset-paginated. `SourceDocument::find_by_sbom_id(id)` is then called **only for the IDs returned**.

### Rejected alternative

`sbom::Entity::find().all(db)` (or `Document::all()`) followed by an in-Rust check
`if labels["type"] == "spdx"`. This loads every SBOM row, potentially hundreds of
thousands of CycloneDX rows, into memory, and it is a short step from there to
fetching source documents before filtering. That breaks the "CycloneDX not loaded"
acceptance criterion and the I/O guidance in the Implementation Notes.

## 4. Why

| Aspect | Unfiltered (`all()` + Rust filter) | Chosen (SQL-filtered, keyset batches) |
|---|---|---|
| Rows read from `sbom` | every SBOM (mostly CycloneDX) | SPDX only |
| Source documents fetched | risk of all of them | SPDX only |
| Memory | entire table at once | at most 500 IDs per batch |
| AC "CycloneDX not loaded" | violated | satisfied |

- The filter can be expressed at the query level, so per rule 3 of the check the narrower
  query is required. No "full dataset needed" rationale applies.
- `@>` is preferred over `->>` because a GIN index on `labels` can serve it. If no index
  exists, both still filter in the database rather than in the application. Adding an
  index is outside the task's scope; I would mention it in the PR as a suggestion and
  not add it.
- Keyset pagination (`id > last_id`) keeps memory bounded and avoids OFFSET scans when
  there are many SPDX documents. Selecting only `id` avoids pulling the label/metadata
  payload.
- The secondary queries are scoped too. The `sbom_package` UPDATEs filter on
  `sbom_id = <spdx id>` plus the package identifier, so CycloneDX `sbom_package` rows are
  never touched. Test `backfill_skips_cyclonedx` verifies this.
- Edge case: if any legacy SPDX row lacks the `type` label, the filter would miss it.
  Step 4 would include a quick check, `SELECT count(*) FROM sbom WHERE labels->>'type' IS NULL`,
  against a test DB or fixtures. If such rows exist, I would raise it with the user rather
  than widen the query silently.

## Result

**Check 12 — PASS.** The target scope (SPDX only) matches the actual query scope
(`labels @> '{"type":"spdx"}'`), and the filtering happens at the database level. A code
comment above the query in `m0042_backfill_suppliers/mod.rs` records the scope and the reason for it.
