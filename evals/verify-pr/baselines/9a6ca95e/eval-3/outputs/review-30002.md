# Review Comment Classification: 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Review ID:** 20001

## Classification: suggestion

## Reasoning

The reviewer uses the phrases "should also add" and "would help", which are suggestive language rather than imperative. The word "also" frames the index as an addition to the existing migration work, not a correction of a defect. The phrase "would help" is conditional and advisory, indicating a performance recommendation rather than a mandatory requirement. The reviewer provides a SQL example ("Something like:") using hedging language that further signals this is a proposal, not a directive.

Key language indicators:
1. "should also" -- suggestive; "also" implies an optional enhancement beyond the current scope
2. "would help" -- conditional language, not imperative ("must", "needs to", "is required")
3. "Something like:" -- hedging language presenting an example approach, not a prescribed fix
4. No correctness issue identified -- the code works correctly without the index; this is a performance optimization

This contrasts with comment 30001, where the reviewer uses imperative directives ("Wrap the three operations") and identifies a concrete correctness defect (inconsistent state).

## Convention Upgrade Evaluation

The comment was evaluated for convention upgrade eligibility. Convention upgrades apply when a suggestion is backed by an explicit, documented project convention (e.g., in CONVENTIONS.md or equivalent) that mandates the suggested practice.

### Evaluation

1. **CONVENTIONS.md check:** The repository structure shows a `CONVENTIONS.md` file exists at the root of `trustify-backend/`. However, the contents of this file are not available in the provided data. The "Key Conventions" section in the repository structure document describes framework choices (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing patterns, and caching -- none of which mention index creation requirements for migration files.

2. **No documented convention found:** There is no documented convention requiring that migration files include indexes for columns used in WHERE clause filters. Without an explicit, verifiable convention, the suggestion cannot be upgraded.

3. **Codebase pattern check:** While adding indexes for frequently-filtered columns is a general database best practice, best practices alone do not constitute a project convention for upgrade purposes. A convention upgrade requires an explicit project rule, not an inferred industry practice.

### Upgrade Decision

The suggestion is **not upgraded**. No documented project convention backs the requirement to add indexes in migration files for filtered columns. The suggestion remains classified as a **suggestion**.

## Action

No sub-task created. Suggestions are informational feedback that do not require tracked work unless backed by a project convention that upgrades them.
