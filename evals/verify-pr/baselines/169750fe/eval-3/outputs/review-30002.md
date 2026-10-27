# Review Comment Classification: #30002

## Comment Details
- **Author:** reviewer-a
- **File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
- **Content:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: **Suggestion**

## Reasoning

The reviewer uses suggestive, non-directive language:

1. **"should also add"** — While "should" can sometimes be directive, in combination with "also" it reads as an additional recommendation rather than a requirement. The reviewer is proposing an optimization, not flagging a correctness issue.
2. **"would help"** — This is explicitly suggestive language. "Would help" acknowledges that the system works without the change but could be improved.
3. **"Something like:"** — The code example is presented as an illustration of a possible approach, not a prescriptive instruction. "Something like" signals flexibility in implementation.

The suggestion addresses a performance optimization (indexing for query filtering), not a correctness or data integrity issue. The system functions correctly without the index; it would merely perform better with one.

### Convention Upgrade Eligibility

Evaluated whether this suggestion matches a documented or demonstrated project convention that would warrant upgrading it to a code change request:

- **CONVENTIONS.md check:** The repository has a `CONVENTIONS.md` file (per repo-backend.md), but no convention about mandatory indexing on nullable filter columns was provided in the fixture data.
- **Codebase pattern check:** No evidence from the fixture data demonstrates a consistent pattern of adding partial indexes on nullable columns in migrations.
- **Conclusion:** No documented convention or established codebase pattern backs an upgrade from suggestion to code change request. The suggestion remains classified as a suggestion.

## Action
- **Sub-task creation:** NO
- **Reason:** Suggestions that are not backed by documented conventions or established codebase patterns do not trigger sub-task creation.
