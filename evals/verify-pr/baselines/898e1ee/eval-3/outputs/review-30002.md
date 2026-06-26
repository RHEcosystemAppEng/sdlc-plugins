# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: suggestion

## Reasoning

The reviewer proposes an optimization -- adding a partial index on the `deleted_at` column to improve query performance for the `deleted_at IS NULL` filter. The language uses "should also add" which could be interpreted as directive, but the core feedback is a performance optimization suggestion rather than a correctness requirement. The SBOM deletion endpoint and list filtering will function correctly without this index; it is a query performance improvement.

Convention upgrade was considered (Step 6b): No CONVENTIONS.md content was available to verify whether the project documents an index-creation convention for new columns. The PR diff contains only one migration file and does not include evidence of `Index::create` usage patterns in other migrations. Without concrete evidence from CONVENTIONS.md or counted codebase patterns demonstrating that partial indexes are an established convention in this project, the suggestion cannot be upgraded. General database best practices alone are not sufficient for upgrade per the skill rules.

## Action

No sub-task created. The suggestion remains classified as a suggestion -- it proposes a valid optimization but is not backed by documented project conventions or demonstrated codebase patterns.
