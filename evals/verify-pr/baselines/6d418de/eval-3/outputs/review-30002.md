# Review Comment Classification: 30002

## Comment
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14
**Text:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: suggestion

## Reasoning
The reviewer proposes adding a partial index on the `deleted_at` column for performance optimization. While the reviewer uses "should also add," the suggestion is about improving query performance rather than fixing a correctness bug — the feature works correctly without the index. The reviewer provides a rationale ("queries filtering by `deleted_at IS NULL` will be frequent") but this is a forward-looking performance optimization, not a requirement from the task specification.

No convention upgrade applies because:
- No CONVENTIONS.md content is available to check for documented index creation patterns
- The repository has only one existing migration (`m0001_initial`), so there is no established codebase pattern of adding indexes alongside column additions to demonstrate this as a project convention
- General database best practices ("indexes improve query performance") are not sufficient grounds for upgrade per the convention upgrade rules

The suggestion remains classified as **suggestion** — no sub-task is created.
