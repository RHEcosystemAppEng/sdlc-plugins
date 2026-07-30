# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language throughout: "should also" (additive, not corrective), "would help" (conditional benefit, not a requirement), and "Something like" (proposing one possible approach rather than mandating a specific change). The comment proposes adding an index as a performance optimization but does not frame it as a required fix for correctness or functionality. The SBOM deletion feature works correctly without the index; the index is an optimization that may improve query performance.

### Convention upgrade eligibility evaluation

Per the Style/Conventions sub-agent's Check 1 (Convention Upgrade), suggestions are evaluated for upgrade to code change request if they match a documented or demonstrated project convention.

1. **CONVENTIONS.md check:** The repository structure (repo-backend.md) indicates a `CONVENTIONS.md` file exists at the repository root. However, the fixture data does not include its contents. The Key Conventions section in the repository description does not mention index creation patterns, migration conventions for indexes, or any requirement to add indexes for filtered columns.

2. **Codebase pattern check:** The PR diff and repository structure do not demonstrate a consistent pattern of adding indexes in migration files. Only one migration is visible in the fixture data (`m0001_initial/mod.rs` and the new `m0042_sbom_soft_delete/mod.rs`), and neither shows an index creation pattern. There is no evidence of multiple migration files following an "add index for filtered columns" convention.

3. **Performance-related scrutiny:** While the suggestion relates to performance (index creation), no performance-specific conventions are documented in the available fixture data. General database best practices ("indexes improve query performance") are not sufficient for convention upgrade -- the upgrade requires project-specific evidence from CONVENTIONS.md or demonstrated codebase patterns.

**Conclusion:** No project convention in the fixture data supports upgrading this suggestion to a code change request. The suggestion remains classified as **suggestion**. No sub-task is created.

## Action

No sub-task created. The suggestion does not match a documented or demonstrated project convention.
