# Review Comment Classification: #30002

## Author: reviewer-a
## File: migration/src/m0042_sbom_soft_delete/mod.rs
## Line: 14

## Comment Text
The migration should also add an index on `deleted_at` for the sbom table. Queries filtering by `deleted_at IS NULL` will be frequent and a partial index would help. Something like:

```sql
CREATE INDEX idx_sbom_not_deleted ON sbom (deleted_at) WHERE deleted_at IS NULL;
```

## Classification: suggestion

## Reasoning
The reviewer uses suggestive rather than directive language. The phrase "should also add" is additive ("also") rather than corrective -- it proposes an enhancement beyond what the current implementation does, not a fix for something broken. The phrase "would help" is conditional and non-imperative, indicating the reviewer believes this is beneficial but is not requiring it. The reviewer provides an example with "Something like:", which frames the SQL as illustrative rather than prescriptive. Unlike comment #30001 which identifies a correctness bug (inconsistent state), this comment identifies a performance optimization opportunity -- the code is functionally correct without the index, it would just perform better with one.

This is a suggestion, not a code change request, because:
1. The language is suggestive ("should also", "would help", "Something like") rather than directive ("must", "wrap", "you need to").
2. The absence of the index does not cause incorrect behavior -- it is a performance consideration.
3. The reviewer is proposing an addition, not identifying a defect.

No sub-task is created for suggestions.

### Convention Upgrade Eligibility
This suggestion is eligible for convention upgrade consideration. Adding partial indexes on soft-delete timestamp columns is a well-established database performance best practice for tables that use soft-delete patterns. If the trustify-backend codebase adopts soft-delete in additional entities beyond SBOM, a convention requiring a partial index on `deleted_at IS NULL` for all soft-deletable tables would ensure consistent query performance. This could be documented in the project's CONVENTIONS.md as a database migration guideline.
