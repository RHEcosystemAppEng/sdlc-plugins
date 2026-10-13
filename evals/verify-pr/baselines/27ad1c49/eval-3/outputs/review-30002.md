# Review Comment Classification: 30002

## Comment

- **Author:** reviewer-a
- **File:** `migration/src/m0042_sbom_soft_delete/mod.rs`
- **Line:** 14
- **Body:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: Suggestion

## Reasoning

The reviewer proposes adding a partial index on the `deleted_at` column as a performance optimization. While the language uses "should also add" which has a prescriptive tone, the key word is "also" -- this is an addition beyond the task's core requirements, not a correction of existing behavior. The task description does not mention indexing, and this is a performance improvement rather than a correctness fix.

The classification criteria distinguish between:
- **Code change request:** the reviewer asks for a code modification to fix or complete existing functionality
- **Suggestion:** the reviewer proposes an alternative or enhancement that is not strictly required

This comment falls into the suggestion category because:
1. It proposes adding something new beyond the task scope (an index)
2. The "also" indicates it's supplementary to the required changes
3. It addresses performance, not correctness -- the feature works without the index
4. The reviewer provides a "something like" example, indicating flexibility in approach

### Convention Upgrade Assessment

The Style/Conventions sub-agent evaluated this suggestion for convention upgrade eligibility:
- **CONVENTIONS.md check:** No CONVENTIONS.md content was available for the trustify-backend repository, so no documented convention match was found.
- **Codebase pattern check:** Insufficient evidence within the PR diff alone to establish that index creation for new columns is a consistent project pattern. The diff only contains one migration file (the new one), so no count of similar patterns is available.
- **Performance-related scrutiny:** Applied per the skill's requirement for index-related suggestions. Without documented or demonstrated convention evidence, the suggestion cannot be upgraded based on general best practices alone.

**Result:** Suggestion remains as-is. No sub-task created.
