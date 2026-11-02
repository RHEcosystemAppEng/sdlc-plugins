# Review Comment Classification: #30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Content:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: **Suggestion**

### Reasoning

The reviewer uses suggestive, non-directive language throughout:

1. **"should also add"** — suggestive phrasing. While "should" can be directive in some contexts, "should also" implies an additional improvement rather than a required fix. The word "also" signals this is supplementary to the core migration, not a correction of what exists.
2. **"would help"** — conditional/advisory language indicating a potential benefit, not a requirement. This is a hallmark of suggestion-class feedback.
3. **"Something like:"** — proposes an approach rather than mandating it. The reviewer offers a possible implementation but does not require it.

The comment proposes a performance optimization (partial index on `deleted_at`) rather than identifying a correctness issue. The migration is functionally complete without the index — queries will work correctly, just potentially slower at scale.

### Convention Upgrade Eligibility

Evaluated whether this suggestion matches a documented or demonstrated project convention that would warrant upgrading to a code change request:

1. **CONVENTIONS.md check:** The repository structure (repo-backend.md) indicates a CONVENTIONS.md exists at the repository root, but no CONVENTIONS.md content is available in the fixture data. Without access to the actual conventions documentation, no documented convention match can be established.

2. **Codebase pattern check:** The PR diff does not contain other migration files that demonstrate a pattern of creating indexes for nullable timestamp columns. The single migration file in the diff (`m0042_sbom_soft_delete/mod.rs`) only adds the column without an index. No established codebase pattern of index creation in migrations is demonstrable from the available fixture data.

3. **Performance-related scrutiny:** While the suggestion relates to database performance (index creation), no performance conventions or index creation patterns are documented or demonstrated in the fixture data.

**Upgrade decision: No upgrade.** The suggestion does not match any documented convention in the available data, and no established codebase pattern supports the upgrade. The suggestion remains classified as a **suggestion** based on the reviewer's own language and the absence of convention backing.

### Sub-task Required: No

No sub-task is created. The suggestion classification is retained — suggestive language, no directive requirement, and no project convention backs an upgrade from suggestion to code change request.
