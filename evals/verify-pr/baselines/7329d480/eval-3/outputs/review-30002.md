# Review Comment Classification: 30002

**Reviewer**: reviewer-a
**File**: `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Date**: 2026-04-20T14:35:00Z

## Comment Text

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

## Classification: Suggestion

**Reasoning**: The reviewer uses suggestive language throughout the comment. The key phrases are:

1. **"should also add"**: The word "also" frames this as a supplementary recommendation rather than a required correction. It signals an additional improvement on top of the core change, not a fix for a defect.
2. **"would help"**: "a partial index would help" is conditional/hedging language. The reviewer is proposing a performance optimization that they believe would be beneficial, not identifying a correctness defect that must be fixed.
3. **"Something like"**: This phrase explicitly frames the SQL example as one possible approach, not a mandated implementation. It invites the author to consider the idea rather than execute a specific instruction.

The reviewer is recommending a performance improvement (adding a partial index) and provides a helpful code example, but the phrasing consistently frames it as a recommendation rather than a mandatory requirement. There is no directive language ("must", "needs to be", "fix this"), and no correctness defect is identified -- the code works correctly without the index, it would simply perform better with one.

### Convention Upgrade Eligibility Assessment

The suggestion was evaluated for convention upgrade from suggestion to code change request:

- **CONVENTIONS.md check**: The repository structure shows a `CONVENTIONS.md` file exists at the root of `trustify-backend/`. However, the contents of this file are not available in the fixture data. Without access to the actual documented conventions, it is not possible to confirm whether the project has a documented requirement for indexes on columns used in frequent WHERE clauses.
- **File-type applicability**: The comment targets `migration/src/m0042_sbom_soft_delete/mod.rs`, a migration file. If a migration index convention existed, it would apply to this file type. The applicability check is structurally valid but moot without convention text.
- **Codebase pattern check**: The fixture data includes only the repository directory tree and the PR diff. No other migration files are available to verify whether a consistent pattern of index creation alongside column additions exists in the codebase.
- **Documented convention requirement**: Convention upgrade requires a documented project convention that can be cited as specific evidence for the upgrade. No documented convention text is available in the fixture data to support the claim that indexes must accompany columns used in WHERE clauses.

**Upgrade decision**: The suggestion is NOT upgraded to code change request. While adding a partial index on a frequently-filtered column is a widely recognized database best practice, the convention upgrade mechanism requires a specific, documented project convention -- not general industry best practices. The available fixture data does not contain documented convention text that would justify the upgrade. The classification remains SUGGESTION.

**Action**: No sub-task created. Suggestions are advisory feedback that do not require tracked work.
