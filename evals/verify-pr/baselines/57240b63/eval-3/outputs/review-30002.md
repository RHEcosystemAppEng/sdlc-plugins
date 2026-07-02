# Review Comment Classification: 30002

## Comment
**Reviewer**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text**: The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: Suggestion

## Reasoning

The reviewer uses suggestive, non-imperative language:
- "should also add" -- advisory phrasing ("also" implies additive, optional improvement rather than a required fix)
- "would help" -- conditional language indicating a performance optimization that is beneficial but not strictly necessary
- "Something like:" -- proposes one possible approach rather than demanding a specific implementation

Unlike comment 30001, which identifies a correctness bug (inconsistent state), this comment identifies a performance optimization. The current code is functionally correct without the index -- queries will work, just potentially slower at scale.

## Convention Upgrade Evaluation

The repository structure lists a `CONVENTIONS.md` file in the repo root. However, no convention content is available in the fixture data to evaluate whether a project convention mandates indexes on nullable filter columns or similar database performance rules. Without an applicable convention backing an upgrade, this remains classified as a suggestion.

## Sub-task Required: NO

Suggestions do not trigger sub-task creation. Only code change requests produce sub-tasks. No convention was found that would upgrade this suggestion to a code change request.
