# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Classification:** code change request

## Reasoning

The reviewer explicitly requests a code modification: wrapping the three UPDATE statements in the `soft_delete` method inside a single database transaction. The language is directive ("should run ... inside a single database transaction", "Wrap the three operations in `self.db.transaction(|txn| { ... })`") and identifies a concrete correctness issue -- if the `sbom_advisory` update fails after `sbom_package` succeeds, the database would be left in an inconsistent state with partially applied soft-delete markers.

This is not a suggestion or nit -- it addresses a data integrity bug where a partial failure during cascade updates could leave orphaned soft-delete states. The reviewer provides the specific fix pattern (`self.db.transaction(|txn| { ... })`) making this a clear code change request.

**Action:** Sub-task creation required to wrap the three update operations in a transaction.
