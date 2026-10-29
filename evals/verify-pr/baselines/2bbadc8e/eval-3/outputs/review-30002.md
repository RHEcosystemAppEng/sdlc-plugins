# Review Comment Classification: Comment 30002

## Comment Details
- **Author:** reviewer-a
- **File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
- **Content:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: **Suggestion**

## Reasoning

The reviewer uses suggestive, non-directive language:
- "should also add" — while "should" can sometimes be directive, combined with "also" it frames this as an additional improvement, not a required fix
- "would help" — conditional language indicating a benefit, not a requirement
- "Something like:" — presents an example as one possible approach, not a mandate

The comment proposes an optimization (adding a partial index for performance) rather than identifying a correctness issue. The PR would function correctly without this index; queries would simply be slower at scale. The reviewer is suggesting an enhancement, not requesting a fix to broken behavior.

### Convention Upgrade Evaluation

Checked whether this suggestion aligns with a documented or demonstrated project convention that would warrant upgrading it to a code change request:

1. **CONVENTIONS.md:** The repository has a CONVENTIONS.md file (visible in repo-backend.md directory tree), but no content from it was provided in the fixture data. Without documented conventions about index creation for nullable columns or migration patterns, there is no CONVENTIONS.md-based evidence to support an upgrade.

2. **Codebase patterns:** The fixture data does not include other migration files or demonstrate an established pattern of creating indexes on nullable filter columns. The only migration in the PR diff (`m0042_sbom_soft_delete/mod.rs`) is the one being reviewed, and it only adds the column. No `Index::create` patterns are visible in the provided diff or repository structure.

3. **Conclusion:** No documented convention (CONVENTIONS.md) or demonstrated codebase pattern (counted instances of similar index creation in migrations) supports upgrading this suggestion to a code change request. General database best practices about indexing are not sufficient for a convention upgrade — the evidence must cite a concrete project-specific convention or counted codebase pattern.

## Action
No sub-task created. Classification remains **suggestion**.
