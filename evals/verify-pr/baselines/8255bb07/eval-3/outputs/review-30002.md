# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language ("should also add", "would help") rather than directive language identifying a defect. The phrase "should also" proposes an addition beyond the current scope, and "would help" frames the index as a performance optimization rather than a correctness requirement. The reviewer is suggesting an enhancement -- adding a partial index for query performance -- not flagging a bug or missing requirement from the task specification.

The task's acceptance criteria do not require any indexes on the `deleted_at` column; they only require that the column be added with a NULL default. The suggestion is a valid performance consideration but is not required by the task.

## Convention Upgrade Eligibility Assessment

Convention upgrade was evaluated to determine whether this suggestion should be elevated to a code change request:

1. **CONVENTIONS.md check:** The repository's CONVENTIONS.md was examined for documented conventions regarding index creation on migration columns, partial indexes, or performance-related migration patterns. No matching convention was found that requires indexes on nullable filter columns or soft-delete columns.

2. **Codebase pattern check:** The PR diff and repository structure were examined for consistent patterns of index creation in migration files. The repository contains only the initial migration (`m0001_initial/mod.rs`), which does not provide sufficient evidence of a consistent pattern of creating indexes alongside column additions. Without multiple migration files demonstrating this practice, there is no established codebase convention to cite.

3. **Performance-related scrutiny:** Performance-related suggestions receive extra scrutiny per the convention upgrade rules. However, the upgrade decision requires evidence from the specific project's CONVENTIONS.md or demonstrated codebase patterns -- general database best practices (such as "indexes improve query performance") are explicitly excluded as upgrade evidence. Adding a partial index is sound database practice, but without project-specific convention backing, it cannot be upgraded.

**Upgrade decision: NOT upgraded.** The suggestion does not match any documented convention in CONVENTIONS.md, and no established codebase pattern of index creation in migrations was found to justify an upgrade. It remains classified as a suggestion.

## Action

No sub-task created. The suggestion is valid but optional -- no project convention backs an upgrade to a code change request.
