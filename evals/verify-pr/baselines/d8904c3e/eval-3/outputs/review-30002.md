# Review Comment Classification: Comment 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language rather than directive language:

1. **"should also"** -- the phrase "should also" proposes an additional improvement on top of the existing work, rather than requiring a change to what was already implemented. The word "also" signals this is supplementary, not a correction of existing code.
2. **"would help"** -- the conditional phrasing "would help" indicates this is a performance optimization that the reviewer believes would be beneficial, but does not frame it as a requirement. Compare with directive language like "must add" or "add an index" (imperative).
3. **"Something like:"** -- presenting a code example with "something like" frames it as one possible approach, not a prescribed solution.

The reviewer is proposing an alternative/additional approach (adding a partial index for performance) but does not require it. This matches the **suggestion** classification.

## Convention Upgrade Eligibility (Step 6b / Check 1)

Before finalizing this classification, the convention upgrade check was evaluated to determine whether this suggestion should be elevated to a code change request:

### Check 1a -- CONVENTIONS.md

No CONVENTIONS.md fixture data is available for the trustify-backend repository. The repository structure file (repo-backend.md) lists a `CONVENTIONS.md` file in the directory tree, but no fixture content for this file was provided. Without the actual CONVENTIONS.md content, no documented convention match can be established for index creation patterns on new columns.

### Check 1b -- Codebase Patterns

No codebase pattern data is available in the fixture. The PR diff contains only the migration file for the `deleted_at` column addition. There are no other migration files in the diff to count occurrences of `Index::create` or similar index creation patterns. Without access to the actual codebase (only fixture data is available), it is not possible to determine whether adding indexes on new columns is a demonstrated codebase convention.

### Check 1c -- Performance-Related Scrutiny

This suggestion relates to performance (adding an index for query optimization). Extra scrutiny applies, but the same limitation holds: no fixture data demonstrates whether performance-related index patterns are established in this project's migration files.

### Check 1d -- Upgrade Decision

**Not upgraded.** The suggestion does not match any documented convention in CONVENTIONS.md (no content available) and no codebase pattern evidence exists in the fixture data to demonstrate that index creation is a consistent practice in this project's migrations. Upgrading based on general industry best practices ("indexes are a database best practice") is explicitly prohibited by the convention upgrade rules -- the evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern.

The suggestion remains classified as **suggestion**.

## Action

No sub-task created. The suggestion is not backed by a documented or demonstrated project convention.
