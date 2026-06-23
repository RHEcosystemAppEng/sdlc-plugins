# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language rather than directive language:

1. **"should also add"** -- while "should" can be directive, the addition of "also" softens it to a suggestion of something supplementary rather than a strict requirement. The comment proposes an enhancement on top of the existing migration, not a correction of a defect.
2. **"would help"** -- conditional language indicating the reviewer believes this is beneficial but not strictly necessary. This phrasing acknowledges the system will function without the change.
3. **"Something like:"** -- explicitly frames the provided SQL as an example approach, not a mandated implementation. This is characteristic of suggestion-class feedback where the reviewer offers a possible direction.

The comment proposes a performance optimization (adding a partial index) rather than identifying a correctness bug or missing requirement. The SBOM deletion feature will work correctly without this index; the index would improve query performance for filtered list operations.

### Convention Upgrade Eligibility Analysis

Per Step 4b/6b of the verify-pr skill, suggestions must be checked for convention upgrade eligibility. A suggestion is upgraded to a code change request only if it matches a documented convention in CONVENTIONS.md or is demonstrated by consistent codebase usage patterns.

1. **CONVENTIONS.md check:** The fixture data includes a `repo-backend.md` that shows a `CONVENTIONS.md` file exists in the repository structure. However, no CONVENTIONS.md content is available in the fixture data for analysis. Without access to the actual CONVENTIONS.md content, it is impossible to determine whether the project documents an index creation convention for migration files.

2. **Codebase pattern check:** The PR diff contains only one migration file (`m0042_sbom_soft_delete/mod.rs`), which does not include any index creation. The repository structure shows only `m0001_initial/` as another migration. Without access to the full codebase to count `Index::create` occurrences across migration files, a codebase pattern cannot be established from the available fixture data.

3. **Upgrade decision:** Since neither a documented CONVENTIONS.md convention nor a demonstrated codebase pattern can be confirmed from the available data, the suggestion is **NOT upgraded**. General industry best practices (e.g., "indexes improve query performance") are explicitly excluded as upgrade evidence per the Style/Conventions sub-agent's Check 1d rules.

## Action

No sub-task created. The classification remains "suggestion" -- the reviewer proposes an optional performance enhancement using suggestive language, and no project convention backing was found to warrant an upgrade.
