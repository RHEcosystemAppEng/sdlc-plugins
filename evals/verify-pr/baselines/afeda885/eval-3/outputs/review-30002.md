# Review Comment Classification: 30002

## Comment
**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Content:** The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: suggestion

## Reasoning

The reviewer uses suggestive, advisory language: "should also add", "would help", "Something like". The phrase "should also" proposes an additional enhancement rather than directing a required change. The phrase "would help" frames the index as a performance optimization that is beneficial but not strictly necessary for correctness. The phrase "Something like" further indicates this is a proposed approach, not a mandated one.

This meets the classification criteria for **suggestion**: the reviewer proposes an alternative or additional approach but does not require it.

## Convention Upgrade Evaluation

The suggestion was evaluated for potential upgrade to code change request based on project conventions:

1. **CONVENTIONS.md check:** The target repository (trustify-backend) has a CONVENTIONS.md file listed in its directory structure (repo-backend.md). However, the actual content of CONVENTIONS.md is not available in the fixture data. The listed key conventions in repo-backend.md describe framework choices (Axum, SeaORM), module patterns, error handling, endpoint registration, response types, query helpers, testing patterns, and caching -- none of which document index creation conventions for migration files.

2. **Codebase pattern check:** The PR diff only contains one migration file (`m0042_sbom_soft_delete/mod.rs`), and the repository structure shows only one other migration (`m0001_initial/`). There is insufficient evidence of a consistent codebase pattern for index creation in migrations. Only the diff content is available for pattern analysis, and it contains no `Index::create` calls or similar index patterns.

3. **Performance-related scrutiny:** While adding an index is a database performance optimization, there is no documented performance convention in the project's conventions or demonstrated codebase pattern that would mandate index creation for filtered columns.

**Decision: NOT upgraded.** The suggestion uses suggestive language ("should also", "would help"), and there is no documented project convention or demonstrated codebase pattern backing this practice. General database best practices alone are insufficient for upgrade -- the evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern.

## Sub-task required: No
