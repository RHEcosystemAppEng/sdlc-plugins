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

The reviewer uses suggestive language: "should also add" and "would help." The phrase "should also" proposes an addition beyond the current scope rather than identifying a defect in the existing code. The phrase "would help" frames this as a performance improvement that is beneficial but not strictly required for correctness. The reviewer provides a "Something like:" example, further indicating this is a recommendation for an optimization rather than a mandatory fix. The code as written is functionally correct without the index -- queries will work, just potentially slower at scale. This is a performance optimization suggestion, not a correctness fix.

## Convention Upgrade Eligibility

Evaluated whether this suggestion should be upgraded to a code change request based on project conventions:

1. **CONVENTIONS.md check:** The repository has a CONVENTIONS.md file. However, based on the available information, there is no documented convention requiring indexes on `deleted_at` columns or nullable filter columns in migrations. The CONVENTIONS.md documents framework conventions (Axum for HTTP, SeaORM for database) and module patterns, but does not contain a specific indexing convention for soft-delete columns or foreign key columns.

2. **Codebase pattern check:** The PR diff and repository structure do not demonstrate an established pattern of adding indexes in migration files alongside column additions. The migration directory shows only `m0001_initial/mod.rs` as a prior migration, which is insufficient to establish a counted codebase pattern. Without multiple migration files demonstrating consistent index creation for similar columns, there is no quantifiable codebase convention to cite.

3. **Performance-related scrutiny:** While adding a partial index on `deleted_at IS NULL` is a reasonable database optimization, upgrading a suggestion requires either a documented convention in CONVENTIONS.md or a demonstrated codebase pattern with multiple counted occurrences. General database best practices ("indexes improve query performance") are not sufficient grounds for upgrade per the convention upgrade rules.

**Upgrade decision:** No upgrade. The suggestion does not match a documented CONVENTIONS.md convention and lacks a demonstrated codebase pattern (insufficient migration history to establish a counted pattern). It remains classified as a suggestion.

## Action

No sub-task created. This is a suggestion proposing a performance optimization that is not backed by a documented project convention or established codebase pattern.
