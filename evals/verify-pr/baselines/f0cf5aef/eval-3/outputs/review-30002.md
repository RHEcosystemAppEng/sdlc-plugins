# Review Comment Classification: 30002

**Comment ID:** 30002
**Author:** reviewer-a
**File:** migration/src/m0042_sbom_soft_delete/mod.rs
**Line:** 14
**Classification:** code change request

## Reasoning

The reviewer asks for a specific code modification: adding a partial index on the `deleted_at` column in the migration. The language "The migration should also add an index" is directive, not optional. The reviewer explains the rationale (queries filtering by `deleted_at IS NULL` will be frequent) and provides a concrete SQL example for the index. This is a request to add additional code to the migration, not a suggestion of an alternative approach.

While the original task specification did not mention indexing, the reviewer is identifying a gap where the migration would be incomplete without an index for the query pattern being introduced. The phrasing "should also add" treats this as a requirement for the migration to be considered complete.

**Action:** Sub-task created to address this feedback.
