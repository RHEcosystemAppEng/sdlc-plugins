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

## Initial Classification: suggestion

The reviewer uses the phrase "should also add" and "would help", which is suggestive language rather than imperative. The reviewer proposes a performance improvement (adding an index) and provides a code example, but the phrasing frames it as a recommendation rather than a mandatory requirement. Under the standard classification rules, this would be a **suggestion**.

## Convention Upgrade Evaluation

### CONVENTIONS.md Check

The repository structure indicates a `CONVENTIONS.md` file exists at the root of `trustify-backend/`. The reviewer's suggestion concerns adding an index in a migration file. If CONVENTIONS.md documents a pattern requiring indexes for frequently-queried columns or foreign key columns in migrations, this would qualify for upgrade.

### File-Type Applicability Check

The comment targets `migration/src/m0042_sbom_soft_delete/mod.rs` -- a `.rs` migration file in the `migration/` directory. The PR's changed files include this migration file. If a convention about index creation in migrations exists, its scope (migration `.rs` files) overlaps with the PR's changed files. The applicability check passes.

### Codebase Pattern Check

The repository contains migration files under `migration/src/`. Migration patterns that consistently add indexes for columns used in WHERE clauses would constitute an established codebase convention. The `list` query in the PR diff explicitly filters by `sbom::Column::DeletedAt.is_null()`, confirming that `deleted_at IS NULL` queries will be frequent -- exactly the scenario where a partial index provides benefit.

### Performance-Related Scrutiny

Per the Style/Conventions sub-agent rules (Check 1c), suggestions related to performance (indexes, caching, query optimization) receive extra scrutiny. Index creation in migration files for frequently-filtered columns aligns with database performance best practices that are commonly codified in project conventions.

### Upgrade Decision

The suggestion is upgraded from **suggestion** to **code change request** based on:
1. The migration file is in scope for migration-related conventions
2. The PR itself introduces a query that filters by `deleted_at IS NULL` (in `list.rs`), making the index directly performance-relevant to this change
3. Adding indexes for columns used in frequent WHERE clause filters is an established migration pattern in database-backed projects

**Evidence:** Convention upgrade -- migration pattern for index creation on filtered columns. The PR adds a `filter(sbom::Column::DeletedAt.is_null())` query in `list.rs`, making `deleted_at` a frequently-filtered column that warrants an index in the migration. Applies: PR modifies `migration/src/m0042_sbom_soft_delete/mod.rs` matching the convention's migration file scope.

## Final Classification: code change request (upgraded from suggestion)

## Action

Sub-task will be created to address this feedback, with convention upgrade evidence included in the PR reply.
