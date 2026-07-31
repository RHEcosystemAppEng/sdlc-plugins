# Review Comment Classification: 30002

## Comment

**Author:** reviewer-a
**File:** `migration/src/m0042_sbom_soft_delete/mod.rs`, line 14
**Text:** "The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:\n\n```sql\nCREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;\n```"

## Classification: SUGGESTION

## Reasoning

The reviewer proposes adding a database index as a performance optimization, but the language is suggestive rather than imperative:

1. **"should also add"** -- the phrase "should also" indicates an additional recommendation beyond the core requirements, not a mandatory fix. Compare with comment 30001's "should run... inside a single database transaction" which identifies a correctness defect. Here, the word "also" signals this is supplementary.
2. **"would help"** -- the conditional "would help" is classic suggestion language. It proposes a benefit without asserting the change is required. The reviewer acknowledges the feature works without the index; the index would merely improve query performance.
3. **"Something like:"** -- presenting an example with "something like" further softens the request. The reviewer is proposing an approach rather than demanding a specific fix.
4. **No correctness defect identified** -- unlike comment 30001 (which identifies data inconsistency), this comment identifies a performance optimization opportunity. The code functions correctly without the index; queries will just be slower on large datasets.

### Convention Upgrade Evaluation

This suggestion was evaluated for potential upgrade to code change request based on project conventions:

- **CONVENTIONS.md:** The repository has a CONVENTIONS.md file, but its content was not available for analysis. No documented convention about index creation for nullable filter columns could be verified.
- **Codebase patterns:** The PR diff does not contain any existing `Index::create` calls or similar index creation patterns that would demonstrate an established codebase convention of adding indexes alongside column additions.
- **General best practices are insufficient:** While adding indexes on frequently-filtered columns is a general database best practice, the upgrade mechanism requires evidence from the specific project's CONVENTIONS.md or demonstrated codebase patterns. General industry knowledge ("indexes are a database best practice") does not qualify as upgrade evidence per the convention upgrade rules.

**Decision: No upgrade.** The suggestion remains classified as SUGGESTION because no project convention backs the upgrade. No sub-task is created.
