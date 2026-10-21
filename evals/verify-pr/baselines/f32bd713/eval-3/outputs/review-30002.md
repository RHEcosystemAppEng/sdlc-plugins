# Review Comment Classification: 30002

## Comment Details

- **ID:** 30002
- **Author:** reviewer-a
- **File:** migration/src/m0042_sbom_soft_delete/mod.rs
- **Line:** 14
- **Body:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: SUGGESTION

## Reasoning

The reviewer proposes adding a database index as a performance optimization. The language analysis reveals suggestive rather than directive intent:

1. **"should also add"** -- while "should" can indicate a directive, the word "also" frames this as an addition beyond the core requirement, not a correction of existing code. The phrase "should also" is suggestive language proposing an enhancement rather than demanding a fix.
2. **"would help"** -- conditional language indicating a potential benefit, not a required correction. This is a hallmark of suggestion-level feedback.
3. **"Something like:"** -- explicitly presents the code as one possible approach, not the required implementation. This phrasing signals the reviewer is offering an idea rather than mandating a specific change.

The comment proposes a performance improvement (adding a partial index) rather than identifying a correctness issue. The code without the index is functionally correct; the index is an optimization that may improve query performance.

## Convention Upgrade Eligibility

To determine whether this suggestion should be upgraded to a code change request, I evaluated it against project conventions:

1. **CONVENTIONS.md check:** The repository structure shows a `CONVENTIONS.md` file exists at the root of trustify-backend. However, the fixture data does not include the contents of CONVENTIONS.md. The documented Key Conventions in the repository description (repo-backend.md) cover framework choices (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing patterns, and caching. None of these documented conventions mention index creation requirements for migration files or FK columns.

2. **Codebase pattern check:** The PR diff and repository structure do not demonstrate a consistent pattern of adding indexes in migration files. Only one migration directory is visible (`m0001_initial/`), and the PR adds `m0042_sbom_soft_delete/`. Without evidence of multiple migrations that consistently add indexes for nullable filter columns, there is no demonstrated codebase convention to support upgrading this suggestion.

3. **Performance-related scrutiny:** While the suggestion is performance-related (indexes for query optimization), the lack of documented conventions or demonstrated codebase patterns for index creation in migrations means extra scrutiny does not change the verdict. The suggestion is based on general database best practices (indexing frequently filtered columns), which is not sufficient for a convention upgrade per the skill instructions: "Do NOT upgrade based on general industry best practices."

**Conclusion:** The suggestion does not match a documented project convention in CONVENTIONS.md or a demonstrated codebase pattern. It remains classified as SUGGESTION and does not warrant a sub-task.

## Action

No sub-task created. The suggestion is a valid performance optimization but is not backed by project conventions.
