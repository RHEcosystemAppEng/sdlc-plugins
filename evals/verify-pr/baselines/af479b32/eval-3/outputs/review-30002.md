# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive, non-imperative language:

1. "should also add" -- the word "also" signals this is an addition beyond the core requirements, not a correction of existing code. "Should also" is softer than a bare imperative "must" or "wrap this in".
2. "would help" -- conditional/hedging language indicating the reviewer is proposing an optimization rather than requiring a fix. Compare to comment 30001 where the reviewer says "you'll have inconsistent state" (a definitive problem statement).
3. "Something like:" -- the reviewer provides a code example prefaced by "something like", indicating this is one possible approach rather than a prescribed fix.

The comment proposes a performance optimization (adding a partial index) rather than identifying a correctness defect. The code functions correctly without the index; the index improves query performance for a specific access pattern.

### Convention Upgrade Eligibility

Checked whether project conventions support upgrading this suggestion to a code change request:

- **CONVENTIONS.md:** The repository structure shows a CONVENTIONS.md file exists at the root, but no content is available in the fixture data. Cannot verify whether index creation for frequently-filtered columns is a documented convention.
- **Codebase patterns:** The PR diff does not contain other migration files to count index creation patterns. Without access to the full codebase, cannot verify whether FK/filter column indexes are a consistent practice.

**Decision:** Without convention data backing an upgrade, this suggestion remains classified as **suggestion**. No sub-task created.
