## Review Comment 30002 -- Classification: Suggestion

**Comment by:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs, line 14
**Comment text:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

### Classification Reasoning

This comment is classified as a **suggestion** because:

1. **Suggestive language:** The reviewer uses the phrase "should also" and "would help" rather than directive language. "Should also add" frames this as an additional improvement beyond the core requirement, not a mandatory fix. "Would help" indicates the reviewer is proposing a beneficial optimization rather than identifying a required correction. These are characteristic markers of suggestive rather than imperative feedback.

2. **No convention match -- CONVENTIONS.md:** The repository contains a CONVENTIONS.md file, but no documented convention requiring indexes on nullable timestamp columns, soft-delete columns, or filter-target columns was found. Without an explicit convention mandating index creation alongside column additions, there is no basis for upgrading this suggestion to a code change request via the convention upgrade path.

3. **No convention match -- codebase patterns:** The PR diff contains a single migration file (m0042_sbom_soft_delete). There is no demonstrated codebase pattern of adding indexes alongside new columns in migration files within the PR diff. Without evidence of a consistent, established project practice (e.g., multiple migration files showing `Index::create` for similar columns), the codebase pattern check does not support an upgrade.

4. **Performance optimization, not correctness:** The suggested index is a performance optimization for queries filtering by `deleted_at IS NULL`. While potentially valuable, it does not affect the correctness of the soft-delete feature. The feature will function correctly without the index; queries may just be slower at scale. Performance suggestions without convention backing remain classified as suggestions.

5. **Convention upgrade eligibility -- evaluated and rejected:** The convention upgrade pipeline (Style/Conventions Check 1) was evaluated for this comment. Both CONVENTIONS.md matching (Check 1a) and codebase pattern matching (Check 1b) were checked. Neither produced evidence sufficient to upgrade the classification. The suggestion does not meet the upgrade threshold.

### Action

No sub-task created. This is an optional performance improvement proposed by the reviewer with suggestive language. No project convention (documented or demonstrated) backs an upgrade to code change request.
