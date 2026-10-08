## Review Comment 30002 — Classification

**Reviewer:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Comment:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

### Classification: Suggestion

**Reasoning:** The reviewer uses suggestive language rather than directive language. The phrase "should also" in context reads as an additive recommendation ("it would be good to also do this") rather than a mandatory requirement. The word "would help" further indicates this is a performance optimization suggestion, not a correctness fix that must be addressed. The reviewer is proposing a beneficial enhancement (a partial index for query performance) but is not requiring it as a condition for approval. Compare with comment 30001 where "should" is used to flag a correctness bug (inconsistent state) -- here "should also" proposes an optimization that does not affect correctness.

### Convention Upgrade Eligibility

After initial classification as a suggestion, this comment was evaluated for upgrade to code change request based on whether the suggestion matches a documented project convention or a demonstrated codebase pattern.

**Documented conventions:** The repository contains a `CONVENTIONS.md` file (listed in repo-backend.md), but no fixture data for its contents was provided. Without the actual contents of `CONVENTIONS.md`, there is no evidence that adding indexes on soft-delete columns is a documented project convention.

**Demonstrated codebase pattern:** The repository structure shows only one migration (`m0001_initial/mod.rs`). There is no evidence of an established pattern of adding partial indexes alongside soft-delete columns in prior migrations.

**Conclusion:** Since no convention data or demonstrated pattern backs an upgrade, comment 30002 remains classified as **suggestion** and does not result in a sub-task.

**Action:** No sub-task created.
