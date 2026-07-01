# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: Suggestion

## Reasoning

The reviewer uses suggestive language throughout this comment. The phrases "should also" and "would help" indicate a recommendation rather than a firm requirement. The reviewer proposes an optimization (adding a partial index on `deleted_at`) and provides a sample SQL snippet, but does not frame this as a blocking issue or a correctness concern.

Key language indicators:
- "should also add" -- suggestive phrasing, proposing an addition rather than demanding a fix
- "would help" -- conditional/hedging language indicating this is a nice-to-have
- "Something like:" -- presents a possible implementation rather than a required one

Additionally, no project convention in the fixture data backs upgrading this to a code change request. The repository's CONVENTIONS.md is referenced in repo-backend.md but its contents are not provided in the fixtures, meaning there is no documented convention about index creation patterns for foreign key or filter columns that could justify an upgrade via the convention upgrade mechanism (Step 6b). Without concrete CONVENTIONS.md evidence or a demonstrated codebase pattern of creating indexes on nullable filter columns, this remains classified as a suggestion.

**Action:** No sub-task created.
