# Review Comment Classification: 30002

## Comment
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Content:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`"

## Classification: suggestion

## Reasoning

The reviewer proposes adding a partial index on `deleted_at` as a performance optimization. While the language uses "should," the overall framing is suggestive: the reviewer says the index "would help" and provides it as a recommendation for query performance, not as a correctness requirement. The code functions correctly without this index; the index is a performance enhancement.

**Convention upgrade assessment:** No upgrade was applied. The Style/Conventions sub-agent could not find a matching convention in CONVENTIONS.md (content not available for the target repository) or a counted codebase pattern in the PR diff demonstrating that partial indexes are an established migration convention. Per the verify-pr skill rules, suggestions must not be upgraded based on general industry best practices alone -- concrete project-specific convention evidence is required. The suggestion remains classified as a suggestion.

## Action
No sub-task created.
