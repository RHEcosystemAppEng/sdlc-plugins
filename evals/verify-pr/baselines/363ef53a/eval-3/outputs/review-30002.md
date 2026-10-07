# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive, non-directive language:

1. "should also add" -- the phrase "should also" proposes an addition rather than demanding a fix. Unlike a standalone "should" which directs a change, "should also" introduces an optional enhancement on top of the existing work.
2. "would help" -- conditional language indicating the change is beneficial but not required. This is a hallmark of suggestions: the reviewer believes it would be useful but is not insisting.
3. "Something like:" -- the reviewer offers a possible implementation as an example, not as a mandate. The phrase "something like" signals an advisory tone, not a directive.

The comment proposes a performance optimization (adding a partial index) that goes beyond the task's stated requirements. The task description and acceptance criteria do not mention index creation. The reviewer is recommending a best practice rather than identifying a bug or required behavior.

## Convention Upgrade Eligibility

The suggestion was evaluated for convention upgrade (escalation from suggestion to code change request) based on project conventions:

1. **CONVENTIONS.md check:** No CONVENTIONS.md content is available for the trustify-backend repository. There is no documented convention requiring indexes on soft-delete columns or on nullable timestamp columns in migrations.

2. **Codebase pattern check:** The PR diff does not contain evidence of an established codebase pattern for adding indexes alongside column additions in migrations. Only one migration file is present in the diff (m0042_sbom_soft_delete), and it does not demonstrate an existing index creation pattern. Without access to the full codebase, there is no evidence of a counted, consistent pattern of `Index::create` or equivalent in similar migration files.

3. **Performance-related scrutiny:** While adding an index for a frequently-filtered column is a general database best practice, the upgrade decision requires concrete project-specific evidence -- either a documented convention or a demonstrated codebase pattern. General industry best practices are not sufficient grounds for upgrade per the convention upgrade rules.

**Conclusion:** No project convention backs an upgrade. The suggestion remains classified as **suggestion**. No sub-task is created.

## Sub-task Required: No
