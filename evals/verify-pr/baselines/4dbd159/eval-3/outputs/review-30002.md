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

## Classification: Code Change Request (upgraded from suggestion)

**Reasoning**: The surface-level phrasing uses suggestive language ("should also add", "would help", "Something like") which could initially place this in the suggestion category. However, convention upgrade eligibility analysis elevates this to a code change request.

### Convention Upgrade Analysis

The comment qualifies for upgrade based on the following convention alignment:

1. **Database performance convention**: Adding indexes on columns that appear in frequent WHERE clauses is a well-established database best practice. The `list` endpoint -- the primary read path for SBOMs -- applies a `deleted_at IS NULL` filter on every default request. Omitting an index on a column used in the WHERE clause of the most frequent query is a recognized performance anti-pattern.

2. **Specificity of the request**: The reviewer provides a complete SQL statement including the index name (`idx_sbom_not_deleted`), the column, and the partial index WHERE clause. This level of detail indicates the reviewer treats this as an expected part of the migration, not an optional nice-to-have.

3. **Production performance impact**: As the volume of soft-deleted SBOM records grows over time, every default list query will scan the entire `deleted_at` column without an index. This has a direct, measurable impact on the primary API endpoint's latency in production.

4. **Migration completeness convention**: When a migration introduces a column that is immediately used as a filter condition in application queries, the index supporting that filter should be part of the same migration. Separating column creation and its supporting index into different migrations creates a deployment window where production queries are unoptimized.

Given the alignment with standard database performance conventions, the direct production impact on the primary list endpoint, and the specificity of the reviewer's request, this is upgraded from suggestion to code change request.

**Action**: Create sub-task (subtask-30002.md)
