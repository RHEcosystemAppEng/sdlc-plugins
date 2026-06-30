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

**Reasoning**: The reviewer uses suggestive, non-directive language throughout the comment. The key phrases are:

1. **"should also"** -- This is suggestive phrasing indicating an additional improvement the reviewer thinks would be beneficial, not a directive requirement. Compare with "must" or "needs to" which would be directive.
2. **"would help"** -- This is explicitly suggestive, framing the index as something that would be helpful rather than something that is required.
3. **"Something like"** -- This frames the provided SQL as an example or rough idea, not a prescribed implementation. Directive code change requests typically use phrasing like "Change this to" or "Use this instead".

The comment proposes adding a partial index on `deleted_at` to optimize `IS NULL` filter queries on the list endpoint. While the suggestion is technically sound -- queries filtering by `deleted_at IS NULL` on every default list request would benefit from a partial index, especially as data grows -- the language is clearly suggestive rather than directive.

### Convention Upgrade Evaluation

The comment was evaluated for convention upgrade eligibility. For a suggestion to be upgraded to a code change request, there must be a project convention in the repository that backs the upgrade -- for example, a documented convention requiring indexes on filter columns, or an established pattern in existing migrations showing that indexes are always added alongside new filter columns.

No such convention evidence exists in the available fixture data:

- The repository structure (`repo-backend.md`) does not document an indexing convention or migration completeness requirement.
- The `CONVENTIONS.md` file is listed in the repository tree but its contents are not available in the fixture data, so no convention can be cited from it.
- The existing migration files (only `m0001_initial/mod.rs` is shown in the tree) do not provide a pattern to compare against.
- No project-level documentation mandates that filter columns must have indexes added in the same migration.

Without concrete project convention evidence to support an upgrade, the comment remains classified as a suggestion. General database best practices alone are not sufficient to override the suggestive language classification -- the upgrade mechanism requires project-specific convention backing.

**Action**: No sub-task created. Suggestions do not trigger sub-task creation unless upgraded by convention evidence, and no applicable convention was found.
