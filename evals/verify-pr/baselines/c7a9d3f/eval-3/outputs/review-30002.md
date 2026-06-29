# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14
**Content:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like: `CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;`

## Classification: suggestion

## Reasoning

The reviewer proposes adding a partial index on `deleted_at` for performance optimization. The language uses "should also add" which could be interpreted as directive, but the core recommendation is a performance optimization rather than a correctness fix. The absence of an index does not cause incorrect behavior -- queries will still return correct results, just potentially slower for large datasets.

This was evaluated for convention upgrade (Step 6b) by the Style/Conventions sub-agent. The repository's CONVENTIONS.md content was not available for inspection, so no documented convention match could be established. Without concrete evidence from a CONVENTIONS.md section or a counted codebase pattern (e.g., "N migrations in this project include indexes for filtered columns"), the suggestion cannot be upgraded to a code change request per the verify-pr policy.

The suggestion remains classified as a **suggestion** because:
1. No CONVENTIONS.md evidence supports upgrading it
2. No codebase pattern count was available to demonstrate established practice
3. General industry best practices ("indexes help query performance") are explicitly excluded as upgrade evidence per the skill's rules

**Action:** No sub-task created.
