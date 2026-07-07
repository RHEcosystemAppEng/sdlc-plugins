# Review Comment Classification: 30002

## Comment Details

- **Comment ID:** 30002
- **Author:** reviewer-a
- **File:** migration/src/m0042_sbom_soft_delete/mod.rs
- **Line:** 14
- **Content:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: suggestion

## Reasoning

The reviewer uses suggestive language throughout:
- "should also" -- proposes an addition rather than requiring one; "also" softens the directive
- "would help" -- suggests a potential benefit rather than identifying a requirement or defect

The comment proposes an alternative/enhanced approach (adding a partial index for performance) but does not frame it as a required code change or identify a functional defect. The absence of the index does not break correctness -- it is a performance optimization.

### Convention Upgrade Eligibility Assessment

This suggestion was evaluated for convention upgrade per Step 6b:

1. **CONVENTIONS.md check:** The CONVENTIONS.md file content is not available in the fixture data. No documented convention about index creation for filtered columns could be verified.

2. **Codebase pattern search:** The PR diff was searched for demonstrated patterns of index creation (e.g., `Index::create`, `create_index`, or similar SQL/ORM index operations). Zero occurrences were found anywhere in the diff. The migration file contains only `Table::alter()` with `add_column`/`drop_column` operations.

3. **Performance convention search:** No performance-related conventions are documented or demonstrated in the available data.

4. **Upgrade decision:** The suggestion does NOT match any documented convention (CONVENTIONS.md unavailable) and no demonstrated codebase pattern of index creation exists in the diff. Per the upgrade rules, suggestions must NOT be upgraded based on general industry best practices (e.g., "indexes are a database best practice"). The upgrade evidence must cite a concrete CONVENTIONS.md section or a counted codebase pattern. Neither exists here.

**Result:** No upgrade. The suggestion remains classified as "suggestion". No sub-task created.

## Action

No sub-task created. The suggestion proposes an optional performance improvement not backed by any documented or demonstrated project convention.
