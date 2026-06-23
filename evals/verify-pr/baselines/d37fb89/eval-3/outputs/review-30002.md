# Review Comment Classification: 30002

## Comment
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: Suggestion

## Reasoning

The reviewer uses suggestive language:
- "should also add" -- the word "also" indicates this is an additional enhancement beyond the core requirement, not a correction of a defect
- "would help" -- conditional/suggestive framing indicating this is a recommendation, not a requirement
- "Something like:" -- presents a possible implementation rather than a mandatory fix

The comment proposes a performance optimization (adding a partial index) that is not part of the task's acceptance criteria. The reviewer frames it as a helpful addition rather than a required change.

**Convention upgrade check:** The repository has a `CONVENTIONS.md` file at its root. However, without access to its actual content in this verification context, there is no documented evidence that index creation on filter columns is a project convention. The repo-backend key conventions mention SeaORM, Axum, error handling, endpoint registration, and testing patterns -- none reference index creation conventions. Without concrete CONVENTIONS.md evidence or demonstrated codebase pattern counts, this suggestion cannot be upgraded to a code change request.

**Classification: suggestion** -- no sub-task created.
