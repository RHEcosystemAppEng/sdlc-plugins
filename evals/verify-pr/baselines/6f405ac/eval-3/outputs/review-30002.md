# Review Comment Classification: 30002

## Comment

> The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:
>
> ```sql
> CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
> ```

**File:** `migration/src/m0042_sbom_soft_delete/mod.rs` line 14
**Author:** reviewer-a

## Classification: SUGGESTION

## Reasoning

The reviewer uses suggestive language throughout: "should also add" and "would help". The phrase "should also" proposes an addition beyond what the task required, and "would help" frames the index as a performance enhancement rather than a mandatory fix. The reviewer also uses the phrase "Something like:" followed by sample SQL, which further indicates this is a proposed approach rather than a required change.

### Convention Upgrade Eligibility

The suggestion was evaluated for convention upgrade eligibility per the Style/Conventions sub-agent's Check 1 (Convention Upgrade):

1. **CONVENTIONS.md check:** The target repository (`trustify-backend`) has a `CONVENTIONS.md` file. However, the CONVENTIONS.md documents general patterns (Axum framework, SeaORM, module structure, error handling, endpoint registration, response types, query helpers, testing, caching) but does not include a documented convention requiring indexes on soft-delete columns, partial indexes for `IS NULL` filters, or a general index creation convention for migration files.

2. **Codebase pattern check:** The PR diff does not contain evidence of existing migration files that consistently add indexes alongside new columns. Only the single migration file `m0042_sbom_soft_delete/mod.rs` is included in the diff, and the existing migration directory structure shows only `m0001_initial/`. Without access to the full codebase, there is insufficient evidence of a consistent, demonstrated pattern of adding indexes in migrations for nullable filter columns.

3. **Performance-related scrutiny:** While adding an index for a frequently-filtered nullable column is a well-known database best practice, the upgrade decision requires evidence from the specific project's conventions or codebase patterns. General industry best practices alone are explicitly excluded from upgrade evidence per the Style/Conventions sub-agent rules: "Do NOT upgrade based on general industry best practices, framework documentation, or inferred patterns that are not demonstrated by the specific project's code or documentation."

### Conclusion

The suggestion remains classified as **SUGGESTION** because:
- No matching convention exists in `CONVENTIONS.md`
- No counted codebase pattern demonstrates consistent index creation in migrations
- The reviewer's own language frames this as helpful but not required ("should also", "would help")
- General database best practices are insufficient grounds for upgrade per the classification rules

No sub-task is created for suggestions that are not upgraded to code change requests.
