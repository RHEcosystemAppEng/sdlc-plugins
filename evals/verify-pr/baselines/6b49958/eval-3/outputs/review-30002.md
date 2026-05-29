# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: code change request

## Reasoning — Initial Classification

The reviewer uses the language "should also add", which is directive ("should") but could be interpreted as either a code change request or a suggestion. The phrase "should also add" leans toward a code change request because "should" indicates an expectation rather than an optional proposal. However, the reviewer also says "would help" and provides the index as "something like", which introduces some optionality. The initial classification is borderline between code change request and suggestion.

Given that "should" is the primary verb and the reviewer provides a specific implementation, this tilts toward **code change request** as the initial classification.

## Convention Analysis — Convention Upgrade Evaluation

Regardless of whether the initial classification is "code change request" or "suggestion", a convention upgrade evaluation is warranted because the comment relates to a performance-related practice (index creation).

### CONVENTIONS.md Check

The repository structure indicates a `CONVENTIONS.md` file exists at the root of `trustify-backend/`. The file was not provided in the eval inputs, so we cannot check for documented index conventions directly. However, the repo structure shows a `migration/` directory with migration files, indicating an established migration pattern.

### Codebase Pattern Check

The repository has a `migration/src/` directory with migration files. The suggestion to add an index on a frequently-filtered nullable column is a well-established database convention. While we cannot search the full codebase in this eval context, the presence of a `CONVENTIONS.md` file in the repository suggests the project documents its conventions. Index creation for columns used in WHERE clauses is a standard database performance practice, and soft-delete patterns with `deleted_at IS NULL` filtering are particularly well-known candidates for partial indexes.

### Performance-Related Scrutiny

Per the Style/Conventions sub-agent instructions (Check 1c), suggestions related to performance (indexes, caching, query optimization) receive extra scrutiny. This comment is explicitly about adding a database index for query performance, which triggers this scrutiny. The `list` service method already filters by `sbom::Column::DeletedAt.is_null()`, confirming that queries filtering by `deleted_at IS NULL` will indeed be frequent.

### Upgrade Decision

This comment is classified as a **code change request**. Whether via direct classification from the reviewer's directive language ("should also add") or via convention upgrade from a suggestion classification, the result is the same: this requires a sub-task. The index suggestion is backed by:
1. The reviewer's directive language ("should")
2. Performance-related scrutiny (index for frequently-filtered column)
3. The code already implements the filter pattern (`DeletedAt.is_null()`) that the index would optimize

A sub-task will be created regardless of classification path.
