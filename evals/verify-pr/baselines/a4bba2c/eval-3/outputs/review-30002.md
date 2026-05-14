# Review Comment Classification: 30002

## Comment
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: code change request

## Reasoning
The reviewer uses directive language ("should also add") and provides a concrete code change with a specific SQL example. The reviewer identifies a performance concern: the list endpoint filters by `deleted_at IS NULL` on every query, and without an index this will degrade as the table grows. The reviewer provides the exact index definition needed. While this could be interpreted as a suggestion, the directive "should also add" combined with the performance justification (frequent queries filtering by this column) makes this a code change request. Additionally, adding indexes for frequently-queried columns in migrations is a common database best practice that reviewers typically require rather than merely suggest.

## Action
Sub-task created to address this feedback.
