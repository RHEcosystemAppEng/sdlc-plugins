# Review Comment Classification: 30002

## Comment

- **ID:** 30002
- **Author:** reviewer-a
- **File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
- **Body:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language rather than imperative language:
- "should also" -- the word "also" signals an additive, optional enhancement beyond the core requirement, not a mandatory fix
- "would help" -- conditional/suggestive phrasing indicating a potential improvement, not a required change
- "Something like:" -- tentative framing offering one possible approach, not a specific directive

This is a performance optimization suggestion. While adding an index is generally good practice, the reviewer does not frame it as a requirement or identify a concrete defect. The phrasing indicates the reviewer is proposing an enhancement that would improve query performance but is not strictly necessary for correctness.

### Convention upgrade check

No upgrade is warranted because:
1. **CONVENTIONS.md:** The repository structure (repo-backend.md) shows a `CONVENTIONS.md` exists, but it does not document a convention requiring indexes on nullable timestamp columns or on soft-delete filter columns.
2. **Codebase patterns:** The PR diff and repository structure do not demonstrate a consistent pattern of adding indexes in migration files. Only one migration is visible (`m0001_initial`) and the PR adds `m0042_sbom_soft_delete`. There is insufficient evidence of a project-wide convention of adding indexes alongside column additions.
3. **Performance scrutiny:** While indexes for frequently-filtered columns are a database best practice, general industry best practices alone do not justify upgrading a suggestion to a code change request. The upgrade evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern.

The suggestion remains classified as **suggestion**. No sub-task created.
