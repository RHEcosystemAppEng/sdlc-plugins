# Review Comment Classification: 30002

## Comment

- **ID:** 30002
- **Author:** reviewer-a
- **File:** migration/src/m0042_sbom_soft_delete/mod.rs
- **Line:** 14
- **Body:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer proposes adding a database index as a performance optimization. The language uses suggestive phrasing:
- "should also" -- additive suggestion, not a correction of existing code
- "would help" -- indicates the index is beneficial but not strictly required
- Provides a code example as a proposal ("Something like:"), not a directive

### Convention Upgrade Eligibility Analysis

To determine whether this suggestion should be upgraded to a code change request, the following checks were performed:

1. **CONVENTIONS.md check:** The repository's CONVENTIONS.md (referenced in repo-backend.md) documents conventions for framework usage (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing, and caching. No documented convention mandates adding indexes for nullable timestamp columns or for soft-delete filter columns. No index creation convention is documented.

2. **Codebase pattern check:** The PR diff and repository structure do not provide evidence of a consistent codebase pattern for adding indexes alongside column additions in migrations. The migration directory shows `m0001_initial/mod.rs` but no pattern of index creation in migrations can be confirmed from the available data.

3. **Performance-related scrutiny:** While adding an index for frequently-filtered columns is a database best practice, general industry best practices are insufficient grounds for upgrade. The upgrade decision requires either a documented CONVENTIONS.md section or a counted codebase pattern demonstrating consistent usage in similar files within this specific project.

**Conclusion:** The suggestion does not match any documented project convention in CONVENTIONS.md, and no established codebase pattern for index creation in migrations can be confirmed. The upgrade evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern -- general knowledge ("indexes are a database best practice") is not sufficient per the convention upgrade rules. The classification remains **suggestion**.

## Action

No sub-task created. The suggestion is valid from a performance perspective but does not meet the threshold for upgrade to a code change request. The reviewer or team may choose to adopt this suggestion at their discretion.
