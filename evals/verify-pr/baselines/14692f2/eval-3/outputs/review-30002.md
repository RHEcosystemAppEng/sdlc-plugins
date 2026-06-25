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

## Classification: Suggestion

## Reasoning

The reviewer uses suggestive, non-directive language:

1. **"should also"** -- While "should" can sometimes be directive, the addition of "also" softens it to a suggestion of something supplementary, not a required fix to existing code.
2. **"would help"** -- This is clearly suggestive language. "Would help" indicates the reviewer believes it is beneficial but is not requiring it. Compare with directive phrasing like "is needed" or "must be added."
3. **"Something like:"** -- The phrase "something like" explicitly frames the SQL example as one possible approach, not a required implementation. This is a hallmark of suggestion language.

### Convention Upgrade Check

No upgrade to code change request is warranted because:

- **CONVENTIONS.md:** No CONVENTIONS.md file exists in the fixture data for this evaluation. Without documented conventions, there is no CONVENTIONS.md-based evidence to support an upgrade.
- **Codebase patterns:** In this eval context, there is no real codebase to inspect for patterns (e.g., counting how many existing migrations include `Index::create` or partial indexes). Without concrete codebase evidence showing that adding indexes in migrations is an established project convention, the suggestion cannot be upgraded.

Per the Style/Conventions sub-agent rules (Check 1d), upgrades must be backed by a concrete CONVENTIONS.md section or a counted codebase pattern. General knowledge that "indexes are a database best practice" is explicitly insufficient for an upgrade. Since neither source of convention evidence is available, this comment remains classified as a suggestion.

No sub-task is created for suggestions.
