# Review Comment 30002 — Classification

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14

## Classification

**suggestion**

## Reasoning

The reviewer uses suggestive language throughout: "should also add" (additive, not corrective), "would help" (conditional benefit, not a requirement). The comment proposes a performance optimization — adding a partial index to speed up queries that filter on `deleted_at IS NULL`. This is a forward-looking improvement rather than a fix for broken behavior. The migration as written is functionally correct; it adds the `deleted_at` column with a NULL default, which is exactly what the task requires.

### Convention Upgrade Eligibility Evaluation

To determine whether this suggestion should be upgraded to a code change request, the following checks were performed:

1. **CONVENTIONS.md**: The repository structure listing shows a `CONVENTIONS.md` file exists at the repository root, but no content from this file is available in the fixture data. Without access to the actual conventions document, there is no documented project convention requiring indexes on soft-delete columns or on any new nullable columns added via migrations.

2. **Demonstrated codebase pattern**: The fixture data includes only one migration (`m0001_initial/mod.rs`) in the migration directory, and its content is not available. There is no demonstrated pattern in the available data showing that migrations in this project routinely include index creation alongside column additions.

3. **Key Conventions section**: The repository's Key Conventions section in `repo-backend.md` documents conventions around framework choice (Axum, SeaORM), module structure, error handling, endpoint registration, response types, query helpers, testing, and caching. None of these conventions address database indexing strategy or migration completeness requirements.

**Conclusion**: No documented convention or demonstrated codebase pattern supports upgrading this suggestion to a code change request. The comment remains classified as a **suggestion**. While the index is a reasonable performance consideration, it is not required for correctness and does not violate any known project standard. No sub-task is created for this comment.
