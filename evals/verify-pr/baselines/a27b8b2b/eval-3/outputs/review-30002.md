# Review Comment 30002 — Classification Reasoning

**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs (line 14)
**Classification:** suggestion

## Reviewer Language Analysis

The reviewer uses suggestive, non-imperative language:

- "should also add an index" — "should also" frames this as an addition to consider, not a required change
- "would help" — conditional language indicating the reviewer proposes an improvement, not a mandatory fix

Compare with comment 30001 which uses "should run" (imperative directive) — here "should also" is additive and suggestive, proposing something supplementary rather than correcting a defect.

## Substance Analysis

The comment proposes a performance optimization: adding a partial index on `deleted_at` for the sbom table to speed up queries filtering by `deleted_at IS NULL`. This is a valid optimization but does not address a correctness issue. The endpoint will function correctly without the index; it may just be slower under high load.

## Convention Check

1. **CONVENTIONS.md:** The repository has a CONVENTIONS.md file, but it does not document index creation patterns for migration files or soft-delete columns. No documented convention backs this suggestion.

2. **Codebase patterns:** The PR diff does not contain any `Index::create` calls or partial index patterns in migration files. Without evidence of an established project pattern for adding indexes alongside column additions in migrations, there is no codebase convention to upgrade this suggestion.

3. **Performance scrutiny:** While indexes on frequently-filtered columns are a general database best practice, the Convention Upgrade check requires concrete evidence from the project's CONVENTIONS.md or demonstrated codebase patterns. General industry best practices are not sufficient grounds for upgrading a suggestion to a code change request.

## Classification Decision

**Suggestion.** The reviewer proposes an optional performance optimization using suggestive language ("should also", "would help"). No project convention (documented in CONVENTIONS.md or demonstrated by codebase patterns) supports upgrading this to a code change request.

## Action

No sub-task created.
