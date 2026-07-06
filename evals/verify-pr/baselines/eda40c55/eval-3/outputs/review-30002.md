# Review Comment Classification: Comment 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: SUGGESTION

## Reasoning

The reviewer uses suggestive, non-imperative language: "should also add" and "would help". These phrases propose an enhancement rather than mandate a required change. The reviewer is recommending a performance optimization (a partial index on `deleted_at`) that would benefit query performance, but does not identify a correctness issue or bug.

Key indicators supporting suggestion classification:
1. **Suggestive language**: "should also" (additive suggestion, not fixing something broken) and "would help" (benefit-oriented, not requirement-oriented)
2. **Performance optimization, not correctness fix**: the code works correctly without the index -- the index improves query performance but is not required for functional correctness
3. **No project convention backs an upgrade**: the repository's CONVENTIONS.md content is not available in the fixture data, and the Key Conventions section in the repository structure document does not document any indexing conventions or patterns. Without evidence from CONVENTIONS.md or demonstrated codebase patterns (e.g., other migrations consistently creating indexes for filtered columns), there is no basis to upgrade this suggestion to a code change request.
4. **No established codebase pattern**: the PR diff and repository structure do not provide evidence of a consistent pattern of adding indexes in migration files. The single migration shown (m0001_initial) is not sufficient to establish a convention.

### Convention Upgrade Check

- **CONVENTIONS.md match**: No -- CONVENTIONS.md content not available; the repository's Key Conventions do not mention database indexing patterns
- **Codebase pattern match**: No -- insufficient evidence of a consistent indexing pattern in migration files
- **Performance-related scrutiny**: Applied, but general database best practices ("indexes improve query performance") are not sufficient for upgrade -- the upgrade evidence must cite a concrete project convention or counted codebase pattern

**Conclusion**: This remains classified as SUGGESTION. No sub-task created.
