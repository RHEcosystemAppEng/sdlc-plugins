# Review Comment Classification: #30002

## Comment
"The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:

```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```"

## Classification: SUGGESTION

## Reasoning
The reviewer uses suggestive language throughout this comment. The phrase "should also" is advisory rather than imperative -- it proposes an addition rather than demanding one. The phrase "would help" further signals that this is a recommendation for improvement, not a requirement. The reviewer offers a code example ("Something like:") to illustrate the idea, which is characteristic of a suggestion rather than a directive.

### Convention Upgrade Eligibility

Per the verify-pr convention upgrade process (Check 1 in style-conventions.md), suggestions are eligible for upgrade to code change request when they match a documented project convention in CONVENTIONS.md or a demonstrated codebase pattern.

**CONVENTIONS.md check:** The repository structure (repo-backend.md) indicates a `CONVENTIONS.md` file exists at the repository root. However, the supplied fixture data does not include the contents of this file, and no documented convention about adding indexes on soft-delete columns or migration index requirements is referenced in the available data. Without a matching CONVENTIONS.md section, the first upgrade path is not satisfied.

**Codebase pattern check:** The PR diff contains only one migration file (`m0042_sbom_soft_delete/mod.rs`), and it does not contain any `Index::create` calls or index creation patterns. The diff does not provide evidence of a consistent codebase practice of adding indexes in migration files.

**Conclusion:** No documented convention in CONVENTIONS.md and no demonstrated codebase pattern backs this suggestion. While adding an index on `deleted_at` is a reasonable database performance practice, general industry best practices are explicitly excluded from the upgrade criteria (per Check 1d: "Do NOT upgrade based on general industry best practices"). The suggestion remains classified as SUGGESTION and does not get upgraded to a code change request. No sub-task is created.
