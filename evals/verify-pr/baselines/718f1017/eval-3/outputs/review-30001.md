# Review Comment Classification: 30001

**Comment ID:** 30001
**Author:** reviewer-a
**File:** modules/fundamental/src/sbom/service/sbom.rs
**Line:** 60
**Classification:** code change request

## Reasoning

The reviewer uses imperative language: "The `soft_delete` method **should** run all three UPDATE statements inside a single database transaction." This is a direct request for a specific code change, not a suggestion or question. The reviewer identifies a concrete correctness risk (inconsistent state if `sbom_advisory` update fails after `sbom_package` succeeds) and prescribes a specific fix (wrap in `self.db.transaction(|txn| { ... })` and use `txn` instead of `self.db`).

The language "should run" combined with a specific technical prescription and a concrete failure scenario makes this a code change request rather than a suggestion. The reviewer is not proposing an optional alternative -- they are identifying a bug (lack of atomicity) that must be fixed before merge.

**Action:** Sub-task created to wrap the three UPDATE operations in a database transaction.
