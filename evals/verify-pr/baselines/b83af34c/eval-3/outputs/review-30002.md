# Review Comment Classification: #30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: SUGGESTION

## Reasoning

The reviewer is proposing an enhancement rather than identifying a defect or requesting a required fix. Key indicators:

1. **Suggestive language:** "should also add" uses additive phrasing ("also") indicating this is something extra beyond the current implementation, not a correction of something wrong. The word "also" signals an additional improvement, not a fix for existing code.

2. **Speculative benefit language:** "would help" is conditional/suggestive, indicating the reviewer believes this would be beneficial but is not asserting it is required. Compare with comment #30001 which says "you'll have inconsistent state" (definitive problem statement).

3. **Performance optimization, not correctness:** The suggestion is about query performance optimization. The code functions correctly without the index; adding it improves performance for a specific query pattern. This is an enhancement, not a bug fix.

4. **Provides a sample rather than a mandate:** The reviewer says "Something like:" followed by a SQL example, indicating a suggested approach rather than a required implementation.

## Convention Upgrade Eligibility Check

Checked whether this suggestion should be upgraded to a code change request based on project conventions:

1. **CONVENTIONS.md check:** The repository structure indicates a `CONVENTIONS.md` file exists at the repository root. However, no content from CONVENTIONS.md documents a convention requiring indexes on soft-delete columns or on columns used for `IS NULL` filtering. Without a documented convention backing this pattern, a CONVENTIONS.md-based upgrade is not warranted.

2. **Codebase pattern check:** The PR diff does not contain evidence of existing index creation patterns in migration files (e.g., `Index::create` usage). The only migration in the diff (`m0042_sbom_soft_delete`) adds a column but no indexes. Without evidence of a consistent codebase pattern of adding indexes alongside soft-delete columns, a codebase-pattern-based upgrade is not warranted.

3. **Performance scrutiny:** While this is a performance-related suggestion that receives extra scrutiny per the Style/Conventions sub-agent rules, the scrutiny only elevates suggestions to code change requests when backed by project-specific conventions or demonstrated codebase patterns. General database best practices (indexes on frequently-filtered columns) do not qualify as upgrade evidence.

**Upgrade decision: NOT UPGRADED.** No project convention (documented or demonstrated) backs this suggestion. It remains classified as a suggestion.

## Action

No sub-task created. The suggestion is noted but does not meet the threshold for automatic sub-task creation. The reviewer or PR author can decide whether to adopt the suggestion.
