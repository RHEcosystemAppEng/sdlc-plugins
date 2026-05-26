# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14
**Classification:** suggestion

## Reasoning

The reviewer proposes adding a partial index on the `deleted_at` column for the `sbom` table to improve query performance for `WHERE deleted_at IS NULL` filters. The language uses "should" ("The migration should also add an index") which is suggestive rather than imperative.

While the suggestion is well-reasoned -- frequent queries filtering by `deleted_at IS NULL` would benefit from a partial index -- this is a performance optimization rather than a correctness requirement. The feature will function correctly without the index; it would only affect query performance at scale.

No CONVENTIONS.md is available for the trustify-backend repository to check whether index creation on soft-delete columns is a documented convention. Without evidence of a codebase-wide convention (e.g., other migrations consistently adding indexes for nullable timestamp columns), this remains classified as a suggestion rather than being upgraded to a code change request.

**Action:** No sub-task created. This is an optional performance improvement that the author may choose to adopt.
