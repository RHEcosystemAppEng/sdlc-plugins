## Review Comment Classification: #30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` (line 14)
**Classification:** suggestion

### Reviewer Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

### Reasoning

The reviewer uses suggestive language: "should also add" and "would help." While the comment proposes a concrete change (adding a partial index), the phrasing frames it as an enhancement that would improve performance rather than a required correction. The reviewer does not identify a bug or broken behavior -- the code works correctly without the index; the index is a performance optimization.

### Convention Upgrade Eligibility

Convention upgrade was evaluated and the suggestion does NOT qualify for upgrade:

1. **CONVENTIONS.md check:** The repository's CONVENTIONS.md (referenced in repo-backend.md) documents key conventions including framework choice (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing, and caching. There is no documented convention requiring indexes on soft-delete columns, foreign key columns, or filter columns in migrations. No section prescribes index creation as part of migration patterns.

2. **Codebase pattern check:** The PR diff contains a single migration file (`m0042_sbom_soft_delete/mod.rs`). The diff does not demonstrate any existing index creation pattern. The repository structure shows only one migration directory (`m0001_initial/`), and we have no evidence of index creation patterns in existing migrations. Without access to the full codebase beyond the fixture data, there is no countable codebase pattern of index creation in migrations to cite.

3. **Performance-related scrutiny:** While the suggestion relates to query performance (partial index for IS NULL filtering), no performance-specific conventions are documented in the repository's conventions. The suggestion is based on general database best practice, not on a project-specific convention or demonstrated codebase pattern.

Since no documented convention in CONVENTIONS.md matches and no demonstrated codebase pattern supports the upgrade, the suggestion remains classified as a **suggestion**. General industry best practices (such as "indexes improve query performance") are explicitly insufficient grounds for convention upgrade per the style-conventions skill rules: "Do NOT upgrade based on general industry best practices, framework documentation, or inferred patterns that are not demonstrated by the specific project's code or documentation."

### Action

No sub-task created. The suggestion is valid feedback but does not meet the threshold for a tracked code change request.
