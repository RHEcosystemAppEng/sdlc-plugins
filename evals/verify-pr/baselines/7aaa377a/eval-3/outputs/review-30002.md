# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`
**Line:** 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: SUGGESTION

## Reasoning

The reviewer uses suggestive, additive language rather than directive language:

1. **"should also add"** -- the phrase "should also" frames this as an additional improvement on top of the existing work, not a required correction. Compare with comment 30001 which says "should run" to fix a correctness bug. Here "should also" proposes something supplementary.
2. **"would help"** -- "would help" is conditional/suggestive language indicating this is a performance optimization that would be beneficial, not a correctness requirement. The code functions correctly without the index; the index improves query performance.
3. **"Something like:"** -- the reviewer provides an example with tentative framing ("Something like"), indicating they are proposing an approach rather than prescribing a required change.

The suggestion is about a performance optimization (adding a partial index) rather than a correctness fix. The migration works correctly without the index -- queries will still return correct results, just potentially slower at scale.

### Convention Upgrade Eligibility

This suggestion was evaluated for convention upgrade eligibility per the Style/Conventions sub-agent's Check 1 (Convention Upgrade):

1. **CONVENTIONS.md check:** The target repository (trustify-backend) has a CONVENTIONS.md file. However, the documented Key Conventions in the repository description cover framework choices (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing patterns, and caching. There is no documented convention requiring indexes on `deleted_at` columns, partial indexes for soft-delete patterns, or indexes on foreign key columns in migrations.

2. **Codebase pattern check:** The PR diff does not contain evidence of an established codebase pattern for adding indexes alongside column additions in migrations. The migration file follows the standard `Table::alter().add_column()` pattern without any `Index::create` usage visible in the diff context.

3. **Performance-related scrutiny:** While adding indexes is a general database best practice, the upgrade decision requires a concrete CONVENTIONS.md section or a counted codebase pattern from this specific project. General industry best practices ("indexes are good for frequently filtered columns") are explicitly excluded from upgrade evidence per the Convention Upgrade rules.

**Upgrade decision: NOT UPGRADED.** No project convention backs this suggestion. It remains classified as a **suggestion**. The reviewer's feedback is valid performance advice, but without a documented or demonstrated project convention requiring it, it does not warrant automatic elevation to a code change request.

## Action

No sub-task created. Suggestions that are not backed by a documented project convention or demonstrated codebase pattern do not trigger sub-task creation.
