# Review Comment Classification: 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**Reviewer**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Date**: 2026-04-20T14:35:00Z

## Classification: Suggestion

## Reasoning

The reviewer uses suggestive, non-directive language:

1. **"should also add"** -- the phrase "should also" indicates an additive suggestion rather than a mandatory fix. It proposes something supplementary to what already exists, not a correction of a defect.
2. **"would help"** -- this is conditional/advisory language, not a directive. It frames the index as a performance improvement that "would help," not as something required.
3. **"Something like:"** -- the phrasing "something like" signals this is an illustrative example of what could be done, not a prescribed implementation.

Unlike comment 30001 which uses imperative directives to fix a correctness bug, this comment proposes an optimization that could be beneficial but is not framed as a blocking requirement.

## Convention Upgrade Evaluation

The suggestion was evaluated for convention upgrade eligibility. For a suggestion to be upgraded to a code change request, it must match a documented project convention. The repository structure (repo-backend.md) references a `CONVENTIONS.md` file in the repository root, but the fixture data does not include the contents of `CONVENTIONS.md` and there is no documented convention requiring indexes on soft-delete columns or any specific indexing strategy. Without a matching documented convention, this suggestion cannot be upgraded.

## Action

No sub-task created. This remains a suggestion for the author to consider.
