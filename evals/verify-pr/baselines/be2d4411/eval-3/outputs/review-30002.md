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

## Suggestive Language Analysis

The reviewer's phrasing uses suggestive rather than imperative language throughout:

1. **"should also add"** -- The word "also" frames this as an additional recommendation beyond the core requirement, not a mandatory change. "Should" here is advisory rather than directive, especially paired with "also" which signals an optional extra.
2. **"would help"** -- The conditional "would" indicates the reviewer is proposing a potential improvement, not identifying a defect. "Would help" expresses that the change is beneficial but not strictly necessary.
3. **"Something like:"** -- This phrase introduces the code example as one possible approach rather than the required solution, further reinforcing the suggestive nature of the comment.

The reviewer is recommending a performance optimization (adding a partial index) rather than identifying a correctness bug. The current code functions correctly without the index -- queries will return correct results, just potentially slower at scale. This distinguishes it from comment 30001, where the reviewer identified an actual correctness defect (data inconsistency from non-transactional writes).

## Convention Upgrade Evaluation

### CONVENTIONS.md Check

The repository structure listing in repo-backend.md shows a `CONVENTIONS.md` file exists at the root of `trustify-backend/`. However, the contents of this file are not provided in the fixture data. Without being able to read the actual conventions documented in this file, there is no evidence of a documented convention requiring indexes on frequently-filtered columns in migration files. Convention upgrade requires a match against a documented, verifiable convention -- the mere existence of the file is insufficient.

### Codebase Pattern Check

The repository structure shows only one migration directory (`m0001_initial/`). With only a single existing migration visible, there is no demonstrated codebase pattern of adding indexes alongside column additions in migrations. A convention upgrade based on codebase patterns requires multiple examples showing a consistent practice -- one migration file does not establish a pattern.

### Upgrade Decision

The suggestion is **NOT upgraded** to a code change request because:
1. The CONVENTIONS.md file contents are not available to verify whether a convention about index creation in migrations exists
2. Only one existing migration is visible in the repository structure, which is insufficient to establish a codebase pattern
3. Without verifiable convention evidence or a demonstrated multi-instance codebase pattern, upgrading a suggestion would be speculative

The suggestion remains classified as a **suggestion**. It is a valid performance recommendation that the PR author may choose to adopt, but it does not meet the threshold for a tracked code change request.

## Final Classification: suggestion

## Action

No sub-task created. Suggestions are informational feedback that do not require tracked work unless backed by a verifiable project convention or demonstrated codebase pattern.
